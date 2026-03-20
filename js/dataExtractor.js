/* js/dataExtractor.js — Pattern matching engine for glazing items */

var DataExtractor = (function () {

  var PATTERNS = {
    reference: /\b([WDSCwdsc]\d{2,3})\b/g,
    dimensions: /(\d{3,4})\s*[xX×]\s*(\d{3,4})/g,
    dimWithUnits: /(\d{3,4})\s*(?:mm)?\s*[xX×]\s*(\d{3,4})\s*(?:mm)?/gi,
    quantity: /(?:(?:qty|quantity|nr|no\.?|off|x)\s*[:\-]?\s*(\d+))|(?:\b(\d+)\s*(?:nr|no\.?|off)\b)/gi,
    frameAluminium: /\b(?:aluminium|aluminum|alum|alu)\b/gi,
    framePVCu: /\b(?:pvcu|pvc-u|pvc\.u|upvc|pvc)\b/gi,
    frameTimber: /\b(?:timber|wood|wooden|oak|softwood|hardwood)\b/gi,
    frameSteel: /\b(?:steel|galvanised steel|stainless)\b/gi,
    glazingDouble: /\b(?:double\s*glaz(?:ed|ing)|dgu|dg|double\s*glazing)\b/gi,
    glazingTriple: /\b(?:triple\s*glaz(?:ed|ing)|tgu|tg|triple\s*glazing)\b/gi,
    glazingObscure: /\b(?:obscure|frosted|opaque|satin)\b/gi,
    glazingClear: /\bclear\b/gi,
    openingFixed: /\bfixed\b/gi,
    openingCasement: /\bcasement\b/gi,
    openingTopHung: /\btop[\s\-]?hung\b/gi,
    openingTiltTurn: /\btilt[\s\-]?(?:and[\s\-]?)?turn\b/gi,
    openingSliding: /\b(?:sliding|slide)\b/gi,
    openingPivot: /\bpivot(?:ed|ing)?\b/gi,
    openingBifold: /\bbi[\s\-]?fold\b/gi,
    specialFireRated: /\b(?:fire[\s\-]?rated?|fr\d+|fw\d+|fire[\s\-]?resistant?)\b/gi,
    specialAcoustic: /\b(?:acoustic|sound[\s\-]?proof|noise[\s\-]?reduc)\b/gi,
    specialToughened: /\b(?:toughened|tempered)\b/gi,
    specialLaminated: /\b(?:laminated|lami)\b/gi,
    specialTrickleVent: /\b(?:trickle[\s\-]?vent|ventilator)\b/gi,
    specialRestrictor: /\b(?:restrictor|limiter|stay)\b/gi,
    floorGround: /\b(?:ground[\s\-]?floor|gf)\b/gi,
    floorFirst: /\b(?:first[\s\-]?floor|ff|1st[\s\-]?floor)\b/gi,
    floorSecond: /\b(?:second[\s\-]?floor|sf|2nd[\s\-]?floor)\b/gi,
    floorBasement: /\b(?:basement|lower[\s\-]?ground)\b/gi,
    location: /(?:(?:to|at|in|for)\s+(?:the\s+)?)([\w\s\-]+(?:room|floor|office|kitchen|bedroom|bathroom|hall|living|dining|study|lounge))/gi
  };

  // Classify a document based on its filename so we know how to treat it
  function classifyDocument(docName) {
    var name = (docName || '').toLowerCase();

    // Schedule/BQ keywords take priority — a file named "3847.T12 Window Schedule" is a schedule
    if (/window\s*schedule|door\s*schedule|glazing\s*schedule/.test(name)) return 'schedule';
    if (/\bbq\b|bill\s*of\s*quantities|schedule\s*of\s*works/.test(name)) return 'bq';

    // Admin / legal documents
    if (/warrant|guarantee|collateral|enquiry\s*letter|letter\s*of\s*enquiry/.test(name)) return 'admin';

    // Drawing-number filenames like "3847.C37 ...", "3847.T05 ...", "3847.C05.D ..."
    if (/\d{4}\.[a-z]\d{2}/.test(name)) return 'drawing';

    // Elevation / plan drawings (without the numeric sheet prefix caught above)
    if (/elevation|floor\s*plan|site\s*plan|section|detail/.test(name)) return 'drawing';

    return 'unknown';
  }

  // Return true if this document type should be used for item extraction
  function isScheduleOrBQ(docType) {
    return docType === 'schedule' || docType === 'bq';
  }

  // Return true if this document type should participate in cross-referencing
  function isRelevantForCrossRef(docType) {
    return docType === 'schedule' || docType === 'bq' || docType === 'unknown';
  }

  function extractItems(documents) {
    var allItems = [];
    var allWarnings = [];
    var stats = { docsProcessed: 0, pagesProcessed: 0, itemsFound: 0, warnings: 0 };

    documents.forEach(function (doc) {
      stats.docsProcessed++;
      stats.pagesProcessed += doc.pages.length;
      var docResult = extractFromDocument(doc);
      allItems = allItems.concat(docResult.items);
      allWarnings = allWarnings.concat(docResult.warnings);
    });

    if (documents.length > 1) {
      var crossWarnings = crossReferenceDocuments(documents, allItems);
      allWarnings = allWarnings.concat(crossWarnings);
    }

    allItems = deduplicateItems(allItems);
    stats.itemsFound = allItems.length;
    stats.warnings = allWarnings.length;

    return { items: allItems, warnings: allWarnings, stats: stats };
  }

  function extractFromDocument(doc) {
    var items = [];
    var warnings = [];
    var referenceMap = {};
    var docType = classifyDocument(doc.name);

    doc.pages.forEach(function (page) {
      var pageItems = extractFromText(page.text, doc.name, page.pageNum, docType);
      pageItems.forEach(function (item) {
        var ref = item.reference.toUpperCase();
        if (ref && referenceMap[ref]) {
          var existing = referenceMap[ref];
          if (item.width > 0 && existing.width === 0) { existing.width = item.width; }
          if (item.height > 0 && existing.height === 0) { existing.height = item.height; }
          if (item.quantity > 1 && existing.quantity === 1) { existing.quantity = item.quantity; }
          if (item.location && !existing.location) { existing.location = item.location; }
          mergeNotes(existing, item);
          existing.confidence = scoreConfidence(existing);
        } else {
          if (ref) referenceMap[ref] = item;
          items.push(item);
        }
      });
    });

    items.forEach(function (item) {
      var errs = validateItem(item);
      errs.forEach(function (msg) {
        warnings.push({
          id: generateId(),
          type: 'validation',
          message: msg,
          itemId: item.id,
          severity: 'warning'
        });
      });
    });

    if (items.length === 0) {
      // Only warn about missing items for schedule/BQ documents — drawings and admin are expected to have none
      if (isScheduleOrBQ(docType)) {
        warnings.push({
          id: generateId(),
          type: 'extraction',
          message: 'No glazing items found in "' + doc.name + '". The document may be scanned or use an unrecognised format.',
          itemId: null,
          severity: 'error'
        });
      }
    }

    return { items: items, warnings: warnings };
  }

  function extractFromText(text, sourceName, sourcePage, docType) {
    var items = [];
    if (!text || text.trim().length === 0) return items;

    var refMatches = [];

    var refPattern = /\b([WDSCwdsc]\d{2,3})\b/g;
    var match;

    while ((match = refPattern.exec(text)) !== null) {
      var ref = match[1].toUpperCase();
      var matchIndex = match.index;

      // Reject references that are part of a drawing sheet number pattern like
      // "3847.C37", "3847.T05", "3847.C05.D" — look back 5 characters (exactly
      // enough to capture the "NNNN." prefix that precedes these sheet refs).
      var preceding = text.substring(Math.max(0, matchIndex - 5), matchIndex);
      if (/\d{4}\.$/.test(preceding)) continue;

      refMatches.push({ ref: ref, index: matchIndex });
    }

    if (refMatches.length === 0) {
      // Only attempt to infer items without a reference on schedule/BQ documents.
      // Floor plans, elevation drawings, enquiry letters and admin docs will
      // contain dimension-like numbers that are NOT glazing items.
      if (isScheduleOrBQ(docType)) {
        var inferredItem = tryInferWithoutRef(text, sourceName, sourcePage);
        if (inferredItem) items.push(inferredItem);
      }
      return items;
    }

    refMatches.forEach(function (refMatch, i) {
      var start = refMatch.index;
      var end = i + 1 < refMatches.length ? refMatches[i + 1].index : text.length;
      var context = text.substring(Math.max(0, start - 50), Math.min(text.length, end + 200));

      var item = createItem({
        reference: refMatch.ref,
        type: inferType(refMatch.ref, context),
        sourceDocument: sourceName,
        sourcePage: sourcePage
      });

      var dims = extractDimensions(context);
      if (dims) {
        item.width = dims.width;
        item.height = dims.height;
      }

      item.quantity = extractQuantity(context) || 1;
      item.frameType = extractFrameType(context);
      item.glazingSpec = buildGlazingSpec(context);
      item.openingType = extractOpeningType(context);
      item.location = extractLocation(context);
      item.notes = extractNotes(context);
      item.description = buildDescription(item);
      item.confidence = scoreConfidence(item);

      items.push(item);
    });

    return items;
  }

  function tryInferWithoutRef(text, sourceName, sourcePage) {
    var dims = extractDimensions(text);
    if (!dims) return null;

    return createItem({
      reference: 'X01',
      type: 'other',
      width: dims.width,
      height: dims.height,
      quantity: extractQuantity(text) || 1,
      frameType: extractFrameType(text),
      glazingSpec: buildGlazingSpec(text),
      openingType: extractOpeningType(text),
      location: extractLocation(text),
      notes: extractNotes(text),
      confidence: 'low',
      sourceDocument: sourceName,
      sourcePage: sourcePage
    });
  }

  function extractDimensions(text) {
    var pattern = /(\d{3,4})\s*[xX×]\s*(\d{3,4})/;
    var match = pattern.exec(text);
    if (match) {
      var w = parseInt(match[1], 10);
      var h = parseInt(match[2], 10);
      if (w >= 300 && w <= 9999 && h >= 300 && h <= 9999) {
        return { width: w, height: h };
      }
    }
    return null;
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
        if (qty > 0 && qty < 1000) return qty;
      }
    }
    return 1;
  }

  function extractFrameType(text) {
    if (/\b(?:aluminium|aluminum|alum|alu)\b/i.test(text)) return 'Aluminium';
    if (/\b(?:pvcu|pvc-u|pvc\.u|upvc|pvc)\b/i.test(text)) return 'PVCu';
    if (/\b(?:timber|wood|wooden|oak|softwood|hardwood)\b/i.test(text)) return 'Timber';
    if (/\b(?:steel|galvanised)\b/i.test(text)) return 'Steel';
    return 'Unknown';
  }

  function buildGlazingSpec(text) {
    var parts = [];

    if (/\b(?:triple\s*glaz(?:ed|ing)|tgu|tg)\b/i.test(text)) {
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

    if (/\b(?:laminated|lami)\b/i.test(text)) parts.push('Laminated');
    if (/\b(?:toughened|tempered)\b/i.test(text)) parts.push('Toughened');
    if (/\b(?:fire[\s\-]?rated?|fw\d+|fr\d+)\b/i.test(text)) parts.push('Fire Rated');
    if (/\b(?:acoustic|sound[\s\-]?proof)\b/i.test(text)) parts.push('Acoustic');

    return parts.join(' - ');
  }

  function extractOpeningType(text) {
    if (/\btilt[\s\-]?(?:and[\s\-]?)?turn\b/i.test(text)) return 'Tilt & Turn';
    if (/\btop[\s\-]?hung\b/i.test(text)) return 'Top Hung';
    if (/\bcasement\b/i.test(text)) return 'Casement';
    if (/\b(?:sliding|slider)\b/i.test(text)) return 'Sliding';
    if (/\bpivot\b/i.test(text)) return 'Pivot';
    if (/\bbi[\s\-]?fold\b/i.test(text)) return 'Bi-fold';
    if (/\bfixed\b/i.test(text)) return 'Fixed';
    return 'Fixed';
  }

  function extractLocation(text) {
    var floorPatterns = [
      { pattern: /\b(?:ground[\s\-]?floor|gf)\b/i, label: 'Ground Floor' },
      { pattern: /\b(?:first[\s\-]?floor|ff|1st[\s\-]?floor)\b/i, label: 'First Floor' },
      { pattern: /\b(?:second[\s\-]?floor|sf|2nd[\s\-]?floor)\b/i, label: 'Second Floor' },
      { pattern: /\b(?:third[\s\-]?floor|tf|3rd[\s\-]?floor)\b/i, label: 'Third Floor' },
      { pattern: /\bbasement\b/i, label: 'Basement' }
    ];

    for (var i = 0; i < floorPatterns.length; i++) {
      if (floorPatterns[i].pattern.test(text)) {
        return floorPatterns[i].label;
      }
    }

    var roomMatch = /\b(?:to|at|in|for)\s+(?:the\s+)?([\w]+\s*(?:room|office|kitchen|bedroom|bathroom|hallway|hall|living|dining|study|lounge|lobby|corridor|stair))/i.exec(text);
    if (roomMatch) {
      return roomMatch[1].trim();
    }

    return '';
  }

  function extractNotes(text) {
    var notes = [];
    var notePatterns = [
      { pattern: /\b(?:trickle[\s\-]?vent|ventilator)\b/i, note: 'Trickle vent required' },
      { pattern: /\b(?:restrictor|limiter|stay)\b/i, note: 'Window restrictor required' },
      { pattern: /\b(?:fire[\s\-]?rated?|fw\d+|fr\d+)\b/i, note: 'Fire rated glazing' },
      { pattern: /\b(?:acoustic|sound[\s\-]?proof)\b/i, note: 'Acoustic specification' },
      { pattern: /\b(?:obscure|frosted)\b/i, note: 'Obscure/frosted glass' },
      { pattern: /\blaminated\b/i, note: 'Laminated glass' },
      { pattern: /\btoughened\b/i, note: 'Toughened safety glass' },
      { pattern: /\bhandicapped|accessible|disabled\b/i, note: 'Accessibility requirement' }
    ];
    notePatterns.forEach(function (np) {
      if (np.pattern.test(text)) notes.push(np.note);
    });
    return notes;
  }

  function inferType(ref, context) {
    var upper = ref.toUpperCase();
    if (upper.startsWith('W')) return 'window';
    if (upper.startsWith('D')) return 'door';
    if (upper.startsWith('S')) return 'screen';
    if (upper.startsWith('C')) return 'curtain wall';
    return 'other';
  }

  function buildDescription(item) {
    var parts = [];
    if (item.frameType && item.frameType !== 'Unknown') parts.push(item.frameType);
    var typeLabel = item.type.charAt(0).toUpperCase() + item.type.slice(1);
    parts.push(typeLabel);
    if (item.openingType && item.openingType !== 'Fixed') parts.push(item.openingType);
    if (item.glazingSpec) parts.push(item.glazingSpec);
    return parts.join(' ');
  }

  function scoreConfidence(item) {
    var score = 0;
    if (item.reference && item.reference !== 'X01') score += 2;
    if (item.width > 0) score += 2;
    if (item.height > 0) score += 2;
    if (item.quantity > 0) score += 1;
    if (item.frameType && item.frameType !== 'Unknown') score += 1;
    if (item.location) score += 1;
    if (item.glazingSpec) score += 1;

    if (score >= 8) return 'high';
    if (score >= 5) return 'medium';
    return 'low';
  }

  function mergeNotes(target, source) {
    if (source.notes && source.notes.length > 0) {
      source.notes.forEach(function (n) {
        if (target.notes.indexOf(n) === -1) target.notes.push(n);
      });
    }
  }

  function deduplicateItems(items) {
    var byRef = {};
    items.forEach(function (item) {
      var key = item.reference.toUpperCase();
      if (!byRef[key]) {
        byRef[key] = item;
      } else {
        // Merge: keep the best data from both copies
        var existing = byRef[key];
        if (item.width > 0 && existing.width === 0) existing.width = item.width;
        if (item.height > 0 && existing.height === 0) existing.height = item.height;
        if (item.quantity > 1 && existing.quantity === 1) existing.quantity = item.quantity;
        if (item.location && !existing.location) existing.location = item.location;
        if (item.frameType !== 'Unknown' && existing.frameType === 'Unknown') existing.frameType = item.frameType;
        mergeNotes(existing, item);
        // Re-score confidence based on the merged (improved) data
        existing.confidence = scoreConfidence(existing);
      }
    });
    return Object.keys(byRef).map(function (k) { return byRef[k]; });
  }

  function crossReferenceDocuments(documents, allItems) {
    var warnings = [];
    if (documents.length < 2) return warnings;

    // Only cross-reference between schedule and BQ type documents.
    // Admin, drawing, and unknown documents are excluded to avoid noise warnings.
    var relevantDocs = documents.filter(function (doc) {
      return isRelevantForCrossRef(classifyDocument(doc.name));
    });

    if (relevantDocs.length < 2) return warnings;

    var itemsByDoc = {};
    relevantDocs.forEach(function (doc) {
      itemsByDoc[doc.name] = {};
    });

    allItems.forEach(function (item) {
      if (item.sourceDocument && itemsByDoc[item.sourceDocument]) {
        itemsByDoc[item.sourceDocument][item.reference] = item;
      }
    });

    var docNames = Object.keys(itemsByDoc);
    if (docNames.length < 2) return warnings;

    var allRefs = new Set();
    allItems.forEach(function (i) { if (i.reference) allRefs.add(i.reference); });

    allRefs.forEach(function (ref) {
      var foundIn = docNames.filter(function (d) { return itemsByDoc[d][ref]; });
      if (foundIn.length > 0 && foundIn.length < docNames.length) {
        var missingFrom = docNames.filter(function (d) { return !itemsByDoc[d][ref]; });
        var itemId = null;
        foundIn.forEach(function (d) { if (!itemId) itemId = itemsByDoc[d][ref].id; });
        warnings.push({
          id: generateId(),
          type: 'cross-reference',
          message: 'Item ' + ref + ' found in "' + foundIn.join('", "') + '" but not in "' + missingFrom.join('", "') + '"',
          itemId: itemId,
          severity: 'warning'
        });
      }

      if (foundIn.length >= 2) {
        for (var i = 0; i < foundIn.length - 1; i++) {
          for (var j = i + 1; j < foundIn.length; j++) {
            var itemA = itemsByDoc[foundIn[i]][ref];
            var itemB = itemsByDoc[foundIn[j]][ref];
            if (itemA && itemB) {
              if (itemA.width !== itemB.width || itemA.height !== itemB.height) {
                if (itemA.width > 0 && itemB.width > 0) {
                  warnings.push({
                    id: generateId(),
                    type: 'discrepancy',
                    message: 'Dimension mismatch for ' + ref + ': ' + itemA.width + '×' + itemA.height + 'mm (' + foundIn[i] + ') vs ' + itemB.width + '×' + itemB.height + 'mm (' + foundIn[j] + ')',
                    itemId: itemA.id,
                    severity: 'error'
                  });
                }
              }
              if (itemA.quantity !== itemB.quantity && itemA.quantity > 1 && itemB.quantity > 1) {
                warnings.push({
                  id: generateId(),
                  type: 'discrepancy',
                  message: 'Quantity mismatch for ' + ref + ': qty ' + itemA.quantity + ' (' + foundIn[i] + ') vs qty ' + itemB.quantity + ' (' + foundIn[j] + ')',
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
      sourcePage: 0
    };
    return Object.assign({}, defaults, partial);
  }

  function validateItem(item) {
    var errors = [];
    if (item.width <= 0) errors.push('Item ' + item.reference + ': width not detected');
    if (item.height <= 0) errors.push('Item ' + item.reference + ': height not detected');
    if (item.frameType === 'Unknown') errors.push('Item ' + item.reference + ': frame type not detected');
    return errors;
  }

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
