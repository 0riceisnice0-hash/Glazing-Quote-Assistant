# Glazing Quote Assistant

A professional, client-side web application for glazing contractors to extract items from tender PDFs and generate detailed quotation PDFs — all in the browser, no server required.

**Live Demo:** [https://0riceisnice0-hash.github.io/Glazing-Quote-Assistant/](https://0riceisnice0-hash.github.io/Glazing-Quote-Assistant/)

---

## Features

- 📂 **PDF Upload & Text Extraction** — drag-and-drop or click to upload tender PDFs; uses PDF.js for client-side text extraction
- 🔍 **Automatic Item Detection** — pattern-matches window (W01…), door (D01…), screen (S01…), and curtain walling (C01…) references with dimensions, frame types, and glazing specs
- ✏️ **Inline Editing** — click any table cell to edit it directly; full modal editor for complex items
- 💰 **Flexible Pricing Engine** — base rate per m², per-material multipliers (aluminium, PVCu, timber), opening-type multipliers, special spec multipliers (fire rated, acoustic, toughened, laminated), discount, and VAT
- ⚠️ **Smart Warnings** — flags missing dimensions, unknown frame types, and cross-document discrepancies
- 📑 **Professional PDF Output** — generates a full A4 quotation PDF with itemised schedule, company branding, price summary, terms & conditions, and signature line
- 💾 **Auto-save** — state persists to `localStorage` every 30 seconds
- 🌙 **Dark Mode** — toggle with the moon/sun button in the header
- 📤 **JSON Export/Import** — save and reload sessions

---

## How to Use

### Step 1 — Upload
1. Drag and drop one or more PDF tender documents (window schedules, door schedules, drawing registers) onto the upload zone, or click to browse.
2. Adjust the **Pricing Settings** panel on the right (base rate, multipliers, VAT).
3. Click **Analyse Documents**.

### Step 2 — Review & Edit
- All detected glazing items appear in the table.
- **Inline edit** any cell by clicking it; press Enter or Tab to save.
- Use the **Edit** (✏️) button on a row for the full detail modal.
- **Duplicate** or **Delete** rows with the row action buttons.
- Use **Add Item** to create a blank item manually.
- The **Warnings** panel lists extraction issues; click "Go to item" to highlight the relevant row.
- The **Price Summary** updates automatically.

### Step 3 — Generate Quote
1. Fill in your **Company Details** (name, address, phone, email, logo).
2. Fill in the **Quote Details** (quote number, date, project name, client).
3. Click **Generate Quote PDF** — the PDF downloads automatically.

---

## Running Locally

No build step needed. Just open `index.html`:

```bash
# Option 1: Open directly
open index.html

# Option 2: Serve with npx serve (recommended for full PDF.js worker support)
npx serve .
# Then visit http://localhost:3000
```

---

## Architecture

| File | Purpose |
|---|---|
| `index.html` | Single-page app shell, CDN scripts, step wizard layout |
| `css/styles.css` | All styling — CSS custom properties, dark mode, responsive |
| `js/dataModel.js` | Central state, `DEFAULT_STATE`, `createItem()`, localStorage helpers |
| `js/pdfParser.js` | PDF.js wrapper — drop zone setup, text extraction, scanned detection |
| `js/dataExtractor.js` | Regex pattern engine — reference, dimension, frame, glazing, opening detection |
| `js/pricing.js` | Price calculation engine with multipliers, VAT, discounts |
| `js/ui.js` | All DOM rendering — table, warnings panel, modals, toasts, inline editing |
| `js/quoteGenerator.js` | jsPDF-based PDF generation with autoTable |
| `js/app.js` | Main orchestration — wires everything together, auto-save, step navigation |
| `assets/logo-placeholder.svg` | Default SVG logo shown until a company logo is uploaded |

---

## Customising Pricing

All pricing is configurable through the UI (Step 1 sidebar) and persists to localStorage.

- **Base Rate (£/m²)** — the foundation price per square metre
- **Multipliers** — each factor multiplies the base calculation:
  - Frame type: Aluminium (1.0), PVCu (0.7), Timber (0.9)
  - Opening type: Fixed (0.9), Casement (1.0), Top Hung (1.1), Tilt & Turn (1.15), Sliding (1.2)
  - Special specs: Fire Rated (1.8), Acoustic (1.4), Toughened (1.2), Laminated (1.15)
  - Glazing: Triple Glazed (1.3), Obscure (1.05)

**Formula:** `Base Rate × Area(m²) × Frame Mult × Glazing Mult × Opening Mult × Special Mults`

---

## Tech Stack

| Technology | Usage |
|---|---|
| Plain HTML/CSS/JS | No framework, no build step — pure browser-native |
| [PDF.js 3.11](https://mozilla.github.io/pdf.js/) | Client-side PDF text extraction |
| [jsPDF 2.5](https://rawgit.com/MrRio/jsPDF/master/docs/) | PDF generation |
| [jsPDF AutoTable 3.7](https://github.com/simonbengtsson/jsPDF-AutoTable) | Table rendering in PDF |
| CSS Custom Properties | Theming (light/dark modes) |
| localStorage | State persistence, dark mode preference |

---

## Workflow Screenshot Summary

1. **Upload screen** — Drop zone + file list + pricing panel sidebar
2. **Review screen** — Sortable/filterable table with inline editing, warnings sidebar, price summary
3. **Generate screen** — Company/quote forms, live preview panel, one-click PDF generation

---

## Notes

- Works best with **text-based PDFs** (digitally created, not scanned). For scanned documents, the app will warn you and allow manual entry.
- All data stays in your browser — nothing is uploaded to any server.
- Quote number auto-generates as `GQ-YYYYMMDD-NNN` format on first load.
