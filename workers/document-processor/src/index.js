import JSZip from 'jszip';

const IMAGE_RE = /\.(jpe?g|png)$/i;
const DOCX_RE = /\.docx$/i;
const EML_RE = /\.eml$/i;
const MSG_RE = /\.msg$/i;
const ZIP_RE = /\.zip$/i;
const WORKBOOK_RE = /\.(xlsx|xlsm|xls)$/i;
const PDF_RE = /\.pdf$/i;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (request.method === 'OPTIONS') return cors(new Response(null, { status: 204 }));
    if (url.pathname === '/health') {
      return json({ ok: true, service: 'gqa-document-processor', version: '0.1.0' });
    }
    if (request.method !== 'POST') {
      return json({ error: 'Method not allowed' }, 405);
    }
    if (url.pathname === '/process-file' || url.pathname === '/process-pack') {
      return handleProcess(request, env);
    }
    return json({ error: 'Not found' }, 404);
  }
};

async function handleProcess(request, env) {
  const maxBytes = Number(env.GQA_MAX_FILE_BYTES || 25000000);
  const form = await request.formData();
  const files = form.getAll('files').filter((value) => value && typeof value.arrayBuffer === 'function');
  if (!files.length) return json({ documents: [], risks: [risk('critical', 'No files were supplied to the worker.')] });

  const result = emptyResult();
  for (const file of files) {
    if (file.size > maxBytes) {
      result.risks.push(risk('critical', `File is too large for worker processing: ${file.name}`, {
        sourceDocumentName: file.name,
        suggestedAction: 'Split the file or process it locally.'
      }));
      continue;
    }
    merge(result, await processBlob(file, {
      name: file.name || 'upload',
      originalPath: file.name || 'upload',
      parentArchive: ''
    }));
  }
  return json(result);
}

async function processBlob(blob, context) {
  const name = context.originalPath || context.name;
  if (ZIP_RE.test(name)) return processZip(blob, context);
  if (DOCX_RE.test(name)) return processDocx(blob, context);
  if (EML_RE.test(name)) return processEml(blob, context);
  if (MSG_RE.test(name)) return unsupported(name, 'msg', 'MSG parsing is not implemented in the free worker yet.');
  if (IMAGE_RE.test(name)) return unsupported(name, 'image', 'Worker OCR is not configured yet; use browser OCR/Tesseract or add an OCR provider.');
  if (PDF_RE.test(name) || WORKBOOK_RE.test(name)) {
    return {
      documents: [],
      risks: [risk('warning', `Worker skipped locally-supported file: ${name}`, {
        sourceDocumentName: name,
        suggestedAction: 'Process this file in the browser PDF/Excel path.'
      })],
      supplierEvidence: [],
      intakeRecords: [record(name, context.parentArchive, inferKind(name), 'local-preferred')]
    };
  }
  return unsupported(name, 'unsupported', 'Unsupported file type.');
}

async function processZip(blob, context) {
  const result = emptyResult();
  result.intakeRecords.push(record(context.originalPath, context.parentArchive, 'zip', 'zip-opened-worker'));
  const zip = await JSZip.loadAsync(await blob.arrayBuffer());
  const entries = [];
  zip.forEach((relativePath, entry) => {
    if (!entry.dir) entries.push({ relativePath, entry });
  });
  for (const item of entries) {
    const childName = `${context.originalPath}/${item.relativePath}`;
    const childBlob = new Blob([await item.entry.async('arraybuffer')]);
    merge(result, await processBlob(childBlob, {
      name: item.relativePath,
      originalPath: childName,
      parentArchive: context.originalPath
    }));
  }
  if (!entries.length) {
    result.risks.push(risk('warning', `ZIP archive was empty: ${context.originalPath}`, {
      sourceDocumentName: context.originalPath
    }));
  }
  return result;
}

