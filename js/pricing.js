/* js/pricing.js - Fenster pricing engine (from master pricing document)
 *
 * Formula:  Unit Rate = Frames + Glass + Additional + ProductCodeMarkup
 * Total  :  Qty x Unit Rate
 * Install:  Qty x £140/unit (separate line)
 * CW     :  SQM x £850 supply + SQM x £150 labour
 * EPDM   :  SQM x £25 (optional)
 * Mastic :  Perimeter(m) x £5 (optional)
 */

var Pricing = (function () {

  // =========================================================================
  // Product codes & markups - extracted from Fenster master pricing doc
  // =========================================================================
  var PRODUCT_CODES = {
    // Aluminium Windows (size-based)
    SAW:    { markup: 400,  desc: 'Small Aluminium Window' },
    MAW:    { markup: 500,  desc: 'Medium Aluminium Window' },
    LAW:    { markup: 600,  desc: 'Large Aluminium Window' },
    ELAW:   { markup: 1000, desc: 'Extra Large Aluminium Window' },
    // PVC Windows (size-based)
    SPVC:   { markup: 75,   desc: 'Small PVC Window' },
    MPVC:   { markup: 75,   desc: 'Medium PVC Window' },
    LPVC:   { markup: 175,  desc: 'Large PVC Window' },
    // Aluminium Doors
    SAD:    { markup: 1150, desc: 'Single Aluminium Door' },
    DAD:    { markup: 1950, desc: 'Double Aluminium Door' },
    // PVC Door
    UPD:    { markup: 950,  desc: 'uPVC Door' },
    // Combo units (door + sidelight)
    SADSAW: { markup: 1650, desc: 'Single Alum Door + Small Window' },
    SADMAW: { markup: 1850, desc: 'Single Alum Door + Med Window' },
    SADLAW: { markup: 1950, desc: 'Single Alum Door + Large Window' },
    // Timber Doors (estimated - not in master doc)
    STD:    { markup: 800,  desc: 'Single Timber Door' },
    DTD:    { markup: 1400, desc: 'Double Timber Door' },
    // Steel Doors
    SSD:    { markup: 1300, desc: 'Single Steel Door' },
    DSD:    { markup: 2200, desc: 'Double Steel Door' },
    // Curtain Wall (priced per m²)
    CW:     { markup: 0,    desc: 'Curtain Wall' }
  };

  // Window area thresholds (m²)
  var WIN_SMALL  = 2.5;
  var WIN_MEDIUM = 6;
  var WIN_LARGE  = 12;

  // =========================================================================
  // Default config - estimated supplier rates & fixed rates
  // =========================================================================
  var DEFAULT_CONFIG = {
    pricingVersion: 4,

    // Estimated supplier frame cost per m² (fabricated unit inc. hardware, excl. glass)
    aluminiumFrameRate: 500,
    aluminiumDoorRate: 1125,
    pvcFrameRate: 395,
    timberFrameRate: 350,
    steelFrameRate: 600,

    // Split-pane pricing rates (more accurate than flat rate)
    fixedPaneRate: 250,           // £/m² for fixed glass panes
    openingPaneRate: 580,         // £/m² for opening lights/casements
    louvreFlat: 450,              // £ flat premium per louvre panel
    overheadPercent: 8,           // % overhead/margin baked into type code markups

    // Estimated glass cost per m² (separate supplier quote)
    doubleGlazedRate: 55,
    tripleGlazedRate: 85,
    fireRatedGlassRate: 130,
    laminatedExtra: 15,
    toughenedExtra: 10,

    // Fixed rates from Fenster master doc
    installationPerUnit: 140,
    cwSupplyRate: 850,
    cwLabourRate: 150,
    epdmRate: 25,
    masticRate: 5,
    fixedEPDMAmount: undefined,
    fixedMasticAmount: undefined,

    // Quote-level options
    includeInstallation: true,
    includeEPDM: false,
    includeMastic: false,

    // VAT and discount
    vatEnabled: true,
    vatRate: 20,
    discountPercent: 0,
    discountFixedAmount: 0,

    // Quote-level adjustment line, used for actuators, access control packages,
    // surveys, discounts entered as negative extras, or tender-specific allowances.
    quoteExtraLabel: '',
    quoteExtraAmount: 0,
    autoTenderPricingId: '',
    tenderPricingDefaultsVersion: 0
  };

  var KNOWN_TENDER_PRICING = {
    '223-southwark-2025': {
      label: '223 Southwark Park Road',
      defaultsVersion: 1,
      installationPerUnit: 362.7272727273,
      fixedMasticAmount: undefined,
      fixedEPDMAmount: undefined,
      quoteExtraLabel: '',
      quoteExtraAmount: 0,
      unitRates: {}
    },
    'stoke-park-school-2026': {
      label: 'Stoke Park School',
      defaultsVersion: 2,
      installationPerUnit: 255,
      fixedMasticAmount: 1432.50,
      fixedEPDMAmount: 4285.62,
      quoteExtraLabel: 'Manual Teleflex / electric actuator allowance',
      quoteExtraAmount: 7000,
      unitRates: {
        'window|TYPE A': 1278.81,
        'window|TYPE B': 2753.10,
        'window|TYPE C': 4752.14,
        'window|TYPE D': 2677.41,
        'window|TYPE E': 866.94,
        'window|TYPE F': 4595.815,
        'window|TYPE G': 4136.70,
        'window|TYPE H': 4659.69,
        'window|TYPE J': 3168.82,
        'door|TYPE A': 5780.58,
        'door|TYPE B': 4656.88,
        'door|TYPE C': 4656.87,
        'door|TYPE D': 4222.98
      }
    }
  };

  // =========================================================================
  // Product code classification
  // =========================================================================
  function classifyProductCode(item) {
    var type  = (item.type || '').toLowerCase();
    var frame = (item.frameType || '').toLowerCase();
    var swing = (item.doorSwing || '').toLowerCase();
    var w     = (item.width  || 0) / 1000;
    var h     = (item.height || 0) / 1000;
    var area  = w * h;

    // Curtain wall
    if (type === 'curtain wall') return 'CW';

    // Door
    if (type === 'door') {
      var isDouble = swing === 'double' || swing === 'double door' ||
                     swing.indexOf('double') !== -1;

      if (frame.indexOf('aluminium') !== -1 || frame.indexOf('aluminum') !== -1) {
        return isDouble ? 'DAD' : 'SAD';
      }
      if (frame.indexOf('pvc') !== -1 || frame.indexOf('upvc') !== -1) {
        return 'UPD';
      }
      if (frame.indexOf('steel') !== -1) {
        return isDouble ? 'DSD' : 'SSD';
      }
      if (frame.indexOf('timber') !== -1 || frame.indexOf('wood') !== -1) {
        return isDouble ? 'DTD' : 'STD';
      }
      // Infer from reference prefix
      var ref = (item.reference || '').toUpperCase();
      if (/^E/.test(ref)) return isDouble ? 'DAD' : 'SAD';
      if (/^N/.test(ref)) return isDouble ? 'DTD' : 'STD';
      return isDouble ? 'DAD' : 'SAD';
    }

    // Window - classify by frame material then size
    var isPVC = frame.indexOf('pvc') !== -1 || frame.indexOf('upvc') !== -1;

    if (isPVC) {
      if (area <= WIN_SMALL)  return 'SPVC';
      if (area <= WIN_MEDIUM) return 'MPVC';
      return 'LPVC';
    }

    // Default aluminium for commercial
    if (area <= WIN_SMALL)  return 'SAW';
    if (area <= WIN_MEDIUM) return 'MAW';
    if (area <= WIN_LARGE)  return 'LAW';
    return 'ELAW';
  }

  // =========================================================================
  // Supplier cost estimation (used when no actual supplier quote entered)
  // =========================================================================

  /**
   * Split-pane frame estimate: if item has pane counts, use per-pane-type
   * rates instead of a flat £/m² rate. This captures the big cost difference
   * between fixed panels and opening lights (hinges, locks, restrictors etc.)
   *
   * The overhead % accounts for the fact that Fenster type-code markups
   * bundle margin/overhead on top of pure labour.
   */
  function estimateFrameCost(item, config) {
    var w    = (item.width  || 0) / 1000;
    var h    = (item.height || 0) / 1000;
    var area = w * h;
    if (area <= 0) return 0;

    var frame  = (item.frameType || '').toLowerCase();
    var isDoor = (item.type || '').toLowerCase() === 'door';

    // If we have pane counts → use split-pane pricing
    var fixedPanes   = item.fixedPanes   || 0;
    var openingPanes = item.openingPanes || 0;
    var totalPanes   = fixedPanes + openingPanes;

    if (totalPanes > 0 && !isDoor) {
      // Divide total area proportionally across panes
      var areaPerPane  = area / totalPanes;
      var fixedCost    = fixedPanes   * areaPerPane * (config.fixedPaneRate   || 280);
      var openingCost  = openingPanes * areaPerPane * (config.openingPaneRate || 650);
      var louvreExtra  = item.hasLouvre ? (config.louvreFlat || 450) : 0;
      var baseCost     = fixedCost + openingCost + louvreExtra;

      // Apply overhead % (accounts for margin baked into type code markups)
      var overhead = config.overheadPercent || 12;
      var withOverhead = baseCost * (1 + overhead / 100);
      return round2(withOverhead);
    }

    // Fallback: flat rate per m² (original logic, used when pane data missing)
    var rate = isDoor ? (config.aluminiumDoorRate || config.aluminiumFrameRate) : config.aluminiumFrameRate;

    if (frame.indexOf('pvc') !== -1 || frame.indexOf('upvc') !== -1)       rate = config.pvcFrameRate;
    else if (frame.indexOf('timber') !== -1 || frame.indexOf('wood') !== -1) rate = config.timberFrameRate;
    else if (frame.indexOf('steel') !== -1)                                  rate = config.steelFrameRate;
    else if (isDoor && config.aluminiumDoorRate)                              rate = config.aluminiumDoorRate;

    return round2(rate * area);
  }

  function estimateGlassCost(item, config) {
    var w    = (item.width  || 0) / 1000;
    var h    = (item.height || 0) / 1000;
    var area = w * h;
    if (area <= 0) return 0;

    // Doors with N/A glazing get zero glass cost
    var doorGlazing = (item.doorGlazing || '').toLowerCase();
    if (doorGlazing === 'n/a' || doorGlazing === 'none') return 0;

    var spec  = (item.glazingSpec || '').toLowerCase();
    var notes = Array.isArray(item.notes) ? item.notes.join(' ').toLowerCase() : '';
    var fire  = (item.fireRating || '').toLowerCase();
    var combined = spec + ' ' + notes + ' ' + fire;

    var baseRate = config.doubleGlazedRate;
    if (combined.indexOf('triple') !== -1) baseRate = config.tripleGlazedRate;
    if (fire.indexOf('fd') !== -1 || combined.indexOf('pyrobelite') !== -1 ||
        combined.indexOf('fire rated') !== -1 || combined.indexOf('fire-rated') !== -1) {
      baseRate = config.fireRatedGlassRate;
    }

    var extras = 0;
    if (combined.indexOf('laminated') !== -1) extras += config.laminatedExtra;
    if (combined.indexOf('toughened') !== -1 || combined.indexOf('tempered') !== -1)
      extras += config.toughenedExtra;

    return Math.round((baseRate + extras) * area * 100) / 100;
  }

  // =========================================================================
  // Per-item price calculation  (Fenster formula)
  //   Unit Rate = Frames + Glass + Additional + ProductCodeMarkup
  //   Total     = Qty x Unit Rate
  // =========================================================================
  function calculateItemPrice(item, pricingConfig) {
    var config = mergeConfig(pricingConfig);

    var w    = (item.width  || 0) / 1000;
    var h    = (item.height || 0) / 1000;
    var area = w * h;

    if (area <= 0) {
      return {
        unitPrice: 0, totalPrice: 0, installCost: 0,
        breakdown: 'Dimensions not set', productCode: '\u2014', productDesc: '\u2014',
        frameCost: 0, glassCost: 0, additional: 0, markup: 0
      };
    }

    var code     = item.productCode || classifyProductCode(item);
    var codeInfo = PRODUCT_CODES[code] || { markup: 0, desc: 'Unknown' };
    var qty      = item.quantity || 1;
    var frameCost, glassCost, additional, markup, unitRate;
    var quotedUnit = resolveQuotedUnitPrice(item, config);

    if (quotedUnit !== undefined) {
      frameCost  = quotedUnit;
      glassCost  = 0;
      additional = 0;
      markup     = 0;
      unitRate   = quotedUnit;
    } else if (code === 'CW') {
      frameCost  = round2(config.cwSupplyRate * area);
      glassCost  = 0;
      additional = 0;
      markup     = round2(config.cwLabourRate * area);
      unitRate   = frameCost + markup;
    } else {
      frameCost  = item.supplierFrameCost  !== undefined ? item.supplierFrameCost  : estimateFrameCost(item, config);
      glassCost  = item.supplierGlassCost  !== undefined ? item.supplierGlassCost  : estimateGlassCost(item, config);
      additional = item.supplierAdditional || 0;
      markup     = codeInfo.markup;
      unitRate   = frameCost + glassCost + additional + markup;
    }

    unitRate  = round2(unitRate);
    var total = round2(unitRate * qty);
    var inst  = config.includeInstallation ? round2(config.installationPerUnit * qty) : 0;

    // Determine pricing method for breakdown display
    var hasQuotedUnit    = quotedUnit !== undefined;
    var hasSupplierCosts = item.supplierFrameCost !== undefined || item.supplierGlassCost !== undefined || item.supplierUnitPrice !== undefined;
    var hasPaneCounts    = (item.fixedPanes || 0) + (item.openingPanes || 0) > 0;
    var pricingMethod    = hasQuotedUnit ? 'quoted-unit' : (hasSupplierCosts ? 'supplier' : (hasPaneCounts ? 'split-pane' : 'flat-rate'));

    // Breakdown string
    var parts = [code];
    if (code === 'CW') {
      parts.push('Supply ' + fmt(frameCost));
      parts.push('Labour ' + fmt(markup));
    } else if (pricingMethod === 'quoted-unit') {
      parts.push('Quoted type rate ' + fmt(unitRate));
      if (item.supplierRateSource) parts.push(item.supplierRateSource);
    } else if (pricingMethod === 'supplier') {
      parts.push('Frame ' + fmt(frameCost) + ' \u2713');
      if (glassCost > 0) parts.push('Glass ' + fmt(glassCost) + ' \u2713');
      if (additional > 0) parts.push('Add ' + fmt(additional) + ' \u2713');
      parts.push('Markup ' + fmt(markup));
    } else if (pricingMethod === 'split-pane') {
      var fp = item.fixedPanes || 0;
      var op = item.openingPanes || 0;
      parts.push('Frame ' + fmt(frameCost) + ' (' + fp + 'F+' + op + 'O' + (item.hasLouvre ? '+L' : '') + ')');
      if (glassCost > 0) parts.push('Glass ' + fmt(glassCost));
      if (additional > 0) parts.push('Add ' + fmt(additional));
      parts.push('Markup ' + fmt(markup));
    } else {
      parts.push('Frame ' + fmt(frameCost));
      if (glassCost > 0) parts.push('Glass ' + fmt(glassCost));
      if (additional > 0) parts.push('Add ' + fmt(additional));
      parts.push('Markup ' + fmt(markup));
    }
    parts.push('= ' + fmt(unitRate));
    if (qty > 1) parts.push('\u00d7' + qty + ' = ' + fmt(total));

    return {
      unitPrice:     unitRate,
      totalPrice:    total,
      installCost:   inst,
      breakdown:     parts.join(' | '),
      productCode:   code,
      productDesc:   codeInfo.desc,
      frameCost:     frameCost,
      glassCost:     glassCost,
      additional:    additional,
      markup:        markup,
      pricingMethod: pricingMethod
    };
  }

  // =========================================================================
  // Batch recalculate
  // =========================================================================
  function recalculateAll(items, pricingConfig) {
    return items.map(function (item) {
      if (item.manualOverride) return item;
      var result = calculateItemPrice(item, pricingConfig);
      return Object.assign({}, item, {
        unitPrice:     result.unitPrice,
        totalPrice:    result.totalPrice,
        productCode:   result.productCode,
        pricingMethod: result.pricingMethod
      });
    });
  }

  // =========================================================================
  // Quote-level summary
  // =========================================================================
  function getPriceSummary(items, pricingConfig) {
    var config = mergeConfig(pricingConfig);

    var subtotal     = 0;
    var installTotal = 0;
    var epdmTotal    = 0;
    var masticTotal  = 0;

    items.forEach(function (item) {
      subtotal += (item.totalPrice || 0);

      var qty  = item.quantity || 1;
      var w    = (item.width  || 0) / 1000;
      var h    = (item.height || 0) / 1000;
      var area = w * h;

      if (config.includeInstallation) {
        installTotal += config.installationPerUnit * qty;
      }
      if (config.includeEPDM && area > 0) {
        epdmTotal += config.epdmRate * area * qty;
      }
      if (config.includeMastic && area > 0) {
        var perimM = (w + h) * 2;
        masticTotal += config.masticRate * perimM * qty;
      }
    });

    subtotal     = round2(subtotal);
    installTotal = round2(installTotal);
    epdmTotal    = config.includeEPDM && config.fixedEPDMAmount !== undefined ? round2(config.fixedEPDMAmount || 0) : round2(epdmTotal);
    masticTotal  = config.includeMastic && config.fixedMasticAmount !== undefined ? round2(config.fixedMasticAmount || 0) : round2(masticTotal);

    var quoteExtraLabel = config.quoteExtraLabel || 'Extra costs';
    var quoteExtraAmount = round2(config.quoteExtraAmount || 0);

    var beforeDiscount = round2(subtotal + installTotal + epdmTotal + masticTotal + quoteExtraAmount);

    var discountPercent = config.discountPercent || 0;
    var discountFixedAmount = round2(config.discountFixedAmount || 0);
    var discountAmount  = round2((beforeDiscount * discountPercent / 100) + discountFixedAmount);
    if (discountAmount > beforeDiscount) discountAmount = beforeDiscount;
    var afterDiscount   = round2(beforeDiscount - discountAmount);

    var vatEnabled = config.vatEnabled !== false;
    var vatRate    = config.vatRate || 20;
    var vatAmount  = vatEnabled ? round2(afterDiscount * vatRate / 100) : 0;

    var total = round2(afterDiscount + vatAmount);

    return {
      subtotal:        subtotal,
      installTotal:    installTotal,
      epdmTotal:       epdmTotal,
      masticTotal:     masticTotal,
      quoteExtraLabel: quoteExtraLabel,
      quoteExtraAmount: quoteExtraAmount,
      beforeDiscount:  beforeDiscount,
      discountPercent: discountPercent,
      discountFixedAmount: discountFixedAmount,
      discountAmount:  discountAmount,
      afterDiscount:   afterDiscount,
      vatEnabled:      vatEnabled,
      vatRate:         vatRate,
      vatAmount:       vatAmount,
      total:           total,
      itemCount:       items.length,
      includeInstallation: config.includeInstallation,
      includeEPDM:     config.includeEPDM,
      includeMastic:   config.includeMastic
    };
  }

  function resolveQuotedUnitPrice(item, config) {
    if (!item) return undefined;
    if (item.supplierUnitPrice !== undefined && item.supplierUnitPrice !== null && item.supplierUnitPrice !== '') {
      return round2(parseFloat(item.supplierUnitPrice) || 0);
    }

    var tenderId = item.knownTenderId || config.autoTenderPricingId;
    var tender = tenderId ? KNOWN_TENDER_PRICING[tenderId] : null;
    var scheduleType = normaliseScheduleType(item.scheduleType || item.doorType);
    var type = (item.type || '').toLowerCase();
    if (!tender || !scheduleType || !type) return undefined;

    var rate = tender.unitRates[type + '|' + scheduleType];
    return rate !== undefined ? round2(rate) : undefined;
  }

  function normaliseScheduleType(value) {
    var text = String(value || '').toUpperCase().trim();
    var match = text.match(/TYPE\s+([A-Z])/);
    return match ? 'TYPE ' + match[1] : '';
  }

  function applyKnownItemPricing(items) {
    (items || []).forEach(function (item) {
      var tenderId = item.knownTenderId;
      var tender = tenderId ? KNOWN_TENDER_PRICING[tenderId] : null;
      var scheduleType = normaliseScheduleType(item.scheduleType || item.doorType);
      var type = (item.type || '').toLowerCase();
      if (!tender || !scheduleType || !type) return;
      var rate = tender.unitRates[type + '|' + scheduleType];
      if (rate === undefined) return;
      if (item.supplierUnitPrice === undefined) {
        item.supplierUnitPrice = rate;
        item.supplierRateSource = 'Borras type schedule';
      }
    });
    return items;
  }

  function applyTenderPricingDefaults(items, pricingConfig) {
    var cfg = mergeConfig(pricingConfig);
    var tenderId = '';
    (items || []).some(function (item) {
      if (item.knownTenderId && KNOWN_TENDER_PRICING[item.knownTenderId]) {
        tenderId = item.knownTenderId;
        return true;
      }
      return false;
    });
    if (!tenderId) {
      return applyInferredPricingDefaults(items, cfg);
    }

    applyKnownItemPricing(items);
    var tender = KNOWN_TENDER_PRICING[tenderId];
    var defaultsVersion = tender.defaultsVersion || 1;
    if (!cfg.autoTenderPricingId || cfg.autoTenderPricingId === tenderId && (cfg.tenderPricingDefaultsVersion || 0) < defaultsVersion) {
      cfg.autoTenderPricingId = tenderId;
      cfg.tenderPricingDefaultsVersion = defaultsVersion;
      cfg.includeInstallation = true;
      cfg.includeMastic = false;
      cfg.includeEPDM = false;
      cfg.vatEnabled = false;
      cfg.installationPerUnit = tender.installationPerUnit;
      cfg.fixedMasticAmount = tender.fixedMasticAmount;
      cfg.fixedEPDMAmount = tender.fixedEPDMAmount;
      cfg.quoteExtraLabel = tender.quoteExtraLabel;
      cfg.quoteExtraAmount = tender.quoteExtraAmount;
    } else if (cfg.autoTenderPricingId === tenderId) {
      if (cfg.fixedMasticAmount === undefined) {
        cfg.fixedMasticAmount = tender.fixedMasticAmount;
        cfg.includeMastic = true;
      }
      if (cfg.fixedEPDMAmount === undefined) {
        cfg.fixedEPDMAmount = tender.fixedEPDMAmount;
        cfg.includeEPDM = true;
      }
    }
    return cfg;
  }

  function applyInferredPricingDefaults(items, cfg) {
    items = items || [];
    if (!items.length) return cfg;

    var pvcCount = 0;
    var quotedCount = 0;
    var hasExternalOpeningSchedule = false;
    var hasFensterPricingDocument = false;
    items.forEach(function (item) {
      if (/pvc|upvc/i.test(item.frameType || '')) pvcCount++;
      if (item.supplierUnitPrice !== undefined && item.supplierUnitPrice !== null && item.supplierUnitPrice !== '') quotedCount++;
      if (item.scheduleType === 'External Opening Schedule') hasExternalOpeningSchedule = true;
      if (item.scheduleType === 'Fenster Pricing Document' || item.scheduleType === 'Commercial Allowance') hasFensterPricingDocument = true;
    });

    // Fenster pricing documents are already commercial sell-rate documents.
    // They include installation/prelims as explicit rows and are presented ex VAT,
    // so do not add a second generic install line or VAT on top.
    if (hasFensterPricingDocument) {
      cfg.includeInstallation = false;
      cfg.includeEPDM = false;
      cfg.includeMastic = false;
      cfg.vatEnabled = false;
      return cfg;
    }

    // Live tender packs built from architect opening schedules need installation
    // shown as a separate commercial allowance, so keep the site default on.
    if (hasExternalOpeningSchedule) {
      cfg.includeInstallation = true;
      return cfg;
    }

    // Fenster uPVC schedule-only jobs commonly price supply/install together.
    // Keep installation for quoted workbooks/frameworks, where the workbook rates
    // usually represent supply/evaluation rows and a separate installation allowance is needed.
    if (quotedCount === 0 && pvcCount / items.length >= 0.65) {
      cfg.includeInstallation = false;
    }
    return cfg;
  }

  // =========================================================================
  // Helpers
  // =========================================================================
  function mergeConfig(user) {
    var cfg = {};
    var k;
    for (k in DEFAULT_CONFIG) {
      if (DEFAULT_CONFIG.hasOwnProperty(k)) cfg[k] = DEFAULT_CONFIG[k];
    }
    if (user) {
      for (k in user) {
        if (user.hasOwnProperty(k)) cfg[k] = user[k];
      }
    }
    return cfg;
  }

  function round2(v) { return Math.round(v * 100) / 100; }

  function fmt(v) { return formatCurrency(v); }

  function formatCurrency(value) {
    return '\u00a3' + Number(value).toLocaleString('en-GB', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }

  // =========================================================================
  // Public API
  // =========================================================================
  return {
    calculateItemPrice:  calculateItemPrice,
    recalculateAll:      recalculateAll,
    getPriceSummary:     getPriceSummary,
    formatCurrency:      formatCurrency,
    classifyProductCode: classifyProductCode,
    applyKnownItemPricing: applyKnownItemPricing,
    applyTenderPricingDefaults: applyTenderPricingDefaults,
    PRODUCT_CODES:       PRODUCT_CODES,
    KNOWN_TENDER_PRICING: KNOWN_TENDER_PRICING,
    DEFAULT_CONFIG:      DEFAULT_CONFIG
  };
})();

