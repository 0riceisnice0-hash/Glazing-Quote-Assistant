/* js/pricing.js — Fenster pricing engine (from master pricing document)
 *
 * Formula:  Unit Rate = Frames + Glass + Additional + ProductCodeMarkup
 * Total  :  Qty × Unit Rate
 * Install:  Qty × £140/unit (separate line)
 * CW     :  SQM × £850 supply + SQM × £150 labour
 * EPDM   :  SQM × £25 (optional)
 * Mastic :  Perimeter(m) × £5 (optional)
 */

var Pricing = (function () {

  // =========================================================================
  // Product codes & markups — extracted from Fenster master pricing doc
  // =========================================================================
  var PRODUCT_CODES = {
    // Aluminium Windows (size-based)
    SAW:    { markup: 400,  desc: 'Small Aluminium Window' },
    MAW:    { markup: 500,  desc: 'Medium Aluminium Window' },
    LAW:    { markup: 600,  desc: 'Large Aluminium Window' },
    ELAW:   { markup: 1000, desc: 'Extra Large Aluminium Window' },
    // PVC Windows (size-based)
    SPVC:   { markup: 300,  desc: 'Small PVC Window' },
    MPVC:   { markup: 350,  desc: 'Medium PVC Window' },
    LPVC:   { markup: 400,  desc: 'Large PVC Window' },
    // Aluminium Doors
    SAD:    { markup: 1150, desc: 'Single Aluminium Door' },
    DAD:    { markup: 1950, desc: 'Double Aluminium Door' },
    // PVC Door
    UPD:    { markup: 950,  desc: 'uPVC Door' },
    // Combo units (door + sidelight)
    SADSAW: { markup: 1650, desc: 'Single Alum Door + Small Window' },
    SADMAW: { markup: 1850, desc: 'Single Alum Door + Med Window' },
    SADLAW: { markup: 1950, desc: 'Single Alum Door + Large Window' },
    // Timber Doors (estimated — not in master doc)
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
  // Default config — estimated supplier rates & fixed rates
  // =========================================================================
  var DEFAULT_CONFIG = {
    pricingVersion: 3,

    // Estimated supplier frame cost per m² (fabricated unit inc. hardware, excl. glass)
    aluminiumFrameRate: 500,
    aluminiumDoorRate: 1125,
    pvcFrameRate: 395,
    timberFrameRate: 350,
    steelFrameRate: 600,

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

    // Quote-level options
    includeInstallation: true,
    includeEPDM: false,
    includeMastic: false,

    // VAT and discount
    vatEnabled: true,
    vatRate: 20,
    discountPercent: 0
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

    // Window — classify by frame material then size
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
  function estimateFrameCost(item, config) {
    var w    = (item.width  || 0) / 1000;
    var h    = (item.height || 0) / 1000;
    var area = w * h;
    if (area <= 0) return 0;

    var frame = (item.frameType || '').toLowerCase();
    var isDoor = (item.type || '').toLowerCase() === 'door';
    var rate  = isDoor ? (config.aluminiumDoorRate || config.aluminiumFrameRate) : config.aluminiumFrameRate;

    if (frame.indexOf('pvc') !== -1 || frame.indexOf('upvc') !== -1)       rate = config.pvcFrameRate;
    else if (frame.indexOf('timber') !== -1 || frame.indexOf('wood') !== -1) rate = config.timberFrameRate;
    else if (frame.indexOf('steel') !== -1)                                  rate = config.steelFrameRate;
    else if (isDoor && config.aluminiumDoorRate)                              rate = config.aluminiumDoorRate;

    return Math.round(rate * area * 100) / 100;
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
  //   Total     = Qty × Unit Rate
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

    if (code === 'CW') {
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

    // Breakdown string
    var parts = [code];
    if (code === 'CW') {
      parts.push('Supply ' + fmt(frameCost));
      parts.push('Labour ' + fmt(markup));
    } else {
      parts.push('Frame ' + fmt(frameCost));
      if (glassCost > 0) parts.push('Glass ' + fmt(glassCost));
      if (additional > 0) parts.push('Add ' + fmt(additional));
      parts.push('Markup ' + fmt(markup));
    }
    parts.push('= ' + fmt(unitRate));
    if (qty > 1) parts.push('\u00d7' + qty + ' = ' + fmt(total));

    return {
      unitPrice:   unitRate,
      totalPrice:  total,
      installCost: inst,
      breakdown:   parts.join(' | '),
      productCode: code,
      productDesc: codeInfo.desc,
      frameCost:   frameCost,
      glassCost:   glassCost,
      additional:  additional,
      markup:      markup
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
        unitPrice:   result.unitPrice,
        totalPrice:  result.totalPrice,
        productCode: result.productCode
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
    epdmTotal    = round2(epdmTotal);
    masticTotal  = round2(masticTotal);

    var beforeDiscount = round2(subtotal + installTotal + epdmTotal + masticTotal);

    var discountPercent = config.discountPercent || 0;
    var discountAmount  = round2(beforeDiscount * discountPercent / 100);
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
      beforeDiscount:  beforeDiscount,
      discountPercent: discountPercent,
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
    PRODUCT_CODES:       PRODUCT_CODES,
    DEFAULT_CONFIG:      DEFAULT_CONFIG
  };
})();
