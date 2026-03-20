/* js/pricing.js — Flexible pricing engine */

var Pricing = (function () {

  function calculateItemPrice(item, pricingConfig) {
    var base = pricingConfig.baseRatePerM2 || 150;
    var mults = pricingConfig.multipliers || {};

    var widthM = item.width / 1000;
    var heightM = item.height / 1000;
    var areaM2 = widthM * heightM;

    if (areaM2 <= 0) {
      return { unitPrice: 0, totalPrice: 0, breakdown: 'Dimensions not set' };
    }

    var frameMult = getFrameMultiplier(item.frameType, mults);
    var glazingMult = getGlazingMultiplier(item.glazingSpec, mults);
    var openingMult = getOpeningMultiplier(item.openingType, mults);
    var specialMult = getSpecialMultipliers(item, mults);

    var unitPrice = base * areaM2 * frameMult * glazingMult * openingMult * specialMult;
    unitPrice = Math.round(unitPrice * 100) / 100;
    var totalPrice = Math.round(unitPrice * item.quantity * 100) / 100;

    var breakdownParts = [
      formatCurrency(base) + '/m²',
      '× ' + areaM2.toFixed(2) + 'm²',
      '× ' + frameMult.toFixed(2) + ' (' + (item.frameType || 'Unknown') + ')'
    ];

    if (glazingMult !== 1.0) {
      breakdownParts.push('× ' + glazingMult.toFixed(2) + ' (Glazing)');
    }
    if (openingMult !== 1.0) {
      breakdownParts.push('× ' + openingMult.toFixed(2) + ' (' + (item.openingType || 'Opening') + ')');
    }
    if (specialMult !== 1.0) {
      breakdownParts.push('× ' + specialMult.toFixed(2) + ' (Spec)');
    }
    breakdownParts.push('= ' + formatCurrency(unitPrice));

    return {
      unitPrice: unitPrice,
      totalPrice: totalPrice,
      breakdown: breakdownParts.join(' ')
    };
  }

  function getFrameMultiplier(frameType, mults) {
    if (!frameType) return 1.0;
    var ft = frameType.toLowerCase();
    if (ft.includes('aluminium') || ft.includes('aluminum') || ft.includes('alum')) {
      return mults.aluminium !== undefined ? mults.aluminium : 1.0;
    }
    if (ft.includes('pvcu') || ft.includes('pvc-u') || ft.includes('upvc') || ft.includes('pvc')) {
      return mults.pvcu !== undefined ? mults.pvcu : 0.7;
    }
    if (ft.includes('timber') || ft.includes('wood')) {
      return mults.timber !== undefined ? mults.timber : 0.9;
    }
    if (ft.includes('steel')) {
      return 1.1;
    }
    return 1.0;
  }

  function getGlazingMultiplier(glazingSpec, mults) {
    if (!glazingSpec) return 1.0;
    var gs = glazingSpec.toLowerCase();
    var mult = 1.0;

    if (gs.includes('triple')) {
      mult *= (mults.tripleGlazed !== undefined ? mults.tripleGlazed : 1.3);
    } else {
      mult *= (mults.doubleGlazed !== undefined ? mults.doubleGlazed : 1.0);
    }

    if (gs.includes('obscure') || gs.includes('frosted')) {
      mult *= (mults.obscure !== undefined ? mults.obscure : 1.05);
    }

    return mult;
  }

  function getOpeningMultiplier(openingType, mults) {
    if (!openingType) return 1.0;
    var ot = openingType.toLowerCase();

    if (ot.includes('top hung') || ot === 'top hung') {
      return mults.topHung !== undefined ? mults.topHung : 1.1;
    }
    if (ot.includes('tilt') && ot.includes('turn')) {
      return mults.tiltAndTurn !== undefined ? mults.tiltAndTurn : 1.15;
    }
    if (ot.includes('casement')) {
      return mults.casement !== undefined ? mults.casement : 1.0;
    }
    if (ot.includes('sliding')) {
      return mults.sliding !== undefined ? mults.sliding : 1.2;
    }
    if (ot.includes('fixed')) {
      return mults.fixed !== undefined ? mults.fixed : 0.9;
    }
    return 1.0;
  }

  function getSpecialMultipliers(item, mults) {
    var mult = 1.0;
    var spec = (item.glazingSpec || '').toLowerCase();
    var notes = (item.notes || []).join(' ').toLowerCase();
    var combined = spec + ' ' + notes;

    if (combined.includes('fire rated') || combined.includes('fire-rated')) {
      mult *= (mults.fireRated !== undefined ? mults.fireRated : 1.8);
    }
    if (combined.includes('acoustic')) {
      mult *= (mults.acoustic !== undefined ? mults.acoustic : 1.4);
    }
    if (combined.includes('toughened') || combined.includes('tempered')) {
      mult *= (mults.toughened !== undefined ? mults.toughened : 1.2);
    }
    if (combined.includes('laminated')) {
      mult *= (mults.laminated !== undefined ? mults.laminated : 1.15);
    }
    if (combined.includes('trickle vent') || combined.includes('trickle-vent')) {
      mult *= (mults.trickleVent !== undefined ? mults.trickleVent : 1.05);
    }
    if (combined.includes('restrictor')) {
      mult *= (mults.restrictor !== undefined ? mults.restrictor : 1.02);
    }

    return mult;
  }

  function recalculateAll(items, pricingConfig) {
    return items.map(function (item) {
      if (item.manualOverride) return item;
      var result = calculateItemPrice(item, pricingConfig);
      return Object.assign({}, item, {
        unitPrice: result.unitPrice,
        totalPrice: result.totalPrice
      });
    });
  }

  function getPriceSummary(items, pricingConfig) {
    var subtotal = items.reduce(function (sum, item) {
      return sum + (item.totalPrice || 0);
    }, 0);

    var discountPercent = pricingConfig.discountPercent || 0;
    var discountAmount = Math.round(subtotal * discountPercent / 100 * 100) / 100;
    var afterDiscount = subtotal - discountAmount;

    var vatEnabled = pricingConfig.vatEnabled !== false;
    var vatRate = pricingConfig.vatRate || 20;
    var vatAmount = vatEnabled ? Math.round(afterDiscount * vatRate / 100 * 100) / 100 : 0;

    var total = afterDiscount + vatAmount;

    return {
      subtotal: Math.round(subtotal * 100) / 100,
      discountPercent: discountPercent,
      discountAmount: discountAmount,
      afterDiscount: Math.round(afterDiscount * 100) / 100,
      vatEnabled: vatEnabled,
      vatRate: vatRate,
      vatAmount: vatAmount,
      total: Math.round(total * 100) / 100,
      itemCount: items.length
    };
  }

  function formatCurrency(value) {
    return '£' + Number(value).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  return {
    calculateItemPrice: calculateItemPrice,
    recalculateAll: recalculateAll,
    getPriceSummary: getPriceSummary,
    formatCurrency: formatCurrency
  };
})();
