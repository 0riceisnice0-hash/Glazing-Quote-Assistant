# Developer Summary — Shaftesbury Tender Support & Fenster Pricing Model

## What Was Built

The Glazing Quote Assistant was extended from handling simple W01/D01-style window/door schedules to supporting **Shaftesbury Hotel style tender documents** (NW/ND reference patterns, J-number drawings, 10 new detail fields) and a **realistic pricing engine** based on Fenster's actual master pricing document.

---

## Files Changed & What Was Added

### 1. `js/dataExtractor.js` — Core Extraction Engine (~400 lines added)

**Reference patterns:**
- Extended `REF_FIRST_PATTERN` regex to accept `NW01–NW99` (windows) and `ND01–ND99` (doors) alongside existing `W/D/S/C/EW/ED` prefixes
- Added J-number filename detection (`J4715-YMD-01-XX-DR-A-3300` style) for document classification

**10 new detail extractor functions:**
| Function | What it finds | Example matches |
|---|---|---|
| `extractFinish()` | Frame/door finish | "PPC Aluminium", "Formica Laminate", "RAL Colour TBC" |
| `extractUValue()` | Thermal performance | "1.4 W/m²K", "U Value 1.4" |
| `extractSillHeight()` | Sill height in mm | "Sill Height 640" |
| `extractHeadHeight()` | Head height in mm | "Head Height 2175" |
| `extractDoorSwing()` | Door handing | "RHS", "LHS", "Double" |
| `extractFireRating()` | Fire resistance | "FD30S", "FD60", "N/A" |
| `extractIronmongery()` | Hardware sets | "Set C3/C6", "Doc M pack" |
| `extractDoorType()` | YMD door type | "YMD Door Type 1" |
| `extractFrameType()` | Frame material | "Aluminium", "Timber", "PVC" |
| `inferFrameTypeFromFields()` | Fallback from finish/system | Infers from "PPC Aluminium" → Aluminium |

