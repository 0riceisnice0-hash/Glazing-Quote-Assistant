/* js/ui.js — Full UI rendering and interaction */

var UI = (function () {

  var _state = null;
  var _callbacks = {};
  var _sortColumn = null;
  var _sortDir = 'asc';
  var _searchQuery = '';
  var _filters = { type: '', frame: '', confidence: '', location: '' };

  var TOAST_ICONS = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
  var TYPE_OPTIONS = ['window', 'door', 'screen', 'curtain wall', 'other'];
  var FRAME_OPTIONS = ['Aluminium', 'PVCu', 'Timber', 'Steel', 'Unknown'];
  var OPENING_OPTIONS = ['Fixed', 'Casement', 'Top Hung', 'Tilt & Turn', 'Sliding', 'Pivot', 'Bi-fold'];
  var CONFIDENCE_OPTIONS = ['high', 'medium', 'low'];

  function initUI(state, callbacks) {
    _state = state;
    _callbacks = callbacks || {};

    _setupThemeToggle();
    _setupNavTabs();
    _setupStep1();
    _setupPricingPanel();
    _setupPresetEditor();
    _setupCompanyForm();
    _setupQuoteMetaForm();
    _setupExportImport();
    _setupManualAddItem();

    renderStep(1);
    _updateSummaryBar();
  }

  function _setupThemeToggle() {
    var btn = document.getElementById('darkModeToggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      document.body.classList.toggle('dark-mode');
      var isDark = document.body.classList.contains('dark-mode');
      btn.textContent = isDark ? '☀️' : '🌙';
      localStorage.setItem('darkMode', isDark ? '1' : '0');
      if (_callbacks.onDarkModeToggle) _callbacks.onDarkModeToggle(isDark);
    });
    var stored = localStorage.getItem('darkMode');
    if (stored === '1') {
      document.body.classList.add('dark-mode');
      btn.textContent = '☀️';
    }
  }

  function _setupNavTabs() {
    var tabs = document.querySelectorAll('.wizard-step-tab');
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var step = parseInt(tab.dataset.step, 10);
        if (tab.classList.contains('disabled')) return;
        if (_callbacks.onBeforeStepChange) _callbacks.onBeforeStepChange(step);
        renderStep(step);
      });
    });
  }

  function _setupStep1() {
    var dropZone = document.getElementById('dropZone');
    var fileInput = document.getElementById('fileInput');
    if (!dropZone || !fileInput) return;
    initDropZone(dropZone, fileInput, function (files) {
      if (_callbacks.onFilesAdded) _callbacks.onFilesAdded(files);
    });
  }

  function _setupPricingPanel() {
    // Bind all numeric rate inputs
    var rateFields = [
      'aluminiumFrameRate', 'aluminiumDoorRate', 'pvcFrameRate', 'timberFrameRate', 'steelFrameRate',
      'doubleGlazedRate', 'tripleGlazedRate', 'fireRatedGlassRate', 'toughenedExtra',
      'installationPerUnit', 'cwSupplyRate', 'cwLabourRate', 'epdmRate', 'masticRate'
    ];
    rateFields.forEach(function (field) {
      var el = document.getElementById(field);
      if (!el) return;
      el.value = _state.pricing[field] !== undefined ? _state.pricing[field] : (Pricing.DEFAULT_CONFIG[field] || 0);
      el.addEventListener('change', function () {
        _state.pricing[field] = parseFloat(el.value) || 0;
        _triggerPriceUpdate();
      });
    });

    // Checkbox toggles
    var toggleFields = ['includeInstallation', 'includeEPDM', 'includeMastic'];
    toggleFields.forEach(function (field) {
      var el = document.getElementById(field);
      if (!el) return;
      el.checked = _state.pricing[field] !== undefined ? _state.pricing[field] : (Pricing.DEFAULT_CONFIG[field] || false);
      el.addEventListener('change', function () {
        _state.pricing[field] = el.checked;
        _triggerPriceUpdate();
      });
    });

    // Discount
    var discountInput = document.getElementById('discountPercent');
    if (discountInput) {
      discountInput.value = _state.pricing.discountPercent || 0;
      discountInput.addEventListener('change', function () {
        _state.pricing.discountPercent = parseFloat(discountInput.value) || 0;
        _triggerPriceUpdate();
      });
    }

    // VAT
    var vatToggle = document.getElementById('vatEnabled');
    if (vatToggle) {
      vatToggle.checked = _state.pricing.vatEnabled !== false;
      vatToggle.addEventListener('change', function () {
        _state.pricing.vatEnabled = vatToggle.checked;
        _triggerPriceUpdate();
      });
    }
    var vatRate = document.getElementById('vatRate');
    if (vatRate) {
      vatRate.value = _state.pricing.vatRate || 20;
      vatRate.addEventListener('change', function () {
        _state.pricing.vatRate = parseFloat(vatRate.value) || 20;
        _triggerPriceUpdate();
      });
    }

    // Product code markup reference grid (read-only)
    _renderProductCodeGrid();
  }

  function _renderProductCodeGrid() {
    var container = document.getElementById('productCodeGrid');
    if (!container) return;
    container.innerHTML = '';
    var codes = Pricing.PRODUCT_CODES;
    Object.keys(codes).forEach(function (key) {
      var info = codes[key];
      var div = document.createElement('div');
      div.style.cssText = 'display:flex;justify-content:space-between;padding:2px 6px;background:var(--bg);border-radius:4px';
      div.innerHTML = '<span style="font-weight:600">' + key + '</span><span>' +
        (info.markup > 0 ? Pricing.formatCurrency(info.markup) : 'per m\u00b2') + '</span>';
      div.title = info.desc;
      container.appendChild(div);
    });
  }

  function _setupPresetEditor() {
    var fields = document.querySelectorAll('.preset-field');
    fields.forEach(function (input) {
      var presetType = input.dataset.preset;  // 'window' or 'door'
      var fieldName = input.dataset.field;     // 'system', 'colour' etc.
      if (_state.presets && _state.presets[presetType]) {
        input.value = _state.presets[presetType][fieldName] || '';
      }
      input.addEventListener('change', function () {
        if (!_state.presets) _state.presets = {};
        if (!_state.presets[presetType]) _state.presets[presetType] = {};
        _state.presets[presetType][fieldName] = input.value.trim();
        if (_callbacks.onStateChange) _callbacks.onStateChange();
      });
    });

    var profileSelect = document.getElementById('presetProfileSelect');
    var profileApplyBtn = document.getElementById('presetProfileApplyBtn');
    if (profileSelect && profileApplyBtn) {
      profileApplyBtn.addEventListener('click', function () {
        var profileName = profileSelect.value;
        if (!profileName) return;
        var profiles = (_state.presets && _state.presets.profiles) || {};
        var profile = profiles[profileName];
        if (!profile) { showToast('Profile not found: ' + profileName, 'warning'); return; }
        var targetType = /window/i.test(profileName) ? 'window' : 'door';
        if (!_state.presets) _state.presets = {};
        if (!_state.presets[targetType]) _state.presets[targetType] = {};
        Object.keys(profile).forEach(function (key) {
          _state.presets[targetType][key] = profile[key];
        });
        fields.forEach(function (input) {
          if (input.dataset.preset === targetType) {
            input.value = _state.presets[targetType][input.dataset.field] || '';
          }
        });
        if (_callbacks.onStateChange) _callbacks.onStateChange();
        showToast('Loaded profile: ' + profileName, 'success');
      });
    }
  }

  function _setupCompanyForm() {
    var fields = ['companyName', 'companyAddress', 'companyPhone', 'companyEmail'];
    var stateFields = ['name', 'address', 'phone', 'email'];
    fields.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (!el) return;
      el.value = _state.company[stateFields[i]] || '';
      el.addEventListener('input', function () {
        _state.company[stateFields[i]] = el.value;
        if (_callbacks.onStateChange) _callbacks.onStateChange();
      });
    });

    var logoInput = document.getElementById('logoFileInput');
    var logoPreview = document.getElementById('logoPreview');
    if (logoInput) {
      logoInput.addEventListener('change', function () {
        var file = logoInput.files[0];
        if (!file) return;
        var reader = new FileReader();
        reader.onload = function (e) {
          _state.company.logoDataUrl = e.target.result;
          if (logoPreview) {
            logoPreview.src = e.target.result;
            logoPreview.classList.remove('hidden');
          }
          if (_callbacks.onStateChange) _callbacks.onStateChange();
        };
        reader.readAsDataURL(file);
      });
    }

    if (logoPreview && _state.company.logoDataUrl) {
      logoPreview.src = _state.company.logoDataUrl;
      logoPreview.classList.remove('hidden');
    }
  }

  function _setupQuoteMetaForm() {
    var mapping = [
      { id: 'projectName', key: 'projectName' },
      { id: 'clientName', key: 'clientName' },
      { id: 'quoteNumber', key: 'quoteNumber' },
      { id: 'quoteDate', key: 'quoteDate' },
      { id: 'validityDays', key: 'validityDays' },
      { id: 'quoteNotes', key: 'notes' }
    ];
    mapping.forEach(function (m) {
      var el = document.getElementById(m.id);
      if (!el) return;
      el.value = _state.metadata[m.key] || '';
      el.addEventListener('input', function () {
        _state.metadata[m.key] = el.value;
        if (_callbacks.onStateChange) _callbacks.onStateChange();
      });
    });
  }

  function _setupExportImport() {
    var exportBtn = document.getElementById('exportJsonBtn');
    if (exportBtn) {
      exportBtn.addEventListener('click', function () {
        if (_callbacks.onExportJSON) _callbacks.onExportJSON();
      });
    }

    var importInput = document.getElementById('importJsonInput');
    if (importInput) {
      importInput.addEventListener('change', function () {
        var file = importInput.files[0];
        if (!file) return;
        var reader = new FileReader();
        reader.onload = function (e) {
          if (_callbacks.onImportJSON) _callbacks.onImportJSON(e.target.result);
        };
        reader.readAsText(file);
        importInput.value = '';
      });
    }
  }

  function _setupManualAddItem() {
    var btn = document.getElementById('addItemBtn');
    if (btn) {
      btn.addEventListener('click', function () {
        if (_callbacks.onAddItem) _callbacks.onAddItem();
      });
    }

    // Preset buttons
    var winPresetBtn = document.getElementById('applyWindowPresetBtn');
    if (winPresetBtn) {
      winPresetBtn.addEventListener('click', function () { _applyPreset('window'); });
    }
    var doorPresetBtn = document.getElementById('applyDoorPresetBtn');
    if (doorPresetBtn) {
      doorPresetBtn.addEventListener('click', function () { _applyPreset('door'); });
    }

    // Step-1 "Add Items Manually" button — go directly to the table view
    var btnStep1 = document.getElementById('addItemBtnStep1');
    if (btnStep1) {
      btnStep1.addEventListener('click', function () {
        showTableView();
        renderStep(2);
        setTimeout(function () {
          if (_callbacks.onAddItem) _callbacks.onAddItem();
        }, 100);
      });
    }
  }

  function renderStep(stepNumber) {
    document.querySelectorAll('.step-panel').forEach(function (p) { p.classList.remove('active'); });
    var panel = document.getElementById('step' + stepNumber);
    if (panel) panel.classList.add('active');

    document.querySelectorAll('.wizard-step-tab').forEach(function (t) {
      t.classList.remove('active');
      var s = parseInt(t.dataset.step, 10);
      if (s === stepNumber) t.classList.add('active');
      if (s < stepNumber) t.classList.add('completed');
      else if (s > stepNumber) t.classList.remove('completed');
    });

    if (stepNumber === 2) {
      // When navigating to step 2 via tab or back button, always show the table
      showTableView();
      renderItemsTable(_state.items, _state.warnings);
      renderWarningsPanel(_state.warnings, _state.items);
      renderSourceDocuments(_state.sourceDocuments);
      _updateSummaryBar();
    }
    if (stepNumber === 3) {
      renderQuoteMeta();
      renderPricingPreview();
    }
  }

  function showPDFVerifyView(docResults, items, onConfirm) {
    var verifyPanel = document.getElementById('pdfVerifyPanel');
    var tablePanel = document.getElementById('tableReviewPanel');
    if (verifyPanel) verifyPanel.classList.remove('hidden');
    if (tablePanel) tablePanel.classList.add('hidden');

    var container = document.getElementById('pdfViewerContainer');
    if (container) {
      PDFViewer.init(docResults, items, container, {
        onConfirm: function (acceptedItems) {
          if (onConfirm) onConfirm(acceptedItems);
          showTableView();
        }
      });
    }
  }

  function showTableView() {
    var verifyPanel = document.getElementById('pdfVerifyPanel');
    var tablePanel = document.getElementById('tableReviewPanel');
    if (verifyPanel) verifyPanel.classList.add('hidden');
    if (tablePanel) tablePanel.classList.remove('hidden');
    PDFViewer.destroy();
  }

  function renderItemsTable(items, warnings) {
    var container = document.getElementById('itemsTableContainer');
    if (!container) return;

    if (!items || items.length === 0) {
      container.innerHTML = _emptyStateHTML();
      return;
    }

    var filtered = _applyFiltersAndSearch(items);

    var html = '<div class="table-container"><table class="items-table" id="itemsTable">' +
      _buildTableHead() +
      '<tbody>' +
      filtered.map(function (item) { return _buildTableRow(item, warnings); }).join('') +
      '</tbody></table></div>';

    container.innerHTML = html;
    setupInlineEditing(document.getElementById('itemsTable'));
    _updateSummaryBar();
  }

  function _emptyStateHTML() {
    return '<div class="empty-state">' +
      '<span class="empty-icon">📋</span>' +
      '<h3>No items yet</h3>' +
      '<p>Upload PDF documents and click "Analyse Documents" to extract glazing items,<br>or add items manually using the button below.</p>' +
      '</div>';
  }

  function _buildTableHead() {
    var cols = [
      { key: 'reference', label: 'Ref', class: '' },
      { key: 'type', label: 'Type', class: '' },
      { key: 'location', label: 'Location', class: '' },
      { key: 'width', label: 'W (mm)', class: 'text-right' },
      { key: 'height', label: 'H (mm)', class: 'text-right' },
      { key: 'quantity', label: 'Qty', class: 'text-right' },
      { key: 'frameType', label: 'Frame', class: '' },
      { key: 'colour', label: 'Colour', class: '' },
      { key: 'finish', label: 'Finish', class: '' },
      { key: 'system', label: 'System', class: '' },
      { key: 'glazingSpec', label: 'Glazing', class: '' },
      { key: 'openingType', label: 'Opening', class: '' },
      { key: 'fireRating', label: 'Fire', class: '' },
      { key: 'doorSwing', label: 'Swing', class: '' },
      { key: 'ironmongery', label: 'Ironmongery', class: '' },
      { key: 'uValue', label: 'U-Val', class: '' },
      { key: 'notes', label: 'Notes', class: '' },
      { key: 'productCode', label: 'Code', class: 'text-center' },
      { key: 'unitPrice', label: 'Unit Price', class: 'text-right' },
      { key: 'totalPrice', label: 'Total', class: 'text-right' },
      { key: 'confidence', label: 'Conf.', class: 'text-center' },
      { key: 'actions', label: '', class: '' }
    ];

    return '<thead><tr>' + cols.map(function (c) {
      var sortClass = _sortColumn === c.key ? (_sortDir === 'asc' ? 'sorted-asc' : 'sorted-desc') : '';
      var sortable = c.key !== 'actions' ? 'onclick="UI._sortBy(\'' + c.key + '\')"' : '';
      return '<th class="' + c.class + ' ' + sortClass + '" ' + sortable + '>' + c.label + '</th>';
    }).join('') + '</tr></thead>';
  }

  function _buildTableRow(item, warnings) {
    var hasWarning = warnings && warnings.some(function (w) { return w.itemId === item.id; });
    var rowClass = hasWarning ? 'has-warning' : '';

    return '<tr data-item-id="' + item.id + '" class="' + rowClass + '">' +
      _editableCell(item.id, 'reference', item.reference || '-') +
      _selectCell(item.id, 'type', item.type, TYPE_OPTIONS) +
      _editableCell(item.id, 'location', item.location || '') +
      _numericCell(item.id, 'width', item.width) +
      _numericCell(item.id, 'height', item.height) +
      _numericCell(item.id, 'quantity', item.quantity) +
      _selectCell(item.id, 'frameType', item.frameType, FRAME_OPTIONS) +
      _editableCell(item.id, 'colour', item.colour || '') +
      _editableCell(item.id, 'finish', item.finish || '') +
      _editableCell(item.id, 'system', item.system || '') +
      _editableCell(item.id, 'glazingSpec', item.glazingSpec || '') +
      _selectCell(item.id, 'openingType', item.openingType, OPENING_OPTIONS) +
      _editableCell(item.id, 'fireRating', item.fireRating || '') +
      _editableCell(item.id, 'doorSwing', item.doorSwing || '') +
      _editableCell(item.id, 'ironmongery', item.ironmongery || '') +
      _editableCell(item.id, 'uValue', item.uValue || '') +
      '<td class="text-muted" style="font-size:0.75rem">' + (item.notes || []).join(', ') + '</td>' +
      '<td class="text-center font-mono" style="font-size:0.75rem;font-weight:600">' + (item.productCode || Pricing.classifyProductCode(item)) + '</td>' +
      '<td class="text-right font-mono">' + Pricing.formatCurrency(item.unitPrice) + '</td>' +
      '<td class="text-right font-mono"><strong>' + Pricing.formatCurrency(item.totalPrice) + '</strong></td>' +
      '<td class="text-center"><span class="badge ' + item.confidence + '">' + (item.confidence || 'low') + '</span></td>' +
      '<td><div class="row-actions">' +
      '<button class="btn-row-action" title="Edit" onclick="UI._editItem(\'' + item.id + '\')">✏️</button>' +
      '<button class="btn-row-action duplicate" title="Duplicate" onclick="UI._duplicateItem(\'' + item.id + '\')">📋</button>' +
      '<button class="btn-row-action delete" title="Delete" onclick="UI._deleteItem(\'' + item.id + '\')">🗑️</button>' +
      '</div></td>' +
      '</tr>';
  }

  function _editableCell(itemId, field, value) {
    return '<td class="editable-cell" data-item-id="' + itemId + '" data-field="' + field + '">' +
      _escapeHtml(String(value)) + '</td>';
  }

  function _numericCell(itemId, field, value) {
    return '<td class="editable-cell text-right" data-item-id="' + itemId + '" data-field="' + field + '">' +
      (value > 0 ? value : '<span class="text-muted">—</span>') + '</td>';
  }

  function _selectCell(itemId, field, value, options) {
    return '<td class="editable-cell" data-item-id="' + itemId + '" data-field="' + field + '" data-type="select" data-options="' +
      options.join('|') + '">' + _escapeHtml(value || '') + '</td>';
  }

  function setupInlineEditing(tableEl) {
    if (!tableEl) return;
    tableEl.querySelectorAll('.editable-cell').forEach(function (cell) {
      cell.addEventListener('click', function (e) {
        if (cell.classList.contains('editing')) return;
        _activateCellEdit(cell);
      });
    });
  }

  function _activateCellEdit(cell) {
    var itemId = cell.dataset.itemId;
    var field = cell.dataset.field;
    var currentValue = _getItemFieldValue(itemId, field);
    var isSelect = cell.dataset.type === 'select';
    var options = isSelect ? (cell.dataset.options || '').split('|') : [];

    cell.classList.add('editing');
    cell.dataset.originalContent = cell.innerHTML;

    var input;
    if (isSelect) {
      input = document.createElement('select');
      input.className = 'cell-select';
      options.forEach(function (opt) {
        var o = document.createElement('option');
        o.value = opt;
        o.textContent = opt;
        if (opt === currentValue) o.selected = true;
        input.appendChild(o);
      });
    } else {
      input = document.createElement('input');
      input.className = 'cell-input';
      input.type = ['width', 'height', 'quantity'].includes(field) ? 'number' : 'text';
      input.value = currentValue || '';
      if (input.type === 'number') input.min = '0';
    }

    cell.innerHTML = '';
    cell.appendChild(input);
    input.focus();
    if (input.type === 'text' || input.type === 'number') input.select();

    function commitEdit() {
      var newVal = isSelect ? input.value : input.value.trim();
      cell.classList.remove('editing');
      _updateItemField(itemId, field, newVal);
      cell.innerHTML = _escapeHtml(String(newVal || ''));
      var row = cell.closest('tr');
      if (row) { row.classList.add('row-changed'); setTimeout(function () { row.classList.remove('row-changed'); }, 700); }
    }

    function cancelEdit() {
      cell.classList.remove('editing');
      cell.innerHTML = cell.dataset.originalContent;
    }

    input.addEventListener('blur', commitEdit);
    input.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') { e.preventDefault(); input.blur(); }
      if (e.key === 'Escape') { input.removeEventListener('blur', commitEdit); cancelEdit(); }
      if (e.key === 'Tab') { commitEdit(); }
    });
  }

  function _getItemFieldValue(itemId, field) {
    var item = _state.items.find(function (i) { return i.id === itemId; });
    return item ? item[field] : '';
  }

  function _updateItemField(itemId, field, value) {
    var item = _state.items.find(function (i) { return i.id === itemId; });
    if (!item) return;

    var numFields = ['width', 'height', 'quantity'];
    if (numFields.includes(field)) {
      item[field] = parseFloat(value) || 0;
    } else {
      item[field] = value;
    }

    item.description = item.reference + ' ' + item.type;
    if (_callbacks.onItemUpdated) _callbacks.onItemUpdated(item);
    _updateSummaryBar();
  }

  function _applyFiltersAndSearch(items) {
    return items.filter(function (item) {
      if (_searchQuery) {
        var q = _searchQuery.toLowerCase();
        var searchable = [item.reference, item.type, item.location, item.frameType, item.glazingSpec, item.description].join(' ').toLowerCase();
        if (!searchable.includes(q)) return false;
      }
      if (_filters.type && item.type !== _filters.type) return false;
      if (_filters.frame && item.frameType !== _filters.frame) return false;
      if (_filters.confidence && item.confidence !== _filters.confidence) return false;
      if (_filters.location && item.location !== _filters.location) return false;
      return true;
    }).sort(function (a, b) {
      if (!_sortColumn) return 0;
      var va = a[_sortColumn];
      var vb = b[_sortColumn];
      if (typeof va === 'number' && typeof vb === 'number') {
        return _sortDir === 'asc' ? va - vb : vb - va;
      }
      va = String(va || '').toLowerCase();
      vb = String(vb || '').toLowerCase();
      if (va < vb) return _sortDir === 'asc' ? -1 : 1;
      if (va > vb) return _sortDir === 'asc' ? 1 : -1;
      return 0;
    });
  }

  function _sortBy(column) {
    if (_sortColumn === column) {
      _sortDir = _sortDir === 'asc' ? 'desc' : 'asc';
    } else {
      _sortColumn = column;
      _sortDir = 'asc';
    }
    renderItemsTable(_state.items, _state.warnings);
  }

  function renderWarningsPanel(warnings, items) {
    var container = document.getElementById('warningsList');
    var countBadge = document.getElementById('warningsCount');
    if (!container) return;

    if (!warnings || warnings.length === 0) {
      container.innerHTML = '<div class="empty-state" style="padding:20px"><span style="font-size:2rem">✅</span><p>No warnings</p></div>';
      if (countBadge) countBadge.classList.add('hidden');
      return;
    }

    if (countBadge) {
      countBadge.textContent = warnings.length;
      countBadge.classList.remove('hidden');
    }

    var grouped = { error: [], warning: [], info: [] };
    warnings.forEach(function (w) {
      var sev = w.severity || 'warning';
      if (!grouped[sev]) grouped[sev] = [];
      grouped[sev].push(w);
    });

    var html = '';
    ['error', 'warning', 'info'].forEach(function (sev) {
      var group = grouped[sev];
      if (!group || group.length === 0) return;
      html += '<div class="warning-group"><div style="font-size:0.75rem;font-weight:700;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:6px;color:var(--text-muted)">' + sev + 's (' + group.length + ')</div>';
      group.forEach(function (w) {
        html += '<div class="warning-item ' + sev + '">' +
          '<div class="warning-msg">' + _escapeHtml(w.message) + '</div>' +
          (w.itemId ? '<button class="warning-link" onclick="UI.highlightItem(\'' + w.itemId + '\')">→ Go to item</button>' : '') +
          '</div>';
      });
      html += '</div>';
    });

    container.innerHTML = html;
  }

  function renderPricingSummary(summary) {
    var el = document.getElementById('priceSummaryPanel');
    if (!el) return;
    var fc = Pricing.formatCurrency;
    var rows = '<tr><td>Product Subtotal (' + summary.itemCount + ' items)</td><td>' + fc(summary.subtotal) + '</td></tr>';
    if (summary.includeInstallation) {
      rows += '<tr><td>Installation</td><td>' + fc(summary.installTotal) + '</td></tr>';
    }
    if (summary.includeEPDM) {
      rows += '<tr><td>EPDM</td><td>' + fc(summary.epdmTotal) + '</td></tr>';
    }
    if (summary.includeMastic) {
      rows += '<tr><td>Mastic</td><td>' + fc(summary.masticTotal) + '</td></tr>';
    }
    if (summary.discountAmount > 0) {
      rows += '<tr><td>Discount (' + summary.discountPercent + '%)</td><td style="color:var(--accent-danger)">\u2212 ' + fc(summary.discountAmount) + '</td></tr>';
      rows += '<tr><td>After Discount</td><td>' + fc(summary.afterDiscount) + '</td></tr>';
    }
    if (summary.vatEnabled) {
      rows += '<tr><td>VAT (' + summary.vatRate + '%)</td><td>' + fc(summary.vatAmount) + '</td></tr>';
    }
    rows += '<tr class="total-row"><td>TOTAL</td><td>' + fc(summary.total) + '</td></tr>';
    el.innerHTML = '<table class="price-summary-table">' + rows + '</table>';
  }

  function renderPricingSettings(pricingConfig) {
    _state.pricing = pricingConfig;
    var rateFields = [
      'aluminiumFrameRate', 'aluminiumDoorRate', 'pvcFrameRate', 'timberFrameRate', 'steelFrameRate',
      'doubleGlazedRate', 'tripleGlazedRate', 'fireRatedGlassRate', 'toughenedExtra',
      'installationPerUnit', 'cwSupplyRate', 'cwLabourRate', 'epdmRate', 'masticRate'
    ];
    rateFields.forEach(function (field) {
      var el = document.getElementById(field);
      if (el) el.value = pricingConfig[field] !== undefined ? pricingConfig[field] : '';
    });
    var toggleFields = ['includeInstallation', 'includeEPDM', 'includeMastic'];
    toggleFields.forEach(function (field) {
      var el = document.getElementById(field);
      if (el) el.checked = !!pricingConfig[field];
    });
    var disc = document.getElementById('discountPercent');
    if (disc) disc.value = pricingConfig.discountPercent || 0;
    var vat = document.getElementById('vatEnabled');
    if (vat) vat.checked = pricingConfig.vatEnabled !== false;
    var vatRateEl = document.getElementById('vatRate');
    if (vatRateEl) vatRateEl.value = pricingConfig.vatRate || 20;
    _renderProductCodeGrid();
  }

  function renderCompanyForm(company) {
    _state.company = company;
    var fields = { companyName: 'name', companyAddress: 'address', companyPhone: 'phone', companyEmail: 'email' };
    Object.keys(fields).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.value = company[fields[id]] || '';
    });
  }

  function renderQuoteMetaForm(metadata) {
    _state.metadata = metadata;
    var mapping = { projectName: 'projectName', clientName: 'clientName', quoteNumber: 'quoteNumber', quoteDate: 'quoteDate', validityDays: 'validityDays', quoteNotes: 'notes' };
    Object.keys(mapping).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.value = metadata[mapping[id]] || '';
    });
  }

  function renderQuoteMeta() {
    renderQuoteMetaForm(_state.metadata);
    renderCompanyForm(_state.company);

    var summaryEl = document.getElementById('step3PriceSummary');
    if (summaryEl) {
      var s = Pricing.getPriceSummary(_state.items, _state.pricing);
      var fc = Pricing.formatCurrency;
      var rows = '<tr><td>Product Subtotal (' + s.itemCount + ' items)</td><td>' + fc(s.subtotal) + '</td></tr>';
      if (s.includeInstallation) rows += '<tr><td>Installation</td><td>' + fc(s.installTotal) + '</td></tr>';
      if (s.includeEPDM) rows += '<tr><td>EPDM</td><td>' + fc(s.epdmTotal) + '</td></tr>';
      if (s.includeMastic) rows += '<tr><td>Mastic</td><td>' + fc(s.masticTotal) + '</td></tr>';
      if (s.discountAmount > 0) {
        rows += '<tr><td>Discount (' + s.discountPercent + '%)</td><td style="color:var(--accent-danger)">\u2212 ' + fc(s.discountAmount) + '</td></tr>';
        rows += '<tr><td>After Discount</td><td>' + fc(s.afterDiscount) + '</td></tr>';
      }
      if (s.vatEnabled) rows += '<tr><td>VAT (' + s.vatRate + '%)</td><td>' + fc(s.vatAmount) + '</td></tr>';
      rows += '<tr class="total-row"><td>TOTAL</td><td>' + fc(s.total) + '</td></tr>';
      summaryEl.innerHTML = '<table class="price-summary-table">' + rows + '</table>';
    }
  }

  function renderPricingPreview() {
    var previewEl = document.getElementById('quotePreview');
    if (!previewEl) return;

    var meta = _state.metadata;
    var company = _state.company;
    var summary = Pricing.getPriceSummary(_state.items, _state.pricing);

    previewEl.innerHTML =
      '<div class="qp-header">' +
      '<div>' +
      '<div class="qp-company-name">' + _escapeHtml(company.name || 'Your Company') + '</div>' +
      '<div style="font-size:0.8rem;color:#555;margin-top:4px">' + _escapeHtml(company.address ? company.address.replace(/\n/g, ', ') : '') + '</div>' +
      '</div>' +
      '<div style="text-align:right">' +
      '<div class="qp-title">QUOTATION</div>' +
      '<div style="font-size:0.9rem;color:#555">' + _escapeHtml(meta.quoteNumber || 'GQ-DRAFT') + '</div>' +
      '</div>' +
      '</div>' +
      '<div class="qp-meta-grid">' +
      '<div class="qp-meta-label">Project:</div><div class="qp-meta-value">' + _escapeHtml(meta.projectName || '—') + '</div>' +
      '<div class="qp-meta-label">Client:</div><div class="qp-meta-value">' + _escapeHtml(meta.clientName || '—') + '</div>' +
      '<div class="qp-meta-label">Date:</div><div class="qp-meta-value">' + _escapeHtml(meta.quoteDate || '—') + '</div>' +
      '<div class="qp-meta-label">Valid for:</div><div class="qp-meta-value">' + (meta.validityDays || 30) + ' days</div>' +
      '</div>' +
      '<hr class="section-divider">' +
      '<div style="font-size:0.85rem;font-weight:600;margin-bottom:8px">' + _state.items.length + ' items • ' + Pricing.formatCurrency(summary.total) + ' total (inc. VAT)</div>' +
      '<p style="font-size:0.8rem;color:#666;font-style:italic">Full itemised schedule will appear in the generated PDF.</p>';
  }

  function _updateSummaryBar() {
    var items = _state.items || [];
    var summary = Pricing.getPriceSummary(items, _state.pricing);

    var setVal = function (id, val) { var el = document.getElementById(id); if (el) el.textContent = val; };

    setVal('statItemCount', items.length);
    setVal('statSubtotal', Pricing.formatCurrency(summary.subtotal));
    setVal('statTotal', Pricing.formatCurrency(summary.total));

    var warnings = (_state.warnings || []).filter(function (w) { return w.severity === 'error'; });
    setVal('statWarnings', warnings.length);

    var priceSummaryPanel = document.getElementById('priceSummaryPanel');
    if (priceSummaryPanel) renderPricingSummary(summary);
  }

  function highlightItem(itemId) {
    renderStep(2);
    setTimeout(function () {
      var row = document.querySelector('tr[data-item-id="' + itemId + '"]');
      if (row) {
        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        row.classList.add('row-highlight');
        setTimeout(function () { row.classList.remove('row-highlight'); }, 2500);
      }
    }, 100);
  }

  function showToast(message, type) {
    type = type || 'info';
    var container = document.getElementById('toastContainer');
    if (!container) return;

    var toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML =
      '<span class="toast-icon">' + (TOAST_ICONS[type] || 'ℹ️') + '</span>' +
      '<span class="toast-msg">' + _escapeHtml(message) + '</span>' +
      '<button class="toast-dismiss" onclick="this.closest(\'.toast\').remove()">✕</button>';

    container.appendChild(toast);

    setTimeout(function () {
      toast.classList.add('hiding');
      setTimeout(function () { if (toast.parentNode) toast.parentNode.removeChild(toast); }, 280);
    }, 4500);
  }

  function showModal(title, contentHTML, actions) {
    var backdrop = document.getElementById('modalBackdrop');
    var modalTitle = document.getElementById('modalTitle');
    var modalBody = document.getElementById('modalBody');
    var modalFooter = document.getElementById('modalFooter');
    if (!backdrop) return;

    if (modalTitle) modalTitle.textContent = title;
    if (modalBody) modalBody.innerHTML = contentHTML;

    if (modalFooter && actions) {
      modalFooter.innerHTML = '';
      actions.forEach(function (action) {
        var btn = document.createElement('button');
        btn.className = 'btn ' + (action.class || 'btn-secondary');
        btn.textContent = action.label;
        btn.addEventListener('click', function () {
          if (action.onClick) action.onClick();
          if (action.close !== false) closeModal();
        });
        modalFooter.appendChild(btn);
      });
    }

    backdrop.classList.remove('hidden');
  }

  function closeModal() {
    var backdrop = document.getElementById('modalBackdrop');
    if (backdrop) backdrop.classList.add('hidden');
  }

  function showLoadingOverlay(message, subMessage) {
    var overlay = document.getElementById('loadingOverlay');
    var text = document.getElementById('loadingText');
    var sub = document.getElementById('loadingSub');
    if (!overlay) return;
    if (text) text.textContent = message || 'Processing…';
    if (sub) sub.textContent = subMessage || '';
    overlay.classList.remove('hidden');
  }

  function updateLoadingMessage(message, subMessage) {
    var text = document.getElementById('loadingText');
    var sub = document.getElementById('loadingSub');
    if (text) text.textContent = message || '';
    if (sub) sub.textContent = subMessage || '';
  }

  function hideLoadingOverlay() {
    var overlay = document.getElementById('loadingOverlay');
    if (overlay) overlay.classList.add('hidden');
  }

  function updateFileList(files) {
    var list = document.getElementById('fileList');
    if (!list) return;

    if (!files || files.length === 0) {
      list.innerHTML = '';
      return;
    }

    list.innerHTML = files.map(function (f, i) {
      return '<li class="file-item">' +
        '<span class="file-icon">📄</span>' +
        '<span class="file-name">' + _escapeHtml(f.name) + '</span>' +
        '<span class="file-status" id="fileStatus_' + i + '">Ready</span>' +
        '<button class="file-remove" onclick="App.removeFile(' + i + ')">Remove</button>' +
        '</li>';
    }).join('');
  }

  function updateFileStatus(index, status) {
    var el = document.getElementById('fileStatus_' + index);
    if (el) el.textContent = status;
  }

  function _editItem(itemId) {
    var item = _state.items.find(function (i) { return i.id === itemId; });
    if (!item) return;

    var DRAINAGE_OPTIONS = ['', 'Concealed', 'Exposed', 'N/A'];
    var ESCAPE_OPTIONS = ['', 'Yes', 'No'];

    var SWING_OPTIONS = ['', 'LHS', 'RHS', 'Double'];
    var DOOR_TYPE_OPTIONS = ['', 'Single', 'Double', 'Sliding', 'Revolving', 'Bi-fold'];

    var formHTML = '<div class="form-grid">' +
      _formField('Reference', 'edit_reference', item.reference, 'text') +
      _formField('Type', 'edit_type', item.type, 'select', TYPE_OPTIONS) +
      _formField('Width (mm)', 'edit_width', item.width, 'number') +
      _formField('Height (mm)', 'edit_height', item.height, 'number') +
      _formField('Quantity', 'edit_quantity', item.quantity, 'number') +
      _formField('Location', 'edit_location', item.location, 'text') +
      _formField('Frame Type', 'edit_frameType', item.frameType, 'select', FRAME_OPTIONS) +
      _formField('Opening Type', 'edit_openingType', item.openingType, 'select', OPENING_OPTIONS) +
      '</div>' +
      '<h4 style="margin:0.8rem 0 0.3rem;color:#64b5f6;font-size:0.85rem;">Specification Details</h4>' +
      '<div class="form-grid">' +
      _formField('System / Profile', 'edit_system', item.system || '', 'text') +
      _formField('Colour', 'edit_colour', item.colour || '', 'text') +
      _formField('Finish', 'edit_finish', item.finish || '', 'text') +
      _formField('Hardware', 'edit_hardware', item.hardware || '', 'text') +
      _formField('Cill Type', 'edit_cillType', item.cillType || '', 'text') +
      _formField('Glazing Makeup', 'edit_glazingMakeup', item.glazingMakeup || '', 'text') +
      _formField('Ventilation', 'edit_ventilation', item.ventilation || '', 'text') +
      _formField('Drainage', 'edit_drainage', item.drainage || '', 'select', DRAINAGE_OPTIONS) +
      _formField('Escape Window', 'edit_escapeWindow', item.escapeWindow || '', 'select', ESCAPE_OPTIONS) +
      _formField('Actual Frame Size', 'edit_actualFrameSize', item.actualFrameSize || '', 'text') +
      _formField('U-Value', 'edit_uValue', item.uValue || '', 'text') +
      _formField('Sill Height', 'edit_sillHeight', item.sillHeight || '', 'text') +
      _formField('Head Height', 'edit_headHeight', item.headHeight || '', 'text') +
      '</div>' +
      '<h4 style="margin:0.8rem 0 0.3rem;color:#64b5f6;font-size:0.85rem;">Door Details</h4>' +
      '<div class="form-grid">' +
      _formField('Door Type', 'edit_doorType', item.doorType || '', 'select', DOOR_TYPE_OPTIONS) +
      _formField('Door Swing', 'edit_doorSwing', item.doorSwing || '', 'select', SWING_OPTIONS) +
      _formField('Fire Rating', 'edit_fireRating', item.fireRating || '', 'text') +
      _formField('Door Frame', 'edit_doorFrame', item.doorFrame || '', 'text') +
      _formField('Door Glazing', 'edit_doorGlazing', item.doorGlazing || '', 'text') +
      _formField('Ironmongery', 'edit_ironmongery', item.ironmongery || '', 'text') +
      '</div>' +
      _formField('Glazing Specification', 'edit_glazingSpec', item.glazingSpec, 'text', null, 'col-span-2') +
      _formField('Notes (comma separated)', 'edit_notes', (item.notes || []).join(', '), 'text', null, 'col-span-2') +
      '<div class="form-group mt-2"><label><input type="checkbox" id="edit_manualOverride" ' + (item.manualOverride ? 'checked' : '') + '> Manual price override</label></div>' +
      '<div class="form-group"><label>Unit Price Override (£)</label><input type="number" class="form-control" id="edit_unitPrice" value="' + item.unitPrice + '" step="0.01" min="0" ' + (!item.manualOverride ? 'disabled' : '') + '></div>';

    showModal('Edit Item — ' + item.reference, formHTML, [
      {
        label: 'Save Changes',
        class: 'btn-primary',
        close: false,
        onClick: function () {
          var getValue = function (id) {
            var el = document.getElementById(id);
            return el ? el.value : '';
          };

          item.reference = getValue('edit_reference');
          item.type = getValue('edit_type');
          item.width = parseFloat(getValue('edit_width')) || 0;
          item.height = parseFloat(getValue('edit_height')) || 0;
          item.quantity = parseInt(getValue('edit_quantity'), 10) || 1;
          item.location = getValue('edit_location');
          item.frameType = getValue('edit_frameType');
          item.openingType = getValue('edit_openingType');
          item.glazingSpec = getValue('edit_glazingSpec');
          item.notes = getValue('edit_notes').split(',').map(function (n) { return n.trim(); }).filter(Boolean);
          item.system = getValue('edit_system');
          item.colour = getValue('edit_colour');
          item.hardware = getValue('edit_hardware');
          item.cillType = getValue('edit_cillType');
          item.glazingMakeup = getValue('edit_glazingMakeup');
          item.ventilation = getValue('edit_ventilation');
          item.drainage = getValue('edit_drainage');
          item.escapeWindow = getValue('edit_escapeWindow');
          item.actualFrameSize = getValue('edit_actualFrameSize');
          item.finish = getValue('edit_finish');
          item.uValue = getValue('edit_uValue');
          item.sillHeight = getValue('edit_sillHeight');
          item.headHeight = getValue('edit_headHeight');
          item.doorType = getValue('edit_doorType');
          item.doorSwing = getValue('edit_doorSwing');
          item.fireRating = getValue('edit_fireRating');
          item.doorFrame = getValue('edit_doorFrame');
          item.doorGlazing = getValue('edit_doorGlazing');
          item.ironmongery = getValue('edit_ironmongery');
          item.manualOverride = document.getElementById('edit_manualOverride').checked;
          if (item.manualOverride) {
            item.unitPrice = parseFloat(getValue('edit_unitPrice')) || 0;
            item.totalPrice = item.unitPrice * item.quantity;
          }

          if (_callbacks.onItemUpdated) _callbacks.onItemUpdated(item);
          renderItemsTable(_state.items, _state.warnings);
          _updateSummaryBar();
          closeModal();
          showToast('Item ' + item.reference + ' updated', 'success');
        }
      },
      { label: 'Cancel', class: 'btn-secondary' }
    ]);

    var overrideChk = document.getElementById('edit_manualOverride');
    var priceInput = document.getElementById('edit_unitPrice');
    if (overrideChk && priceInput) {
      overrideChk.addEventListener('change', function () {
        priceInput.disabled = !overrideChk.checked;
      });
    }
  }

  function _formField(label, id, value, type, options, extraClass) {
    var cls = 'form-group' + (extraClass ? ' ' + extraClass : '');
    if (type === 'select' && options) {
      return '<div class="' + cls + '"><label>' + label + '</label><select class="form-control" id="' + id + '">' +
        options.map(function (o) { return '<option value="' + o + '" ' + (o === value ? 'selected' : '') + '>' + o + '</option>'; }).join('') +
        '</select></div>';
    }
    return '<div class="' + cls + '"><label>' + label + '</label>' +
      '<input type="' + type + '" class="form-control" id="' + id + '" value="' + _escapeHtml(String(value || '')) + '"' +
      (type === 'number' ? ' min="0"' : '') + '></div>';
  }

  function _duplicateItem(itemId) {
    if (_callbacks.onDuplicateItem) _callbacks.onDuplicateItem(itemId);
  }

  function _applyPreset(itemType, profileName) {
    var presets = _state.presets;
    var preset;
    if (profileName && presets.profiles && presets.profiles[profileName]) {
      preset = presets.profiles[profileName];
    } else if (presets && presets[itemType]) {
      preset = presets[itemType];
    } else {
      showToast('No preset defined for ' + itemType, 'warning');
      return;
    }
    var PRESET_FIELDS = ['frameType', 'system', 'colour', 'hardware', 'cillType', 'glazingMakeup', 'ventilation', 'drainage', 'finish'];
    var count = 0;
    _state.items.forEach(function (item) {
      if (item.type !== itemType) return;
      var changed = false;
      PRESET_FIELDS.forEach(function (f) {
        var isBlank = !item[f] || item[f] === '' || (f === 'frameType' && item[f] === 'Unknown');
        if (isBlank && preset[f]) {
          item[f] = preset[f];
          changed = true;
        }
      });
      if (changed) count++;
    });
    if (count > 0) {
      // Recalculate pricing since frameType may have changed product codes
      if (_callbacks.onPricingChanged) _callbacks.onPricingChanged(_state.pricing);
      showToast('Preset applied to ' + count + ' ' + itemType + '(s)', 'success');
    } else {
      showToast('No blank fields to fill on ' + itemType + 's', 'info');
    }
  }

  function _deleteItem(itemId) {
    var item = _state.items.find(function (i) { return i.id === itemId; });
    if (!item) return;
    showModal(
      'Delete Item',
      '<p>Are you sure you want to delete item <strong>' + _escapeHtml(item.reference) + '</strong>?</p><p class="text-muted mt-2">This action cannot be undone.</p>',
      [
        {
          label: 'Delete',
          class: 'btn-danger',
          onClick: function () {
            if (_callbacks.onDeleteItem) _callbacks.onDeleteItem(itemId);
          }
        },
        { label: 'Cancel', class: 'btn-secondary' }
      ]
    );
  }

  function setupSearchAndFilters() {
    var searchInput = document.getElementById('tableSearch');
    if (searchInput) {
      searchInput.addEventListener('input', function () {
        _searchQuery = searchInput.value.trim();
        renderItemsTable(_state.items, _state.warnings);
      });
    }

    var filterIds = ['filterType', 'filterFrame', 'filterConfidence'];
    var filterKeys = ['type', 'frame', 'confidence'];
    filterIds.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (el) {
        el.addEventListener('change', function () {
          _filters[filterKeys[i]] = el.value;
          renderItemsTable(_state.items, _state.warnings);
        });
      }
    });
  }

  function updateState(newState) {
    _state = newState;
  }

  function _triggerPriceUpdate() {
    if (_callbacks.onPricingChanged) _callbacks.onPricingChanged(_state.pricing);
  }

  function _escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  function renderSourceDocuments(sourceDocs) {
    var container = document.getElementById('sourceDocsList');
    if (!container) return;

    if (!sourceDocs || sourceDocs.length === 0) {
      container.innerHTML = '<span style="font-size:0.8rem;color:var(--text-muted)">No documents processed yet.</span>';
      return;
    }

    var typeLabels = {
      schedule: '📋 Schedule',
      bq: '📑 BQ',
      drawing: '📐 Drawing',
      admin: '📁 Admin',
      specification: '📝 Specification',
      unknown: '📄 Document'
    };

    var html = sourceDocs.map(function (doc) {
      var label = typeLabels[doc.docType] || typeLabels.unknown;
      var pages = doc.pageCount != null ? doc.pageCount + (doc.pageCount === 1 ? ' page' : ' pages') : '? pages';
      return '<div style="padding:4px 0;border-bottom:1px solid var(--border-color)">' +
        '<div style="font-weight:600;font-size:0.8rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="' + _escapeHtml(doc.name) + '">' +
        _escapeHtml(doc.name) + '</div>' +
        '<div style="color:var(--text-muted);font-size:0.75rem">' + label + ' &bull; ' + pages + '</div>' +
        '</div>';
    }).join('');

    container.innerHTML = html;
  }

  return {
    initUI: initUI,
    renderStep: renderStep,
    renderItemsTable: renderItemsTable,
    renderWarningsPanel: renderWarningsPanel,
    renderPricingSummary: renderPricingSummary,
    renderPricingSettings: renderPricingSettings,
    renderCompanyForm: renderCompanyForm,
    renderQuoteMetaForm: renderQuoteMetaForm,
    setupInlineEditing: setupInlineEditing,
    setupSearchAndFilters: setupSearchAndFilters,
    showToast: showToast,
    showModal: showModal,
    closeModal: closeModal,
    showLoadingOverlay: showLoadingOverlay,
    updateLoadingMessage: updateLoadingMessage,
    hideLoadingOverlay: hideLoadingOverlay,
    highlightItem: highlightItem,
    updateFileList: updateFileList,
    updateFileStatus: updateFileStatus,
    updateState: updateState,
    renderSourceDocuments: renderSourceDocuments,
    showPDFVerifyView: showPDFVerifyView,
    showTableView: showTableView,
    _sortBy: _sortBy,
    _editItem: _editItem,
    _duplicateItem: _duplicateItem,
    _deleteItem: _deleteItem
  };
})();
