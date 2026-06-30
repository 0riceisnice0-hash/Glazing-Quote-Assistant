# Glazing Quote Assistant

A professional, client-side web application for glazing contractors to extract items from tender PDFs and generate detailed quotation PDFs — all in the browser, no server required.

**Live App:** [https://glazing-quote-assistant.pages.dev](https://glazing-quote-assistant.pages.dev)

Legacy GitHub Pages URL: [https://0riceisnice0-hash.github.io/Glazing-Quote-Assistant/](https://0riceisnice0-hash.github.io/Glazing-Quote-Assistant/)

---

## Features

- 📂 **Tender Pack Intake** — drag-and-drop PDFs, Excel workbooks, ZIPs, DOCX, EML, JPG and PNG files; ZIP/DOCX/Excel/PDF are normalised before extraction
- 🔬 **OCR Fallback** — scanned PDFs are automatically detected and processed with Tesseract.js OCR if available
- 🔍 **Automatic Item Detection** — pattern-matches window (W01…), door (D01…), screen (S01…), and curtain walling (C01…) references with dimensions, frame types, and glazing specs
- 🧠 **Rich Document Classification** — classifies each document as schedule, BQ, drawing, specification, admin, or unknown, with confidence level and reason
- 🔬 **Extraction Diagnostics** — toggle the diagnostics panel to inspect raw text, classification, extracted items, and warnings per document
- ✏️ **Inline Editing** — click any table cell to edit it directly; full modal editor for complex items
- 💰 **Flexible Pricing Engine** — base rate per m², per-material multipliers (aluminium, PVCu, timber), opening-type multipliers, special spec multipliers (fire rated, acoustic, toughened, laminated), discount, and VAT
- ⚠️ **Smart Warnings** — flags missing dimensions, unknown frame types, cross-document discrepancies, and references found in drawings but missing from the window schedule
- ✅ **Estimator Approval Gate** — critical risks such as no schedule, no priced items, missing dimensions, or OCR/drawing-derived items must be reviewed or accepted before quote generation
- ☁️ **Optional Cloudflare Worker Intake** — unsupported local files can be sent to an internal Worker for ZIP/DOCX/EML normalisation
- 📑 **Professional PDF Output** — generates a full A4 quotation PDF with itemised schedule, company branding, price summary, terms & conditions, and signature line
- 💾 **Auto-save** — state persists to `localStorage` every 30 seconds
- 🌙 **Dark Mode** — toggle with the moon/sun button in the header
- 📤 **JSON Export/Import** — save and reload sessions

---

## How to Use

### Step 1 — Upload Documents

1. Drag and drop one or more tender files onto the upload area, or click to browse.
2. You can upload multiple documents: window schedule, bill of quantities, drawings, specifications, ZIP packs, DOCX/EML documents, and images.
3. Click **Analyse Documents**.

The app will:
- Extract text from each supported file using the relevant local parser
- Classify each document (schedule, BQ, drawing, admin, specification, unknown)
- Attempt OCR on scanned pages and image files (if Tesseract.js is loaded)
- Extract glazing items from schedule and BQ documents
- Cross-reference drawing references against the window schedule

### Step 2 — Review & Edit

1. Review the extracted items in the table.
2. Edit dimensions, frame types, glazing specs, quantities, and locations inline.
3. Accept or reject individual items in the PDF verify view.
4. Use **🔬 Diagnostics** (header button) to see raw text, classification, and warnings per document.

### Step 3 — Generate Quote

1. Fill in company details and quote metadata.
2. Click **Generate Quote PDF** to download the A4 quotation.

---

## Document Types

| Type | Description | Extraction Behaviour |
|------|-------------|----------------------|
| `schedule` | Window/Door/Glazing Schedule | Full item extraction (refs + dims + attributes) |
| `bq` | Bill of Quantities / Schedule of Works | Item extraction; dims merged with schedule |
| `drawing` | Architectural drawings (elevation, plan, section, etc.) | Reference markers extracted for cross-validation only |
| `specification` | Specification documents | Material notes extracted (triple glazing, fire rating, acoustics, BS EN standards) |
| `admin` | Warranties, guarantees, enquiry letters | Skipped entirely |
| `unknown` | Unclassified documents | Cautious extraction attempted |

### Classification Confidence

| Confidence | Meaning |
|------------|---------|
| `high` | Classified from filename pattern (e.g. `Window Schedule.pdf`, `3847.C37.pdf`) |
| `medium` | Classified from document content (first 3000 characters) |
| `low` | Could not classify |

---

## Technical Architecture

```
index.html
├── css/styles.css          — All styles including diagnostics panel
├── js/dataModel.js         — State management, item schema, localStorage
├── js/pdfParser.js         — PDF.js/SheetJS wrapper, text extraction, canvas rendering
├── js/documentIntake.js    — ZIP/DOCX/EML/image intake, provenance, supplier evidence and workflow risks
├── js/dataExtractor.js     — Multi-strategy extraction engine
│   ├── classifyDocument()  — Returns {type, confidence, reason}
│   ├── extractDrawingRefs()— Drawing ref cross-validation
│   ├── extractSpecNotes()  — Specification notes
│   └── extractItems()      — Orchestrates all strategies
├── js/ocrFallback.js       — Tesseract.js OCR for scanned PDFs
├── js/diagnostics.js       — Diagnostics panel UI
├── js/pricing.js           — Pricing calculations
├── js/ui.js                — UI rendering
├── js/pdfViewer.js         — PDF overlay viewer
├── js/quoteGenerator.js    — jsPDF quote generation
└── js/app.js               — Main orchestration
```

### Extraction Strategies (in priority order)

1. **Structured Table** — Identifies header rows (Ref, Width, Height, Qty, Frame…) and maps columns spatially
2. **Row-Based** — Finds rows containing glazing references and extracts numbers nearby
3. **Enhanced Regex** — Falls back to regex over the full page text with spatial context
4. **Line-Based** — Splits text by newlines and processes each line individually
5. **Infer Without Ref** — Creates a single item from dimensions alone (schedule/BQ only)

### Item Fields

Each extracted item includes:
- `reference` — e.g. `EW01`, `W01`, `D01`
- `type` — `window` | `door` | `screen` | `curtain wall` | `other`
- `width` / `height` — in millimetres
- `quantity`
- `frameType` — `Aluminium` | `PVCu` | `Timber` | `Steel` | `Unknown`
- `glazingSpec` — e.g. `Double Glazed - Clear`, `Triple Glazed`, `Fire Rated`
- `openingType` — `Fixed` | `Casement` | `Top Hung` | `Tilt & Turn` | `Sliding` | `Bi-fold` | `Pivot`
- `location` — floor/room if detected
- `notes` — array of special requirements
- `confidence` — `high` | `medium` | `low`
- `extractionMethod` — `pdf.js` | `ocr` | `manual`
- `sourceDocument` / `sourcePage`

---

## OCR Support

When a scanned PDF is detected (less than 100 chars/page), the app will:
1. Check if `Tesseract.js` is available (loaded from jsDelivr CDN)
2. If available, render each page to canvas at 2× scale and run OCR
3. Replace pages with no text with the OCR result
4. Mark items with `extractionMethod: 'ocr'`

OCR adds significant processing time (~5–30 seconds per page depending on hardware). The diagnostics panel shows OCR status per document.

---

## Cloudflare Deployment

The primary production frontend is Cloudflare Pages:

```text
https://glazing-quote-assistant.pages.dev
```

The document intake Worker is:

```text
https://gqa-document-processor.0riceisnice0.workers.dev
```

Deploy the static frontend from a clean artifact so tender packs, test results and `node_modules` are not uploaded:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\build-pages.ps1
npx.cmd wrangler pages deploy dist-pages --project-name glazing-quote-assistant --branch main
```

Deploy the Worker:

```powershell
cd workers\document-processor
npm.cmd run deploy
```

---

## Optional Cloud Worker

The upload screen can be configured with a Cloudflare Worker URL for internal testing. When enabled, unsupported local intake files can be sent to the Worker.

Current Worker support:

- ZIP expansion
- DOCX text extraction
- EML body extraction
- Supplier evidence proposal from extracted text

Current Worker limits:

- PDF and Excel still process in the browser.
- Image OCR still uses browser Tesseract. The Worker returns an OCR-needed risk for JPG/PNG until an OCR provider is added.
- MSG parsing is not implemented yet.

Worker source lives in `workers/document-processor`.

---

## Legacy GitHub Pages Deployment

GitHub Pages can still serve the app as a fallback static host, but Cloudflare Pages is the preferred production deployment.

---

## Known Limitations

- **Scanned PDFs** — OCR quality depends on scan resolution and Tesseract.js availability. For best results, use text-based PDFs exported from CAD/BIM software.
- **Non-standard schedules** — PDFs with unusual table layouts or no spatial text positioning may extract fewer items. Use the diagnostics panel to investigate.
- **BQ item quantities** — BQ documents often contain quantity-only data without dimensions. The smart merge will combine BQ quantities with schedule dimensions where references match.
- **Drawing false positives** — Drawing filenames matching `\d{4}.[a-z]\d{2}` (e.g. `3847.C37.pdf`) are classified as drawings and their content skipped to avoid false positives from title block references.
- **Large files** — Very large PDFs (100+ pages) may be slow in the browser. Consider splitting before uploading.

---

## Privacy

By default, processing happens in your browser. If the optional Cloudflare Worker setting is enabled, selected unsupported files are sent to the configured Worker URL for internal document intake.

---

*Glazing Quote Assistant — built for glazing professionals.*