**CharContext extraction approach:**
- Instead of relying on fixed column positions (which vary between different architects' CAD exports), the system maps the position of every reference in the raw PDF text, then extracts the text *between* the current reference and the next one as context
- Uses `MIN_DATA_SPAN = 60` chars to reject tiny fragments, `MAX_CHAR_CONTEXT = 500` to prevent bleed
- Prefers the first occurrence with sufficient data, falls back to longest candidate

**Document-level frame type inference:**
- If per-item extraction fails, searches the entire document text for phrases like "PPC Aluminium", "aluminium frame", "window frame finish" near the reference
- Added false-positive rejection for postcodes (CV7 7LB), revision markers (C01), and scale prefixes

**Header column keywords expanded:**
- Added column mappings for `sillHeight`, `headHeight`, `uValue`, `finish`, `doorSwing`, `fireRating`, `doorFrame`, `doorGlazing`, `ironmongery`, `doorType`

---

### 2. `js/dataModel.js` — Data Schema

**New item fields:**
```
sillHeight, headHeight, uValue, doorSwing, fireRating,
doorFrame, doorGlazing, ironmongery, finish, doorType
```

**Preset profiles system** — four built-in templates:
- Aluminium Commercial Window/Door
- uPVC Residential Window/Door

**Pricing schema** migrated from v2 (generic multipliers) to v3 (Fenster model):
- Removed: `fixedCostPerUnit`, `baseRatePerM2`, `doorFixedCostPerUnit`, `doorRatePerM2`, `multipliers{}`
- Added: `aluminiumFrameRate`, `pvcFrameRate`, `timberFrameRate`, `steelFrameRate`, glass rates, `installationPerUnit`, `cwSupplyRate`, `cwLabourRate`, `epdmRate`, `masticRate`, toggle flags

---

### 3. `js/pricing.js` — Complete Rewrite (~290 lines)

Replaced generic formula (`fixedCost + ratePerM² × area × multipliers`) with Fenster's actual model:

**Formula:** `Unit Rate = Frames + Glass + Additional + ProductCodeMarkup`

**18 product codes** with markups extracted from master pricing spreadsheet:

| Code | Markup | Description |
|------|--------|-------------|
| SAW | £400 | Small Aluminium Window (≤2.5m²) |
| MAW | £500 | Medium Aluminium Window (≤6m²) |
| LAW | £600 | Large Aluminium Window (≤12m²) |
| ELAW | £1,000 | Extra Large Aluminium Window (>12m²) |
| SPVC | £300 | Small PVC Window |
| MPVC | £350 | Medium PVC Window |
| LPVC | £400 | Large PVC Window |
| SAD | £1,150 | Single Aluminium Door |
| DAD | £1,950 | Double Aluminium Door |
| UPD | £950 | uPVC Door |
| SADSAW | £1,650 | Single Alum Door + Small Window |
| SADMAW | £1,850 | Single Alum Door + Med Window |
| SADLAW | £1,950 | Single Alum Door + Large Window |
| STD | £800 | Single Timber Door (estimated) |
| DTD | £1,400 | Double Timber Door (estimated) |
| SSD | £1,300 | Single Steel Door |
| DSD | £2,200 | Double Steel Door |
| CW | per m² | Curtain Wall (£850 supply + £150 labour) |

**Automatic classification** — `classifyProductCode(item)` assigns codes based on item type, frame material, door swing, reference prefix, and window area thresholds.

**Supplier cost estimation** — when no actual supplier quotes are available, estimates frame and glass costs using configurable £/m² rates.

**Separate line items** — Installation (£140/unit), EPDM (£25/m²), Mastic (£5/linear m) as toggleable additions.

---

### 4. `js/ui.js` — UI Updates (~150 lines changed)

- **Item table:** added columns for Finish, Fire Rating, Swing, Ironmongery, U-Value, and Product Code
- **Edit modal:** added all 10 new fields as editable inputs
- **Pricing panel:** replaced old form (fixedCost/ratePerM²/multiplierGrid) with Fenster-model inputs (frame rates, glass rates, fixed rates, toggles, product code reference grid)
- **Price summary:** shows Installation, EPDM, Mastic as separate line items in both step 2 panel and step 3 summary

---

### 5. `js/quoteGenerator.js` — PDF Output (~50 lines changed)

- **Per-item spec cards** now include system, colour, finish, hardware, cill type, drainage, ventilation
- **Type spec block** renders preset general specifications once per item type
- **Price summary box** dynamically sizes to include Installation, EPDM, Mastic rows

---

### 6. `index.html` — HTML (~80 lines changed)

- Replaced pricing settings panel with Fenster-model inputs
- Cache bust version bumped to `?v=20260328`

---

### 7. `test/extraction-test.html` — Test Suite (~300 lines added)

**4 new test suites (Suites 9–12):**

| Suite | What it tests | Assertions |
|-------|---------------|------------|
| 9 — Shaftesbury Windows | NW01–NW11 extraction, dimensions, U-Value, sill/head height, finish, frame type, BOQ quantities | ~15 assertions |
| 10 — Shaftesbury Doors | ND01–ND14 + ED01, door swing, fire rating, ironmongery, door frame/glazing | ~15 assertions |
| 11 — Document Classification | J-number filenames → schedule/drawing/BQ type detection | ~5 assertions |
| 12 — Full Pipeline | Combined window + door + BOQ + elevation extraction, quantity cross-reference | ~10 assertions |

All 17 test suites passing.

---

## What Would Need to Change for New Tender Formats

When a new tender comes in with a different layout, here's what will likely need attention:

### Almost Certainly Needed

1. **Reference patterns** (`dataExtractor.js`, line ~591)
   - If the new tender uses different prefixes (e.g. `WN01`, `DR01`, `FW-01`, `EXT.W.01`), add them to `REF_FIRST_PATTERN`
   - This is the single most common difference between architects

2. **Document classification** (`dataExtractor.js`, line ~23–35)
   - If filenames don't match existing patterns (J-numbers, standard schedule names), add new filename regex
   - Some architects use completely different naming conventions

3. **Location patterns** (`dataExtractor.js`, `extractLocation()`)
   - Floor naming varies: "Ground Floor" vs "GF" vs "Level 0" vs "Floor 00"
   - Building wing/zone naming is project-specific

### Probably Needed

4. **Header column keywords** (`dataExtractor.js`, lines ~191–207)
   - Different architects use different column headers: "Window Width" vs "Overall Width" vs "Structural Opening" vs "W"
   - Add aliases to `HEADER_COLUMN_KEYWORDS` for new terminology

5. **Detail extraction regexes** (the `extract*()` functions)
   - Finish descriptions vary hugely: "Anodised", "Marine Grade", "Syntha Pulvin" etc.
   - Fire ratings may use different notation: "E30", "EI30", "REI60"
   - Hardware/ironmongery descriptions are completely project-specific

6. **Product code classification thresholds** (`pricing.js`, `classifyProductCode()`)
   - Window size thresholds (S/M/L/EL) may need tuning for different project mixes
   - New frame materials (composite frames, GRP) would need new codes
   - Combo units (door + sidelight) detection currently based on explicit codes — may need automated detection from linked references

### Possibly Needed

7. **CharContext tuning** (`dataExtractor.js`)
   - `MIN_DATA_SPAN` (60 chars) and `MAX_CHAR_CONTEXT` (500 chars) work for current tenders but dense schedules might need adjustment
   - If a tender uses merged cells or very wide tables, the character ordering from PDF.js may be unexpected

8. **Pricing rates** (`pricing.js`, `DEFAULT_CONFIG`)
   - Supplier rates change over time and by project
   - Product code markups may be revised by Fenster's estimating team
   - New product types (bifold doors, roof lanterns, automatic doors) would need new codes

9. **PDF text extraction strategy**
   - Some architects produce PDFs from Revit (structured), some from AutoCAD (flat text), some are scanned images
   - Scanned documents need OCR fallback (already partially implemented in `ocrFallback.js`)
   - Very complex multi-page schedules might need page-aware extraction

### The Pattern for Adding Support

The general workflow for each new tender format:

1. **Load a sample PDF** and check what references are detected (or not)
2. **Add reference prefix** to `REF_FIRST_PATTERN` if needed
3. **Run the test suite** to make sure existing tenders still work
4. **Check extraction quality** — are dimensions, types, and details populating?
5. **Add/tweak extraction regexes** for any project-specific terminology
6. **Add a test suite** with representative data from the new format
7. **Verify pricing** — do product codes classify correctly for the new items?

The architecture is designed so that most adaptations only require regex additions, not structural changes. The charContext approach and multiple-strategy fallback (structured table → reference-first → page-walking) handle most PDF layout variations automatically.
