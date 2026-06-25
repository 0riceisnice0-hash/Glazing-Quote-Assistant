import fs from 'node:fs/promises';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';
import os from 'node:os';
import { execFileSync } from 'node:child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const defaultTenderDir = path.join(rootDir, 'newest tender docs - codex look at this');
const bundledNodeModules = 'C:\\Users\\zacpl\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules';
const require = createRequire(import.meta.url);

const args = parseArgs(process.argv.slice(2));
const tenderDir = path.resolve(args.dir || defaultTenderDir);
const outDir = path.resolve(args.out || path.join(rootDir, 'test-results'));
const mode = args.mode || 'clean';
const pdfOnly = Boolean(args.pdfOnly);
const intakeRisks = [];
const intakeRecords = [];
const inputAliases = new Map();

installPdfJsPolyfills();
const pdfjs = await loadPdfJs();
const { DataExtractor, Pricing } = await loadBotGlobals();

await fs.mkdir(outDir, { recursive: true });

const inputFiles = (await listFiles(tenderDir))
  .filter(isSupportedTenderInput)
  .filter((filePath) => !isQuoteOrSupplierPath(filePath))
  .sort((a, b) => path.basename(a).localeCompare(path.basename(b)));

if (!inputFiles.length) {
  throw new Error(`No PDF/XLSX tender inputs found in ${tenderDir}`);
}

console.log(`Tender directory: ${tenderDir}`);
console.log(`Tender inputs found: ${inputFiles.length}`);
console.log(`Mode: ${mode}`);
if (pdfOnly) console.log('Input filter: PDF only');

const expandedInputFiles = [];
for (const filePath of inputFiles) {
  expandedInputFiles.push(...await expandInputFile(filePath));
}
if (expandedInputFiles.length !== inputFiles.length) {
  console.log(`Expanded inputs: ${expandedInputFiles.length}`);
}

const firstPassDocs = [];
for (const filePath of expandedInputFiles) {
  const doc = await extractInput(filePath);
  const classification = DataExtractor.classifyDocument(doc.name, doc.fullText || '');
  firstPassDocs.push({ ...doc, classification });
  console.log(`${doc.name}: ${classification.type} (${classification.confidence}) - ${classification.reason}`);
}

const extractionDocs = firstPassDocs.filter((doc) => shouldUseDocument(doc.classification.type));

const skippedDocs = firstPassDocs.filter((doc) => !extractionDocs.includes(doc));
console.log(`Using ${extractionDocs.length}/${firstPassDocs.length} PDFs for extraction/pricing.`);
if (skippedDocs.length) {
  console.log(`Skipped: ${skippedDocs.map((doc) => doc.name).join(', ')}`);
}

const extraction = withQuietConsole(() => DataExtractor.extractItems(extractionDocs));
let pricingConfig = { ...Pricing.DEFAULT_CONFIG };
pricingConfig = Pricing.applyTenderPricingDefaults(extraction.items, pricingConfig);
Pricing.applyKnownItemPricing(extraction.items);
const pricedItems = Pricing.recalculateAll(extraction.items, pricingConfig);
const summary = Pricing.getPriceSummary(pricedItems, pricingConfig);

