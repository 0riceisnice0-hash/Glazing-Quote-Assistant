/* js/app.js — Main orchestration */

var App = (function () {

  var _state = null;
  var _pendingFiles = [];
  var _autoSaveTimer = null;

  function init() {
    _loadState();
    _generateQuoteNumberIfNeeded();

    UI.initUI(_state, {
      onFilesAdded: onFilesAdded,
      onItemUpdated: onItemUpdated,
      onDuplicateItem: onDuplicateItem,
      onDeleteItem: onDeleteItem,
      onAddItem: onAddItem,
      onPricingChanged: onPricingChanged,
      onStateChange: onStateChange,
      onExportJSON: onExportJSON,
      onImportJSON: onImportJSON,
      onDarkModeToggle: onDarkModeToggle,
      onBeforeStepChange: function (step) {
        // Sync form fields to model whenever navigating to the Generate Quote step
        if (step === 3) _syncFormStateToModel();
      }
    });

    UI.setupSearchAndFilters();
    _setupAnalyseButton();
    _setupGenerateButton();
    _setupClearButton();
    _setupResetButton();
    _setupModalClose();
    _startAutoSave();
    Diagnostics.init();

    UI.updateFileList(_pendingFiles);
    UI.renderItemsTable(_state.items, _state.warnings);

    if (_state.items.length > 0) {
      _enableStep2Tab();
      _enableStep3Tab();
    }

    if (_state.metadata.quoteDate === '') {
      _state.metadata.quoteDate = new Date().toISOString().split('T')[0];
      var dateEl = document.getElementById('quoteDate');
      if (dateEl) dateEl.value = _state.metadata.quoteDate;
    }
  }

  function _loadState() {
    var saved = loadFromLocalStorage();
    if (saved) {
      _state = saved;
      // Migrate pricing config from older versions.
      // pricingVersion tracks schema changes — bump when defaults change.
      var currentVersion = 2;
      if (!_state.pricing || (_state.pricing.pricingVersion || 0) < currentVersion) {
        if (!_state.pricing) _state.pricing = {};
        _state.pricing.pricingVersion = currentVersion;
        _state.pricing.fixedCostPerUnit = 596;
        _state.pricing.baseRatePerM2 = 99;
        _state.pricing.doorFixedCostPerUnit = 166;
        _state.pricing.doorRatePerM2 = 1644;
        // Reset multipliers to neutral — standard features are already reflected
        // in the fixed cost + area rate derived from real supplier quotes.
        _state.pricing.multipliers = {
          aluminium: 1.0, pvcu: 1.0, timber: 0.9,
          fireRated: 1.8, acoustic: 1.4, toughened: 1.2, laminated: 1.15,
          tripleGlazed: 1.3, doubleGlazed: 1.0, obscure: 1.05,
          topHung: 1.0, casement: 1.0, tiltAndTurn: 1.15, sliding: 1.2, fixed: 0.95,
          trickleVent: 1.0, restrictor: 1.0
        };
        saveToLocalStorage(_state);
      }
      UI.showToast('Previous session restored', 'info');
    } else {
      _state = JSON.parse(JSON.stringify(DEFAULT_STATE));
    }
  }

  function _generateQuoteNumberIfNeeded() {
    if (!_state.metadata.quoteNumber) {
      var today = new Date();
      var yyyy = today.getFullYear();
      var mm = String(today.getMonth() + 1).padStart(2, '0');
      var dd = String(today.getDate()).padStart(2, '0');
      var rand = String(Math.floor(Math.random() * 900) + 100);
      _state.metadata.quoteNumber = 'GQ-' + yyyy + mm + dd + '-' + rand;
    }
  }

  function onFilesAdded(files) {
    files.forEach(function (file) {
      var alreadyAdded = _pendingFiles.some(function (f) { return f.name === file.name && f.size === file.size; });
      if (!alreadyAdded) {
        _pendingFiles.push(file);
      }
    });
    UI.updateFileList(_pendingFiles);
    var analyseBtn = document.getElementById('analyseBtn');
    if (analyseBtn) analyseBtn.disabled = _pendingFiles.length === 0;
    UI.showToast(_pendingFiles.length + ' file(s) ready to analyse', 'info');
  }

  function removeFile(index) {
    _pendingFiles.splice(index, 1);
    UI.updateFileList(_pendingFiles);
    var analyseBtn = document.getElementById('analyseBtn');
    if (analyseBtn) analyseBtn.disabled = _pendingFiles.length === 0;
  }

  function _setupAnalyseButton() {
    var btn = document.getElementById('analyseBtn');
    if (!btn) return;
    btn.disabled = _pendingFiles.length === 0;
    btn.addEventListener('click', function () {
      if (_pendingFiles.length === 0) {
        UI.showToast('Please add at least one PDF file', 'warning');
        return;
      }
      _runAnalysis();
    });
  }

  function _runAnalysis() {
    UI.showLoadingOverlay('Analysing Documents…', 'Starting PDF text extraction');
    Diagnostics.clear();

    // Reset extraction results so re-running analysis doesn't accumulate duplicates
    _state.items = [];
    _state.warnings = [];
    _state.sourceDocuments = [];

    var filePromises = _pendingFiles.map(function (file, i) {
      UI.updateFileStatus(i, '⏳ Extracting…');
      return extractTextFromPDF(file, function (done, total, msg) {
        UI.updateLoadingMessage('Analysing Documents…', file.name + ': ' + msg);
        UI.updateFileStatus(i, done + '/' + total + ' pages');
      }).then(function (docResult) {
        var classification = DataExtractor.classifyDocument(docResult.name, docResult.fullText || '');
        UI.updateFileStatus(i, '✅ Done (' + docResult.pageCount + ' pages)');

        // For scanned documents, attempt OCR (skip admin/drawing types)
        if (docResult.isScanned && classification.type !== 'admin' && classification.type !== 'drawing') {
          if (OcrFallback.checkAvailability()) {
            UI.updateLoadingMessage('Running OCR…', '"' + file.name + '" appears scanned — running OCR (this may take a moment)');
            UI.updateFileStatus(i, '🔬 Running OCR…');
            return OcrFallback.processScannedDocument(docResult, function (pg, total, msg) {
              UI.updateLoadingMessage('Running OCR…', msg);
              UI.updateFileStatus(i, 'OCR ' + pg + '/' + total);
            }).then(function (ocrResult) {
              UI.updateFileStatus(i, '✅ OCR done (' + ocrResult.pageCount + ' pages)');
              _state.sourceDocuments.push({
                name: ocrResult.name,
                pageCount: ocrResult.pageCount,
                docType: classification.type,
                classification: classification,
                extractedText: ocrResult.fullText ? ocrResult.fullText.substring(0, 500) : '',
                ocrAttempted: true,
                ocrSuccess: ocrResult.ocrSuccess || false
              });
              return ocrResult;
            });
          } else {
            UI.showToast('"' + file.name + '" appears to be a scanned PDF — OCR library unavailable. Refresh the page or add items manually.', 'warning');
          }
        }

        _state.sourceDocuments.push({
          name: docResult.name,
          pageCount: docResult.pageCount,
          docType: classification.type,
          classification: classification,
          extractedText: docResult.fullText ? docResult.fullText.substring(0, 500) : ''
        });

        return docResult;
      }).catch(function (err) {
        UI.updateFileStatus(i, '❌ Error');
        UI.showToast('Error reading "' + file.name + '": ' + err.message, 'error');
        return null;
      });
    });

    Promise.all(filePromises).then(function (docResults) {
      var validDocs = docResults.filter(Boolean);

      if (validDocs.length === 0) {
        UI.hideLoadingOverlay();
        UI.showToast('No documents could be processed', 'error');
        return;
      }

      UI.updateLoadingMessage('Extracting Glazing Items…', 'Analysing patterns and references');

      setTimeout(function () {
        try {
          var extractResult = DataExtractor.extractItems(validDocs);
          var newItems = extractResult.items;
          var newWarnings = extractResult.warnings;
          var stats = extractResult.stats;
          var debugLog = extractResult.debugLog || [];

          // Record diagnostics for each document
          validDocs.forEach(function (doc) {
            var cls = DataExtractor.classifyDocument(doc.name, doc.fullText || '');
            var docItems = newItems.filter(function (it) { return it.sourceDocument === doc.name; });
            var docWarnings = newWarnings.filter(function (w) {
              return w.itemId && docItems.some(function (it) { return it.id === w.itemId; });
            });
            Diagnostics.recordDocument(doc, cls, docItems, docWarnings, doc.ocrAttempted);
          });

          if (debugLog.length > 0) {
            console.group('Glazing Extractor — Diagnostic Log');
            debugLog.forEach(function (line) { console.log(line); });
            console.groupEnd();
          }

          newItems = Pricing.recalculateAll(newItems, _state.pricing);

          _state.items = newItems;
          _state.warnings = newWarnings;

          saveToLocalStorage(_state);
          UI.updateState(_state);
          UI.renderSourceDocuments(_state.sourceDocuments);
          UI.hideLoadingOverlay();

          if (newItems.length === 0) {
            UI.showToast('No glazing items found. Documents may be scanned or use an unrecognised format. Use "🔬 Diagnostics" to investigate.', 'warning');
            _showManualEntryPrompt();
          } else {
            UI.showToast('Extracted ' + newItems.length + ' item(s) from ' + stats.docsProcessed + ' document(s) — please verify below', 'success');
            _enableStep2Tab();
            _enableStep3Tab();
            // Show PDF verify view so user can review detections before the table
            UI.renderStep(2);
            UI.showPDFVerifyView(validDocs, _state.items, function (acceptedItems) {
              // Replace state items with only the accepted ones
              _state.items = Pricing.recalculateAll(acceptedItems, _state.pricing);
              _state.warnings = _state.warnings.filter(function (w) {
                return _state.items.some(function (it) { return it.id === w.itemId; }) || !w.itemId;
              });
              saveToLocalStorage(_state);
              UI.updateState(_state);
              UI.renderItemsTable(_state.items, _state.warnings);
              UI.renderWarningsPanel(_state.warnings, _state.items);
              UI.renderSourceDocuments(_state.sourceDocuments);
              UI.showToast(_state.items.length + ' item(s) confirmed', 'success');
            });
          }
        } catch (err) {
          UI.hideLoadingOverlay();
          UI.showToast('Extraction failed: ' + err.message, 'error');
          console.error('Extraction error:', err);
        }
      }, 100);
    });
  }

  function _showManualEntryPrompt() {
    UI.showModal(
      'No Items Extracted',
      '<div class="alert alert-warning"><span class="alert-icon">⚠️</span>' +
      '<div>No glazing items could be automatically extracted from the uploaded documents. ' +
      'This can happen with scanned PDFs, image-based files, or documents in an unexpected format.</div></div>' +
      '<p style="margin-top:12px">You can:</p>' +
      '<ul style="margin:8px 0 0 20px;font-size:0.875rem">' +
      '<li>Add items manually using the "Add Item" button</li>' +
      '<li>Import a previously saved JSON session</li>' +
      '<li>Try a different, text-based PDF</li>' +
      '</ul>',
      [
        {
          label: 'Go to Review & Edit',
          class: 'btn-primary',
          onClick: function () {
            _enableStep2Tab();
            UI.renderStep(2);
          }
        },
        { label: 'Close', class: 'btn-secondary' }
      ]
    );
  }

  function _setupGenerateButton() {
    var btn = document.getElementById('generateQuoteBtn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (_state.items.length === 0) {
        UI.showToast('No items to generate a quote for', 'warning');
        return;
      }
      _generatePDF();
    });
  }

  function _generatePDF() {
    UI.showLoadingOverlay('Generating PDF…', 'Building quote document');

    _syncFormStateToModel();

    setTimeout(function () {
      try {
        var doc = QuoteGenerator.generateQuotePDF(_state, _state.pricing);
        var filename = (_state.metadata.quoteNumber || 'GQ-DRAFT') + '.pdf';
        doc.save(filename);
        UI.hideLoadingOverlay();
        UI.showToast('Quote PDF generated: ' + filename, 'success');
      } catch (err) {
        UI.hideLoadingOverlay();
        UI.showToast('PDF generation failed: ' + err.message, 'error');
        console.error('PDF error:', err);
      }
    }, 150);
  }

  function _syncFormStateToModel() {
    var syncField = function (id, obj, key, isNum) {
      var el = document.getElementById(id);
      if (el) obj[key] = isNum ? (parseFloat(el.value) || 0) : el.value;
    };
    syncField('projectName', _state.metadata, 'projectName');
    syncField('clientName', _state.metadata, 'clientName');
    syncField('quoteNumber', _state.metadata, 'quoteNumber');
    syncField('quoteDate', _state.metadata, 'quoteDate');
    syncField('validityDays', _state.metadata, 'validityDays', true);
    syncField('quoteNotes', _state.metadata, 'notes');
    syncField('companyName', _state.company, 'name');
    syncField('companyAddress', _state.company, 'address');
    syncField('companyPhone', _state.company, 'phone');
    syncField('companyEmail', _state.company, 'email');
  }

  function _setupClearButton() {
    var btn = document.getElementById('clearItemsBtn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      if (_state.items.length === 0) return;
      UI.showModal(
        'Clear All Items',
        '<p>Are you sure you want to remove all <strong>' + _state.items.length + '</strong> items?</p>' +
        '<p class="text-muted mt-2">This action cannot be undone.</p>',
        [
          {
            label: 'Clear All',
            class: 'btn-danger',
            onClick: function () {
              _state.items = [];
              _state.warnings = [];
              saveToLocalStorage(_state);
              UI.updateState(_state);
              UI.renderItemsTable([], []);
              UI.renderWarningsPanel([], []);
              UI.showToast('All items cleared', 'info');
            }
          },
          { label: 'Cancel', class: 'btn-secondary' }
        ]
      );
    });
  }

  function _setupResetButton() {
    var btn = document.getElementById('resetSessionBtn');
    if (!btn) return;
    btn.addEventListener('click', function () {
      UI.showModal(
        'Reset Session',
        '<p>Are you sure you want to reset the entire session?</p>' +
        '<p class="text-muted mt-2">All items, documents, and settings will be cleared.</p>',
        [
          {
            label: 'Reset',
            class: 'btn-danger',
            onClick: function () {
              localStorage.removeItem('glazingQuoteState');
              _state = JSON.parse(JSON.stringify(DEFAULT_STATE));
              _pendingFiles = [];
              _generateQuoteNumberIfNeeded();
              _state.metadata.quoteDate = new Date().toISOString().split('T')[0];
              UI.updateState(_state);
              UI.updateFileList([]);
              UI.renderItemsTable([], []);
              UI.renderWarningsPanel([], []);
              UI.renderCompanyForm(_state.company);
              UI.renderQuoteMetaForm(_state.metadata);
              UI.renderStep(1);
              _disableStep2Tab();
              _disableStep3Tab();
              UI.showToast('Session reset', 'info');
            }
          },
          { label: 'Cancel', class: 'btn-secondary' }
        ]
      );
    });
  }

  function _setupModalClose() {
    var backdrop = document.getElementById('modalBackdrop');
    if (backdrop) {
      backdrop.addEventListener('click', function (e) {
        if (e.target === backdrop) UI.closeModal();
      });
    }
    var closeBtn = document.getElementById('modalCloseBtn');
    if (closeBtn) closeBtn.addEventListener('click', UI.closeModal);
  }

  function onItemUpdated(item) {
    var idx = _state.items.findIndex(function (i) { return i.id === item.id; });
    if (idx !== -1) {
      if (!item.manualOverride) {
        var priceResult = Pricing.calculateItemPrice(item, _state.pricing);
        item.unitPrice = priceResult.unitPrice;
        item.totalPrice = priceResult.totalPrice;
      }
      item.confidence = _rescoreConfidence(item);
      _state.items[idx] = item;
    }
    saveToLocalStorage(_state);
  }

  function _rescoreConfidence(item) {
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

  function onDuplicateItem(itemId) {
    var item = _state.items.find(function (i) { return i.id === itemId; });
    if (!item) return;
    var newItem = JSON.parse(JSON.stringify(item));
    newItem.id = generateId();
    newItem.reference = getNextReference(_state.items, item.type);
    newItem.manualOverride = false;
    _state.items.push(newItem);
    saveToLocalStorage(_state);
    UI.updateState(_state);
    UI.renderItemsTable(_state.items, _state.warnings);
    UI.showToast('Item duplicated as ' + newItem.reference, 'success');
  }

  function onDeleteItem(itemId) {
    var item = _state.items.find(function (i) { return i.id === itemId; });
    _state.items = _state.items.filter(function (i) { return i.id !== itemId; });
    _state.warnings = _state.warnings.filter(function (w) { return w.itemId !== itemId; });
    saveToLocalStorage(_state);
    UI.updateState(_state);
    UI.renderItemsTable(_state.items, _state.warnings);
    UI.renderWarningsPanel(_state.warnings, _state.items);
    if (item) UI.showToast('Item ' + item.reference + ' deleted', 'info');
  }

  function onAddItem() {
    var newItem = createItem({
      reference: getNextReference(_state.items, 'window'),
      type: 'window',
      confidence: 'high',
      manualOverride: false
    });
    _state.items.push(newItem);
    saveToLocalStorage(_state);
    UI.updateState(_state);
    UI.renderItemsTable(_state.items, _state.warnings);
    _enableStep2Tab();
    _enableStep3Tab();
    UI.highlightItem(newItem.id);
    UI.showToast('New item added: ' + newItem.reference, 'success');
  }

  function onPricingChanged(pricing) {
    _state.pricing = pricing;
    _state.items = Pricing.recalculateAll(_state.items, pricing);
    saveToLocalStorage(_state);
    UI.updateState(_state);
    UI.renderItemsTable(_state.items, _state.warnings);
    var summary = Pricing.getPriceSummary(_state.items, _state.pricing);
    UI.renderPricingSummary(summary);
  }

  function onStateChange() {
    _scheduleAutoSave();
  }

  function onExportJSON() {
    _syncFormStateToModel();
    var json = exportJSON(_state);
    var blob = new Blob([json], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = (_state.metadata.quoteNumber || 'GQ-DRAFT') + '.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    UI.showToast('Session exported as JSON', 'success');
  }

  function onImportJSON(jsonString) {
    try {
      var imported = importJSON(jsonString);
      _state = imported;
      _pendingFiles = [];
      UI.updateState(_state);
      UI.renderItemsTable(_state.items, _state.warnings);
      UI.renderWarningsPanel(_state.warnings, _state.items);
      UI.renderCompanyForm(_state.company);
      UI.renderQuoteMetaForm(_state.metadata);
      UI.renderPricingSettings(_state.pricing);
      saveToLocalStorage(_state);
      if (_state.items.length > 0) {
        _enableStep2Tab();
        _enableStep3Tab();
        UI.renderStep(2);
      }
      UI.showToast('Session imported (' + _state.items.length + ' items)', 'success');
    } catch (err) {
      UI.showToast('Import failed: ' + err.message, 'error');
    }
  }

  function onDarkModeToggle(isDark) {
    // persisted via localStorage in UI.js
  }

  function _enableStep2Tab() {
    var tab = document.querySelector('.wizard-step-tab[data-step="2"]');
    if (tab) tab.classList.remove('disabled');
  }

  function _disableStep2Tab() {
    var tab = document.querySelector('.wizard-step-tab[data-step="2"]');
    if (tab) tab.classList.add('disabled');
  }

  function _enableStep3Tab() {
    var tab = document.querySelector('.wizard-step-tab[data-step="3"]');
    if (tab) tab.classList.remove('disabled');
  }

  function _disableStep3Tab() {
    var tab = document.querySelector('.wizard-step-tab[data-step="3"]');
    if (tab) tab.classList.add('disabled');
  }

  function _startAutoSave() {
    _autoSaveTimer = setInterval(function () {
      saveToLocalStorage(_state);
    }, 30000);
  }

  function _scheduleAutoSave() {
    clearTimeout(_autoSaveTimer);
    _autoSaveTimer = setTimeout(function () {
      saveToLocalStorage(_state);
    }, 2000);
  }

  return {
    init: init,
    removeFile: removeFile,
    getState: function () { return _state; }
  };
})();

document.addEventListener('DOMContentLoaded', function () {
  try {
    App.init();
  } catch (err) {
    console.error('App initialization error:', err);
  }
});
