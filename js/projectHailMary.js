/* js/projectHailMary.js - commercial estimator review workflow */

var ProjectHailMary = (function () {
  var REQUIREMENT_RULES = [
    { key: 'projectName', label: 'Project name', pattern: /\b(?:project|customer\s+ref)\s*:?\s*([^\n\r]+)/i },
    { key: 'client', label: 'Client / main contractor', pattern: /\b(?:client|main\s+contractor|contractor)\s*:?\s*([^\n\r]+)/i },
    { key: 'siteAddress', label: 'Site address', pattern: /\b(?:site\s+address|address)\s*:?\s*([^\n\r]+)/i },
    { key: 'colour', label: 'Finish / colour', pattern: /\b(?:colour|color|ext\s+colour)\s*:?\s*([^\n\r]+)/i },
    { key: 'uValue', label: 'U-value / Part L', pattern: /\bu[\s-]*value\s*:?\s*([0-9.]+\s*w\/?m2?k?)/i },
    { key: 'gValue', label: 'G-value / solar control', pattern: /\bg[\s-]*value\s*:?\s*([0-9.]+)/i },
    { key: 'ltValue', label: 'LT-value / light transmission', pattern: /\blt[\s-]*value\s*:?\s*([0-9.]+%?)/i },
    { key: 'aluminium', label: 'Aluminium windows/doors', pattern: /\bppc\s+aluminium|aluminium\s+framed|aluminum\s+framed/i },
    { key: 'upvc', label: 'uPVC windows/doors', pattern: /\bupvc|u-pvc|pvc-u/i },
    { key: 'curtainWalling', label: 'Curtain walling', pattern: /\bcurtain\s+wall|kawneer\s+aa100/i },
    { key: 'secondaryGlazing', label: 'Secondary glazing', pattern: /\bsecondary\s+glazing/i },
    { key: 'windowFilm', label: 'Window film', pattern: /\bwindow\s+film|manifestation/i },
    { key: 'louvres', label: 'Louvres', pattern: /\blouv?re|louvre\s+panel/i },
    { key: 'roofLanterns', label: 'Roof lanterns / rooflights', pattern: /\broof\s*(?:lantern|light)|skylight/i },
    { key: 'bifoldsSliding', label: 'Bifolds / sliding doors', pattern: /\bbifold|bi-fold|sliding\s+door/i },
    { key: 'rollerShutters', label: 'Roller shutters', pattern: /\broller\s+shutter/i },
    { key: 'pas24', label: 'PAS24 / security', pattern: /\bpas\s*24|secured\s+by\s+design|sbd\b/i },
    { key: 'trickleVents', label: 'Trickle vents / ventilation', pattern: /\btrickle\s+vent|linkvent|ventilation/i },
    { key: 'restrictors', label: 'Restrictors', pattern: /\brestrictor/i },
    { key: 'ddaThresholds', label: 'DDA / accessibility thresholds', pattern: /\bdda|accessible\s+threshold|part\s+m/i },
    { key: 'fireRating', label: 'Fire rating', pattern: /\bfd\s*30|fd\s*60|fire\s+rated|fire\s+door/i },
    { key: 'acoustic', label: 'Acoustic', pattern: /\bacoustic|db\b/i },
    { key: 'safetyGlazing', label: 'Safety glazing', pattern: /\bsafety\s+glazing|bs\s*en\s*12600|toughened|laminated/i },
    { key: 'accessControl', label: 'Access control / automation', pattern: /\baccess\s+control|automatic|actuator|teleflex|powered/i },
    { key: 'removalDisposal', label: 'Removal and disposal', pattern: /\bremov(?:al|e)\b|\bdisposal\b|strip\s+out/i },
    { key: 'makingGood', label: 'Making good / builders work', pattern: /\bmaking\s+good|builder'?s?\s+work|builders\s+work/i },
    { key: 'accessScaffold', label: 'Access / scaffold', pattern: /\bscaffold|access\s+equipment|hoist|cranage|cherry\s+picker/i },
    { key: 'programme', label: 'Programme / lead time', pattern: /\bprogramme|lead\s*time|completion\s+date|deadline|return\s+quote\s+by/i }
  ];

  var RED_FLAG_RULES = [
    { key: 'fireRating', label: 'Fire-rated glazing mentioned but not allocated clearly', severity: 'critical', query: 'Please confirm which items require fire-rated glazing and the required rating.' },
    { key: 'acoustic', label: 'Acoustic glazing mentioned; confirm dB rating and affected units', severity: 'warning', query: 'Please confirm acoustic performance requirements and which items they apply to.' },
    { key: 'pas24', label: 'PAS24 / Secured by Design requirement needs supplier confirmation', severity: 'critical', query: 'Please confirm PAS24/SBD compliance in the supplier quote or specification.' },
    { key: 'uValue', label: 'Low U-value / Part L requirement needs whole-unit confirmation', severity: 'warning', query: 'Please confirm whole-unit U-value compliance for the proposed systems.' },
    { key: 'gValue', label: 'G-value requirement must be passed to glass supplier', severity: 'warning', query: 'Please confirm required G-value and glass specification.' },
    { key: 'ltValue', label: 'LT-value requirement must be passed to glass supplier', severity: 'warning', query: 'Please confirm required LT-value and glass specification.' },
    { key: 'colour', label: 'Colour / finish must be confirmed before issue', severity: 'warning', query: 'Please confirm the required RAL colour and finish.' },
    { key: 'trickleVents', label: 'Trickle vents / ventilation requirement needs item-level confirmation', severity: 'warning', query: 'Please confirm whether trickle vents are required and to which items.' },
    { key: 'restrictors', label: 'Restrictors requirement needs item-level confirmation', severity: 'warning', query: 'Please confirm whether restrictors are required and to which windows.' },
    { key: 'ddaThresholds', label: 'DDA / accessibility threshold requirement needs door review', severity: 'warning', query: 'Please confirm threshold/accessibility requirements for door items.' },
    { key: 'accessControl', label: 'Automation/access control interface responsibility unclear', severity: 'critical', query: 'Please confirm access control, automation, wiring and interface responsibilities.' },
    { key: 'makingGood', label: 'Making good / builders work responsibility must be explicit', severity: 'warning', query: 'Please confirm whether making good/builders work is included or excluded.' },
    { key: 'accessScaffold', label: 'Access/scaffold responsibility must be explicit', severity: 'warning', query: 'Please confirm whether access equipment/scaffold is provided by others.' },
    { key: 'curtainWalling', label: 'Curtain walling must be treated separately from standard window/door codes', severity: 'critical', query: 'Please confirm curtain wall scope, system, loads and supplier pricing.' }
  ];

  var STANDARD_EXCLUSIONS = [
    'Builders work, making good, decoration and builder-prepared openings are excluded unless specifically included.',
    'Final site survey is required before manufacture.',
    'Structural calculations, planning and building-control approvals are excluded unless specifically stated.',
    'Electrical wiring, containment, access-control interfaces and fire-alarm interfaces are by others unless included.',
    'Access equipment, scaffolding, cranage, hoists and traffic management are excluded unless included as a priced allowance.',
    'Fire stopping and perimeter fire barriers are excluded unless specifically stated.',
    'Lead times are subject to design approval, supplier confirmation and order acceptance.'
  ];

  function buildReview(state, documents) {
    state = state || {};
    documents = documents || [];
    var requirements = extractRequirements(documents);
    var supplierQuotes = extractSupplierQuotes(documents);
    var supplierItems = flattenSupplierItems(supplierQuotes);
    var sourceItems = supplierItems.length >= ((state.items && state.items.length) || 0) ? supplierItems : (state.items || []);
    var codingChecks = buildCodingChecks(sourceItems);
    var comparison = compareTenderAndSupplier(requirements, supplierQuotes, supplierItems, sourceItems);
    var assumptions = buildAssumptions(requirements, supplierQuotes);
    var exclusions = buildExclusions(requirements, comparison);
    var redFlags = buildRedFlags(requirements, supplierQuotes, documents);
    var riskRegister = buildRiskRegister(requirements, comparison, redFlags, documents, sourceItems);
    var rfis = buildRfis(requirements, comparison, redFlags);
    var readiness = determineReadiness(comparison, rfis, sourceItems, riskRegister);
    var summary = buildSummary(state, supplierQuotes, codingChecks);
    var specExtraction = buildSpecificationExtraction(requirements, redFlags);
    var itemList = buildScheduleItemList(sourceItems);
    var pricingReview = buildPricingReview(requirements, supplierQuotes, supplierItems, codingChecks, comparison);
    var preIssueChecklist = buildPreIssueChecklist(requirements, supplierQuotes, sourceItems, codingChecks, comparison, riskRegister);

    return {
      generatedAt: new Date().toISOString(),
      status: readiness.status,
      statusLabel: readiness.label,
      summary: summary,
      documentsReviewed: documents.map(function (doc) {
        return {
          name: doc.name,
          kind: doc.kind || '',
          role: doc.role || '',
          classification: doc.classification || null,
          textChars: (doc.fullText || '').length
        };
      }),
      tenderRequirements: requirements,
      specificationExtraction: specExtraction,
      drawingScheduleItemList: itemList,
      supplierQuotes: supplierQuotes,
      supplierItems: supplierItems,
      supplierQuoteComparison: pricingReview,
      codingChecks: codingChecks,
      scopeComparison: comparison,
      assumptions: assumptions,
      exclusions: exclusions,
      rfis: rfis,
      redFlags: redFlags,
      riskRegister: riskRegister,
      preIssueChecklist: preIssueChecklist,
      proposalDraft: buildProposalDraft(state, requirements, supplierQuotes, assumptions, exclusions, rfis),
      pricingDocumentDraft: buildPricingDraft(state, codingChecks, supplierQuotes, assumptions, exclusions, rfis),
      markdown: ''
    };
  }

  function finaliseReview(review) {
    review.markdown = toMarkdown(review);
    return review;
  }

  function extractRequirements(documents) {
    var found = [];
    documents.forEach(function (doc) {
      var text = normaliseText(doc.fullText || '');
      if (!text) return;
      if (isTrainingMaterialDoc(doc, text)) return;
      REQUIREMENT_RULES.forEach(function (rule) {
        var match = text.match(rule.pattern);
        if (!match) return;
        var value = match[1] ? cleanValue(match[1]) : 'Mentioned';
        pushUnique(found, {
          key: rule.key,
          label: rule.label,
          value: value,
          sourceDocument: doc.name,
          confidence: match[1] ? 'medium' : 'low'
        }, function (a, b) {
          return a.key === b.key && a.value === b.value && a.sourceDocument === b.sourceDocument;
        });
      });
    });
    return found;
  }

  function extractSupplierQuotes(documents) {
    var quotes = [];
    documents.forEach(function (doc) {
      var text = normaliseText(doc.fullText || '');
      var name = doc.name || '';
      if (isTrainingMaterialDoc(doc, text)) return;
      var looksSupplier = /\bquotation\b|quote\s+number|total\s+nett|grand\s+total\s+net|bellview|sheerline|bsw/i.test(text + ' ' + name);
      if (!looksSupplier) return;
      var supplierHint = text + ' ' + name;
      var supplier = /sheerline|bsw|QT\d+/i.test(supplierHint) ? 'BSW / Sheerline' :
        (/bellview/i.test(supplierHint) ? 'Bellview Products' : 'Supplier');
      var quoteNumber = firstMatch(text, /\bquote(?:ation)?\s*(?:number|no\.?)\s*:?\s*([A-Z0-9-]+)/i) || firstMatch(text, /\bQuotation No\.?\s*:?\s*([A-Z0-9-]+)/i) || '';
      var project = firstMatch(text, /\b(?:project|customer\s+ref)\s*:?\s*([^\n\r]+)/i) || '';
      var exVat = moneyAfterLabel(text, /Total\s+Nett\s+Ex\.?\s*VAT/i);
      if (!exVat) exVat = moneyAfterLabel(text, /Grand\s+Total\s+Net/i);
      var vat = moneyAfterLabel(text, /VAT\s*@?\s*20|Value\s+Added\s+Tax\s+20/i);
      var incVat = moneyAfterLabel(text, /TOTAL\s+INC\.?\s+VAT|Total\s+price/i);
      var items = extractSupplierItems(text, name, supplier);
      var extrasTotal = moneyMatch(text, /\bTotal\s+Extras\s+Value[\s\S]{0,25}?([0-9,]+\.\d{2})/i);
      var itemTotalFallback = round2(items.reduce(function (sum, item) { return sum + (item.supplierTotal || 0); }, 0) + extrasTotal);
      if (items.length && (!exVat || itemTotalFallback > exVat * 2)) {
        exVat = itemTotalFallback;
      }
      quotes.push({
        sourceDocument: name,
        supplier: supplier,
        quoteNumber: quoteNumber,
        project: cleanValue(project),
        exVatTotal: round2(exVat),
        vatAmount: round2(vat),
        incVatTotal: round2(incVat),
        items: items,
        notes: extractSupplierNotes(text),
        flags: extractCoverageFlags(text)
      });
    });
    return quotes;
  }

  function extractSupplierItems(text, sourceDocument, supplier) {
    var items = [];
    var sheerlineRe = /Dimensions:\s*Overall\s+Size:\s*([0-9,]+)\s*x\s*([0-9,]+)[\s\S]{0,180}?Qty:\s*([0-9]+)\s*([A-Za-z ]+?)\s+Location:\s*([A-Z0-9\s-]+|Item\s+\d+)\s*£\s*([0-9,]+\.\d{2})/gi;
    var match;
    while ((match = sheerlineRe.exec(text))) {
      var desc = cleanValue(match[4]);
      var ref = cleanValue(match[5]).replace(/\s+-\s+/g, '-').replace(/\s+/g, ' ');
      items.push(makeSupplierItem({
        sourceDocument: sourceDocument,
        supplier: supplier,
        reference: ref,
        description: desc,
        type: /door/i.test(desc) ? 'door' : 'window',
        width: parseNum(match[1]),
        height: parseNum(match[2]),
        quantity: parseNum(match[3]) || 1,
        supplierTotal: parseMoney(match[6])
      }));
    }

    var bellviewRe = /^\s*\d{3}\s+([0-9]+)\s+Pcs\s+([0-9,]+)\s*x\s*([0-9,]+)\s*mm\s+(.+?)\s+([0-9,]+\.\d{2})\s+([0-9,]+\.\d{2})\s*$/gmi;
    while ((match = bellviewRe.exec(text))) {
      var bellDesc = cleanValue(match[4]);
      items.push(makeSupplierItem({
        sourceDocument: sourceDocument,
        supplier: supplier,
        reference: firstMatch(bellDesc, /\b(?:type|EXT)\s*[- ]?([A-Z0-9]+)/i) || 'Supplier item',
        description: bellDesc,
        type: /door/i.test(bellDesc) ? 'door' : 'window',
        width: parseNum(match[2]),
        height: parseNum(match[3]),
        quantity: parseNum(match[1]) || 1,
        supplierUnit: parseMoney(match[5]),
        supplierTotal: parseMoney(match[6])
      }));
    }
    return items;
  }

  function makeSupplierItem(input) {
    input.frameType = /pvc|upvc/i.test(input.description || '') ? 'uPVC' : 'Aluminium';
    input.productCode = classifyCode(input);
    input.labourAllowance = getLabour(input.productCode);
    input.labourTotal = round2((input.quantity || 1) * input.labourAllowance);
    input.totalWithLabour = round2((input.supplierTotal || 0) + input.labourTotal);
    input.reason = reasonForCode(input);
    input.risk = codeRisk(input);
    return input;
  }

  function flattenSupplierItems(quotes) {
    var out = [];
    (quotes || []).forEach(function (q) {
      (q.items || []).forEach(function (item) { out.push(item); });
    });
    return out;
  }

  function buildCodingChecks(items) {
    return (items || []).map(function (item) {
      var code = item.productCode || classifyCode(item);
      var qty = item.quantity || 1;
      var labour = getLabour(code);
      var supplierTotal = item.supplierTotal || item.totalPrice || 0;
      return {
        reference: item.reference || '',
        description: item.description || item.openingType || item.type || '',
        material: item.frameType || 'Unknown',
        quantity: qty,
        selectedCode: code,
        labourAllowance: labour,
        labourTotal: round2(qty * labour),
        reason: reasonForCode(item),
        queryOrRisk: codeRisk(item),
        supplierTotal: round2(supplierTotal),
        sourceDocument: item.sourceDocument || ''
      };
    });
  }

  function compareTenderAndSupplier(requirements, quotes, supplierItems, sourceItems) {
    var reqText = requirements.map(function (r) { return r.key + ' ' + r.value; }).join(' ').toLowerCase();
    var supplierText = JSON.stringify(quotes || []).toLowerCase();
    var supplierFlags = mergeCoverageFlags(quotes || []);
    var gaps = [];
    var confirmations = [];

    checkCoverage('colour', 'Black / PPC colour requirement', /black|9005|jet\s+black/.test(reqText), supplierFlags.black || /black|9005|jet\s+black|bl\b/.test(supplierText), gaps, confirmations);
    checkCoverage('uValue', 'U-value requirement', /uvalue|u-value|w\/m/i.test(reqText), supplierFlags.uValue || /uvalue|u-value|ecoplus|1\.0|1\.4/i.test(supplierText), gaps, confirmations);
    checkCoverage('louvres', 'Louvre panels / louvred doors', /louvre|louver/.test(reqText), supplierFlags.louvres || /louvre|louver/.test(supplierText), gaps, confirmations);
    checkCoverage('rollerShutters', 'Roller shutter doors', /roller\s+shutter/.test(reqText), supplierFlags.rollerShutters || /roller\s+shutter/.test(supplierText), gaps, confirmations);
    checkCoverage('pas24', 'PAS24 / SBD', /pas\s*24|secured\s+by\s+design|sbd/.test(reqText), supplierFlags.pas24 || /pas\s*24|secured\s+by\s+design|sbd/.test(supplierText), gaps, confirmations);
    checkCoverage('restrictors', 'Window restrictors', /restrictor/.test(reqText), supplierFlags.restrictors || /restrictor/.test(supplierText), gaps, confirmations);
    checkCoverage('trickleVents', 'Trickle vents / ventilation', /trickle|ventilation|linkvent/.test(reqText), supplierFlags.ventilation || /trickle|linkvent|ventilation/.test(supplierText), gaps, confirmations);

    if (!quotes.length) {
      gaps.push(makeGap('supplierQuotes', 'No supplier quotes detected', 'critical', 'Upload supplier quotations or enter supplier costs manually.'));
    }
    if (!sourceItems.length && !supplierItems.length) {
      gaps.push(makeGap('scopeItems', 'No priced scope or supplier item lines detected', 'critical', 'Review schedules, run OCR/takeoff, or add items manually.'));
    }

    return { gaps: gaps, confirmations: confirmations };
  }

  function checkCoverage(key, label, required, covered, gaps, confirmations) {
    if (required && covered) confirmations.push({ key: key, message: label + ' appears covered by supplier evidence.' });
    if (required && !covered) gaps.push(makeGap(key, label + ' appears in tender but not in supplier evidence.', key === 'rollerShutters' ? 'critical' : 'warning', 'Confirm with supplier or carry as exclusion/RFI.'));
  }

  function makeGap(key, message, severity, suggestedAction) {
    return { key: key, message: message, severity: severity || 'warning', suggestedAction: suggestedAction || '' };
  }

  function buildAssumptions(requirements, supplierQuotes) {
    var out = [];
    var hasBlack = hasReq(requirements, 'colour', /black|9005/i) || JSON.stringify(supplierQuotes).match(/9005|black/i);
    if (hasBlack) out.push('Finish assumed as PPC black / RAL 9005 where stated in tender or supplier quote.');
    if (supplierQuotes.length) out.push('Supplier quotation rates are used as cost evidence and mapped back to tender scope where possible.');
    out.push('All dimensions and quantities are subject to final site survey and supplier/manufacturer confirmation.');
    out.push('Where references differ between architect schedules and supplier quotes, the mapping must be reviewed before issue.');
    return uniqueStrings(out);
  }

  function buildExclusions(requirements, comparison) {
    var out = STANDARD_EXCLUSIONS.slice();
    if ((comparison.gaps || []).some(function (g) { return g.key === 'rollerShutters'; })) {
      out.unshift('Roller shutter doors are excluded unless separately confirmed and priced.');
    }
    return uniqueStrings(out);
  }

  function buildRedFlags(requirements, supplierQuotes, documents) {
    var flags = [];
    var supplierText = JSON.stringify(supplierQuotes || []).toLowerCase();
    RED_FLAG_RULES.forEach(function (rule) {
      if (!hasReq(requirements, rule.key)) return;
      var covered = supplierText && supplierText.indexOf(rule.key.toLowerCase()) >= 0;
      if (rule.key === 'colour') covered = /ral|black|white|grey|7016|9005|9010/i.test(supplierText);
      if (rule.key === 'pas24') covered = /pas\s*24|secured\s+by\s+design|sbd/i.test(supplierText);
      if (rule.key === 'uValue') covered = /\bu[\s-]*value|1\.0|1\.2|1\.4|part\s+l/i.test(supplierText);
      if (rule.key === 'trickleVents') covered = /trickle|linkvent|ventilation/i.test(supplierText);
      if (rule.key === 'restrictors') covered = /restrictor/i.test(supplierText);
      flags.push({
        key: rule.key,
        issue: rule.label,
        severity: rule.severity,
        supplierEvidence: covered ? 'Supplier evidence appears to mention this item; estimator should verify details.' : 'Not clearly confirmed in supplier evidence.',
        recommendedAction: rule.query
      });
    });

    (documents || []).forEach(function (doc) {
      var text = normaliseText(doc.fullText || '');
      if (isTrainingMaterialDoc(doc, text)) return;
      if (doc.isScanned || (doc.kind === 'image') || (doc.kind === 'pdf' && text.length < 80)) {
        flags.push({
          key: 'ocr',
          issue: 'Document may be scanned/image-only and not reliable for extraction: ' + doc.name,
          severity: 'critical',
          supplierEvidence: 'No machine-readable text available.',
          recommendedAction: 'Run OCR/drawing takeoff or review manually before pricing.'
        });
      }
      if (/contractor\s+to\s+design|design\s+by\s+contractor/i.test(text)) {
        flags.push({
          key: 'designResponsibility',
          issue: 'Tender wording suggests contractor design responsibility.',
          severity: 'critical',
          supplierEvidence: doc.name,
          recommendedAction: 'Confirm whether Fenster has design responsibility and whether design/calculation fees are included.'
        });
      }
      if (/allow\s+for/i.test(text) && /window|door|glazing|curtain|louv/i.test(text)) {
        flags.push({
          key: 'allowFor',
          issue: 'BoQ/spec contains "allow for" glazing wording that may lack enough detail.',
          severity: 'warning',
          supplierEvidence: doc.name,
          recommendedAction: 'Review allowance wording and confirm quantity/specification before final pricing.'
        });
      }
    });
    return uniqueObjects(flags, function (a, b) {
      return a.key === b.key && a.issue === b.issue && a.supplierEvidence === b.supplierEvidence;
    });
  }

  function buildSpecificationExtraction(requirements, redFlags) {
    return (requirements || []).map(function (req) {
      var flag = (redFlags || []).find(function (risk) { return risk.key === req.key; });
      return {
        item: req.label,
        requirement: req.value,
        sourceDocument: req.sourceDocument,
        pageReference: req.pageReference || '',
        appliesTo: appliesToForRequirement(req.key),
        riskComment: flag ? flag.issue : ''
      };
    });
  }

  function buildScheduleItemList(items) {
    return (items || []).map(function (item) {
      return {
        itemRef: item.reference || '',
        location: item.location || '',
        description: item.description || item.openingType || item.type || '',
        quantity: item.quantity || 1,
        materialSystem: item.frameType || item.system || 'Unknown',
        notes: item.glazingSpec || item.finish || '',
        query: codeRisk(item) || (!item.width || !item.height ? 'Missing dimensions: confirm before issue.' : '')
      };
    });
  }

  function buildPricingReview(requirements, supplierQuotes, supplierItems, codingChecks, comparison) {
    var rows = [];
    (requirements || []).forEach(function (req) {
      var gap = ((comparison && comparison.gaps) || []).find(function (g) { return g.key === req.key; });
      rows.push({
        tenderRequirement: req.label + ': ' + req.value,
        supplierQuoteReference: supplierQuotes.length ? supplierQuotes.map(function (q) { return q.sourceDocument; }).join('; ') : 'No supplier quote detected',
        fensterPricingItem: matchingPricingRefs(req, codingChecks),
        covered: gap ? 'No/Partial' : 'Review',
        riskQuery: gap ? gap.message : 'Confirm against supplier quote and schedule.',
        actionRequired: gap ? gap.suggestedAction : 'Estimator to verify before issue.'
      });
    });
    if (!(supplierItems || []).length) {
      rows.push({
        tenderRequirement: 'Supplier itemised schedule',
        supplierQuoteReference: supplierQuotes.length ? 'Supplier quote detected, but item rows were not extracted.' : 'No supplier quote detected',
        fensterPricingItem: '',
        covered: 'No/Partial',
        riskQuery: 'Cannot confirm supplier coverage against tender item list.',
        actionRequired: 'Review supplier PDF/workbook manually or harden parser for this supplier format.'
      });
    }
    return rows;
  }

  function buildRiskRegister(requirements, comparison, redFlags, documents, items) {
    var risks = [];
    (redFlags || []).forEach(function (flag) {
      risks.push({
        risk: flag.issue,
        severity: flag.severity,
        reason: flag.supplierEvidence || 'Triggered by tender requirement.',
        recommendedAction: flag.recommendedAction
      });
    });
    ((comparison && comparison.gaps) || []).forEach(function (gap) {
      risks.push({
        risk: gap.message,
        severity: gap.severity,
        reason: 'Supplier/tender comparison gap.',
        recommendedAction: gap.suggestedAction
      });
    });
    if (!(documents || []).length) {
      risks.push({
        risk: 'No tender documents reviewed.',
        severity: 'critical',
        reason: 'Estimator review has no evidence base.',
        recommendedAction: 'Upload tender documents, emails, schedules and supplier quotes.'
      });
    }
    if (!(items || []).length) {
      risks.push({
        risk: 'No item list available for pricing/code allocation.',
        severity: 'critical',
        reason: 'Pricing document cannot be checked without scope rows.',
        recommendedAction: 'Extract a schedule, parse supplier rows, or add manual takeoff items.'
      });
    }
    return uniqueObjects(risks, function (a, b) {
      return a.risk === b.risk && a.reason === b.reason;
    });
  }

  function buildPreIssueChecklist(requirements, supplierQuotes, items, codingChecks, comparison, riskRegister) {
    var hasFireAcousticSecurity = hasReq(requirements, 'fireRating') || hasReq(requirements, 'acoustic') || hasReq(requirements, 'pas24');
    return [
      checkItem('Project name confirmed', hasReq(requirements, 'projectName'), 'Confirm project name from email/tender docs.'),
      checkItem('Client/main contractor confirmed', hasReq(requirements, 'client'), 'Confirm client or main contractor.'),
      checkItem('Site address confirmed', hasReq(requirements, 'siteAddress'), 'Confirm site address.'),
      checkItem('Scope item list available', (items || []).length > 0, 'Extract schedule/supplier rows or complete manual takeoff.'),
      checkItem('Supplier quote reviewed', (supplierQuotes || []).length > 0, 'Upload/review supplier quotations.'),
      checkItem('Pricing codes applied', (codingChecks || []).length > 0, 'Produce coding check table.'),
      checkItem('Colour confirmed or flagged', hasReq(requirements, 'colour'), 'Flag colour/RAL as query if absent.'),
      checkItem('Glass/U-value requirements reviewed where mentioned', !(hasReq(requirements, 'uValue') || hasReq(requirements, 'safetyGlazing')), 'Review glass and performance requirements before issue.'),
      checkItem('Fire/acoustic/PAS24 reviewed where mentioned', !hasFireAcousticSecurity, 'Resolve any fire/acoustic/PAS24 requirements before issue.'),
      checkItem('Supplier quote covers tender scope', !((comparison && comparison.gaps) || []).length, 'Resolve supplier/tender gaps.'),
      checkItem('High-risk items resolved', !hasCriticalRisk(riskRegister), 'Human estimator review required before issue.')
    ];
  }

  function checkItem(label, passed, action) {
    return {
      item: label,
      status: passed ? 'checked' : 'open',
      actionRequired: passed ? '' : action
    };
  }

  function buildRfis(requirements, comparison, redFlags) {
    var rfis = [];
    (comparison.gaps || []).forEach(function (gap) {
      rfis.push({
        question: gap.message,
        reason: gap.suggestedAction,
        severity: gap.severity,
        status: 'open'
      });
    });
    if (hasReq(requirements, 'uValue')) {
      rfis.push({
        question: 'Please confirm whole-unit U-value compliance for the proposed systems.',
        reason: 'Tender/specification includes U-value requirements; supplier quote text may only confirm glass makeup.',
        severity: 'warning',
        status: 'open'
      });
    }
    (redFlags || []).forEach(function (flag) {
      rfis.push({
        question: flag.recommendedAction,
        reason: flag.issue,
        severity: flag.severity,
        status: 'open'
      });
    });
    return uniqueObjects(rfis, function (a, b) {
      return a.question === b.question;
    });
  }

  function determineReadiness(comparison, rfis, items, riskRegister) {
    var critical = (comparison.gaps || []).filter(function (g) { return g.severity === 'critical'; }).length;
    var criticalRisks = (riskRegister || []).filter(function (g) { return g.severity === 'critical'; }).length;
    if (!items.length) return { status: 'blocked', label: 'Blocked - no priced scope detected' };
    if (critical > 0 || criticalRisks > 0) return { status: 'review', label: 'Needs estimator review' };
    if ((rfis || []).length) return { status: 'review', label: 'Needs estimator review' };
    return { status: 'ready', label: 'Ready to issue subject to estimator approval' };
  }

  function buildSummary(state, supplierQuotes, codingChecks) {
    var supplierTotal = round2((supplierQuotes || []).reduce(function (sum, q) { return sum + (q.exVatTotal || 0); }, 0));
    var labourTotal = round2((codingChecks || []).reduce(function (sum, row) { return sum + (row.labourTotal || 0); }, 0));
    var itemTotal = round2((state.items || []).reduce(function (sum, item) { return sum + (item.totalPrice || 0); }, 0));
    return {
      supplierTotal: supplierTotal,
      labourTotal: labourTotal,
      extractedItemTotal: itemTotal,
      codingRows: (codingChecks || []).length,
      supplierQuoteCount: (supplierQuotes || []).length
    };
  }

  function buildProposalDraft(state, requirements, supplierQuotes, assumptions, exclusions, rfis) {
    var project = (state.metadata && state.metadata.projectName) || inferProject(requirements, supplierQuotes) || 'the project';
    var supplierNames = uniqueStrings((supplierQuotes || []).map(function (q) { return q.supplier; }).filter(Boolean)).join(' and ') || 'approved suppliers';
    return {
      executiveSummary: 'Fenster Glazing proposes to supply and install the glazing package for ' + project + ', based on the tender documents and supplier quotation evidence reviewed. The current scope includes aluminium windows, external doors and associated louvres where confirmed, using ' + supplierNames + ' systems where quoted. Items not clearly confirmed by the tender and supplier evidence are flagged as RFIs or exclusions before issue.',
      scopeOfWorks: requirementsToScope(requirements),
      inclusions: [
        'Review of tender documents, schedules, specifications and supplier quotations.',
        'Supply of quoted aluminium windows and doors where mapped to the tender scope.',
        'Installation labour allowances based on Fenster product coding where enabled.',
        'Commercial review of assumptions, exclusions and RFIs before issue.'
      ],
      exclusions: exclusions,
      clarifications: assumptions.concat((rfis || []).map(function (r) { return r.question; })),
      qualityAndHandover: 'Works to be subject to Fenster QA checks, final survey, approved drawings, supplier/manufacturer confirmation and O&M handover information where included.'
    };
  }

  function buildPricingDraft(state, codingChecks, supplierQuotes, assumptions, exclusions, rfis) {
    var supplierTotal = round2((supplierQuotes || []).reduce(function (sum, q) { return sum + (q.exVatTotal || 0); }, 0));
    var labourTotal = round2((codingChecks || []).reduce(function (sum, row) { return sum + (row.labourTotal || 0); }, 0));
    var appSummary = state.items && state.items.length && typeof Pricing !== 'undefined'
      ? Pricing.getPriceSummary(state.items, state.pricing || {})
      : null;
    return {
      itemRows: codingChecks || [],
      supplierTotal: supplierTotal,
      labourTotal: labourTotal,
      appSummary: appSummary,
      assumptions: assumptions,
      exclusions: exclusions,
      rfis: rfis,
      notes: 'Pricing document draft is for estimator review. Supplier quote rows are cost evidence; tender scope gaps must be resolved before final issue.'
    };
  }

  function toMarkdown(review) {
    var lines = [];
    lines.push('# Project Hail Mary Estimator Review');
    lines.push('');
    lines.push('Status: ' + review.statusLabel);
    lines.push('');
    lines.push('## Summary');
    lines.push('- Supplier quote total: ' + money(review.summary.supplierTotal));
    lines.push('- Labour allowance total: ' + money(review.summary.labourTotal));
    lines.push('- Coding rows: ' + review.summary.codingRows);
    lines.push('- Supplier quotes detected: ' + review.summary.supplierQuoteCount);
    lines.push('');
    lines.push('## Tender Requirements');
    (review.tenderRequirements || []).forEach(function (r) {
      lines.push('- ' + r.label + ': ' + r.value + ' [' + r.sourceDocument + ']');
    });
    lines.push('');
    lines.push('## Supplier Quotes');
    (review.supplierQuotes || []).forEach(function (q) {
      lines.push('- ' + q.supplier + ' ' + (q.quoteNumber || '') + ': ' + money(q.exVatTotal) + ' ex VAT [' + q.sourceDocument + ']');
    });
    lines.push('');
    lines.push('## RFIs');
    (review.rfis || []).forEach(function (r) {
      lines.push('- ' + r.question + (r.reason ? ' - ' + r.reason : ''));
    });
    lines.push('');
    lines.push('## Risk Register');
    (review.riskRegister || []).forEach(function (r) {
      lines.push('- [' + r.severity + '] ' + r.risk + (r.recommendedAction ? ' - ' + r.recommendedAction : ''));
    });
    lines.push('');
    lines.push('## Pre-Issue Checklist');
    (review.preIssueChecklist || []).forEach(function (c) {
      lines.push('- ' + c.status + ': ' + c.item + (c.actionRequired ? ' - ' + c.actionRequired : ''));
    });
    lines.push('');
    lines.push('## Exclusions');
    (review.exclusions || []).forEach(function (e) { lines.push('- ' + e); });
    return lines.join('\n');
  }

  function classifyCode(item) {
    if (!item) return '';
    var type = String(item.type || '').toLowerCase();
    var desc = String(item.description || '').toLowerCase();
    var frame = String(item.frameType || '').toLowerCase();
    var area = ((item.width || 0) / 1000) * ((item.height || 0) / 1000);
    var isDouble = /\bdouble\b|pair|leafs|leaves/.test(desc + ' ' + String(item.doorSwing || '').toLowerCase());
    var isDoor = type === 'door' || /\bdoor\b/.test(desc);
    var isPvc = /pvc|upvc/.test(frame + ' ' + desc);
    if (isDoor && /with\s+(?:window|screen|sidelight|fanlight)|fixed\s+fields|door\s+element/.test(desc)) {
      if (area <= 4) return 'SADSAW';
      if (area <= 8) return 'SADMAW';
      return 'SADLAW';
    }
    if (isDoor && isPvc) return isDouble ? 'DUPD' : 'SUPD';
    if (isDoor) return isDouble ? 'DAD' : 'SAD';
    if (isPvc) {
      if (area <= 2.5) return 'SPVC';
      if (area <= 6) return 'MPVC';
      return 'LPVC';
    }
    if (area <= 2.5) return 'SAW';
    if (area <= 6) return 'MAW';
    if (area <= 12) return 'LAW';
    return 'ELAW';
  }

  function getLabour(code) {
    if (typeof Pricing !== 'undefined' && Pricing.getLabourAllowanceForCode) {
      return Pricing.getLabourAllowanceForCode(code);
    }
    var fallback = { SUPD: 250, DUPD: 500, SAD: 250, DAD: 500, ELAW: 250, LAW: 160, MAW: 160, SAW: 160, LPVC: 160, MPVC: 160, SPVC: 160, SADLAW: 410, SADMAW: 410, SADSAW: 410 };
    return fallback[String(code || '').toUpperCase()] || 0;
  }

  function reasonForCode(item) {
    var code = item.productCode || classifyCode(item);
    if (/^SAD/.test(code) && code.length > 3) return 'Combined aluminium door/screen item; review against supplier description.';
    if (/DAD|DUPD/.test(code)) return 'Double-door code selected from description/door swing.';
    if (/SAD|SUPD/.test(code)) return 'Single-door code selected from description/door swing.';
    return 'Window code selected from material and size category.';
  }

  function codeRisk(item) {
    var text = (item.description || '') + ' ' + (item.reference || '');
    if (/roller\s+shutter/i.test(text)) return 'Curtain/roller shutter item needs separate code or supplier confirmation.';
    if (/louv?re/i.test(text)) return 'Louvre item: confirm whether standard window/door code is appropriate.';
    if (/item\s+\d+|supplier item/i.test(text)) return 'Supplier reference is generic; map back to architect/tender ref.';
    return '';
  }

  function extractSupplierNotes(text) {
    var notes = [];
    if (/valid\s+for\s+thirty\s+days|prices\s+are\s+held\s+for\s+thirty\s+days/i.test(text)) notes.push('Quote validity appears to be 30 days.');
    if (/ex\s+works|delivery\s+charges/i.test(text)) notes.push('Supplier quote may exclude delivery or include ex-works terms.');
    if (/please\s+check\s+all\s+items/i.test(text)) notes.push('Supplier asks customer to check missing items.');
    return notes;
  }

  function extractCoverageFlags(text) {
    text = String(text || '');
    return {
      black: /black|9005|jet\s+black|\bBL\b/i.test(text),
      uValue: /\bu[\s-]*value|ecoplus|1\.0|1\.4\s*w\/?m/i.test(text),
      louvres: /louv?re/i.test(text),
      rollerShutters: /roller\s+shutter/i.test(text),
      pas24: /pas\s*24|secured\s+by\s+design|sbd/i.test(text),
      restrictors: /restrictor/i.test(text),
      ventilation: /trickle\s+vent|linkvent|ventilation/i.test(text)
    };
  }

  function mergeCoverageFlags(quotes) {
    var merged = {};
    (quotes || []).forEach(function (quote) {
      var flags = quote.flags || {};
      Object.keys(flags).forEach(function (key) {
        merged[key] = merged[key] || !!flags[key];
      });
    });
    return merged;
  }

  function requirementsToScope(requirements) {
    var scope = [];
    if (hasReq(requirements, 'aluminium')) scope.push('PPC aluminium framed windows and doors.');
    if (hasReq(requirements, 'louvres')) scope.push('Louvre panels/doors where confirmed by drawings and supplier quote.');
    if (hasReq(requirements, 'trickleVents')) scope.push('Ventilation/restrictors where shown or quoted.');
    if (!scope.length) scope.push('Glazing package as extracted from reviewed tender documents.');
    return scope;
  }

  function inferProject(requirements, supplierQuotes) {
    var projectReq = (requirements || []).find(function (r) { return r.key === 'projectName'; });
    if (projectReq) return projectReq.value;
    var quote = (supplierQuotes || []).find(function (q) { return q.project; });
    return quote ? quote.project : '';
  }

  function isTrainingMaterialDoc(doc, text) {
    var haystack = ((doc && doc.name) || '') + '\n' + String(text || '').slice(0, 12000);
    var score = 0;
    if (/estimating\s+bot\s+training\s+brief/i.test(haystack)) score += 3;
    if (/pricing\s+code\s+training\s+notes/i.test(haystack)) score += 3;
    if (/standard\s+exclusions\s+bank/i.test(haystack)) score += 1;
    if (/standard\s+inclusions\s+bank/i.test(haystack)) score += 1;
    if (/required\s+output\s+format\s+for\s+each\s+project/i.test(haystack)) score += 1;
    if (/the\s+bot\s+must\s+learn|you\s+are\s+being\s+trained/i.test(haystack)) score += 2;
    if (/suggested\s+prompts\s+for\s+the\s+bot/i.test(haystack)) score += 1;
    return score >= 3;
  }

  function appliesToForRequirement(key) {
    var map = {
      colour: 'All visible PPC/painted items',
      uValue: 'Windows, doors and glazed screens',
      gValue: 'Glazed units where solar control is required',
      ltValue: 'Glazed units where light transmission is specified',
      aluminium: 'Aluminium windows, doors and screens',
      upvc: 'uPVC windows and doors',
      curtainWalling: 'Curtain walling only',
      louvres: 'Louvre panels/doors shown on tender information',
      pas24: 'Security-rated windows and doors where required',
      trickleVents: 'Ventilated windows/doors where required',
      restrictors: 'Opening windows where required',
      ddaThresholds: 'Entrance and external doors',
      fireRating: 'Fire-rated screens/doors/glazing only where allocated',
      acoustic: 'Acoustic glazing only where allocated',
      safetyGlazing: 'Critical locations and specified toughened/laminated glass',
      accessControl: 'Automated/access-controlled doors or windows',
      removalDisposal: 'Existing frames/items affected by replacement work',
      makingGood: 'Surrounding builder finishes/openings',
      accessScaffold: 'Installation logistics',
      programme: 'Tender submission and delivery programme'
    };
    return map[key] || 'Project scope';
  }

  function matchingPricingRefs(requirement, codingChecks) {
    var key = requirement && requirement.key;
    var rows = (codingChecks || []).filter(function (row) {
      var haystack = (row.description + ' ' + row.material + ' ' + row.selectedCode + ' ' + row.reference).toLowerCase();
      if (key === 'aluminium') return /aluminium|sad|dad|law|maw|saw|elaw/.test(haystack);
      if (key === 'upvc') return /upvc|pvc|supd|dupd|lpvc|mpvc|spvc/.test(haystack);
      if (key === 'louvres') return /louv/.test(haystack);
      if (key === 'curtainWalling') return /curtain|cw/.test(haystack);
      if (key === 'accessControl') return /access|automatic|actuator|teleflex/.test(haystack);
      if (key === 'fireRating') return /fire|fd30|fd60/.test(haystack);
      if (key === 'acoustic') return /acoustic|db/.test(haystack);
      return false;
    });
    return rows.slice(0, 8).map(function (row) { return row.reference || row.description; }).filter(Boolean).join(', ');
  }

  function hasReq(requirements, key, regex) {
    return (requirements || []).some(function (r) {
      return r.key === key && (!regex || regex.test(r.value || ''));
    });
  }

  function hasCriticalRisk(risks) {
    return (risks || []).some(function (risk) { return risk.severity === 'critical'; });
  }

  function pushUnique(arr, value, sameFn) {
    if (!arr.some(function (existing) { return sameFn(existing, value); })) arr.push(value);
  }

  function uniqueStrings(values) {
    var seen = {};
    return (values || []).filter(function (value) {
      if (!value || seen[value]) return false;
      seen[value] = true;
      return true;
    });
  }

  function uniqueObjects(values, sameFn) {
    var out = [];
    (values || []).forEach(function (value) {
      if (!out.some(function (existing) { return sameFn(existing, value); })) out.push(value);
    });
    return out;
  }

  function normaliseText(text) {
    return String(text || '').replace(/\r/g, '\n').replace(/[ \t]+/g, ' ');
  }

  function cleanValue(value) {
    return String(value || '').replace(/\s+/g, ' ').replace(/[|]+$/g, '').trim().slice(0, 180);
  }

  function firstMatch(text, regex) {
    var match = String(text || '').match(regex);
    return match && match[1] ? cleanValue(match[1]) : '';
  }

  function moneyMatch(text, regex) {
    var match = String(text || '').match(regex);
    return match && match[1] ? parseMoney(match[1]) : 0;
  }

  function moneyAfterLabel(text, labelRe) {
    var lines = String(text || '').split(/\n+/);
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i];
      var idx = line.search(labelRe);
      if (idx < 0) continue;
      var tail = line.slice(idx);
      var matches = tail.match(/[0-9][0-9,]*\.\d{2}/g);
      if (matches && matches.length) return parseMoney(matches[0]);
    }
    return 0;
  }

  function parseMoney(value) {
    var n = parseFloat(String(value || '').replace(/[^\d.-]/g, ''));
    return isFinite(n) ? n : 0;
  }

  function parseNum(value) {
    var n = parseFloat(String(value || '').replace(/[^\d.-]/g, ''));
    return isFinite(n) ? n : 0;
  }

  function round2(value) {
    value = Number(value || 0);
    return Math.round(value * 100) / 100;
  }

  function money(value) {
    return 'GBP ' + Number(value || 0).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  return {
    buildReview: function (state, documents) { return finaliseReview(buildReview(state, documents)); },
    extractRequirements: extractRequirements,
    extractSupplierQuotes: extractSupplierQuotes,
    buildCodingChecks: buildCodingChecks,
    toMarkdown: toMarkdown
  };
})();