const runStamp = new Date().toISOString().replace(/[:.]/g, '-');
const report = {
  runAt: new Date().toISOString(),
  tenderDir,
  inputDocuments: firstPassDocs.map((doc) => ({
    name: doc.name,
    pageCount: doc.pageCount,
    textChars: doc.fullText.length,
    isScanned: doc.isScanned,
    kind: doc.kind || (/\.pdf$/i.test(doc.name) ? 'pdf' : /\.(xlsx|xlsm|xls)$/i.test(doc.name) ? 'workbook' : 'file'),
    extractionMethod: doc.extractionMethod || '',
    classification: doc.classification
  })),
  usedDocuments: extractionDocs.map((doc) => doc.name),
  skippedDocuments: skippedDocs.map((doc) => ({
    name: doc.name,
    classification: doc.classification
  })),
  stats: extraction.stats,
  warnings: extraction.warnings,
  risks: intakeRisks.concat(buildWorkflowRisks(firstPassDocs, pricedItems)),
  intakeRecords,
  specNotes: extraction.specNotes,
  pricingConfig,
  summary,
  items: pricedItems.map((item) => ({
    reference: item.reference,
    type: item.type,
    width: item.width,
    height: item.height,
    quantity: item.quantity,
    frameType: item.frameType,
    glazingSpec: item.glazingSpec,
    openingType: item.openingType,
    location: item.location,
    finish: item.finish,
    fireRating: item.fireRating,
    doorSwing: item.doorSwing,
    ironmongery: item.ironmongery,
    uValue: item.uValue,
    system: item.system,
    scheduleType: item.scheduleType,
    sourceDocument: item.sourceDocument,
    sourcePage: item.sourcePage,
    confidence: item.confidence,
    productCode: item.productCode,
    pricingMethod: item.pricingMethod,
    unitPrice: item.unitPrice,
    totalPrice: item.totalPrice
  })),
  debugLog: extraction.debugLog
};

const jsonPath = path.join(outDir, `tender-pack-report-${runStamp}.json`);
const csvPath = path.join(outDir, `tender-pack-items-${runStamp}.csv`);
await fs.writeFile(jsonPath, JSON.stringify(report, null, 2), 'utf8');
await fs.writeFile(csvPath, toCsv(report.items), 'utf8');

printSummary(report, jsonPath, csvPath);

function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--dir') parsed.dir = argv[++i];
    else if (arg === '--out') parsed.out = argv[++i];
    else if (arg === '--mode') parsed.mode = argv[++i];
    else if (arg === '--pdf-only') parsed.pdfOnly = true;
    else if (arg === '--help' || arg === '-h') {
      console.log('Usage: node scripts/run-tender-pack.mjs [--dir "path/to/tender docs"] [--out "path/to/results"]');
      process.exit(0);
    }
  }
  return parsed;
}

function shouldUseDocument(docType) {
  if (mode === 'website') return docType !== 'admin';
  if (mode === 'include-unknown') return ['schedule', 'bq', 'specification', 'unknown'].includes(docType);
  return ['schedule', 'bq', 'specification'].includes(docType);
}

async function listFiles(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await listFiles(fullPath));
    else if (entry.isFile()) files.push(fullPath);
  }
  return files;
}

async function expandInputFile(filePath) {
  if (!/\.zip$/i.test(filePath)) return [filePath];
  const extractRoot = path.join(os.tmpdir(), 'gqa-intake-' + Date.now() + '-' + Math.random().toString(16).slice(2));
  await fs.mkdir(extractRoot, { recursive: true });
  try {
    expandArchive(filePath, extractRoot);
  } catch (err) {
    intakeRisks.push(makeRisk('critical', `ZIP could not be unpacked: ${displayName(filePath)}`, {
      sourceDocumentName: displayName(filePath),
      suggestedAction: 'Extract the archive manually or process it with cloud document intake.'
    }));
    return [];
  }
  intakeRecords.push({
    name: displayName(filePath),
    kind: 'zip',
    status: 'expanded',
    extractedTo: extractRoot
  });
  const children = (await listFiles(extractRoot))
    .filter(isSupportedTenderInput)
    .filter((childPath) => !isQuoteOrSupplierPath(childPath));
  children.forEach((childPath) => {
    inputAliases.set(childPath, path.relative(tenderDir, filePath) + '/' + path.relative(extractRoot, childPath));
  });
  if (!children.length) {
    intakeRisks.push(makeRisk('warning', `ZIP had no supported child files: ${displayName(filePath)}`, {
      sourceDocumentName: displayName(filePath)
    }));
  }
  return children;
}

function isSupportedTenderInput(filePath) {
  if (pdfOnly) return /\.pdf$/i.test(filePath);
  return /\.(pdf|xlsx|xlsm|xls|zip|docx|eml|msg|jpe?g|png)$/i.test(filePath);
}

