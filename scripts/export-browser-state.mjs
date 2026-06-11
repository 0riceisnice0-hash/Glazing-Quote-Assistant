import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const require = createRequire(import.meta.url);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, '..');
const bundledNodeModules = 'C:\\Users\\zacpl\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\node\\node_modules';
const { chromium } = loadPlaywright();

const args = parseArgs(process.argv.slice(2));
const tenderDir = path.resolve(args.dir || process.cwd());
const outDir = path.resolve(args.out || path.join(rootDir, 'test-results', 'browser-state'));
const includePattern = new RegExp(args.include || '\\.pdf$', 'i');

await fs.mkdir(outDir, { recursive: true });

const files = (await listFiles(tenderDir))
  .filter((filePath) => includePattern.test(filePath))
  .filter((filePath) => !isQuoteOrSupplierPath(filePath))
  .sort((a, b) => path.basename(a).localeCompare(path.basename(b)));

if (!files.length) {
  throw new Error(`No files matched ${includePattern} under ${tenderDir}`);
}

console.log(`Browser-state export`);
console.log(`Tender directory: ${tenderDir}`);
console.log(`Files: ${files.length}`);

const browser = await chromium.launch({ headless: args.headed ? false : true });
const page = await browser.newPage();
page.setDefaultTimeout(Number(args.timeout || 180000));

const consoleLines = [];
page.on('console', (msg) => {
  const line = `[${msg.type()}] ${msg.text()}`;
  consoleLines.push(line);
  if (args.verbose) console.log(line);
});
page.on('pageerror', (err) => {
  const line = `[pageerror] ${err.message}`;
  consoleLines.push(line);
  console.error(line);
});

try {
  await page.goto(pathToFileURL(path.join(rootDir, 'index.html')).href, {
    waitUntil: 'networkidle',
    timeout: Number(args.timeout || 180000)
  });

  await page.waitForFunction(() => typeof window.App !== 'undefined' && typeof window.pdfjsLib !== 'undefined');

  await page.evaluate(() => localStorage.removeItem('glazingQuoteState'));
  await page.reload({ waitUntil: 'networkidle' });
  await page.waitForFunction(() => typeof window.App !== 'undefined' && typeof window.pdfjsLib !== 'undefined');

  const input = page.locator('#fileInput');
  await input.setInputFiles(files);
  await page.waitForFunction(() => {
    const btn = document.getElementById('analyseBtn');
    return btn && !btn.disabled;
  });

  await page.click('#analyseBtn');
  await page.waitForFunction(() => {
    const state = window.App && window.App.getState && window.App.getState();
    const loadingHidden = document.getElementById('loadingOverlay')?.classList.contains('hidden');
    return loadingHidden && state && Array.isArray(state.items) && state.items.length > 0;
  }, { timeout: Number(args.analysisTimeout || 300000) });

  const state = await page.evaluate(() => JSON.parse(JSON.stringify(window.App.getState())));
  const summary = await page.evaluate(() => {
    const state = window.App.getState();
    return window.Pricing.getPriceSummary(state.items, state.pricing);
  });

  const itemCountText = await textContent(page, '#statItemCount');
  const subtotalText = await textContent(page, '#statSubtotal');
  const totalText = await textContent(page, '#statTotal');
  const warningsText = await textContent(page, '#statWarnings');

  const runStamp = new Date().toISOString().replace(/[:.]/g, '-');
  const jsonPath = path.join(outDir, `browser-state-${runStamp}.json`);
  const csvPath = path.join(outDir, `browser-state-items-${runStamp}.csv`);
  const logPath = path.join(outDir, `browser-state-console-${runStamp}.log`);

  const report = {
    runAt: new Date().toISOString(),
    tenderDir,
    files,
    ui: {
      itemCount: itemCountText,
      subtotal: subtotalText,
      total: totalText,
      warnings: warningsText
    },
    summary,
    state
  };

  await fs.writeFile(jsonPath, JSON.stringify(report, null, 2), 'utf8');
  await fs.writeFile(csvPath, toCsv(state.items), 'utf8');
  await fs.writeFile(logPath, consoleLines.join('\n'), 'utf8');

  console.log(`Items: ${state.items.length}`);
  console.log(`Subtotal: ${summary.subtotal}`);
  console.log(`Installation: ${summary.installTotal}`);
  console.log(`VAT: ${summary.vatAmount}`);
  console.log(`Total: ${summary.total}`);
  console.log(`UI subtotal: ${subtotalText}`);
  console.log(`UI total: ${totalText}`);
  console.log(`JSON: ${jsonPath}`);
  console.log(`CSV: ${csvPath}`);
  console.log(`Console log: ${logPath}`);
} finally {
  await browser.close();
}

function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--dir') parsed.dir = argv[++i];
    else if (arg === '--out') parsed.out = argv[++i];
    else if (arg === '--include') parsed.include = argv[++i];
    else if (arg === '--timeout') parsed.timeout = argv[++i];
    else if (arg === '--analysis-timeout') parsed.analysisTimeout = argv[++i];
    else if (arg === '--headed') parsed.headed = true;
    else if (arg === '--verbose') parsed.verbose = true;
    else if (arg === '--help' || arg === '-h') {
      console.log('Usage: node scripts/export-browser-state.mjs --dir "path/to/tender pack" [--out test-results/browser] [--include "\\\\.pdf$"]');
      process.exit(0);
    }
  }
  return parsed;
}

function loadPlaywright() {
  try {
    return require('playwright');
  } catch {
    const bundledRequire = createRequire(path.join(bundledNodeModules, 'playwright', 'package.json'));
    return bundledRequire('playwright');
  }
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

function isQuoteOrSupplierPath(filePath) {
  const relative = path.relative(tenderDir, filePath).toLowerCase();
  const parts = relative.split(/[\\/]+/);
  return parts.some((part) => /\bclient quote\b/.test(part)) ||
    parts.some((part) => /\bsupplier quotes?\b/.test(part)) ||
    /\bquote\b/i.test(path.basename(filePath)) && !/\bboq\b|\bbq\b|bill|schedule|pricing schedule/i.test(path.basename(filePath));
}

async function textContent(page, selector) {
  const value = await page.locator(selector).textContent().catch(() => '');
  return (value || '').trim();
}

function toCsv(items) {
  const headers = [
    'reference', 'type', 'location', 'width', 'height', 'quantity', 'frameType',
    'colour', 'finish', 'glazingSpec', 'openingType', 'securityRequirement',
    'fireRating', 'uValue', 'notes', 'productCode', 'unitPrice', 'totalPrice',
    'confidence', 'sourceDocument', 'sourcePage'
  ];
  const lines = [headers.join(',')];
  for (const item of items || []) {
    lines.push(headers.map((header) => {
      const value = Array.isArray(item[header]) ? item[header].join('; ') : item[header];
      return csvCell(value);
    }).join(','));
  }
  return `${lines.join('\n')}\n`;
}

function csvCell(value) {
  if (value === undefined || value === null) return '';
  const text = String(value);
  if (/[",\n\r]/.test(text)) return `"${text.replace(/"/g, '""')}"`;
  return text;
}