async function processDocx(blob, context) {
  const zip = await JSZip.loadAsync(await blob.arrayBuffer());
  const docXml = zip.file('word/document.xml');
  if (!docXml) {
    return unsupported(context.originalPath, 'docx', 'DOCX has no readable word/document.xml.');
  }
  const text = extractDocxText(await docXml.async('text'));
  const doc = textDocument(context.originalPath, context.parentArchive, 'docx', text, 'worker-docx');
  return {
    documents: [doc],
    risks: risksForTextDoc(doc),
    supplierEvidence: extractSupplierEvidence(doc),
    intakeRecords: [record(context.originalPath, context.parentArchive, 'docx', 'processed-worker')]
  };
}

async function processEml(blob, context) {
  const raw = await blob.text();
  const subject = (raw.match(/^subject:\s*(.+)$/im) || [])[1] || '';
  const body = raw.split(/\r?\n\r?\n/).slice(1).join('\n\n')
    .replace(/--[A-Za-z0-9'()+_,\-\.\/:=?]+(?:--)?/g, '\n')
    .replace(/Content-[^\n]+\n/gi, '\n')
    .trim();
  const text = (subject ? `Subject: ${subject}\n\n` : '') + body;
  const doc = textDocument(context.originalPath, context.parentArchive, 'email', text, 'worker-email');
  const risks = risksForTextDoc(doc);
  if (/attachment/i.test(raw)) {
    risks.push(risk('warning', `Email may contain attachments that need separate processing: ${context.originalPath}`, {
      sourceDocumentName: context.originalPath,
      suggestedAction: 'Upload the attachments or original ZIP pack.'
    }));
  }
  return {
    documents: [doc],
    risks,
    supplierEvidence: extractSupplierEvidence(doc),
    intakeRecords: [record(context.originalPath, context.parentArchive, 'email', 'processed-worker')]
  };
}

function unsupported(name, kind, message) {
  return {
    documents: [],
    risks: [risk(kind === 'image' ? 'warning' : 'critical', `${message} ${name}`, {
      sourceDocumentName: name,
      suggestedAction: kind === 'image'
        ? 'Run browser OCR or add an OCR provider to the Worker.'
        : 'Convert this file to PDF/DOCX/EML or process manually.'
    })],
    supplierEvidence: [],
    intakeRecords: [record(name, '', kind, 'unsupported-worker')]
  };
}

function textDocument(name, parentArchive, kind, text, extractionMethod) {
  const doc = {
    id: id(),
    name,
    originalPath: name,
    parentArchive: parentArchive || '',
    kind,
    role: inferRole(name, text),
    pageCount: 1,
    pages: [{ pageNum: 1, text: text || '', textItems: [], width: 0, height: 0 }],
    fullText: text || '',
    textItems: [],
    isScanned: false,
    extractionMethod,
    provenance: { originalPath: name, parentArchive: parentArchive || '' }
  };
  doc.classification = {
    type: doc.role === 'supplier_quote' || doc.role === 'client_quote' ? 'admin' : doc.role,
    confidence: doc.role === 'unknown' ? 'low' : 'medium',
    reason: 'Worker document intake classification'
  };
  return doc;
}

function inferRole(name, text) {
  const lowerName = String(name || '').toLowerCase();
  const sample = String(text || '').slice(0, 3000).toLowerCase();
  if (/\bclient quote\b|\bclient quotation\b|\bglazing quote\b/.test(lowerName)) return 'client_quote';
  if (/\bsupplier quotes?\b|\bsupplier quotation\b/.test(lowerName)) return 'supplier_quote';
  if (/window\s*schedule|door\s*schedule|glazing\s*schedule|opening\s*size|window\s*ref/.test(lowerName + ' ' + sample)) return 'schedule';
  if (/\bboq\b|\bbq\b|bill\s*of\s*quantities|schedule\s*of\s*works/.test(lowerName + ' ' + sample)) return 'bq';
  if (/\bspec(?:ification)?\b|\bbs\s*en\b/.test(lowerName + ' ' + sample)) return 'specification';
  if (/\bdrawing\b|\belevation\b|\bplan\b|\bsection\b/.test(lowerName + ' ' + sample)) return 'drawing';
  return 'unknown';
}

function risksForTextDoc(doc) {
  const risks = [];
  if (!doc.fullText || doc.fullText.trim().length < 30) {
    risks.push(risk('warning', `Worker extracted little text from: ${doc.name}`, {
      sourceDocumentId: doc.id,
      sourceDocumentName: doc.name
    }));
  }
  if (doc.role === 'supplier_quote') {
    risks.push(risk('info', `Supplier quote treated as cost evidence only: ${doc.name}`, {
      sourceDocumentId: doc.id,
      sourceDocumentName: doc.name
    }));
  }
  if (doc.role === 'client_quote') {
    risks.push(risk('info', `Client quote excluded from extraction: ${doc.name}`, {
      sourceDocumentId: doc.id,
      sourceDocumentName: doc.name
    }));
  }
  return risks;
}

function extractSupplierEvidence(doc) {
  if (doc.role !== 'supplier_quote') return [];
  const evidence = [];
  String(doc.fullText || '').split(/\r?\n/).forEach((line, idx) => {
    const refMatch = line.match(/\b(?:EW|ED|WG|WF|W|D|S|C|SAW|MAW|LAW|SPVC|MPVC|LPVC)[- ]?\d{1,3}[A-Z]?\b/i);
    const moneyMatches = line.match(/(?:£|\bGBP\s*)?\d{1,3}(?:,\d{3})*(?:\.\d{2})/g);
    if (!refMatch || !moneyMatches) return;
    const amounts = moneyMatches.map(parseMoney).filter((amount) => amount > 0);
    if (!amounts.length) return;
    evidence.push({
      id: id(),
      supplierName: '',
      sourceDocumentId: doc.id,
      sourceDocumentName: doc.name,
      sourceLocation: `line ${idx + 1}`,
      matchedItemId: null,
      reference: refMatch[0].replace(/\s+/g, '').toUpperCase(),
      description: line.trim(),
      quantity: 1,
      unitRate: amounts[amounts.length - 1],
      total: amounts[amounts.length - 1],
      matchConfidence: 'low',
      status: 'proposed'
    });
  });
  return evidence;
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

function record(name, parentArchive, kind, status) {
  return { id: id(), name, parentArchive: parentArchive || '', kind, status, documentId: null };
}

function risk(severity, message, extra = {}) {
  return { id: id(), type: 'risk', severity, message, status: 'open', suggestedAction: '', ...extra };
}

function inferKind(name) {
  if (ZIP_RE.test(name)) return 'zip';
  if (DOCX_RE.test(name)) return 'docx';
  if (EML_RE.test(name)) return 'email';
  if (IMAGE_RE.test(name)) return 'image';
  if (PDF_RE.test(name)) return 'pdf';
  if (WORKBOOK_RE.test(name)) return 'workbook';
  return 'file';
}

function parseMoney(value) {
  return parseFloat(String(value).replace(/[£,\s]|GBP/gi, '')) || 0;
}

function emptyResult() {
  return { documents: [], risks: [], supplierEvidence: [], intakeRecords: [] };
}

function merge(target, source) {
  target.documents.push(...(source.documents || []));
  target.risks.push(...(source.risks || []));
  target.supplierEvidence.push(...(source.supplierEvidence || []));
  target.intakeRecords.push(...(source.intakeRecords || []));
}

function id() {
  return crypto.randomUUID ? crypto.randomUUID() : `id-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function json(payload, status = 200) {
  return cors(new Response(JSON.stringify(payload, null, 2), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8' }
  }));
}

function cors(response) {
  response.headers.set('access-control-allow-origin', '*');
  response.headers.set('access-control-allow-methods', 'GET,POST,OPTIONS');
  response.headers.set('access-control-allow-headers', 'content-type');
  return response;
}