function isQuoteOrSupplierPath(filePath) {
  var relative = path.relative(tenderDir, filePath).toLowerCase();
  var parts = relative.split(/[\\/]+/);
  return parts.some((part) => /\bclient quote\b/.test(part)) ||
    parts.some((part) => /\bsupplier quotes?\b/.test(part)) ||
    /\bquote\b/i.test(path.basename(filePath)) && !/\bboq\b|\bbq\b|bill|schedule|pricing schedule/i.test(path.basename(filePath));
}

function displayName(filePath) {
  return inputAliases.get(filePath) || path.relative(tenderDir, filePath);
}

async function loadPdfJs() {
  const local = path.join(rootDir, 'node_modules', 'pdfjs-dist', 'legacy', 'build', 'pdf.mjs');
  const bundled = path.join(bundledNodeModules, 'pdfjs-dist', 'legacy', 'build', 'pdf.mjs');
  const pdfPath = await exists(local) ? local : bundled;
  return import(pathToFileURL(pdfPath).href);
}

function installPdfJsPolyfills() {
  if (!globalThis.DOMMatrix) {
    globalThis.DOMMatrix = class DOMMatrix {
      constructor(init) {
        this.a = 1; this.b = 0; this.c = 0; this.d = 1; this.e = 0; this.f = 0;
        if (Array.isArray(init)) {
          [this.a, this.b, this.c, this.d, this.e, this.f] = init;
        } else if (init && typeof init === 'object') {
          this.a = init.a ?? this.a;
          this.b = init.b ?? this.b;
          this.c = init.c ?? this.c;
          this.d = init.d ?? this.d;
          this.e = init.e ?? this.e;
          this.f = init.f ?? this.f;
        }
      }

      multiplySelf(other) {
        const m = new globalThis.DOMMatrix(other);
        const a = this.a * m.a + this.c * m.b;
        const b = this.b * m.a + this.d * m.b;
        const c = this.a * m.c + this.c * m.d;
        const d = this.b * m.c + this.d * m.d;
        const e = this.a * m.e + this.c * m.f + this.e;
        const f = this.b * m.e + this.d * m.f + this.f;
        this.a = a; this.b = b; this.c = c; this.d = d; this.e = e; this.f = f;
        return this;
      }

      preMultiplySelf(other) {
        const m = new globalThis.DOMMatrix(other);
        return this.setMatrixValue(m.multiplySelf(this));
      }

      translate(x = 0, y = 0) {
        return new globalThis.DOMMatrix(this).translateSelf(x, y);
      }

      translateSelf(x = 0, y = 0) {
        return this.multiplySelf([1, 0, 0, 1, x, y]);
      }

      scale(scaleX = 1, scaleY = scaleX) {
        return new globalThis.DOMMatrix(this).scaleSelf(scaleX, scaleY);
      }

      scaleSelf(scaleX = 1, scaleY = scaleX) {
        return this.multiplySelf([scaleX, 0, 0, scaleY, 0, 0]);
      }

      invertSelf() {
        const det = this.a * this.d - this.b * this.c;
        if (!det) {
          this.a = this.b = this.c = this.d = this.e = this.f = NaN;
          return this;
        }
        const a = this.d / det;
        const b = -this.b / det;
        const c = -this.c / det;
        const d = this.a / det;
        const e = (this.c * this.f - this.d * this.e) / det;
        const f = (this.b * this.e - this.a * this.f) / det;
        this.a = a; this.b = b; this.c = c; this.d = d; this.e = e; this.f = f;
        return this;
      }

      setMatrixValue(other) {
        this.a = other.a; this.b = other.b; this.c = other.c;
        this.d = other.d; this.e = other.e; this.f = other.f;
        return this;
      }
    };
  }
}

async function loadBotGlobals() {
  const context = {
    console,
    crypto: {
      randomUUID: () => {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
          const r = Math.random() * 16 | 0;
          const v = c === 'x' ? r : (r & 0x3 | 0x8);
          return v.toString(16);
        });
      }
    }
  };
  vm.createContext(context);
  for (const relativePath of ['js/dataModel.js', 'js/dataExtractor.js', 'js/pricing.js']) {
    const code = await fs.readFile(path.join(rootDir, relativePath), 'utf8');
    vm.runInContext(code, context, { filename: relativePath });
  }
  if (!context.DataExtractor || !context.Pricing) {
    throw new Error('Could not load DataExtractor/Pricing globals');
  }
  return { DataExtractor: context.DataExtractor, Pricing: context.Pricing };
}

