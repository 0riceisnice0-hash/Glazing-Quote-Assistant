import fs from 'node:fs/promises';
import path from 'node:path';

const args = parseArgs(process.argv.slice(2));
if (!args.state) {
  console.error('Usage: node scripts/compare-state-to-quote.mjs --state exported-session.json [--actual 119800.19] [--label "Addington Road uPVC"]');
  process.exit(1);
}

const raw = JSON.parse(await fs.readFile(path.resolve(args.state), 'utf8'));
const state = normaliseState(raw);
const summary = state.summary || calculateSummaryFromItems(state);
const actual = args.actual !== undefined ? Number(args.actual) : undefined;
const label = args.label || path.basename(args.state);

const result = {
  label,
  stateFile: path.resolve(args.state),
  sourceDocuments: (state.sourceDocuments || []).map((doc) => ({
    name: doc.name,
    type: doc.docType || doc.classification?.type || '',
    pages: doc.pageCount
  })),
  itemCount: (state.items || []).length,
  warningCount: (state.warnings || []).length,
  subtotal: round2(summary.subtotal),
  installation: round2(summary.installTotal || 0),
  beforeVat: round2(summary.beforeDiscount ?? ((summary.subtotal || 0) + (summary.installTotal || 0))),
  vat: round2(summary.vatAmount || 0),
  total: round2(summary.total),
  actual: actual !== undefined ? round2(actual) : undefined,
  variance: actual !== undefined ? round2((summary.beforeDiscount ?? summary.total) - actual) : undefined,
  variancePercent: actual !== undefined && actual ? round2(((summary.beforeDiscount ?? summary.total) - actual) / actual * 100) : undefined,
  topSourceDocuments: topSourceDocuments(state.items || []),
  incompleteCounts: {
    missingDimensions: (state.items || []).filter((item) => !item.width || !item.height).length,
    unknownFrame: (state.items || []).filter((item) => item.frameType === 'Unknown').length
  }
};

console.log(JSON.stringify(result, null, 2));

function parseArgs(argv) {
  const parsed = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--state') parsed.state = argv[++i];
    else if (arg === '--actual') parsed.actual = argv[++i];
    else if (arg === '--label') parsed.label = argv[++i];
  }
  return parsed;
}

function normaliseState(raw) {
  if (raw.state) return raw.state.summary ? raw.state : { ...raw.state, summary: raw.summary };
  if (raw.items && raw.summary) return raw;
  return raw;
}

function calculateSummaryFromItems(state) {
  const items = state.items || [];
  const subtotal = items.reduce((sum, item) => sum + Number(item.totalPrice || 0), 0);
  const pricing = state.pricing || {};
  const includeInstallation = pricing.includeInstallation !== false;
  const installTotal = includeInstallation
    ? items.reduce((sum, item) => sum + Number(pricing.installationPerUnit || 140) * Number(item.quantity || 1), 0)
    : 0;
  const beforeDiscount = subtotal + installTotal + Number(pricing.quoteExtraAmount || 0);
  const vatEnabled = pricing.vatEnabled !== false;
  const vatRate = Number(pricing.vatRate || 20);
  const vatAmount = vatEnabled ? beforeDiscount * vatRate / 100 : 0;
  return {
    subtotal,
    installTotal,
    beforeDiscount,
    vatAmount,
    total: beforeDiscount + vatAmount
  };
}

function topSourceDocuments(items) {
  const counts = {};
  for (const item of items) {
    const key = item.sourceDocument || '(none)';
    counts[key] = (counts[key] || 0) + 1;
  }
  return Object.entries(counts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([sourceDocument, count]) => ({ sourceDocument, count }));
}

function round2(value) {
  return Math.round(Number(value || 0) * 100) / 100;
}
