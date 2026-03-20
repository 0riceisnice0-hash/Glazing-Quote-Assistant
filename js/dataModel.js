/* js/dataModel.js — Central state management */

const DEFAULT_STATE = {
  items: [],
  metadata: {
    projectName: '',
    clientName: '',
    quoteNumber: '',
    quoteDate: '',
    validityDays: 30,
    notes: ''
  },
  company: {
    name: '',
    address: '',
    phone: '',
    email: '',
    logoDataUrl: null
  },
  pricing: {
    pricingVersion: 2,
    fixedCostPerUnit: 596,
    baseRatePerM2: 99,
    doorFixedCostPerUnit: 166,
    doorRatePerM2: 1644,
    multipliers: {
      aluminium: 1.0,
      pvcu: 1.0,
      timber: 0.9,
      fireRated: 1.8,
      acoustic: 1.4,
      toughened: 1.2,
      laminated: 1.15,
      tripleGlazed: 1.3,
      doubleGlazed: 1.0,
      obscure: 1.05,
      topHung: 1.0,
      casement: 1.0,
      tiltAndTurn: 1.15,
      sliding: 1.2,
      fixed: 0.95,
      trickleVent: 1.0,
      restrictor: 1.0
    },
    discountPercent: 0,
    vatEnabled: true,
    vatRate: 20
  },
  sourceDocuments: [],
  warnings: [],
  lastSaved: null
};

function generateId() {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

function createItem(partial) {
  const defaults = {
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
    extractionMethod: ''  // 'pdf.js' | 'ocr' | 'manual'
  };
  return Object.assign({}, defaults, partial);
}

function validateItem(item) {
  const errors = [];
  if (!item.reference || item.reference.trim() === '') {
    errors.push('Reference is required');
  }
  if (item.width <= 0) {
    errors.push('Width must be greater than 0');
  }
  if (item.height <= 0) {
    errors.push('Height must be greater than 0');
  }
  if (item.quantity <= 0) {
    errors.push('Quantity must be at least 1');
  }
  if (item.width > 10000) {
    errors.push('Width seems unusually large (>10,000 mm)');
  }
  if (item.height > 10000) {
    errors.push('Height seems unusually large (>10,000 mm)');
  }
  return errors;
}

function exportJSON(state) {
  const exportData = Object.assign({}, state, { lastSaved: new Date().toISOString() });
  return JSON.stringify(exportData, null, 2);
}

function importJSON(jsonString) {
  let parsed;
  try {
    parsed = JSON.parse(jsonString);
  } catch (e) {
    throw new Error('Invalid JSON: ' + e.message);
  }
  if (!parsed || typeof parsed !== 'object') {
    throw new Error('JSON must be an object');
  }
  const state = deepMerge(deepClone(DEFAULT_STATE), parsed);
  return state;
}

function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

function deepMerge(target, source) {
  for (const key of Object.keys(source)) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') continue;
    if (
      source[key] !== null &&
      typeof source[key] === 'object' &&
      !Array.isArray(source[key]) &&
      typeof target[key] === 'object' &&
      target[key] !== null &&
      !Array.isArray(target[key])
    ) {
      deepMerge(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
  return target;
}

function saveToLocalStorage(state) {
  try {
    const data = Object.assign({}, state, { lastSaved: new Date().toISOString() });
    localStorage.setItem('glazingQuoteState', JSON.stringify(data));
    return true;
  } catch (e) {
    console.warn('Could not save to localStorage:', e);
    return false;
  }
}

function loadFromLocalStorage() {
  try {
    const raw = localStorage.getItem('glazingQuoteState');
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    return deepMerge(deepClone(DEFAULT_STATE), parsed);
  } catch (e) {
    console.warn('Could not load from localStorage:', e);
    return null;
  }
}

function getNextReference(items, type) {
  const prefixMap = {
    window: 'W',
    door: 'D',
    screen: 'S',
    'curtain wall': 'C',
    other: 'X'
  };
  const prefix = prefixMap[type] || 'X';
  const existing = items
    .filter(i => i.reference && i.reference.startsWith(prefix))
    .map(i => {
      const num = parseInt(i.reference.replace(prefix, ''), 10);
      return isNaN(num) ? 0 : num;
    });
  const max = existing.length > 0 ? Math.max(...existing) : 0;
  return prefix + String(max + 1).padStart(2, '0');
}