async function extractPdf(filePath) {
  const data = await fs.readFile(filePath);
  const loadingTask = pdfjs.getDocument({
    data: new Uint8Array(data),
    disableWorker: true,
    useSystemFonts: true
  });
  const pdf = await loadingTask.promise;
  const pages = [];
  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const viewport = page.getViewport({ scale: 1 });
    const content = await page.getTextContent();
    const textItems = content.items.map((item) => ({
      str: item.str,
      x: item.transform[4],
      y: item.transform[5],
      width: item.width || 0,
      height: Math.abs(item.transform[3]) || 10
    }));
    pages.push({
      pageNum,
      text: joinTextItems(textItems),
      textItems,
      width: viewport.width,
      height: viewport.height
    });
  }
  const fullText = pages.map((page) => page.text).join('\n');
  return {
    name: displayName(filePath),
    path: filePath,
    kind: 'pdf',
    pageCount: pdf.numPages,
    pages,
    fullText,
    isScanned: DataExtractor.isLikelyScanned(fullText, pdf.numPages),
    extractionMethod: 'pdfjs'
  };
}

async function extractInput(filePath) {
  if (/\.pdf$/i.test(filePath)) return extractPdf(filePath);
  if (/\.(xlsx|xlsm|xls)$/i.test(filePath)) return extractWorkbook(filePath);
  if (/\.docx$/i.test(filePath)) return extractDocx(filePath);
  if (/\.eml$/i.test(filePath)) return extractEml(filePath);
  if (/\.msg$/i.test(filePath)) return unsupportedInputDoc(filePath, 'msg', 'MSG email files need cloud processing or export to EML/PDF.');
  if (/\.(jpe?g|png)$/i.test(filePath)) return unsupportedInputDoc(filePath, 'image', 'Image tender inputs need OCR/cloud processing before pricing.');
  return unsupportedInputDoc(filePath, 'unsupported', 'Unsupported tender input.');
}

async function extractDocx(filePath) {
  const extractRoot = path.join(os.tmpdir(), 'gqa-docx-' + Date.now() + '-' + Math.random().toString(16).slice(2));
  await fs.mkdir(extractRoot, { recursive: true });
  try {
    expandArchive(filePath, extractRoot);
  } catch (err) {
    intakeRisks.push(makeRisk('critical', `DOCX could not be unpacked: ${displayName(filePath)}`, {
      sourceDocumentName: displayName(filePath),
      suggestedAction: 'Open manually, export to PDF, or process with cloud document intake.'
    }));
    return textDocument(filePath, 'docx', '');
  }
  const xmlPath = path.join(extractRoot, 'word', 'document.xml');
  if (!await exists(xmlPath)) {
    intakeRisks.push(makeRisk('critical', `DOCX has no readable document body: ${displayName(filePath)}`, {
      sourceDocumentName: displayName(filePath),
      suggestedAction: 'Open manually, export to PDF, or process with cloud document intake.'
    }));
    return textDocument(filePath, 'docx', '');
  }
  const xml = await fs.readFile(xmlPath, 'utf8');
  const text = extractDocxText(xml);
  return textDocument(filePath, 'docx', text);
}

