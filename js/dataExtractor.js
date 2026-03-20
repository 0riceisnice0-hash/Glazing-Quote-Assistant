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
    if (/\bbq\b|bill\s*of\s*quantities|schedule\s*of\s*works/.test(name))
      return { type: 'bq', confidence: 'high', reason: 'Filename contains BQ keyword' };
    if (/warrant|guarantee|collateral|enquiry\s*letter|letter\s*of\s*enquiry/.test(name))
      return { type: 'admin', confidence: 'high', reason: 'Filename matches admin/legal document pattern' };
    // Drawing-number filenames like "3847.C37 …", "3847.T05 …"
    // IMPORTANT: Only classify as 'drawing' when no schedule/BQ keywords are also present.
    // A filename like "3847.T12 Window Schedule.pdf" contains both a drawing number AND schedule
    // keywords — the schedule checks above already return early, but this guard makes the intent
    // explicit and prevents any future regression.
    if (/\d{4}\.[a-z]\d{2}/.test(name) &&
        !/window\s*schedule|door\s*schedule|glazing\s*schedule/.test(name) &&
        !/\bbq\b|bill\s*of\s*quantities/.test(name))
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
    location:    ['location', 'position', 'floor', 'room', 'level', 'area'],
    description: ['description', 'notes', 'specification', 'note', 'remarks', 'comments']
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
      for (var fi = 0; fi < fields.length; fi++) {
        var field = fields[fi];
        if (columns[field]) continue; // already mapped
        var keywords = HEADER_COLUMN_KEYWORDS[field];
        var matched = keywords.some(function (kw) {
          return text === kw || text.indexOf(kw) !== -1;
        });
        if (matched) {
          columns[field] = { x: item.x, label: item.str };
          break;
        }
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
    if (REF_PATTERN.test(s)) return s.toUpperCase();
    return null;
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

      var refItem = row.items[refItemIdx];
      item.textPosition = { x: refItem.x, y: refItem.y, width: refItem.width || 30, height: refItem.height || 12 };

      item.confidence = scoreConfidence(item, 'row');
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
    var normText = text.replace(/\b([A-Z]{1,2}[WDSC])\s+(\d{2,4})\b/gi, '$1$2');

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
      if (/\d{4,}\.\s*[A-Z]\d*\s*$/.test(preceding)) continue;

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

    // Track best items per ref per doc-type for smart merging
    var scheduleItems = {};
    var bqItems       = {};

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

      if (docResult.items.length > 0) {
        debugLog.push('  → Found ' + docResult.items.length + ' item(s): ' +
          docResult.items.slice(0, 10).map(function (i) { return i.reference; }).join(', ') +
          (docResult.items.length > 10 ? ' …' : ''));
      } else if (docType !== 'admin' && docType !== 'drawing') {
        debugLog.push('  → No items extracted');
      } else {
        debugLog.push('  → Skipped (document type: ' + docType + ')');
      }

      docResult.items.forEach(function (item) {
        var key = item.reference.toUpperCase();
        if (docType === 'schedule' && !scheduleItems[key]) {
          scheduleItems[key] = item;
        } else if (docType === 'bq' && !bqItems[key]) {
          bqItems[key] = item;
        }
      });
    });

    // Smart merge: schedule dims override BQ dims; BQ qty preferred
    var mergeWarnings = smartMerge(scheduleItems, bqItems, allItems);
    allWarnings = allWarnings.concat(mergeWarnings);

    // Cross-reference warnings between schedule and BQ only
    if (documents.length > 1) {
      var crossWarnings = crossReferenceDocuments(documents, allItems);
      allWarnings = allWarnings.concat(crossWarnings);
    }

    // Cross-validate drawing refs against schedule items — group by prefix to avoid
    // generating one warning per reference (which can easily reach 140+ for a large project).
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
        if (!/\d{4,}\.\s*[A-Z]\d*\s*$/.test(preceding)) {
          refs[ref] = true;
        }
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

    var items       = [];
    var warnings    = [];
    var referenceMap = {};

    doc.pages.forEach(function (page) {
      var pageItems = extractFromPage(page, doc.name, docType);
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

    // Validation warnings for incomplete items
    items.forEach(function (item) {
      validateItemForWarnings(item).forEach(function (msg) {
        warnings.push({ id: generateId(), type: 'validation', message: msg, itemId: item.id, severity: 'warning' });
      });
    });

    // Warn about items that were inferred without a proper reference (X01 fallback).
    // These have even lower confidence and must be verified by the user.
    items.filter(function (item) { return item.reference === 'X01'; }).forEach(function (item) {
      warnings.push({
        id: generateId(),
        type: 'inference',
        message: 'An item was inferred from "' + doc.name + '" (page ' + item.sourcePage + ') without a ' +
                 'recognisable reference — dimensions: ' + item.width + '\u00d7' + item.height + 'mm. ' +
                 'Please verify this is a real glazing item and update the reference.',
        itemId: item.id,
        severity: 'warning'
      });
    });

    // Only warn about missing items in schedule/BQ docs
    if (items.length === 0 && isScheduleOrBQ(docType)) {
      // Determine if the document has any text at all (to give a better message)
      var hasText = doc.pages.some(function (p) { return p.text && p.text.trim().length > 50; });
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
      if (tableItems.length > 0) return tableItems;

      // Strategy 2: Row-based reference pattern
      var rowItems = tryRowBasedExtraction(rows, sourceName, page.pageNum, docType);
      if (rowItems.length > 0) return rowItems;
    }

    // Strategy 3: Enhanced regex with spatial context
    var regexItems = tryEnhancedRegex(textItems, text, sourceName, page.pageNum);
    if (regexItems.length > 0) return regexItems;

    // Strategy 4: Line-based text fallback — split on newlines and process each line.
    // This handles PDFs where position data is absent or unreliable but the text layer
    // is clean enough to produce one item per line.
    var lineItems = tryLineBasedExtraction(text, sourceName, page.pageNum);
    if (lineItems.length > 0) return lineItems;

    // Strategy 5: Infer an item without a reference (schedule/BQ docs only)
    if (isScheduleOrBQ(docType)) {
      var inferred = tryInferWithoutRef(text, sourceName, page.pageNum);
      if (inferred) return [inferred];
    }

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
      if (/\d{4,}\.\s*[A-Z]\d*\s*$/.test(pre)) return;
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
    return 'Unknown';
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

  function extractLocation(text) {
    if (!text) return '';
    var floorPatterns = [
      { pattern: /\b(?:ground[\s\-]?floor|gf)\b/i,           label: 'Ground Floor' },
      { pattern: /\b(?:first[\s\-]?floor|ff|1st[\s\-]?floor)\b/i, label: 'First Floor' },
      { pattern: /\b(?:second[\s\-]?floor|sf|2nd[\s\-]?floor)\b/i, label: 'Second Floor' },
      { pattern: /\b(?:third[\s\-]?floor|tf|3rd[\s\-]?floor)\b/i,  label: 'Third Floor' },
      { pattern: /\bbasement\b/i,                             label: 'Basement' }
    ];
    for (var i = 0; i < floorPatterns.length; i++) {
      if (floorPatterns[i].pattern.test(text)) return floorPatterns[i].label;
    }
    var roomMatch = /\b(?:to|at|in|for)\s+(?:the\s+)?([\w]+\s*(?:room|office|kitchen|bedroom|bathroom|hallway|hall|living|dining|study|lounge|lobby|corridor|stair))/i.exec(text);
    if (roomMatch) return roomMatch[1].trim();
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
    if (strategy === 'table')  score += 1.5;
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
      extractionMethod: 'pdf.js'
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
