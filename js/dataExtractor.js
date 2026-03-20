/* js/dataExtractor.js — Spatial extraction engine for glazing items */

var DataExtractor = (function () {

  // -----------------------------------------------------------------------
  // Document classification
  // -----------------------------------------------------------------------

  function classifyDocument(docName) {
    var name = (docName || '').toLowerCase();

    // Schedule/BQ keywords take priority
    if (/window\s*schedule|door\s*schedule|glazing\s*schedule/.test(name)) return 'schedule';
    if (/\bbq\b|bill\s*of\s*quantities|schedule\s*of\s*works/.test(name)) return 'bq';

    // Admin / legal documents — skip entirely
    if (/warrant|guarantee|collateral|enquiry\s*letter|letter\s*of\s*enquiry/.test(name)) return 'admin';

    // Drawing-number filenames like "3847.C37 …", "3847.T05 …", "3847.C05.D …", "3847.T12 …"
    if (/\d{4}\.[a-z]\d{2}/.test(name)) return 'drawing';

    // Generic drawing / plan types (without the numeric sheet prefix caught above)
    if (/\b(?:elevation|floor\s*plan|site\s*plan|section|detail|proposed|cladding)\b/.test(name)) return 'drawing';

    // Specification documents
    if (/\b(?:spec(?:ification)?)\b/.test(name)) return 'specification';

    return 'unknown';
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

  // Group text items into rows by Y coordinate.
  // In PDF space the origin (0,0) is bottom-left, so higher Y = higher on page.
  function buildRows(textItems, yTolerance) {
    if (!textItems || textItems.length === 0) return [];
    yTolerance = yTolerance || 4;

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
    ref:         ['ref', 'reference', 'mark', 'item no', 'item', 'schedule ref', 'window ref', 'door ref', 'glazing ref', 'nr.', 'no.'],
    width:       ['width', 'w (mm)', 'w(mm)', 'wd', 'w'],
    height:      ['height', 'h (mm)', 'h(mm)', 'ht', 'h'],
    size:        ['size', 'overall size', 'dimensions', 'dim', 'opening size'],
    qty:         ['qty', 'quantity', 'no', 'nr', 'number', 'nos'],
    frame:       ['frame', 'frame type', 'material', 'profile', 'system', 'construction'],
    glazing:     ['glazing', 'glass', 'infill', 'glazing spec', 'glazing type'],
    opening:     ['opening', 'function', 'operation', 'open'],
    location:    ['location', 'position', 'floor', 'room', 'level', 'area'],
    description: ['description', 'notes', 'specification', 'note', 'remarks', 'comments']
  };

  // Return the index of the first row that looks like a table header (≥2 field matches)
  function findHeaderRow(rows) {
    for (var i = 0; i < Math.min(rows.length, 20); i++) {
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
    colTolerance = colTolerance || 70;
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

  var REF_PATTERN = /^([WDSCwdsc]\d{2,3})$/;

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

      var refText = getCellText(row.items, columns.ref.x).toUpperCase();
      if (!REF_PATTERN.test(refText)) continue;

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

  function tryRowBasedExtraction(rows, sourceName, sourcePage) {
    var items = [];
    var refRows = [];

    // Find rows whose first (leftmost) non-empty item is a glazing reference
    rows.forEach(function (row) {
      if (!row.items || row.items.length < 2) return;
      var firstText = row.items[0].str.trim().toUpperCase();
      if (REF_PATTERN.test(firstText)) {
        refRows.push({ row: row, ref: firstText });
      }
    });

    // Need at least 2 consistent reference rows to be confident this is a real table
    if (refRows.length < 2) return items;

    refRows.forEach(function (refRow) {
      var row = refRow.row;
      var ref = refRow.ref;

      var item = createItem({
        reference: ref,
        type: inferType(ref),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });

      // Find dimensions: collect numbers ≥100mm from subsequent cells
      var numbers = row.items.slice(1).map(function (it) {
        return { str: it.str, x: it.x, val: parseInt(it.str.trim(), 10) };
      }).filter(function (n) { return !isNaN(n.val); });

      // Dimensions are the largest plausible numbers (100–9000mm)
      var dimNums = numbers.filter(function (n) { return n.val >= 100 && n.val <= 9000; });
      if (dimNums.length >= 2) {
        // Assume left number is width, next is height
        item.width = dimNums[0].val;
        item.height = dimNums[1].val;
      }

      // If no separate W/H, try inline "WxH" pattern
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

      var refItem = row.items[0];
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

    var refPattern = /\b([WDSCwdsc]\d{2,3})\b/g;
    var match;

    while ((match = refPattern.exec(text)) !== null) {
      var ref = match[1].toUpperCase();
      var matchIndex = match.index;

      // Reject references preceded by drawing-number patterns like "3847.C37" or "3847. C37"
      var preceding = text.substring(Math.max(0, matchIndex - 8), matchIndex);
      if (/\d{4}\.\s*$/.test(preceding)) continue;

      // Also reject if it looks like a file-name prefix inside the text body
      var preceding12 = text.substring(Math.max(0, matchIndex - 12), matchIndex);
      if (/\d{4,}\.\s*[A-Z]?\s*$/.test(preceding12)) continue;

      // Find the text item that contains this reference
      var refItem = null;
      if (textItems && textItems.length > 0) {
        for (var k = 0; k < textItems.length; k++) {
          var ti = textItems[k];
          if (ti.str && (ti.str.trim().toUpperCase() === ref || ti.str.toUpperCase().indexOf(ref) !== -1)) {
            refItem = ti;
            break;
          }
        }
      }

      // Build spatial or character context
      var context;
      var dimContext; // forward-only context used for dimension extraction to avoid overlap with prior items
      if (refItem && textItems && textItems.length > 0) {
        // Same row (±10pt vertical) within 400pt horizontal
        var nearby = textItems.filter(function (it) {
          return Math.abs(it.y - refItem.y) <= 10 &&
                 Math.abs(it.x - refItem.x) <= 400 &&
                 it.str && it.str.trim().length > 0;
        });
        nearby.sort(function (a, b) { return a.x - b.x; });
        context = nearby.map(function (it) { return it.str; }).join(' ');
        dimContext = context;
      } else {
        // Full context for attribute extraction (frame type, location, notes)
        context = text.substring(Math.max(0, matchIndex - 50), Math.min(text.length, matchIndex + 300));
        // Forward-only context for dimensions to avoid grabbing the previous item's data
        dimContext = text.substring(matchIndex, Math.min(text.length, matchIndex + 250));
      }

      var item = createItem({
        reference: ref,
        type: inferType(ref),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });

      var dims = extractDimensionsFromText(dimContext);
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
    var stats       = { docsProcessed: 0, pagesProcessed: 0, itemsFound: 0, warnings: 0 };

    // Track best items per ref per doc-type for smart merging
    var scheduleItems = {};
    var bqItems       = {};

    documents.forEach(function (doc) {
      stats.docsProcessed++;
      stats.pagesProcessed += doc.pages.length;

      var docResult = extractFromDocument(doc);
      allItems    = allItems.concat(docResult.items);
      allWarnings = allWarnings.concat(docResult.warnings);

      var docType = classifyDocument(doc.name);
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

    allItems = deduplicateItems(allItems);
    stats.itemsFound = allItems.length;
    stats.warnings   = allWarnings.length;

    return { items: allItems, warnings: allWarnings, stats: stats };
  }

  function extractFromDocument(doc) {
    var docType = classifyDocument(doc.name);

    // Admin documents contain no glazing data — skip entirely to avoid false positives
    if (docType === 'admin') return { items: [], warnings: [] };

    // Architectural drawings — skip item extraction (references in title blocks cause false positives)
    if (docType === 'drawing') return { items: [], warnings: [] };

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

    // Only warn about missing items in schedule/BQ docs
    if (items.length === 0 && isScheduleOrBQ(docType)) {
      warnings.push({
        id: generateId(),
        type: 'extraction',
        message: 'No glazing items found in "' + doc.name + '". The document may be scanned or use an unrecognised format.',
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

      // Strategy 1: Structured table with header row
      var tableItems = tryTableExtraction(rows, sourceName, page.pageNum);
      if (tableItems.length > 0) return tableItems;

      // Strategy 2: Row-based reference pattern
      var rowItems = tryRowBasedExtraction(rows, sourceName, page.pageNum);
      if (rowItems.length > 0) return rowItems;
    }

    // Strategy 3: Enhanced regex with spatial context
    var regexItems = tryEnhancedRegex(textItems, text, sourceName, page.pageNum);
    if (regexItems.length > 0) return regexItems;

    // Strategy 4: Infer an item without a reference (schedule/BQ docs only)
    if (isScheduleOrBQ(docType)) {
      var inferred = tryInferWithoutRef(text, sourceName, page.pageNum);
      if (inferred) return [inferred];
    }

    return [];
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
    var pattern = /(\d{3,4})\s*[xX×]\s*(\d{3,4})/;
    var match = pattern.exec(text);
    if (match) {
      var w = parseInt(match[1], 10);
      var h = parseInt(match[2], 10);
      if (w >= 100 && w <= 9000 && h >= 100 && h <= 9000) {
        return { width: w, height: h };
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
    var ch = (ref || '').toUpperCase().charAt(0);
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
      return isRelevantForCrossRef(classifyDocument(doc.name));
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
      textPosition: null
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