async function extractEml(filePath) {
  const raw = await fs.readFile(filePath, 'utf8');
  const subject = (raw.match(/^subject:\s*(.+)$/im) || [])[1] || '';
  const body = raw.split(/\r?\n\r?\n/).slice(1).join('\n\n')
    .replace(/--[A-Za-z0-9'()+_,\-\.\/:=?]+(?:--)?/g, '\n')
    .replace(/Content-[^\n]+\n/gi, '\n')
    .trim();
  return textDocument(filePath, 'email', (subject ? `Subject: ${subject}\n\n` : '') + body);
}

async function unsupportedInputDoc(filePath, kind, message) {
  const doc = textDocument(filePath, kind, '');
  doc.isScanned = /\.(jpe?g|png)$/i.test(filePath);
  intakeRisks.push(makeRisk(kind === 'image' ? 'warning' : 'critical', `${message} ${doc.name}`, {
    sourceDocumentName: doc.name,
    suggestedAction: kind === 'image'
      ? 'Run OCR through the browser/cloud workflow or provide a text PDF/schedule.'
      : 'Export this file to PDF/EML or process it with the cloud worker.'
  }));
  return doc;
}

function textDocument(filePath, kind, text) {
  const relativeName = displayName(filePath);
  const pages = [{
    pageNum: 1,
    text: text || '',
    textItems: [],
    width: 0,
    height: 0
  }];
  return {
    name: relativeName,
    path: filePath,
    kind,
    pageCount: 1,
    pages,
    fullText: text || '',
    isScanned: false,
    extractionMethod: kind
  };
}

function extractDocxText(xml) {
  return xml
    .replace(/<\/w:p>/g, '\n')
    .replace(/<\/w:tr>/g, '\n')
    .replace(/<\/w:tc>/g, ' | ')
    .replace(/<[^>]+>/g, '')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function expandArchive(sourcePath, destinationPath) {
  execFileSync('tar.exe', ['-xf', sourcePath, '-C', destinationPath], { stdio: 'ignore' });
}

async function extractWorkbook(filePath) {
  const XLSX = require(path.join(rootDir, 'node_modules', 'xlsx', 'xlsx.js'));
  const workbook = XLSX.readFile(filePath, { cellDates: false, cellFormula: false, raw: false, cellStyles: true });
  const pages = workbook.SheetNames.map((sheetName, idx) => {
    const sheet = workbook.Sheets[sheetName];
    const rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '', raw: false });
    const normalisedRows = rows.map((row) => row.map((cell) => String(cell || '').trim()));
    function isRedCell(rowIdx, colIdx) {
      const cell = sheet[XLSX.utils.encode_cell({ r: rowIdx, c: colIdx })];
      const style = cell && cell.s;
      const color = style && style.font && style.font.color;
      let rgb = color && (color.rgb || color.fgColor || color.indexed);
      if (!rgb || typeof rgb !== 'string') return false;
      rgb = rgb.replace(/^FF/i, '').slice(-6);
      if (!/^[0-9a-f]{6}$/i.test(rgb)) return false;
      const r = parseInt(rgb.slice(0, 2), 16);
      const g = parseInt(rgb.slice(2, 4), 16);
      const b = parseInt(rgb.slice(4, 6), 16);
      return r > 160 && g < 120 && b < 120;
    }
    const textItems = [];
    normalisedRows.forEach((row, rowIdx) => {
      row.forEach((cell, colIdx) => {
        if (!cell) return;
        const displayCell = isRedCell(rowIdx, colIdx) ? `${cell} [RED_TEXT]` : cell;
        textItems.push({
          str: displayCell,
          x: colIdx * 120,
          y: (rows.length - rowIdx) * 18,
          width: Math.max(30, displayCell.length * 7),
          height: 12
        });
      });
    });
    const lines = normalisedRows
      .map((row, rowIdx) => row.map((cell, colIdx) => {
        if (!cell) return '';
        return isRedCell(rowIdx, colIdx) ? `${cell} [RED_TEXT]` : cell;
      }).filter(Boolean).join('   '))
      .filter(Boolean);
    return {
      pageNum: idx + 1,
      sheetName,
      text: [sheetName, ...lines].join('\n'),
      textItems,
      width: 0,
      height: 0
    };
  });
  const fullText = pages.map((page) => page.text).join('\n');
  return {
    name: displayName(filePath),
    path: filePath,
    kind: 'workbook',
    pageCount: pages.length,
    pages,
    fullText,
    isScanned: false,
    extractionMethod: 'sheetjs'
  };
}

function joinTextItems(textItems) {
  const textParts = [];
  for (let i = 0; i < textItems.length; i++) {
    const curr = textItems[i];
    if (i > 0) {
      const prev = textItems[i - 1];
      const prevRightEdge = prev.x + prev.width;
      const gap = curr.x - prevRightEdge;
      const sameRow = Math.abs(curr.y - prev.y) < 3;
      textParts.push(sameRow && gap >= -2 && gap < 2 ? curr.str : ` ${curr.str}`);
    } else {
      textParts.push(curr.str);
    }
  }
  return textParts.join('');
}

function withQuietConsole(fn) {
  const originalLog = console.log;
  console.log = () => {};
  try {
    return fn();
  } finally {
    console.log = originalLog;
  }
}

function toCsv(rows) {
  const headers = [
    'reference', 'type', 'width', 'height', 'quantity', 'frameType', 'glazingSpec',
    'openingType', 'location', 'finish', 'fireRating', 'doorSwing', 'ironmongery',
    'uValue', 'system', 'scheduleType', 'sourceDocument', 'sourcePage',
    'confidence', 'productCode', 'pricingMethod', 'unitPrice', 'totalPrice'
  ];
  const lines = [headers.join(',')];
  for (const row of rows) {
    lines.push(headers.map((header) => csvCell(row[header])).join(','));
  }
  return `${lines.join('\n')}\n`;
}

function csvCell(value) {
  if (value === undefined || value === null) return '';
  const text = String(value);
  if (/[",\n\r]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
  return text;
}

function buildWorkflowRisks(docs, items) {
  const risks = [];
  const scheduleDocs = docs.filter((doc) => doc.classification && doc.classification.type === 'schedule');
  if (!scheduleDocs.length) {
    risks.push(makeRisk('critical', 'No machine-readable window, door, or glazing schedule was found.', {
      suggestedAction: 'Upload a schedule, use drawing-assisted takeoff, or accept this risk before quote generation.'
    }));
  }
  if (!items.length) {
    risks.push(makeRisk('critical', 'No priced glazing items were extracted from the tender pack.', {
      suggestedAction: 'Review intake records and unsupported image/scanned drawing files.'
    }));
  }
  items.forEach((item) => {
    if (!item.width || !item.height) {
      risks.push(makeRisk('critical', `Item ${item.reference || item.id} is missing dimensions.`, {
        itemId: item.id,
        suggestedAction: 'Enter width and height before quote generation.'
      }));
    }
  });
  return risks;
}

function makeRisk(severity, message, extra = {}) {
  return {
    id: `risk-${Math.random().toString(16).slice(2)}-${Date.now()}`,
    type: 'risk',
    severity,
    message,
    status: 'open',
    suggestedAction: '',
    ...extra
  };
}

function printSummary(report, jsonPath, csvPath) {
  const byType = countBy(report.items, 'type');
  const missingDims = report.items.filter((item) => !item.width || !item.height);
  const unknownFrame = report.items.filter((item) => item.frameType === 'Unknown');
  console.log('');
  console.log('Extraction summary');
  console.log(`Items: ${report.items.length} (${Object.entries(byType).map(([k, v]) => `${k}: ${v}`).join(', ') || 'none'})`);
  console.log(`Warnings: ${report.warnings.length}`);
  console.log(`Risks: ${(report.risks || []).length}`);
  console.log(`Missing dimensions: ${missingDims.length}`);
  console.log(`Unknown frame type: ${unknownFrame.length}`);
  console.log(`Subtotal: ${Pricing.formatCurrency(report.summary.subtotal)}`);
  console.log(`Install: ${Pricing.formatCurrency(report.summary.installTotal)}`);
  console.log(`VAT: ${Pricing.formatCurrency(report.summary.vatAmount)}`);
  console.log(`Total: ${Pricing.formatCurrency(report.summary.total)}`);
  console.log(`JSON: ${jsonPath}`);
  console.log(`CSV: ${csvPath}`);
}

function countBy(rows, key) {
  return rows.reduce((acc, row) => {
    const value = row[key] || 'unknown';
    acc[value] = (acc[value] || 0) + 1;
    return acc;
  }, {});
}

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}
