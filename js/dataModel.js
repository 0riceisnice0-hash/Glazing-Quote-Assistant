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
    pricingVersion: 3,
    aluminiumFrameRate: 500,
    aluminiumDoorRate: 1125,
    pvcFrameRate: 395,
    timberFrameRate: 350,
    steelFrameRate: 600,
    doubleGlazedRate: 55,
    tripleGlazedRate: 85,
    fireRatedGlassRate: 130,
    laminatedExtra: 15,
    toughenedExtra: 10,
    installationPerUnit: 140,
    cwSupplyRate: 850,
    cwLabourRate: 150,
    epdmRate: 25,
    masticRate: 5,
    includeInstallation: true,
    includeEPDM: false,
    includeMastic: false,
    discountPercent: 0,
    vatEnabled: true,
    vatRate: 20,
    // Split-pane pricing rates (Option 2)
    fixedPaneRate: 250,           // £/m² for fixed glass panes
    openingPaneRate: 580,         // £/m² for opening lights/casements
    louvreFlat: 450,              // £ flat premium per louvre panel
    overheadPercent: 8            // % overhead/margin baked into type code markups
  },
  presets: {
    window: {
      frameType: 'PVC',
      system: 'Liniar PVCu',
      colour: 'Black Foil',
      finish: 'Foiled',
      hardware: 'Black Signature Handle / Kenrick Shootbolt / Standard Hinges',
      cillType: '150mm Drop Nose Cill Foil',
      glazingMakeup: '28mm DGU - Unglazed',
      ventilation: '4000 External Linkvent Black / 4000 Internal Linkvent Black',
      drainage: 'Concealed'
    },
    door: {
      frameType: 'Aluminium',
      system: 'Senior SPW 500/501',
      colour: 'RAL 9005 (Jet black)',
      finish: 'Powder Coated',
      hardware: 'Pad Handles / Hook Lock / Euro Cylinder / NHO Closer',
      cillType: '',
      glazingMakeup: '28mm DGU',
      ventilation: '',
      drainage: ''
    },
    profiles: {
      'Aluminium Commercial Window': {
        frameType: 'Aluminium',
        system: 'Senior / Technal',
        colour: 'RAL (per tender docs)',
        finish: 'PPC (Powder Coated)',
        hardware: 'Standard commercial ironmongery',
        cillType: 'Aluminium Cill',
        glazingMakeup: '28mm DGU - Toughened',
        ventilation: 'Trickle Vent',
        drainage: 'Concealed'
      },
      'Aluminium Commercial Door': {
        frameType: 'Aluminium',
        system: 'Senior SPW 500/501',
        colour: 'RAL 9005 (Jet black)',
        finish: 'PPC (Powder Coated)',
        hardware: 'Pad Handles / Hook Lock / Euro Cylinder / NHO Closer',
        cillType: 'Aluminium Threshold',
        glazingMakeup: '28mm DGU - Toughened',
        ventilation: '',
        drainage: ''
      },
      'uPVC Residential Window': {
        frameType: 'PVC',
        system: 'Liniar PVCu',
        colour: 'Black Foil',
        finish: 'Foiled',
        hardware: 'Black Signature Handle / Kenrick Shootbolt / Standard Hinges',
        cillType: '150mm Drop Nose Cill Foil',
        glazingMakeup: '28mm DGU - Unglazed',
        ventilation: '4000 External Linkvent Black / 4000 Internal Linkvent Black',
        drainage: 'Concealed'
      },
      'uPVC Residential Door': {
        frameType: 'PVC',
        system: 'Liniar PVCu',
        colour: 'Black Foil',
        finish: 'Foiled',
        hardware: 'Avocet Falcon Lock / Low Threshold',
        cillType: 'Low Aluminium Threshold',
        glazingMakeup: '28mm DGU - Toughened',
        ventilation: '',
        drainage: ''
      }
    }
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
    // Supplier cost overrides (Option 1: enter actual Fenster BOQ values)
    supplierFrameCost: undefined,   // £ actual frame cost from supplier BOQ
    supplierGlassCost: undefined,   // £ actual glass cost from supplier BOQ
    supplierAdditional: 0,          // £ extras (louvres, teleflex, PAS24 etc.)
    // Pane configuration (Option 2: split-pane auto-pricing)
    fixedPanes: 0,                  // count of fixed panes in unit
    openingPanes: 0,                // count of opening lights/casements
    hasLouvre: false,                // louvre panel present
    sourceDocument: '',
    sourcePage: 0,
    textPosition: null,
    extractionMethod: '',  // 'pdf.js' | 'ocr' | 'manual'
    // Detail fields (Phase 1)
    system: '',           // e.g. 'Liniar PVCu', 'Senior SPW 501 Aluminium'
    colour: '',           // e.g. 'Grey 7016', 'RAL 9005', 'Black Foil'
    hardware: '',         // e.g. 'Black Signature Kenrick Shootbolt'
    cillType: '',         // e.g. '150mm Drop Nose Cill'
    glazingMakeup: '',    // e.g. '28mm DGU - Unglazed'
    ventilation: '',      // e.g. '4000 Linkvent', 'Trickle Vent'
    drainage: '',         // e.g. 'Concealed', 'Exposed'
    actualFrameSize: '',  // e.g. '1010 × 1020'
    escapeWindow: '',     // 'Yes', 'No', or ''
    // Phase 2 detail fields (Shaftesbury+)
    sillHeight: '',       // e.g. '0', '640' (mm above floor)
    headHeight: '',       // e.g. '2175', '2590' (mm above floor)
    uValue: '',           // e.g. '1.4 W/m2k'
    doorSwing: '',        // e.g. 'RHS', 'LHS', 'Double Door'
    fireRating: '',       // e.g. 'FD30S', 'FD60', 'N/A'
    doorFrame: '',        // e.g. '32 x 125mm sw'
    doorGlazing: '',      // e.g. '7mm AGC Glass UK - Pyrobelte 7'
    ironmongery: '',      // e.g. 'Set C3/C6', 'Doc M pack'
    finish: '',           // e.g. 'PPC Aluminium', 'Formica Laminate Finish Colour TBC'
    doorType: ''          // e.g. 'YMD Door Type 1', 'YMD Door Type 5'
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
