import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const bundled = 'C:\Users\zacpl\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules';
let chromium;
try { chromium = require('playwright').chromium; }
catch { chromium = require(bundled + '\playwright').chromium; }

const url = 'https://mary-dashboard.pages.dev/';
const b = await chromium.launch();
const p = await b.newPage();
await p.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
await p.waitForTimeout(4000);
const txt = await p.evaluate(() => document.body.textContent || '');
const checks = {
  'page loaded (chars)': txt.length,
  'Balham appears': (txt.match(/Balham/g) || []).length,
  'NEW: "two packages, one number"': txt.includes('two packages, one number'),
  'NEW: CW 142,760 on the page': txt.includes('142,760'),
  'NEW: Liam Ryan named': txt.includes('Liam Ryan'),
  'OLD (must be gone): "final answer on BALHAM"': txt.includes('final answer on BALHAM'),
  'row value 833,609 still shown': txt.includes('833,609'),
};
for (const [k, v] of Object.entries(checks)) console.log(String(v).padEnd(8), k);
await b.close();
