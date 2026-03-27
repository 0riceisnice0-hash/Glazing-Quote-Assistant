/* js/dataExtractor.js — Spatial extraction engine for glazing items */

var DataExtractor = (function () {

  // -----------------------------------------------------------------------
  // Document classification
  // -----------------------------------------------------------------------

  function classifyDocument(docName, textContent) {
    var name = (docName || '').toLowerCase();

    // Filename-based (high confidence)
    if (/window\s*schedule|door\s*schedule|glazing\s*schedule/.test(name))
      return { type: 'schedule', confidence: 'high', reason: 'Filename contains schedule keyword' };
    if (/\bboq\b|\bbq\b|bill\s*of\s*quantities|schedule\s*of\s*works/.test(name))
      return { type: 'bq', confidence: 'high', reason: 'Filename contains BQ keyword' };
    if (/warrant|guarantee|collateral|enquiry\s*letter|letter\s*of\s*enquiry/.test(name))
      return { type: 'admin', confidence: 'high', reason: 'Filename matches admin/legal document pattern' };
    // Previously generated quote PDFs ("GQ-20260320-203.pdf") — skip to avoid phantom items
    if (/^gq-\d/.test(name))
      return { type: 'admin', confidence: 'high', reason: 'Filename matches generated quote pattern (GQ-)' };
    // Drawing-number filenames like "3847.C37 …", "3847.T05 …"
    // Also matches J-number filenames like "J4715-YMD-01-XX-DR-A-3300..." (Shaftesbury-style).
    // IMPORTANT: Only classify as 'drawing' when no schedule/BQ keywords are also present.
    // A filename like "3847.T12 Window Schedule.pdf" contains both a drawing number AND schedule
    // keywords — the schedule checks above already return early, but this guard makes the intent
    // explicit and prevents any future regression.
    if ((/\d{4}\.[a-z]\d{2}/.test(name) || /j\d{4}[\-_]/.test(name)) &&
        !/window\s*schedule|door\s*schedule|glazing\s*schedule/.test(name) &&
        !/\bboq\b|\bbq\b|bill\s*of\s*quantities/.test(name))
      return { type: 'drawing', confidence: 'high', reason: 'Filename matches architectural drawing number pattern' };
    if (/\b(?:elevation|floor\s*plan|site\s*plan|section|detail|proposed|cladding)\b/.test(name))
      return { type: 'drawing', confidence: 'high', reason: 'Filename contains drawing type keyword' };
    if (/\b(?:spec(?:ification)?)\b/.test(name))
      return { type: 'specification', confidence: 'high', reason: 'Filename contains specification keyword' };

    // Content-based (medium confidence) — only when text is available
    if (textContent && textContent.length > 0) {
      var sample = textContent.substring(0, 3000).toLowerCase();
      if (/window\s*schedule|door\s*schedule|glazing\s*schedule|opening\s*size|window\s*ref|glazing\s*ref/.test(sample))
        return { type: 'schedule', confidence: 'medium', reason: 'Content contains schedule keywords' };
      // Table-header pattern: ref/mark column alongside dimension/qty columns strongly suggests a schedule
      // even when the words "window schedule" don't appear in the first 3000 chars.
      if (/\b(?:ref|mark|item\s*no)\b/i.test(sample) &&
          /\b(?:width|height|w\s*\(mm\)|h\s*\(mm\)|qty|quantity)\b/i.test(sample))
        return { type: 'schedule', confidence: 'medium', reason: 'Content contains schedule table headers (ref + dimensions)' };
      if (/bill\s*of\s*quantities|measured\s*work|trade\s*cont|schedule\s*of\s*rates/.test(sample))
        return { type: 'bq', confidence: 'medium', reason: 'Content contains BQ keywords' };
      if (/drawing\s*no|revision\s*[a-z]\b|scale\s*1\s*:|north\s*point|title\s*block/.test(sample))
        return { type: 'drawing', confidence: 'medium', reason: 'Content contains drawing keywords' };
      if (/\bspecification\b|\bclause\b|\bbritish\s*standard\b|\bbs\s*en\b/.test(sample))
        return { type: 'specification', confidence: 'medium', reason: 'Content contains specification keywords' };
    }

    return { type: 'unknown', confidence: 'low', reason: 'Could not classify document from filename or content' };
  }

  function isScheduleOrBQ(docType) {
    return docType === 'schedule' || docType === 'bq' || docType === 'specification';
  }

  function isRelevantForCrossRef(docType) {
    return docType === 'schedule' || docType === 'bq';
  }

  // -----------------------------------------------------------------------
  // Spatial helpers — group PDF text items into rows and columns
  // -----------------------------------------------------------------------

  // Spatial thresholds (all in PDF user-space points, ~1pt ≈ 0.35mm)
  // Construction PDFs from CAD software can have text items with Y-coordinate drift of
  // 5–15 points within the same visual row.  Use 8 pt so that multi-line type cells
  // (e.g. "Double-glazed\nAluminium PPC") still group with the reference on the same row,
  // while keeping adjacent data rows (typically 12–18 pt apart) separate.
  var ROW_Y_TOLERANCE   = 8;   // max Y-delta to group two items in the same row
  var SPATIAL_ROW_Y     = 18;  // max Y-delta to consider an item "on the same row" as a reference
  var SPATIAL_ROW_X     = 400; // max X-distance from reference to include in spatial context
  // Character-context window sizes for the regex-only fallback (no position data)
  var CTX_LOOKBACK      = 50;  // chars before the reference (for location, frame-type, notes)
  var CTX_FORWARD_FULL  = 300; // chars after the reference (full context)
  var CTX_FORWARD_DIMS  = 250; // chars after the reference (dimension/qty only — forward avoids prior item's data)
  // Drawing-number lookback: "3847. C37" is 9 chars; use 12 to be safe for extra whitespace
  var DRAWING_NUM_LOOKBACK = 12;
  // Drawing-number filter regex — rejects refs that appear to be part of a drawing sheet
  // reference such as "3847.C37" or "3847.T05".  The letter+digits part is optional so
  // that "3847." (where the ref letter begins the captured group) is also matched correctly.
  var DRAWING_NUM_FILTER = /\d{4,}\.\s*([A-Z]\d*)?\s*$/;
  // Space-split reference normalisation: "EW 19" → "EW19", "ID 04" → "ID04".
  // Used in several places to pre-process text before reference scanning.
  var SPACE_SPLIT_REF_NORM = /\b([A-Z]{1,2}[WDSC])\s+(\d{2,4})\b/gi;
  // Minimum number of characters in a page text string for it to be considered
  // textual (as opposed to scanned / image-only).
  var MIN_TEXT_LENGTH = 50;

  // Normalise space-split references arising from PDF text fragmentation.
  // e.g. "EW 19" → "EW19", "ID 04" → "ID04", "E W 01" → "EW01".
  // Creates a fresh regex instance each call to avoid lastIndex state issues.
  function normaliseSpaceSplitRefs(text) {
    // Handle extreme fragmentation: "E W 01" → "EW01" (single letters before W/D/S/C)
    var result = text.replace(/\b([A-Z])\s+([WDSC])\s+(\d{2,4})\b/gi, '$1$2$3');
    // Standard case: "EW 19" → "EW19"
    result = result.replace(/\b([A-Z]{1,2}[WDSC])[\s\u200B\u00A0]+(\d{2,4})\b/gi, '$1$2');
    return result;
  }

  // Drawing-sheet suffix set — populated dynamically from classified drawing documents.
  // Contains refs like "C37", "T05" etc. extracted from filenames like "3847.C37 ...".
  // Strategies check against this to reject drawing sheet numbers appearing as standalone refs.
  var _drawingSheetRefs = {};

  // Validate that a reference is a genuine glazing reference and not a false positive.
  // Returns true if the ref is valid, false if it should be rejected.
  function isValidGlazingReference(ref) {
    if (!ref) return false;
    var upper = ref.toUpperCase();

    // Reject BS/EN standards codes: BS6262, BS EN 1279, EN12600
    if (/^BS/i.test(upper) || /^EN\d/i.test(upper)) return false;

    // Reject refs where a single-letter prefix has >3 digits (e.g. S6262 is not a screen)
    var singleLetterMatch = upper.match(/^([A-Z])([WDSC])(\d+)$/);
    if (singleLetterMatch && singleLetterMatch[3].length > 3) return false;
    // Also reject bare single-type-letter + >3 digits (e.g. "C37" is ambiguous but "C3700" is not glazing)
    var bareMatch = upper.match(/^([WDSC])(\d+)$/);
    if (bareMatch && bareMatch[2].length > 3) return false;

    // Reject refs that match known drawing sheet number suffixes
    if (_drawingSheetRefs[upper]) return false;

    return true;
  }

  // Group text items into rows by Y coordinate.
  // In PDF space the origin (0,0) is bottom-left, so higher Y = higher on page.
  function buildRows(textItems, yTolerance) {
    if (!textItems || textItems.length === 0) return [];
    yTolerance = yTolerance || ROW_Y_TOLERANCE;

    var rows = [];
    // Keep only items with actual text
    var items = textItems.filter(function (it) {
      return it.str && it.str.trim().length > 0;
    });

    // Process items sorted descending by Y (top-of-page first)
    var sorted = items.slice().sort(function (a, b) { return b.y - a.y; });

    sorted.forEach(function (item) {
      var found = false;
      for (var i = 0; i < rows.length; i++) {
        if (Math.abs(rows[i].y - item.y) <= yTolerance) {
          rows[i].items.push(item);
          // Running average Y so tolerance stays accurate
          rows[i].y = rows[i].items.reduce(function (s, it) { return s + it.y; }, 0) / rows[i].items.length;
          found = true;
          break;
        }
      }
      if (!found) {
        rows.push({ y: item.y, items: [item] });
      }
    });

    // Final sort: top-to-bottom (descending Y in PDF space)
    rows.sort(function (a, b) { return b.y - a.y; });

    // Sort items within each row left-to-right (ascending X)
    rows.forEach(function (row) {
      row.items.sort(function (a, b) { return a.x - b.x; });
      row.text = row.items.map(function (it) { return it.str; }).join(' ');
    });

    return rows;
  }

  // Column-header keyword sets mapped to field names
  var HEADER_COLUMN_KEYWORDS = {
    ref:         ['ref', 'reference', 'mark', 'item no', 'item', 'schedule ref', 'window ref', 'door ref', 'window no', 'glazing ref', 'nr.', 'no.'],
    width:       ['width', 'w (mm)', 'w(mm)', 'wd', 'w'],
    height:      ['height', 'h (mm)', 'h(mm)', 'ht', 'h'],
    // 'opening (w' catches "Opening (w x h)" column headers common in UK window schedules
    size:        ['size', 'overall size', 'dimensions', 'dim', 'opening size', 'opening (w', 'w x h', 'w×h'],
    qty:         ['qty', 'quantity', 'no', 'nr', 'number', 'nos'],
    // 'type' added here to catch simple "Type" column headers that specify frame material/construction
    frame:       ['frame', 'frame type', 'material', 'profile', 'system', 'construction', 'type'],
    glazing:     ['glazing', 'glass', 'infill', 'glazing spec', 'glazing type'],
    // 'opening' alone is intentionally not here — it is too ambiguous and is caught by 'size' via 'opening (w'
    opening:     ['opening type', 'function', 'operation', 'open type', 'open'],
    location:    ['location', 'position', 'floor', 'room', 'level', 'area', 'to room'],
    description: ['description', 'notes', 'specification', 'note', 'remarks', 'comments'],
    // Phase 2 columns (Shaftesbury-style window/door schedules)
    sillHeight:  ['sill height', 'sill ht', 'cill height', 'cill ht'],
    headHeight:  ['head height', 'head ht', 'lintel height', 'head'],
    uValue:      ['u value', 'u-value', 'thermal', 'w/m2k', 'w/m\u00b2k'],
    finish:      ['finish', 'frame finish', 'door finish', 'window finish', 'window frame finish'],
    doorSwing:   ['swing', 'door swing', 'hand', 'handing'],
    fireRating:  ['fire rating', 'fire', 'fd rating', 'fire resistance', 'fire rate'],
    doorFrame:   ['door frame', 'frame spec'],
    doorGlazing: ['door glazing'],
    ironmongery: ['ironmongery', 'hardware', 'fittings', 'door ironmongery'],
    doorType:    ['door type', 'ymd door type']
  };

  // Return the index of the first row that looks like a table header (≥2 field matches)
  function findHeaderRow(rows) {
    for (var i = 0; i < Math.min(rows.length, 30); i++) {
      var row = rows[i];
      if (!row.items || row.items.length < 2) continue;

      var cellTexts = row.items.map(function (it) { return it.str.toLowerCase().trim(); });
      var fieldMatchCount = 0;

      var fields = Object.keys(HEADER_COLUMN_KEYWORDS);
      for (var fi = 0; fi < fields.length; fi++) {
        var keywords = HEADER_COLUMN_KEYWORDS[fields[fi]];
        var matched = keywords.some(function (kw) {
          return cellTexts.some(function (cell) {
            return cell === kw || cell.indexOf(kw) !== -1;
          });
        });
        if (matched) fieldMatchCount++;
      }

      if (fieldMatchCount >= 2) return i;
    }
    return -1;
  }

  // Build a map of { fieldName → { x, label } } from a header row
  function mapHeaderColumns(headerRow) {
    var columns = {};
    headerRow.items.forEach(function (item) {
      var text = item.str.toLowerCase().trim();
      var fields = Object.keys(HEADER_COLUMN_KEYWORDS);

      // Two-pass matching: first pass requires exact match or prefix match (text === kw
      // or text starts with kw); second pass allows substring (kw appears anywhere in text).
      // This prevents short keywords like 'type' in the frame field from stealing headers
      // that better match a more-specific field like doorType ('door type').
      var bestField = null;
      var bestKwLen = 0;

      for (var fi = 0; fi < fields.length; fi++) {
        var field = fields[fi];
        if (columns[field]) continue; // already mapped
        var keywords = HEADER_COLUMN_KEYWORDS[field];
        for (var ki = 0; ki < keywords.length; ki++) {
          var kw = keywords[ki];
          if ((text === kw || text.indexOf(kw) !== -1) && kw.length > bestKwLen) {
            bestKwLen = kw.length;
            bestField = field;
          }
        }
      }

      if (bestField) {
        columns[bestField] = { x: item.x, label: item.str };
      }
    });
    return columns;
  }

  // Find the single item in a row closest to a column X position (within tolerance)
  function getCellText(rowItems, columnX, colTolerance) {
    colTolerance = colTolerance || 120;
    var closest = null;
    var minDist = Infinity;
    rowItems.forEach(function (item) {
      var dist = Math.abs(item.x - columnX);
      if (dist < minDist && dist <= colTolerance) {
        minDist = dist;
        closest = item;
      }
    });
    return closest ? closest.str.trim() : '';
  }

  // -----------------------------------------------------------------------
  // Strategy 1 — Structured table extraction (highest confidence)
  // -----------------------------------------------------------------------

  // Reference pattern — matches single-letter refs (W01, D01, S01, C01) and
  // multi-letter prefix refs common in UK construction (EW01 = External Window,
  // ED01 = External Door, ID01 = Internal Door, FW01 = Fixed Window, etc.).
  // The last alphabetic character before the digits must be W, D, S, or C.
  var REF_PATTERN = /^([A-Z]{0,2}[WDSC]\d{2,4})$/i;

  // Normalise a raw text string to a glazing reference if it matches, or return null.
  function normaliseRef(str) {
    if (!str) return null;
    // Strip leading/trailing whitespace and common trailing punctuation
    var s = str.trim().replace(/[\s.,;:]+$/, '').replace(/^[\s.,;:]+/, '');
    if (!REF_PATTERN.test(s)) return null;
    var upper = s.toUpperCase();
    if (!isValidGlazingReference(upper)) return null;
    return upper;
  }

  function tryTableExtraction(rows, sourceName, sourcePage) {
    var items = [];
    var headerIdx = findHeaderRow(rows);
    if (headerIdx === -1) return items;

    var headerRow = rows[headerIdx];
    var columns = mapHeaderColumns(headerRow);

    // Must have at least a reference column to proceed
    if (!columns.ref) return items;

    for (var i = headerIdx + 1; i < rows.length; i++) {
      var row = rows[i];
      if (!row.items || row.items.length === 0) continue;

      var refText = normaliseRef(getCellText(row.items, columns.ref.x));
      if (!refText) continue;

      var item = createItem({
        reference: refText,
        type: inferType(refText),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });

      // Dimensions: try dedicated size column first, then separate W/H columns
      if (columns.size) {
        var sizeText = getCellText(row.items, columns.size.x);
        var dims = extractDimensionsFromText(sizeText);
        if (dims) { item.width = dims.width; item.height = dims.height; }
      }
      if (!item.width && columns.width) {
        var w = parseInt(getCellText(row.items, columns.width.x), 10);
        if (w >= 100 && w <= 9000) item.width = w;
      }
      if (!item.height && columns.height) {
        var h = parseInt(getCellText(row.items, columns.height.x), 10);
        if (h >= 100 && h <= 9000) item.height = h;
      }

      // Quantity
      if (columns.qty) {
        var qty = parseInt(getCellText(row.items, columns.qty.x), 10);
        if (qty > 0 && qty < 500) item.quantity = qty;
      }

      // Frame type
      if (columns.frame) {
        var frameText = getCellText(row.items, columns.frame.x);
        if (frameText) item.frameType = extractFrameType(frameText);
      }

      // Opening type
      if (columns.opening) {
        var openText = getCellText(row.items, columns.opening.x);
        if (openText) item.openingType = extractOpeningType(openText);
      }

      // Location
      if (columns.location) {
        var locText = getCellText(row.items, columns.location.x);
        if (locText) item.location = locText;
      }

      // Glazing spec
      var glazingSource = columns.glazing
        ? getCellText(row.items, columns.glazing.x)
        : row.text;
      item.glazingSpec = buildGlazingSpec(glazingSource);

      // Supplement with full-row text for notes and missing attributes
      var fullRowText = row.text || '';

      // Dimension fallback: if no size/width/height column found (or yielded nothing),
      // try extracting dimensions from the full row text (e.g. "1010 x 1050").
      if (!item.width || !item.height) {
        var rowDims = extractDimensionsFromText(fullRowText);
        if (rowDims) {
          if (!item.width)  item.width  = rowDims.width;
          if (!item.height) item.height = rowDims.height;
        }
      }

      item.notes = extractNotes(fullRowText);
      if (!item.frameType || item.frameType === 'Unknown') item.frameType = extractFrameType(fullRowText);
      if (!item.openingType || item.openingType === 'Fixed') item.openingType = extractOpeningType(fullRowText);
      if (!item.location) item.location = extractLocation(fullRowText);
      item.colour = extractColour(fullRowText);
      item.ventilation = extractVentilation(fullRowText);
      var cillVal1 = extractCillHeight(fullRowText);
      if (cillVal1) item.cillType = cillVal1 + 'mm cill height';
      item.escapeWindow = extractEscapeWindow(fullRowText);

      // --- Phase 2 columns: extract from dedicated column first, fall back to row text ---

      // Sill Height
      if (columns.sillHeight) {
        var shText = getCellText(row.items, columns.sillHeight.x);
        if (shText) item.sillHeight = shText.replace(/\s*mm\s*/gi, '').trim();
      }
      if (!item.sillHeight) item.sillHeight = extractSillHeight(fullRowText);

      // Head Height
      if (columns.headHeight) {
        var hhText = getCellText(row.items, columns.headHeight.x);
        if (hhText) item.headHeight = hhText.replace(/\s*mm\s*/gi, '').trim();
      }
      if (!item.headHeight) item.headHeight = extractHeadHeight(fullRowText);

      // U-Value
      if (columns.uValue) {
        var uvText = getCellText(row.items, columns.uValue.x);
        if (uvText) item.uValue = uvText.trim();
      }
      if (!item.uValue) item.uValue = extractUValue(fullRowText);

      // Finish
      if (columns.finish) {
        var finText = getCellText(row.items, columns.finish.x);
        if (finText) item.finish = finText.trim();
      }
      if (!item.finish) item.finish = extractFinish(fullRowText);

      // Door Swing
      if (columns.doorSwing) {
        var dsText = getCellText(row.items, columns.doorSwing.x);
        if (dsText) item.doorSwing = dsText.trim();
      }
      if (!item.doorSwing) item.doorSwing = extractDoorSwing(fullRowText);

      // Fire Rating
      if (columns.fireRating) {
        var frText = getCellText(row.items, columns.fireRating.x);
        if (frText) item.fireRating = frText.trim();
      }
      if (!item.fireRating) item.fireRating = extractFireRating(fullRowText);

      // Door Frame
      if (columns.doorFrame) {
        var dfText = getCellText(row.items, columns.doorFrame.x);
        if (dfText) item.doorFrame = dfText.trim();
      }

      // Door Glazing
      if (columns.doorGlazing) {
        var dgText = getCellText(row.items, columns.doorGlazing.x);
        if (dgText) item.doorGlazing = dgText.trim();
      }

      // Ironmongery
      if (columns.ironmongery) {
        var imText = getCellText(row.items, columns.ironmongery.x);
        if (imText) item.ironmongery = imText.trim();
      }
      if (!item.ironmongery) item.ironmongery = extractIronmongery(fullRowText);

      // Door Type
      if (columns.doorType) {
        var dtText = getCellText(row.items, columns.doorType.x);
        if (dtText) item.doorType = dtText.trim();
      }
      if (!item.doorType) item.doorType = extractDoorType(fullRowText);

      // Position for PDF viewer overlay (use the ref item's position)
      var refItem = row.items.find(function (it) { return it.str.trim().toUpperCase() === refText; });
      if (refItem) {
        item.textPosition = { x: refItem.x, y: refItem.y, width: refItem.width || 30, height: refItem.height || 12 };
      }

      item.confidence = scoreConfidence(item, 'table');
      items.push(item);
    }

    return items;
  }

  // -----------------------------------------------------------------------
  // Strategy 2 — Row-based pattern matching (medium confidence)
  // -----------------------------------------------------------------------

  function tryRowBasedExtraction(rows, sourceName, sourcePage, docType) {
    var items = [];
    var refRows = [];

    // Find rows whose first 3 (leftmost) non-empty items contain a glazing reference.
    // Checking the first 3 handles tables where a row-number or checkbox column precedes
    // the reference (e.g. "1  EW01  Room 1  …").
    rows.forEach(function (row) {
      if (!row.items || row.items.length < 2) return;
      var ref = null;
      var refItemIdx = 0;
      for (var ci = 0; ci < Math.min(3, row.items.length); ci++) {
        var candidate = normaliseRef(row.items[ci].str);
        if (candidate) { ref = candidate; refItemIdx = ci; break; }
      }
      // Handle split text items: try concatenating adjacent pairs (e.g. "EW" + "19" → "EW19").
      // This occurs when CAD-exported PDFs split reference codes across text items.
      if (!ref) {
        for (var pi = 0; pi < Math.min(4, row.items.length - 1); pi++) {
          var combined = row.items[pi].str.trim() + row.items[pi + 1].str.trim();
          var cand = normaliseRef(combined);
          if (cand) { ref = cand; refItemIdx = pi; break; }
        }
      }
      if (ref) {
        refRows.push({ row: row, ref: ref, refItemIdx: refItemIdx });
      }
    });

    // Need at least 2 consistent reference rows to be confident this is a real table.
    // For schedule/BQ documents, lower the threshold to 1 — a single identifiable reference
    // row is sufficient when the document type is already known.
    if (refRows.length < (isScheduleOrBQ(docType) ? 1 : 2)) return items;

    refRows.forEach(function (refRow) {
      var row = refRow.row;
      var ref = refRow.ref;
      var refItemIdx = refRow.refItemIdx;

      var item = createItem({
        reference: ref,
        type: inferType(ref),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });

      // Find dimensions: collect numbers ≥100mm from cells after the ref cell
      var numbers = row.items.slice(refItemIdx + 1).map(function (it) {
        return { str: it.str, x: it.x, val: parseInt(it.str.trim(), 10) };
      }).filter(function (n) { return !isNaN(n.val); });

      // Dimensions are the largest plausible numbers (100–9000mm)
      var dimNums = numbers.filter(function (n) { return n.val >= 100 && n.val <= 9000; });
      if (dimNums.length >= 2) {
        // Assume left number is width, next is height
        item.width = dimNums[0].val;
        item.height = dimNums[1].val;
      }

      // If no separate W/H, try inline "WxH" pattern from full row text
      if (!item.width || !item.height) {
        var dims = extractDimensionsFromText(row.text);
        if (dims) { item.width = dims.width; item.height = dims.height; }
      }

      // Quantity: small numbers (1–99) that are NOT the dimensions
      var smallNums = numbers.filter(function (n) {
        return n.val >= 1 && n.val <= 99 && n.val !== item.width && n.val !== item.height;
      });
      if (smallNums.length > 0) {
        item.quantity = smallNums[0].val;
      }

      var fullText = row.text;
      item.frameType  = extractFrameType(fullText);
      item.glazingSpec = buildGlazingSpec(fullText);
      item.openingType = extractOpeningType(fullText);
      item.location   = extractLocation(fullText);
      item.notes      = extractNotes(fullText);
      item.colour     = extractColour(fullText);
      item.ventilation = extractVentilation(fullText);
      var cillVal2    = extractCillHeight(fullText);
      if (cillVal2) item.cillType = cillVal2 + 'mm cill height';
      item.escapeWindow = extractEscapeWindow(fullText);
      // Phase 2 fields
      item.sillHeight   = extractSillHeight(fullText);
      item.headHeight   = extractHeadHeight(fullText);
      item.uValue       = extractUValue(fullText);
      item.finish       = extractFinish(fullText);
      item.doorSwing    = extractDoorSwing(fullText);
      item.fireRating   = extractFireRating(fullText);
      item.ironmongery  = extractIronmongery(fullText);
      item.doorType     = extractDoorType(fullText);

      var refItem = row.items[refItemIdx];
      item.textPosition = { x: refItem.x, y: refItem.y, width: refItem.width || 30, height: refItem.height || 12 };

      item.confidence = scoreConfidence(item, 'row');
      items.push(item);
    });

    return items;
  }

  // -----------------------------------------------------------------------
  // Strategy 0 — Reference-first extraction (primary strategy for schedule docs)
  // -----------------------------------------------------------------------

  // Reference pattern for the reference-first strategy — more specific than the
  // generic fallback pattern.  Covers:
  //   E?[WDSC]\d{2,3} — EW01–EW38, ED01–ED03, W01, D01, S01, C01
  //   I[WD]\d{2,3}    — IW01, ID01 (internal window / door)
  //   N[WD]\d{2,3}    — NW01–NW11, ND01–ND14 (Shaftesbury-style)
  var REF_FIRST_PATTERN = /\b(E?[WDSC]\d{2,3}|[IN][WD]\d{2,3})\b/gi;

  // Spatial thresholds specific to reference-first clustering
  var REF_FIRST_Y_TOL   = 15;   // pt — items within this of the ref Y are "same row"
  var REF_FIRST_Y_BELOW = 40;   // pt — items this far below the ref row (multi-line cells)
  var REF_FIRST_X_RANGE = 1500; // pt — max horizontal reach from the ref item
  // Wide range needed because CAD-exported schedules can be A3 (842pt) or A1 (2384pt)
  // landscape, with dimension columns far to the right of the reference column.

  // Find the text item that best represents a given reference string.
  // Handles exact matches, containing matches, and split refs ("EW"+"19").
  function findRefTextItem(textItems, ref) {
    var alphaPrefix = ref.match(/^([A-Z]+)/);
    var prefixMatch = null;

    for (var i = 0; i < textItems.length; i++) {
      var ti = textItems[i];
      if (!ti.str) continue;
      var upper = ti.str.trim().toUpperCase();
      if (upper === ref) return ti;                                    // exact match
      if (upper.indexOf(ref) !== -1 && !prefixMatch) prefixMatch = ti; // contains ref
      // Split ref: alphabetic prefix in its own item (e.g. "EW" for "EW19")
      if (alphaPrefix && alphaPrefix[1].length >= 2 && upper === alphaPrefix[1] && !prefixMatch) {
        prefixMatch = ti;
      }
    }
    return prefixMatch;
  }

  function tryReferenceFirstExtraction(textItems, text, sourceName, sourcePage) {
    var items = [];
    if (!text || text.trim().length === 0) return items;

    // Normalise space-split refs arising from PDF text fragmentation
    // e.g. "EW 19" → "EW19", "ID 04" → "ID04"
    var normText = normaliseSpaceSplitRefs(text);

    // Insert space between trailing digits and reference-like prefixes.
    // Smart text joining can produce "2100EW30" when the gap between text items
    // is <2pt.  \b doesn't fire between two \w chars (digit→letter), so the
    // reference regex misses "EW30".  This targeted fix restores the boundary.
    normText = normText.replace(/(\d)([EI]?[WDSC]\d{2,3}\b)/gi, '$1 $2');

    var hasPositions = textItems.length > 0 && textItems[0] && textItems[0].x !== undefined;

    // Step 1 — Find all unique valid references in this page
    var pattern = new RegExp(REF_FIRST_PATTERN.source, 'gi');
    var foundRefs = {};
    var match;

    while ((match = pattern.exec(normText)) !== null) {
      var ref = match[1].toUpperCase();
      var idx = match.index;

      // Reject drawing-sheet number context (e.g. "3847.C37")
      // But NOT standards codes like "BS 6206." or "EN 12600."
      var preceding = normText.substring(Math.max(0, idx - DRAWING_NUM_LOOKBACK), idx);
      if (DRAWING_NUM_FILTER.test(preceding) && !/\b(?:BS|EN)\s*\d/i.test(preceding)) continue;

      // Reject UK postcode patterns: "S73 9LG", "W12 7RJ" etc.
      // A ref followed by space + digit + 2 letters is almost certainly a postcode
      var following = normText.substring(idx + match[0].length, idx + match[0].length + 30);
      if (/^\s+\d[A-Z]{2}\b/i.test(following)) continue;

      // Reject drawing revision markers: "C01 Construction Issue", "C02 Revision"
      if (/^\s+(?:construction|revision|issue|draft|preliminary|tender|planning|for\s+(?:comment|approval|info))/i.test(following)) continue;

      // Reject CAD title block status/revision codes: "1 : 20 C01 Shaftesbury"
      // Single-letter refs (C/D/W/S + digits) preceded by a drawing scale pattern
      if (/^[CDWS]\d{2,3}$/i.test(ref)) {
        var widerPreceding = normText.substring(Math.max(0, idx - 30), idx);
        if (/\d\s*:\s*\d+\s*$/.test(widerPreceding)) continue;
      }

      // Reject BS/EN codes, drawing sheet numbers, and other false positives
      if (!isValidGlazingReference(ref)) continue;

      if (!foundRefs[ref]) {
        foundRefs[ref] = { ref: ref, firstIndex: idx, allIndices: [idx] };
      } else {
        foundRefs[ref].allIndices.push(idx);
      }
    }

    console.log('[RefFirst] Page ' + sourcePage + ' of "' + sourceName + '": found ' + Object.keys(foundRefs).length + ' unique refs: ' + Object.keys(foundRefs).join(', '));

    // Diagnostic: check if ED/D refs appear in the raw text but were missed
    var edCheck = normText.match(/\b[ED][D]?\d{2,3}\b/gi);
    if (edCheck) {
      var edFiltered = edCheck.filter(function (r) { return !foundRefs[r.toUpperCase()]; });
      if (edFiltered.length > 0) {
        console.log('[RefFirst] Potential door refs in text but NOT captured: ' + edFiltered.join(', '));
      }
    }
    // Also log last 300 chars of normText to see if doors section exists
    if (normText.length > 500) {
      console.log('[RefFirst] normText tail (last 300 chars): "' + normText.substring(normText.length - 300) + '"');
    }

    // Step 2 & 3 — For each reference, gather nearby text cluster and extract attributes
    Object.keys(foundRefs).sort().forEach(function (ref) {
      var refData  = foundRefs[ref];
      var clusterText = '';
      var refTextItem = null;

      if (hasPositions) {
        refTextItem = findRefTextItem(textItems, ref);

        if (refTextItem) {
          // Same-row cluster: items within Y_TOL of the ref and within X_RANGE
          var sameRow = textItems.filter(function (it) {
            return it.str && it.str.trim().length > 0 &&
                   Math.abs(it.y - refTextItem.y) <= REF_FIRST_Y_TOL &&
                   it.x >= refTextItem.x - REF_FIRST_X_RANGE &&
                   it.x <= refTextItem.x + REF_FIRST_X_RANGE;
          });
          sameRow.sort(function (a, b) { return a.x - b.x; });

          // Below-row cluster: next 2–3 visual rows (lower y in PDF space = lower on page)
          var belowRow = textItems.filter(function (it) {
            return it.str && it.str.trim().length > 0 &&
                   it.y < (refTextItem.y - REF_FIRST_Y_TOL) &&
                   (refTextItem.y - it.y) <= REF_FIRST_Y_BELOW &&
                   it.x >= refTextItem.x - REF_FIRST_X_RANGE &&
                   it.x <= refTextItem.x + REF_FIRST_X_RANGE;
          });
          belowRow.sort(function (a, b) { return b.y - a.y || a.x - b.x; });

          clusterText = sameRow.concat(belowRow)
            .map(function (it) { return it.str; })
            .join(' ');
        }
      }

      // Character-context fallback when no position data (or ref item not found)
      if (!clusterText) {
        clusterText = normText.substring(
          refData.firstIndex,
          Math.min(normText.length, refData.firstIndex + CTX_FORWARD_FULL)
        );
      }

      // Build a secondary character-context window for dimension/attribute fallback.
      // Even when spatial clustering produces text, it may miss columns that are far
      // away — the character-context window captures everything between this ref and
      // the next ref in TEXT ORDER (not sorted order), spanning the full table row.
      //
      // When a ref appears multiple times in the text (e.g. once in an elevation
      // annotation and again in a table row), evaluate ALL occurrences and pick the
      // one with the longest span — the data-rich table row, not the short annotation.
      var charContext = '';
      var allRefPositions = [];
      Object.keys(foundRefs).forEach(function (r) {
        foundRefs[r].allIndices.forEach(function (pos) {
          allRefPositions.push({ ref: r, pos: pos });
        });
      });
      allRefPositions.sort(function (a, b) { return a.pos - b.pos; });

      var bestContext = '';
      var bestStart = refData.firstIndex;
      refData.allIndices.forEach(function (occurrencePos) {
        // Find the next DIFFERENT ref's position after this occurrence
        var nextPos = -1;
        for (var pi = 0; pi < allRefPositions.length; pi++) {
          if (allRefPositions[pi].pos > occurrencePos && allRefPositions[pi].ref !== ref) {
            nextPos = allRefPositions[pi].pos;
            break;
          }
        }
        if (nextPos < 0) nextPos = Math.min(normText.length, occurrencePos + CTX_FORWARD_FULL);
        var candidate = normText.substring(occurrencePos, Math.min(normText.length, nextPos));
        if (candidate.length > bestContext.length) {
          bestContext = candidate;
          bestStart = occurrencePos;
        }
      });
      charContext = bestContext;

      var item = createItem({
        reference: ref,
        type: inferType(ref),
        sourceDocument: sourceName,
        sourcePage: sourcePage,
        extractionMethod: 'reference-first'
      });

      // Dimensions — try spatial cluster first, then character-context fallback
      var dims = extractDimensionsFromText(clusterText);
      if (!dims) {
        // Adjacent 3–4 digit numbers may be W and H in separate table columns
        var adjNums = clusterText.match(/\b(\d{3,4})\s+(\d{3,4})\b/);
        if (adjNums) {
          var aw = parseInt(adjNums[1], 10), ah = parseInt(adjNums[2], 10);
          if (aw >= 100 && aw <= 9000 && ah >= 100 && ah <= 9000) {
            dims = { width: aw, height: ah };
          }
        }
      }
      // Character-context fallback for dimensions
      if (!dims && charContext) {
        dims = extractDimensionsFromText(charContext);
        if (!dims) {
          var adjNums2 = charContext.match(/\b(\d{3,4})\s+(\d{3,4})\b/);
          if (adjNums2) {
            var aw2 = parseInt(adjNums2[1], 10), ah2 = parseInt(adjNums2[2], 10);
            if (aw2 >= 100 && aw2 <= 9000 && ah2 >= 100 && ah2 <= 9000) {
              dims = { width: aw2, height: ah2 };
            }
          }
        }
      }
      if (dims) { item.width = dims.width; item.height = dims.height; }

      // Debug: log first 3 items' context and dims for troubleshooting
      if (items.length < 3) {
        console.log('[RefFirst] ' + ref + ' clusterText(' + clusterText.length + '): "' + clusterText.substring(0, 200) + '"');
        console.log('[RefFirst] ' + ref + ' charContext(' + charContext.length + '): "' + charContext.substring(0, 200) + '"');
        console.log('[RefFirst] ' + ref + ' dims: ' + (dims ? dims.width + 'x' + dims.height : 'NONE'));
      }

      // Always prefer charContext for attribute extraction — it represents the
      // text row for this ref in document order.  clusterText may contain data
      // from other columns/rows due to spatial proximity (e.g. in column-based
      // CAD schedules the same-row cluster is just all other ref names).
      var attrContext = charContext || clusterText;
      item.quantity    = extractQuantity(attrContext) || 1;
      item.frameType   = extractFrameType(attrContext);
      item.glazingSpec = buildGlazingSpec(attrContext);
      item.openingType = extractOpeningType(attrContext);
      item.location    = extractLocation(attrContext);
      item.notes       = extractNotes(attrContext);
      item.colour      = extractColour(attrContext);
      item.ventilation = extractVentilation(attrContext);
      var cillVal      = extractCillHeight(attrContext);
      if (cillVal) item.cillType = cillVal + 'mm cill height';
      item.escapeWindow = extractEscapeWindow(attrContext);
      // Phase 2 fields
      item.sillHeight   = extractSillHeight(attrContext);
      item.headHeight   = extractHeadHeight(attrContext);
      item.uValue       = extractUValue(attrContext);
      item.finish       = extractFinish(attrContext);
      item.doorSwing    = extractDoorSwing(attrContext);
      item.fireRating   = extractFireRating(attrContext);
      item.ironmongery  = extractIronmongery(attrContext);
      item.doorType     = extractDoorType(attrContext);

      if (refTextItem) {
        item.textPosition = {
          x: refTextItem.x, y: refTextItem.y,
          width: refTextItem.width || 30, height: refTextItem.height || 12
        };
      }

      item.confidence = scoreConfidence(item, 'reference-first');
      items.push(item);
    });

    return items;
  }

  // -----------------------------------------------------------------------
  // Strategy 3 — Enhanced regex with spatial context (fallback)
  // -----------------------------------------------------------------------

  function tryEnhancedRegex(textItems, text, sourceName, sourcePage) {
    var items = [];
    if (!text || text.trim().length === 0) return items;

    // Normalise space-split references that arise from PDF text fragmentation,
    // e.g. "EW 19" → "EW19", "ID 04" → "ID04".  Use a separate variable so the
    // original text is still available for spatial item lookups via textItems.
    var normText = normaliseSpaceSplitRefs(text);

    // Match single-letter refs (W01) and multi-letter prefix refs (EW01, ID01, etc.)
    // The last alpha char before the digits must be W, D, S, or C.
    var refPattern = /\b([A-Z]{0,2}[WDSC]\d{2,4})\b/gi;
    var match;

    while ((match = refPattern.exec(normText)) !== null) {
      var ref = match[1].toUpperCase();
      var matchIndex = match.index;

      // Reject references that are actually drawing-sheet numbers like "3847.C37"
      // or "3847. EW01".  Require a mandatory letter after the period so that
      // plain dimension values such as "1010." don't trigger a false rejection.
      var preceding = normText.substring(Math.max(0, matchIndex - DRAWING_NUM_LOOKBACK), matchIndex);
      if (DRAWING_NUM_FILTER.test(preceding) && !/\b(?:BS|EN)\s*\d/i.test(preceding)) continue;

      // Reject UK postcodes and revision markers
      var following3 = normText.substring(matchIndex + match[0].length, matchIndex + match[0].length + 30);
      if (/^\s+\d[A-Z]{2}\b/i.test(following3)) continue;
      if (/^\s+(?:construction|revision|issue|draft|preliminary|tender|planning|for\s+(?:comment|approval|info))/i.test(following3)) continue;

      // Reject CAD title block status/revision codes preceded by drawing scale
      if (/^[CDWS]\d{2,3}$/i.test(ref)) {
        var widerPreceding3 = normText.substring(Math.max(0, matchIndex - 30), matchIndex);
        if (/\d\s*:\s*\d+\s*$/.test(widerPreceding3)) continue;
      }

      // Reject BS/EN codes, drawing sheet numbers, and other false positives
      if (!isValidGlazingReference(ref)) continue;

      // Find the text item that contains this reference (or its alphabetic prefix for split refs)
      var refItem = null;
      if (textItems && textItems.length > 0) {
        var alphaPrefix = ref.match(/^([A-Z]+)/);
        for (var k = 0; k < textItems.length; k++) {
          var ti = textItems[k];
          if (ti.str) {
            var tiUpper = ti.str.trim().toUpperCase();
            if (tiUpper === ref || tiUpper.indexOf(ref) !== -1) {
              refItem = ti;
              break;
            }
            // Match the alphabetic prefix of a split ref (e.g. "EW" for ref "EW19")
            if (alphaPrefix && alphaPrefix[1].length >= 2 && tiUpper === alphaPrefix[1] && !refItem) {
              refItem = ti;
            }
          }
        }
      }

      // Build spatial or character context
      var context;
      var dimContext; // forward-only context used for dimension extraction to avoid overlap with prior items
      if (refItem && textItems && textItems.length > 0) {
        // Collect items on the same row (within SPATIAL_ROW_Y pt vertically) and
        // within SPATIAL_ROW_X pt horizontally — sorted left-to-right for a natural read order.
        var nearby = textItems.filter(function (it) {
          return Math.abs(it.y - refItem.y) <= SPATIAL_ROW_Y &&
                 Math.abs(it.x - refItem.x) <= SPATIAL_ROW_X &&
                 it.str && it.str.trim().length > 0;
        });
        nearby.sort(function (a, b) { return a.x - b.x; });
        context = nearby.map(function (it) { return it.str; }).join(' ');
        dimContext = context;
      } else {
        // CTX_LOOKBACK chars before for location/frame/notes, CTX_FORWARD_FULL after for all attributes
        context = normText.substring(Math.max(0, matchIndex - CTX_LOOKBACK), Math.min(normText.length, matchIndex + CTX_FORWARD_FULL));
        // Forward-only window for dims/qty so a prior item's dimensions don't bleed into this item's context
        dimContext = normText.substring(matchIndex, Math.min(normText.length, matchIndex + CTX_FORWARD_DIMS));
      }

      var item = createItem({
        reference: ref,
        type: inferType(ref),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });

      var dims = extractDimensionsFromText(dimContext);
      if (!dims) {
        // Fallback: two consecutive 3-4 digit numbers may be W and H in separate table columns
        // (e.g. "900 1200" in a schedule where width and height are adjacent cells).
        var adjNums = dimContext.match(/\b(\d{3,4})\s+(\d{3,4})\b/);
        if (adjNums) {
          var aw = parseInt(adjNums[1], 10), ah = parseInt(adjNums[2], 10);
          if (aw >= 100 && aw <= 9000 && ah >= 100 && ah <= 9000) dims = { width: aw, height: ah };
        }
      }
      if (dims) { item.width = dims.width; item.height = dims.height; }
      item.quantity    = extractQuantity(dimContext) || 1;
      item.frameType   = extractFrameType(context);
      item.glazingSpec = buildGlazingSpec(context);
      item.openingType = extractOpeningType(context);
      item.location    = extractLocation(context);
      item.notes       = extractNotes(context);
      item.colour      = extractColour(context);
      item.ventilation = extractVentilation(context);
      var cillVal3     = extractCillHeight(context);
      if (cillVal3) item.cillType = cillVal3 + 'mm cill height';
      item.escapeWindow = extractEscapeWindow(context);
      // Phase 2 fields
      item.sillHeight   = extractSillHeight(context);
      item.headHeight   = extractHeadHeight(context);
      item.uValue       = extractUValue(context);
      item.finish       = extractFinish(context);
      item.doorSwing    = extractDoorSwing(context);
      item.fireRating   = extractFireRating(context);
      item.ironmongery  = extractIronmongery(context);
      item.doorType     = extractDoorType(context);

      if (refItem) {
        item.textPosition = { x: refItem.x, y: refItem.y, width: refItem.width || 30, height: refItem.height || 12 };
      }

      item.confidence = scoreConfidence(item, 'regex');
      items.push(item);
    }

    return items;
  }

  // -----------------------------------------------------------------------
  // Main entry point
  // -----------------------------------------------------------------------

  function extractItems(documents) {
    var allItems    = [];
    var allWarnings = [];
    var debugLog    = [];
    var stats       = { docsProcessed: 0, pagesProcessed: 0, itemsFound: 0, warnings: 0 };

    // Build drawing-sheet rejection set from classified drawing documents.
    // e.g. "3847.C37 Proposed Cladding Details.pdf" → reject "C37" as a glazing ref.
    _drawingSheetRefs = {};
    documents.forEach(function (doc) {
      var cls = classifyDocument(doc.name, doc.fullText || '');
      if (cls.type === 'drawing') {
        var sheetMatch = (doc.name || '').match(/\d{4}\.([A-Z]\d{1,3})\b/i);
        if (sheetMatch) {
          _drawingSheetRefs[sheetMatch[1].toUpperCase()] = true;
        }
      }
    });
    if (Object.keys(_drawingSheetRefs).length > 0) {
      debugLog.push('Drawing sheet rejection set: ' + Object.keys(_drawingSheetRefs).join(', '));
    }

    // Track schedule items by reference (schedule is the sole source of truth for items)
    var scheduleItems = {};

    // BQ validation data: { ref: { ref, bqQuantity } } — from all BQ documents
    var bqValidationData = {};

    var allDrawingRefs = {};
    var allSpecNotes   = [];

    documents.forEach(function (doc) {
      stats.docsProcessed++;
      stats.pagesProcessed += doc.pages.length;

      var classification = classifyDocument(doc.name, doc.fullText || '');
      var docType = classification.type;
      debugLog.push('[' + docType.toUpperCase() + ' / ' + classification.confidence + '] ' + doc.name + ' (' + doc.pages.length + ' page(s)) — ' + classification.reason);

      var docResult = extractFromDocument(doc);
      allItems    = allItems.concat(docResult.items);
      allWarnings = allWarnings.concat(docResult.warnings);

      if (docResult.drawingRefs) {
        docResult.drawingRefs.forEach(function (r) { allDrawingRefs[r] = true; });
      }
      if (docResult.specNotes) {
        allSpecNotes = allSpecNotes.concat(docResult.specNotes);
      }
      // Collect BQ validation data (never creates items, just ref→qty pairs)
      if (docResult.bqValidation) {
        docResult.bqValidation.forEach(function (v) {
          if (!bqValidationData[v.ref]) {
            bqValidationData[v.ref] = v;
          } else if (v.bqQuantity > bqValidationData[v.ref].bqQuantity) {
            bqValidationData[v.ref].bqQuantity = v.bqQuantity;
          }
        });
        if (docResult.bqValidation.length > 0) {
          debugLog.push('  → BQ validation: ' + docResult.bqValidation.length + ' ref(s) found for cross-check');
        } else {
          debugLog.push('  → BQ validation: no refs found (scanned or empty)');
        }
      }

      if (docResult.items.length > 0) {
        debugLog.push('  → Found ' + docResult.items.length + ' item(s): ' +
          docResult.items.slice(0, 10).map(function (i) { return i.reference; }).join(', ') +
          (docResult.items.length > 10 ? ' …' : ''));
      } else if (docType !== 'admin' && docType !== 'drawing' && docType !== 'bq') {
        debugLog.push('  → No items extracted');
      } else if (docType !== 'bq') {
        debugLog.push('  → Skipped (document type: ' + docType + ')');
      }

      // Track schedule items (schedule is the only source that creates items)
      if (docType === 'schedule') {
        docResult.items.forEach(function (item) {
          var key = item.reference.toUpperCase();
          if (!scheduleItems[key]) scheduleItems[key] = item;
        });
      }
    });

    // Cross-validate BQ quantities against schedule items
    // (replaces the old smartMerge which relied on BQ items being created)
    var bqCrossWarnings = crossValidateBQQuantities(allItems, bqValidationData, debugLog);
    allWarnings = allWarnings.concat(bqCrossWarnings);

    // Cross-reference warnings between schedule and other docs
    if (documents.length > 1) {
      var crossWarnings = crossReferenceDocuments(documents, allItems);
      allWarnings = allWarnings.concat(crossWarnings);
    }

    // Cross-validate drawing refs against schedule items — group by prefix to avoid
    // generating one warning per reference (which can easily reach 140+ for a large project).
    // Only run if the schedule actually produced items to prevent false positives.
    if (Object.keys(scheduleItems).length > 0 && Object.keys(allDrawingRefs).length > 0) {
      var missingRefs = Object.keys(allDrawingRefs).filter(function (ref) {
        return !scheduleItems[ref];
      });
      if (missingRefs.length > 0) {
        // Group by alphabetic prefix (EW, ED, ID, C, W, D, …)
        var crossRefGroups = {};
        missingRefs.forEach(function (ref) {
          var prefixMatch = ref.match(/^([A-Z]+)/);
          var prefix = prefixMatch ? prefixMatch[1] : 'OTHER';
          if (!crossRefGroups[prefix]) crossRefGroups[prefix] = [];
          crossRefGroups[prefix].push(ref);
        });
        Object.keys(crossRefGroups).sort().forEach(function (prefix) {
          var refs = crossRefGroups[prefix].sort();
          var count = refs.length;
          var range = count > 1 ? refs[0] + '\u2013' + refs[count - 1] : refs[0];
          allWarnings.push({
            id: generateId(),
            type: 'cross-ref',
            message: count + ' ' + prefix + ' reference' + (count > 1 ? 's' : '') +
                     ' (' + range + ') found in drawing(s) but not in Window Schedule' +
                     (count > 1 ? ' — check if these items are missing from the schedule' : ' — check if this item is missing from the schedule'),
            itemId: null,
            severity: 'info'
          });
        });
      }
    }

    if (allSpecNotes.length > 0) {
      debugLog.push('Specification notes: ' + allSpecNotes.join('; '));
    }

    allItems = deduplicateItems(allItems);
    stats.itemsFound = allItems.length;
    stats.warnings   = allWarnings.length;

    return { items: allItems, warnings: allWarnings, stats: stats, debugLog: debugLog, specNotes: allSpecNotes };
  }

  function extractDrawingRefs(doc) {
    var refs = {};
    var refPattern = /\b([A-Z]{0,2}[WDSC]\d{2,4})\b/gi;
    (doc.pages || []).forEach(function (page) {
      var text = page.text || '';
      var match;
      refPattern.lastIndex = 0;
      while ((match = refPattern.exec(text)) !== null) {
        var ref = match[1].toUpperCase();
        var preceding = text.substring(Math.max(0, match.index - DRAWING_NUM_LOOKBACK), match.index);
        if (DRAWING_NUM_FILTER.test(preceding) && !/\b(?:BS|EN)\s*\d/i.test(preceding)) continue;
        if (!isValidGlazingReference(ref)) continue;
        refs[ref] = true;
      }
    });
    return Object.keys(refs);
  }

  function extractSpecNotes(doc) {
    var notes = [];
    var text = (doc.pages || []).map(function (p) { return p.text || ''; }).join('\n');
    if (/triple[\s\-]?glaz/i.test(text)) notes.push('Specification requires triple glazing');
    if (/fire[\s\-]?rated?/i.test(text)) notes.push('Fire-rated glazing specified');
    if (/acoustic/i.test(text)) notes.push('Acoustic glazing specified');
    if (/bs\s*en\s*\d+/i.test(text)) {
      var bsMatches = text.match(/bs\s*en\s*\d+(?:[\s:\-]\d+)*/gi) || [];
      bsMatches.slice(0, 5).forEach(function (m) { notes.push('Standard: ' + m.trim()); });
    }
    return notes;
  }

  // Extract reference → quantity pairs from a BQ document for cross-validation.
  // Never creates glazing items — only returns validation data.
  function extractBQValidation(doc) {
    var bqData = {};
    var pattern = new RegExp(REF_FIRST_PATTERN.source, 'gi');

    (doc.pages || []).forEach(function (page) {
      var text = page.text || '';
      if (!text || text.trim().length === 0) return;

      var normText = normaliseSpaceSplitRefs(text);
      pattern.lastIndex = 0;
      var match;

      while ((match = pattern.exec(normText)) !== null) {
        var ref = match[1].toUpperCase();
        var idx = match.index;

        // Reject drawing-sheet number context
        var preceding = normText.substring(Math.max(0, idx - DRAWING_NUM_LOOKBACK), idx);
        if (DRAWING_NUM_FILTER.test(preceding) && !/\b(?:BS|EN)\s*\d/i.test(preceding)) continue;

        // Reject BS/EN codes, drawing sheet numbers, and other false positives
        if (!isValidGlazingReference(ref)) continue;

        // Grab forward context for quantity extraction
        var context = normText.substring(idx, Math.min(normText.length, idx + CTX_FORWARD_DIMS));
        var qty = extractQuantity(context) || 1;

        if (!bqData[ref]) {
          bqData[ref] = { ref: ref, bqQuantity: qty };
        } else if (qty > bqData[ref].bqQuantity) {
          bqData[ref].bqQuantity = qty;
        }
      }
    });

    return Object.keys(bqData).map(function (k) { return bqData[k]; });
  }

  function extractFromDocument(doc) {
    var classification = classifyDocument(doc.name, doc.fullText || '');
    var docType = classification.type;

    // Admin documents contain no glazing data — skip entirely to avoid false positives
    if (docType === 'admin') return { items: [], warnings: [] };

    // Architectural drawings — extract reference markers for cross-validation only
    if (docType === 'drawing') {
      var drawingRefs = extractDrawingRefs(doc);
      return { items: [], warnings: [], drawingRefs: drawingRefs };
    }

    // Specification documents — extract material notes only, no dimensions
    if (docType === 'specification') {
      var specNotes = extractSpecNotes(doc);
      return { items: [], warnings: [], specNotes: specNotes };
    }

    // BQ documents — validate quantities only; never create items.
    // Items are created exclusively from the schedule (single source of truth).
    if (docType === 'bq') {
      var bqValidation = extractBQValidation(doc);
      var bqWarnings = [];
      var hasText = doc.pages.some(function (p) { return p.text && p.text.trim().length > MIN_TEXT_LENGTH; });
      if (!hasText) {
        bqWarnings.push({
          id: generateId(),
          type: 'extraction',
          message: 'No glazing items found in "' + doc.name + '". The document appears to be a scanned image — text extraction is not possible. Please add items manually.',
          itemId: null,
          severity: 'error'
        });
      }
      return { items: [], warnings: bqWarnings, bqValidation: bqValidation };
    }

    var items       = [];
    var warnings    = [];
    var referenceMap = {};

    doc.pages.forEach(function (page) {
      var pageItems = extractFromPage(page, doc.name, docType);
      console.log('[ExtractDoc] Page ' + page.pageNum + ' of "' + doc.name + '": ' + pageItems.length + ' item(s) — ' +
        pageItems.map(function (i) { return i.reference; }).join(', '));
      pageItems.forEach(function (item) {
        var ref = item.reference.toUpperCase();
        if (ref && referenceMap[ref]) {
          // Merge into the existing item for this doc
          var existing = referenceMap[ref];
          if (item.width  > 0 && existing.width  === 0) existing.width  = item.width;
          if (item.height > 0 && existing.height === 0) existing.height = item.height;
          if (item.quantity > 1 && existing.quantity === 1) existing.quantity = item.quantity;
          if (item.location && !existing.location) existing.location = item.location;
          if (item.frameType !== 'Unknown' && existing.frameType === 'Unknown') {
            existing.frameType = item.frameType;
          }
          mergeNotes(existing, item);
          existing.confidence = scoreConfidence(existing, 'merged');
        } else {
          if (ref) referenceMap[ref] = item;
          items.push(item);
        }
      });
    });

    // Document-level fallback: if per-page extraction found fewer than 3 items for a
    // schedule document, re-run reference-first extraction on the full document text.
    // This sidesteps per-page text splitting issues from PDF.js.
    if (docType === 'schedule' && items.length < 3) {
      console.log('[ExtractDoc] Schedule fallback triggered — only ' + items.length + ' item(s) from per-page extraction. Trying full-document extraction…');
      // Combine all textItems from all pages
      var allTextItems = [];
      doc.pages.forEach(function (page) {
        (page.textItems || []).forEach(function (ti) { allTextItems.push(ti); });
      });
      var fullText = doc.fullText || doc.pages.map(function (p) { return p.text || ''; }).join(' ');
      var fallbackItems = tryReferenceFirstExtraction(allTextItems, fullText, doc.name, 0);
      console.log('[ExtractDoc] Full-document fallback found ' + fallbackItems.length + ' item(s)');

      // Merge fallback items — only add refs NOT already found
      fallbackItems.forEach(function (item) {
        var ref = item.reference.toUpperCase();
        if (ref && !referenceMap[ref]) {
          referenceMap[ref] = item;
          items.push(item);
        }
      });
    }

    // Suppress X01 phantom items when real items have been found
    if (items.length > 1) {
      items = items.filter(function (item) {
        return item.reference !== 'X01';
      });
    }

    // Post-extraction: infer frameType from finish / doorFrame when still Unknown
    items.forEach(function (item) { inferFrameTypeFromFields(item); });

    // Validation warnings for incomplete items
    items.forEach(function (item) {
      validateItemForWarnings(item).forEach(function (msg) {
        warnings.push({ id: generateId(), type: 'validation', message: msg, itemId: item.id, severity: 'warning' });
      });
    });

    // Only warn about missing items in schedule docs (BQ handled above, others skipped earlier)
    if (items.length === 0 && docType === 'schedule') {
      // Determine if the document has any text at all (to give a better message)
      var hasText = doc.pages.some(function (p) { return p.text && p.text.trim().length > MIN_TEXT_LENGTH; });
      var msg = hasText
        ? 'No glazing items found in "' + doc.name + '". The document was read but no recognisable references (e.g. EW01, W01, D01) were found. Please verify the document contains a window/door schedule and add items manually if needed.'
        : 'No glazing items found in "' + doc.name + '". The document appears to be a scanned image — text extraction is not possible. Please add items manually.';
      warnings.push({
        id: generateId(),
        type: 'extraction',
        message: msg,
        itemId: null,
        severity: 'error'
      });
    }

    return { items: items, warnings: warnings };
  }

  function extractFromPage(page, sourceName, docType) {
    var textItems = page.textItems || [];
    var text      = page.text || '';

    if (!text || text.trim().length === 0) return [];

    // Strategy 0 (schedule docs only): Reference-first extraction.
    // Scans all text items for valid glazing references first, then clusters
    // nearby items to extract attributes.  More tolerant of PDF text fragmentation
    // than the table/row strategies because it does not rely on table structure.
    if (docType === 'schedule') {
      var refFirstItems = tryReferenceFirstExtraction(textItems, text, sourceName, page.pageNum);
      if (refFirstItems.length > 0) {
        console.log('[ExtractPage] Page ' + page.pageNum + ': Strategy 0 (reference-first) → ' + refFirstItems.length + ' items');
        return refFirstItems;
      }
    }

    // When we have proper positional data, try spatial strategies first
    if (textItems.length > 0 && textItems[0] && textItems[0].x !== undefined) {
      var rows = buildRows(textItems);

      // Adaptive tolerance: if very few rows have ≥2 items, the initial grouping may
      // be too tight — retry with a wider tolerance (up to 15 pt).
      var multiItemRows = rows.filter(function (r) { return r.items.length >= 2; });
      if (multiItemRows.length < 3 && rows.length > 5) {
        var wideRows = buildRows(textItems, 15);
        var wideMulti = wideRows.filter(function (r) { return r.items.length >= 2; });
        if (wideMulti.length > multiItemRows.length) {
          rows = wideRows;
        }
      }

      // Strategy 1: Structured table with header row
      var tableItems = tryTableExtraction(rows, sourceName, page.pageNum);
      if (tableItems.length > 0) {
        console.log('[ExtractPage] Page ' + page.pageNum + ': Strategy 1 (table) → ' + tableItems.length + ' items');
        return tableItems;
      }

      // Strategy 2: Row-based reference pattern
      var rowItems = tryRowBasedExtraction(rows, sourceName, page.pageNum, docType);
      if (rowItems.length > 0) {
        console.log('[ExtractPage] Page ' + page.pageNum + ': Strategy 2 (row-based) → ' + rowItems.length + ' items');
        return rowItems;
      }
    }

    // Strategy 3: Enhanced regex with spatial context
    var regexItems = tryEnhancedRegex(textItems, text, sourceName, page.pageNum);
    if (regexItems.length > 0) {
      console.log('[ExtractPage] Page ' + page.pageNum + ': Strategy 3 (enhanced regex) → ' + regexItems.length + ' items');
      return regexItems;
    }

    // Strategy 4: Line-based text fallback — split on newlines and process each line.
    // This handles PDFs where position data is absent or unreliable but the text layer
    // is clean enough to produce one item per line.
    var lineItems = tryLineBasedExtraction(text, sourceName, page.pageNum);
    if (lineItems.length > 0) {
      console.log('[ExtractPage] Page ' + page.pageNum + ': Strategy 4 (line-based) → ' + lineItems.length + ' items');
      return lineItems;
    }

    // Strategy 5: Infer an item without a reference (schedule docs only — never BQ)
    if (docType === 'schedule') {
      var inferred = tryInferWithoutRef(text, sourceName, page.pageNum);
      if (inferred) {
        console.log('[ExtractPage] Page ' + page.pageNum + ': Strategy 5 (infer-without-ref) → 1 item');
        return [inferred];
      }
    }

    console.log('[ExtractPage] Page ' + page.pageNum + ': No strategy produced items (text length: ' + text.length + ')');
    return [];
  }

  // -----------------------------------------------------------------------
  // Strategy 4 — Line-based text fallback
  // -----------------------------------------------------------------------

  function tryLineBasedExtraction(text, sourceName, sourcePage) {
    var items = [];
    var lines = text.split(/\r?\n/);
    // Collect lines that start with (or prominently feature) a glazing reference
    var lineRefPattern = /\b([A-Z]{0,2}[WDSC]\d{2,4})\b/i;
    var refLines = [];
    lines.forEach(function (line) {
      var m = line.match(lineRefPattern);
      if (!m) return;
      var ref = m[1].toUpperCase();
      // Verify it doesn't look like a drawing-sheet number context
      var idx = m.index;
      var pre = line.substring(Math.max(0, idx - DRAWING_NUM_LOOKBACK), idx);
      if (DRAWING_NUM_FILTER.test(pre) && !/\b(?:BS|EN)\s*\d/i.test(pre)) return;
      // Reject UK postcodes and revision markers
      var fol = line.substring(idx + m[0].length, idx + m[0].length + 30);
      if (/^\s+\d[A-Z]{2}\b/i.test(fol)) return;
      if (/^\s+(?:construction|revision|issue|draft|preliminary|tender|planning|for\s+(?:comment|approval|info))/i.test(fol)) return;
      // Reject CAD title block status/revision codes preceded by drawing scale
      if (/^[CDWS]\d{2,3}$/i.test(ref)) {
        var widerPre = line.substring(Math.max(0, idx - 30), idx);
        if (/\d\s*:\s*\d+\s*$/.test(widerPre)) return;
      }
      if (!isValidGlazingReference(ref)) return;
      refLines.push({ ref: ref, line: line });
    });

    if (refLines.length < 2) return items;

    refLines.forEach(function (rl) {
      var item = createItem({
        reference: rl.ref,
        type: inferType(rl.ref),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });
      var dims = extractDimensionsFromText(rl.line);
      if (!dims) {
        // Fallback: two consecutive 3-4 digit numbers may be W and H in separate table columns
        var adjNums = rl.line.match(/\b(\d{3,4})\s+(\d{3,4})\b/);
        if (adjNums) {
          var aw = parseInt(adjNums[1], 10), ah = parseInt(adjNums[2], 10);
          if (aw >= 100 && aw <= 9000 && ah >= 100 && ah <= 9000) dims = { width: aw, height: ah };
        }
      }
      if (dims) { item.width = dims.width; item.height = dims.height; }
      item.quantity    = extractQuantity(rl.line) || 1;
      item.frameType   = extractFrameType(rl.line);
      item.glazingSpec = buildGlazingSpec(rl.line);
      item.openingType = extractOpeningType(rl.line);
      item.location    = extractLocation(rl.line);
      item.notes       = extractNotes(rl.line);
      item.confidence  = scoreConfidence(item, 'regex');
      items.push(item);
    });
    return items;
  }

  // -----------------------------------------------------------------------
  // Smart cross-document merging (schedule wins on dims, BQ wins on qty)
  // -----------------------------------------------------------------------

  function smartMerge(scheduleItems, bqItems, allItems) {
    var warnings = [];
    var allRefKeys = {};
    Object.keys(scheduleItems).forEach(function (k) { allRefKeys[k] = true; });
    Object.keys(bqItems).forEach(function (k) { allRefKeys[k] = true; });

    Object.keys(allRefKeys).forEach(function (ref) {
      var sItem = scheduleItems[ref];
      var bItem = bqItems[ref];
      if (!sItem || !bItem) return;

      // Prefer BQ quantity when the schedule only has the default of 1
      if (bItem.quantity > 1 && sItem.quantity === 1) {
        sItem.quantity = bItem.quantity;
      }

      // Flag dimension conflicts (both sources have real dimensions but they differ)
      if (sItem.width > 0 && bItem.width > 0 &&
          (sItem.width !== bItem.width || sItem.height !== bItem.height)) {
        warnings.push({
          id: generateId(),
          type: 'discrepancy',
          message: ref + ': Dimensions differ — Window Schedule: ' + sItem.width + '×' + sItem.height +
                   'mm, BQ: ' + bItem.width + '×' + bItem.height + 'mm — using Window Schedule values',
          itemId: sItem.id,
          severity: 'warning'
        });
        // Override BQ item in allItems with schedule dimensions
        var bItemInAll = allItems.find(function (it) { return it.id === bItem.id; });
        if (bItemInAll) {
          bItemInAll.width  = sItem.width;
          bItemInAll.height = sItem.height;
        }
      }
    });

    return warnings;
  }

  // Cross-validate schedule item quantities against BQ validation data.
  // When the BQ says a different quantity than the schedule default (1), prefer
  // the BQ quantity and flag a warning so the user can verify.
  function crossValidateBQQuantities(items, bqValidationData, debugLog) {
    var warnings = [];
    if (Object.keys(bqValidationData).length === 0) return warnings;

    items.forEach(function (item) {
      var bqEntry = bqValidationData[item.reference];
      if (!bqEntry) return;

      if (bqEntry.bqQuantity > 1 && item.quantity === 1) {
        // Prefer BQ quantity — schedule often shows qty=1 (one type) while BQ shows total
        item.quantity = bqEntry.bqQuantity;
        if (debugLog) {
          debugLog.push('  BQ qty update: ' + item.reference + ' → qty ' + bqEntry.bqQuantity);
        }
      } else if (bqEntry.bqQuantity > 1 && bqEntry.bqQuantity !== item.quantity) {
        warnings.push({
          id: generateId(),
          type: 'discrepancy',
          message: item.reference + ': Quantity discrepancy — Schedule: ' + item.quantity +
                   ', BQ: ' + bqEntry.bqQuantity + ' — please verify',
          itemId: item.id,
          severity: 'warning'
        });
      }
    });

    return warnings;
  }

  // -----------------------------------------------------------------------
  // Attribute extractors (unchanged behaviour, kept for compatibility)
  // -----------------------------------------------------------------------

  function extractDimensionsFromText(text) {
    if (!text) return null;

    // Try patterns in order of specificity / reliability
    var patterns = [
      // "1010 x 1050"  or  "1010x1050"  or  "1010×1050"  (3–4 digits, mm)
      /(\d{3,4})\s*[xX×]\s*(\d{3,4})/,
      // "w=1010 h=1050"  or  "W:1010 H:1050"
      /[wW]\s*[=:]\s*(\d{3,4})\s+[hH]\s*[=:]\s*(\d{3,4})/,
      // "1010w x 1050h"
      /(\d{3,4})\s*[wW]\s*[xX×]\s*(\d{3,4})\s*[hH]/,
      // Metres with decimal point or European comma: "1.010 x 1.050" or "1,010 x 1,050"
      // Pattern: 1–2 digits + separator + exactly 3 digits (avoids matching e.g. "14.1")
      // Both forms are converted to mm by multiplying by 1000 when value < 10.
      /(\d{1,2}[.,]\d{3})\s*[xX×]\s*(\d{1,2}[.,]\d{3})/
    ];

    for (var pi = 0; pi < patterns.length; pi++) {
      var match = patterns[pi].exec(text);
      if (match) {
        // Treat comma as decimal separator (covers both European notation and thousands
        // separator — for glazing dimensions "1,010" means 1010mm either way).
        var w = parseFloat(match[1].replace(',', '.'));
        var h = parseFloat(match[2].replace(',', '.'));
        // Convert metres to mm when values look like metres (< 10)
        if (w < 10 && h < 10) { w = Math.round(w * 1000); h = Math.round(h * 1000); }
        w = Math.round(w);
        h = Math.round(h);
        if (w >= 100 && w <= 9000 && h >= 100 && h <= 9000) {
          return { width: w, height: h };
        }
      }
    }
    return null;
  }

  function extractFrameType(text) {
    if (!text) return 'Unknown';
    if (/\b(?:aluminium|aluminum|alum|alu)\b/i.test(text)) return 'Aluminium';
    if (/\b(?:pvcu|pvc-u|pvc\.u|upvc|pvc)\b/i.test(text))  return 'PVCu';
    if (/\b(?:timber|wood|wooden|oak|softwood|hardwood)\b/i.test(text)) return 'Timber';
    if (/\b(?:steel|galvanised|stainless)\b/i.test(text))   return 'Steel';
    // PPC (Polyester Powder Coated) is aluminium-specific in glazing industry
    if (/\bppc\b/i.test(text)) return 'Aluminium';
    // Abbreviations common in UK door schedules: sw = softwood, hw = hardwood
    if (/\bsw\b/i.test(text)) return 'Timber';
    if (/\bhw\b/i.test(text)) return 'Timber';
    return 'Unknown';
  }

  // Post-extraction inference: if frameType is still 'Unknown', try to derive
  // it from the finish or doorFrame fields that were extracted from table columns.
  function inferFrameTypeFromFields(item) {
    if (!item || item.frameType !== 'Unknown') return;
    // Check finish field (e.g. "PPC Aluminium RAL 7016", "Powder Coated")
    if (item.finish) {
      var ft = extractFrameType(item.finish);
      if (ft !== 'Unknown') { item.frameType = ft; return; }
      // "Powder Coated" / "PPC" without explicit material — typically aluminium
      if (/\b(?:ppc|powder\s*coat)/i.test(item.finish)) { item.frameType = 'Aluminium'; return; }
    }
    // Check doorFrame field (e.g. "Aluminium", "32 x 125mm sw")
    if (item.doorFrame) {
      var ft2 = extractFrameType(item.doorFrame);
      if (ft2 !== 'Unknown') { item.frameType = ft2; return; }
      // "sw" = softwood → Timber
      if (/\bsw\b/i.test(item.doorFrame)) { item.frameType = 'Timber'; return; }
      // "hw" = hardwood → Timber
      if (/\bhw\b/i.test(item.doorFrame)) { item.frameType = 'Timber'; return; }
    }
  }

  function buildGlazingSpec(text) {
    var parts = [];
    if (/\b(?:triple\s*glaz(?:ed|ing)|tgu)\b/i.test(text)) {
      parts.push('Triple Glazed');
    } else {
      parts.push('Double Glazed');
    }
    if (/\b(?:obscure|frosted|opaque|satin)\b/i.test(text)) {
      parts.push('Obscure');
    } else if (/\btinted\b/i.test(text)) {
      parts.push('Tinted');
    } else {
      parts.push('Clear');
    }
    if (/\b(?:laminated|lami)\b/i.test(text))  parts.push('Laminated');
    if (/\b(?:toughened|tempered)\b/i.test(text)) parts.push('Toughened');
    if (/\b(?:fire[\s\-]?rated?|fw\d+|fr\d+)\b/i.test(text)) parts.push('Fire Rated');
    if (/\b(?:acoustic|sound[\s\-]?proof)\b/i.test(text))   parts.push('Acoustic');
    return parts.join(' - ');
  }

  function extractOpeningType(text) {
    if (!text) return 'Fixed';
    if (/\btilt[\s\-]?(?:and[\s\-]?)?turn\b/i.test(text)) return 'Tilt & Turn';
    if (/\btop[\s\-]?hung\b/i.test(text))  return 'Top Hung';
    if (/\bcasement\b/i.test(text))        return 'Casement';
    if (/\b(?:sliding|slider)\b/i.test(text)) return 'Sliding';
    if (/\bpivot\b/i.test(text))           return 'Pivot';
    if (/\bbi[\s\-]?fold\b/i.test(text))   return 'Bi-fold';
    if (/\bfixed\b/i.test(text))           return 'Fixed';
    return 'Fixed';
  }

  // --- Phase 1 detail extractors ---

  function extractColour(text) {
    if (!text) return '';
    // RAL code: "RAL 9005", "RAL9005"
    var ralMatch = /\bRAL\s*(\d{4})\b/i.exec(text);
    if (ralMatch) return 'RAL ' + ralMatch[1];
    // Named foil/finish colours — check BEFORE grey code to avoid
    // "Anthracite Grey" matching "Grey 1010" via the dimension number.
    var foilMatch = /\b(anthracite|black|white|cream|bronze|chartwell\s*green|irish\s*oak|rosewood|golden\s*oak)\s*(foil|grey|woodgrain)?\b/i.exec(text);
    if (foilMatch) {
      var colour = foilMatch[1].replace(/\b\w/g, function (c) { return c.toUpperCase(); });
      if (foilMatch[2]) colour += ' ' + foilMatch[2].charAt(0).toUpperCase() + foilMatch[2].slice(1).toLowerCase();
      return colour;
    }
    // Grey/Gray colour code: "Grey 7016" — only match 4-digit codes ≥ 2000
    // to avoid dimension numbers like 1010, 1050, 1500 being mistaken for colour codes.
    var greyMatch = /\b(grey|gray)\s+(\d{4})\b/i.exec(text);
    if (greyMatch && parseInt(greyMatch[2], 10) >= 2000) return 'Grey ' + greyMatch[2];
    return '';
  }

  function extractCillHeight(text) {
    if (!text) return '';
    // "cill 1050", "sill ht 1050", "cill height 1050", "1050 cill", "1050mm cill"
    var m1 = /\b(?:cill|sill)\s*(?:ht|height|@|at|above[^)]{0,30}?)?\s*(\d{3,4})\b/i.exec(text);
    if (m1) return m1[1];
    // "Structural cill above floor slab mm ... 1050"  — number after "cill" in schedule header context
    var m2 = /\b(\d{3,4})\s*(?:mm\s*)?(?:cill|sill)\b/i.exec(text);
    if (m2) return m2[1];
    return '';
  }

  function extractEscapeWindow(text) {
    if (!text) return '';
    // "Fire Exit" door implicitly an escape route
    if (/\bfire\s*exit\b/i.test(text)) return 'Yes';
    // Look for explicit Yes/No after "Escape" keyword in schedule row context
    var escYes = /\bescape\b[^.]{0,20}\b(yes)\b/i.exec(text);
    if (escYes) return 'Yes';
    var escNo = /\bescape\b[^.]{0,20}\b(no)\b/i.exec(text);
    if (escNo) return 'No';
    return '';
  }

  function extractVentilation(text) {
    if (!text) return '';
    // Named ventilation products: "4000 Linkvent", "Greenwood CV20"
    var ventProduct = /\b(\d{3,5}\s*(?:linkvent|greenwood|titon|vent\s*air))\b/i.exec(text);
    if (ventProduct) return ventProduct[1].trim();
    // Generic: "trickle vent", "ventilator"
    if (/\btrickle[\s\-]?vent/i.test(text)) return 'Trickle Vent';
    if (/\bventilator\b/i.test(text)) return 'Ventilator';
    return '';
  }

  function extractLocation(text) {
    if (!text) return '';
    var floorPatterns = [
      { pattern: /\b(?:ground[\s\-]?floor|gf)\b/i,           label: 'Ground Floor' },
      { pattern: /\b(?:first[\s\-]?floor|ff|1st[\s\-]?floor)\b/i, label: 'First Floor' },
      { pattern: /\b(?:second[\s\-]?floor|sf|2nd[\s\-]?floor)\b/i, label: 'Second Floor' },
      { pattern: /\b(?:third[\s\-]?floor|tf|3rd[\s\-]?floor)\b/i,  label: 'Third Floor' },
      { pattern: /\bbasement\b/i,                             label: 'Basement' },
      // Shaftesbury-style: "GA Ground Floor Level", "Level 1 - GA First Floor Level"
      { pattern: /\bGA\s+Ground\s+Floor/i,                    label: 'Ground Floor' },
      { pattern: /\bGA\s+First\s+Floor/i,                     label: 'First Floor' },
      { pattern: /\bLevel\s+1\b/i,                            label: 'First Floor' }
    ];
    for (var i = 0; i < floorPatterns.length; i++) {
      if (floorPatterns[i].pattern.test(text)) return floorPatterns[i].label;
    }
    var roomMatch = /\b(?:to|at|in|for)\s+(?:the\s+)?([\w]+\s*(?:room|office|kitchen|bedroom|bathroom|hallway|hall|living|dining|study|lounge|lobby|corridor|stair))/i.exec(text);
    if (roomMatch) return roomMatch[1].trim();
    // Direct room name patterns for schedule "To Room" columns (no preposition)
    var directRoom = /\b(Classroom\s*\d*|Sensory\s*Room|Therapy\s*(?:Multi\s*Use\s*)?Room|Meeting\s*(?:\/\s*Office)?|Stairwell|Circulation|Store|Disabled\s*WC)\b/i.exec(text);
    if (directRoom) return directRoom[1].trim();
    return '';
  }

  // --- Phase 2 detail extractors (Shaftesbury+) ---

  function extractUValue(text) {
    if (!text) return '';
    // "1.4 W/m2k", "1.4W/m²K", "U=1.4", "U Value 1.4", "1.4 W/m²k"
    var m = /\b(\d+\.?\d*)\s*W\/m[²2]\s*[kK]\b/i.exec(text);
    if (m) return m[1] + ' W/m2k';
    var m2 = /\bU[\s\-]*(?:value|val)?\s*[=:\s]\s*(\d+\.?\d*)\b/i.exec(text);
    if (m2) return m2[1] + ' W/m2k';
    return '';
  }

  function extractHeadHeight(text) {
    if (!text) return '';
    // "Head Height 2175", "head ht 2590", "lintel 2175"
    var m1 = /\b(?:head|lintel)\s*(?:ht|height)?\s*[:\-]?\s*(\d{3,5})\b/i.exec(text);
    if (m1) return m1[1];
    var m2 = /\b(\d{3,5})\s*(?:mm\s*)?(?:head|lintel)\s*(?:ht|height)?\b/i.exec(text);
    if (m2) return m2[1];
    return '';
  }

  function extractSillHeight(text) {
    if (!text) return '';
    // Reuse cill/sill pattern but return just the number
    var val = extractCillHeight(text);
    if (val) return val;
    // Also check "Sill Height 640", "sill height 0"
    var m = /\b(?:sill|cill)\s*(?:height|ht)\s*[:\-]?\s*(\d{1,5})\b/i.exec(text);
    if (m) return m[1];
    return '';
  }

  function extractDoorSwing(text) {
    if (!text) return '';
    if (/\bdouble\s*doors?\b/i.test(text)) return 'Double';
    var m = /\b(RHS|LHS)\b/i.exec(text);
    if (m) return m[1].toUpperCase();
    if (/\bright[\s\-]?hand/i.test(text)) return 'RHS';
    if (/\bleft[\s\-]?hand/i.test(text)) return 'LHS';
    return '';
  }

  function extractFireRating(text) {
    if (!text) return '';
    // "FD30S", "FD30", "FD60S", "FD60", "FD120"
    var m = /\b(FD\d{2,3}S?)\b/i.exec(text);
    if (m) return m[1].toUpperCase();
    if (/\bfire[\s\-]?rated?\b/i.test(text)) return 'Fire Rated';
    if (/\bN\/?A\b/i.test(text)) return 'N/A';
    return '';
  }

  function extractIronmongery(text) {
    if (!text) return '';
    // "Set C3/C6", "Set P3", "Set A3", "Doc M pack"
    var m = /\b(Set\s+[A-Z0-9\/]+)\b/i.exec(text);
    if (m) return m[1];
    if (/\bdoc\s*m\s*pack\b/i.test(text)) return 'Doc M pack';
    var hw = /\b(lever\s*handle|pull\s*handle|push\s*plate|panic\s*bar|kick\s*plate|thumb\s*turn|knob\s*set|concealed\s*closer|overhead\s*closer)s?\b/i.exec(text);
    if (hw) return hw[1].replace(/\s+/g, ' ');
    return '';
  }

  function extractFinish(text) {
    if (!text) return '';
    // "PPC Aluminium", "Powder Coated", "Formica Laminate", "RAL Colour To match existing"
    if (/\bPPC\s*Aluminium\b/i.test(text)) return 'PPC Aluminium';
    if (/\bpowder[\s\-]?coat/i.test(text)) return 'Powder Coated';
    if (/\bformica[\s\-]?laminate/i.test(text)) return 'Formica Laminate Finish';
    // "RAL Colour To match existing" — pass through the finish description
    var ralFinish = /\b(RAL\s+Colo(?:u)?r\s+(?:To\s+match\s+existing|TBC))\b/i.exec(text);
    if (ralFinish) return ralFinish[1];
    if (/\banodised\b/i.test(text)) return 'Anodised';
    // Standalone "PPC" (Polyester Powder Coated) with optional RAL code
    var ppcRal = /\bPPC\s+(RAL\s*\d+)\b/i.exec(text);
    if (ppcRal) return 'PPC ' + ppcRal[1];
    if (/\bPPC\b/.test(text)) return 'PPC';
    return '';
  }

  function extractDoorType(text) {
    if (!text) return '';
    // "YMD Door Type 1", "Door Type 5"
    var m = /\b((?:YMD\s+)?Door\s+Type\s+\d+)\b/i.exec(text);
    if (m) return m[1];
    return '';
  }

  function extractNotes(text) {
    var notes = [];
    var notePatterns = [
      { pattern: /\b(?:trickle[\s\-]?vent|ventilator)\b/i,      note: 'Trickle vent required' },
      { pattern: /\b(?:restrictor|limiter|stay)\b/i,              note: 'Window restrictor required' },
      { pattern: /\b(?:fire[\s\-]?rated?|fw\d+|fr\d+)\b/i,       note: 'Fire rated glazing' },
      { pattern: /\b(?:acoustic|sound[\s\-]?proof)\b/i,           note: 'Acoustic specification' },
      { pattern: /\b(?:obscure|frosted)\b/i,                       note: 'Obscure/frosted glass' },
      { pattern: /\blaminated\b/i,                                 note: 'Laminated glass' },
      { pattern: /\btoughened\b/i,                                 note: 'Toughened safety glass' },
      { pattern: /\b(?:handicapped|accessible|disabled)\b/i,      note: 'Accessibility requirement' }
    ];
    notePatterns.forEach(function (np) {
      if (np.pattern.test(text)) notes.push(np.note);
    });
    return notes;
  }

  function extractQuantity(text) {
    var patterns = [
      /(?:qty|quantity)\s*[:\-]?\s*(\d+)/i,
      /(?:nr|no\.?)\s*[:\-]?\s*(\d+)/i,
      /(\d+)\s*(?:nr|no\.?|off)\b/i,
      /^(\d+)\s+[WDSCwdsc]\d/m
    ];
    for (var i = 0; i < patterns.length; i++) {
      var m = patterns[i].exec(text);
      if (m) {
        var qty = parseInt(m[1], 10);
        if (qty > 0 && qty < 500) return qty;
      }
    }
    return 1;
  }

  function tryInferWithoutRef(text, sourceName, sourcePage) {
    var dims = extractDimensionsFromText(text);
    if (!dims) return null;
    return createItem({
      reference:    'X01',
      type:         'other',
      width:        dims.width,
      height:       dims.height,
      quantity:     extractQuantity(text) || 1,
      frameType:    extractFrameType(text),
      glazingSpec:  buildGlazingSpec(text),
      openingType:  extractOpeningType(text),
      location:     extractLocation(text),
      notes:        extractNotes(text),
      confidence:   'low',
      sourceDocument: sourceName,
      sourcePage:   sourcePage
    });
  }

  function inferType(ref) {
    // Find the last alphabetic character that is immediately followed by the digit
    // sequence.  For single-letter refs like "W01" this is "W"; for multi-letter
    // prefix refs like "EW01" the regex finds "W" (since E is followed by W, not a
    // digit, while W is followed by "0").  This correctly maps the functional
    // type letter regardless of how many prefix letters precede it.
    var upper = (ref || '').toUpperCase();
    var lastAlpha = upper.match(/([A-Z])(?=\d)/);
    var ch = lastAlpha ? lastAlpha[1] : upper.charAt(0);
    if (ch === 'W') return 'window';
    if (ch === 'D') return 'door';
    if (ch === 'S') return 'screen';
    if (ch === 'C') return 'curtain wall';
    return 'other';
  }

  // -----------------------------------------------------------------------
  // Confidence scoring
  // -----------------------------------------------------------------------

  function scoreConfidence(item, strategy) {
    var score = 0;
    if (item.reference && item.reference !== 'X01') score += 2;
    if (item.width  >= 100) score += 2;
    if (item.height >= 100) score += 2;
    if (item.quantity > 0) score += 1;
    if (item.frameType && item.frameType !== 'Unknown') score += 1;
    if (item.location)     score += 1;
    if (item.glazingSpec)  score += 0.5;
    // Strategy bonus
    if (strategy === 'reference-first') score += 1.0;
    else if (strategy === 'table')  score += 1.5;
    else if (strategy === 'row') score += 0.5;
    if (score >= 9)   return 'high';
    if (score >= 5.5) return 'medium';
    return 'low';
  }

  // -----------------------------------------------------------------------
  // Deduplication and cross-document validation
  // -----------------------------------------------------------------------

  function deduplicateItems(items) {
    var byRef = {};
    var confOrder = { high: 3, medium: 2, low: 1 };

    items.forEach(function (item) {
      var key = item.reference.toUpperCase();
      if (!byRef[key]) {
        byRef[key] = item;
      } else {
        var existing = byRef[key];
        var existingConf = confOrder[existing.confidence] || 0;
        var newConf      = confOrder[item.confidence] || 0;

        // Keep the best data from both copies
        if (item.width  > 0 && existing.width  === 0) existing.width  = item.width;
        if (item.height > 0 && existing.height === 0) existing.height = item.height;
        if (item.quantity > 1 && existing.quantity === 1) existing.quantity = item.quantity;
        if (item.location && !existing.location) existing.location = item.location;
        if (item.frameType !== 'Unknown' && existing.frameType === 'Unknown') {
          existing.frameType = item.frameType;
        }
        mergeNotes(existing, item);

        // If the newer copy has higher confidence, prefer its dimensional data
        if (newConf > existingConf) {
          if (item.width  > 0) existing.width  = item.width;
          if (item.height > 0) existing.height = item.height;
          if (item.frameType !== 'Unknown') existing.frameType = item.frameType;
        }
        existing.confidence = scoreConfidence(existing, 'merged');
      }
    });

    return Object.keys(byRef).map(function (k) { return byRef[k]; });
  }

  function crossReferenceDocuments(documents, allItems) {
    var warnings = [];
    if (documents.length < 2) return warnings;

    // Only cross-reference schedule and BQ type documents
    var relevantDocs = documents.filter(function (doc) {
      return isRelevantForCrossRef(classifyDocument(doc.name).type);
    });
    if (relevantDocs.length < 2) return warnings;

    var itemsByDoc = {};
    relevantDocs.forEach(function (doc) { itemsByDoc[doc.name] = {}; });

    allItems.forEach(function (item) {
      if (item.sourceDocument && itemsByDoc[item.sourceDocument]) {
        itemsByDoc[item.sourceDocument][item.reference] = item;
      }
    });

    var docNames = Object.keys(itemsByDoc);
    if (docNames.length < 2) return warnings;

    var allRefs = {};
    allItems.forEach(function (i) { if (i.reference) allRefs[i.reference] = true; });

    Object.keys(allRefs).forEach(function (ref) {
      var foundIn = docNames.filter(function (d) { return itemsByDoc[d][ref]; });
      if (foundIn.length >= 2) {
        for (var i = 0; i < foundIn.length - 1; i++) {
          for (var j = i + 1; j < foundIn.length; j++) {
            var itemA = itemsByDoc[foundIn[i]][ref];
            var itemB = itemsByDoc[foundIn[j]][ref];
            if (itemA && itemB && itemA.width > 0 && itemB.width > 0) {
              if (itemA.width !== itemB.width || itemA.height !== itemB.height) {
                warnings.push({
                  id: generateId(),
                  type: 'discrepancy',
                  message: 'Dimension mismatch for ' + ref + ': ' + itemA.width + '×' + itemA.height +
                           'mm (' + foundIn[i] + ') vs ' + itemB.width + '×' + itemB.height +
                           'mm (' + foundIn[j] + ')',
                  itemId: itemA.id,
                  severity: 'warning'
                });
              }
            }
          }
        }
      }
    });

    return warnings;
  }

  // -----------------------------------------------------------------------
  // Shared helpers
  // -----------------------------------------------------------------------

  function mergeNotes(target, source) {
    if (source.notes && source.notes.length > 0) {
      source.notes.forEach(function (n) {
        if (target.notes.indexOf(n) === -1) target.notes.push(n);
      });
    }
  }

  function validateItemForWarnings(item) {
    var errors = [];
    if (item.width  <= 0)            errors.push('Item ' + item.reference + ': width not detected');
    if (item.height <= 0)            errors.push('Item ' + item.reference + ': height not detected');
    if (item.frameType === 'Unknown') errors.push('Item ' + item.reference + ': frame type not detected');
    return errors;
  }

  function generateId() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      return crypto.randomUUID();
    }
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
      var r = Math.random() * 16 | 0;
      var v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }

  function createItem(partial) {
    var defaults = {
      id: generateId(),
      reference: '',
      type: 'window',
      description: '',
      width: 0,
      height: 0,
      quantity: 1,
      location: '',
      frameType: 'Unknown',
      glazingSpec: 'Double Glazed - Clear',
      openingType: 'Fixed',
      notes: [],
      confidence: 'low',
      warnings: [],
      unitPrice: 0,
      totalPrice: 0,
      manualOverride: false,
      sourceDocument: '',
      sourcePage: 0,
      textPosition: null,
      extractionMethod: 'pdf.js',
      system: '',
      colour: '',
      hardware: '',
      cillType: '',
      glazingMakeup: '',
      ventilation: '',
      drainage: '',
      actualFrameSize: '',
      escapeWindow: '',
      sillHeight: '',
      headHeight: '',
      uValue: '',
      doorSwing: '',
      fireRating: '',
      doorFrame: '',
      doorGlazing: '',
      ironmongery: '',
      finish: '',
      doorType: ''
    };
    return Object.assign({}, defaults, partial);
  }

  // -----------------------------------------------------------------------
  // Public API
  // -----------------------------------------------------------------------

  return {
    extractItems: extractItems,
    classifyDocument: classifyDocument,
    crossReferenceDocuments: crossReferenceDocuments,
    isLikelyScanned: function (text, pageCount) {
      if (!text || text.trim().length === 0) return true;
      var cleaned = text.replace(/\s+/g, ' ').trim();
      var charsPerPage = pageCount > 0 ? cleaned.length / pageCount : 0;
      return charsPerPage < 100;
    }
  };

})();
