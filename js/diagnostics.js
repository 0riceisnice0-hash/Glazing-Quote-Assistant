/* js/diagnostics.js — Extraction diagnostics panel */

var Diagnostics = (function () {

  var _records = [];
  var _enabled = false;
  var _container = null;

  function init() {
    _container = document.getElementById('diagnosticsPanel');
    var toggleBtn = document.getElementById('diagnosticsToggleBtn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggle);
    }
    var closeBtn = document.getElementById('diagnosticsCloseBtn');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        _enabled = true; // toggle will flip it
        toggle();
      });
    }
  }

  function toggle() {
    _enabled = !_enabled;
    if (_container) {
      _container.classList.toggle('hidden', !_enabled);
    }
    var toggleBtn = document.getElementById('diagnosticsToggleBtn');
    if (toggleBtn) {
      toggleBtn.textContent = _enabled ? '\uD83D\uDD2C Hide Diagnostics' : '\uD83D\uDD2C Diagnostics';
      toggleBtn.classList.toggle('btn-active', _enabled);
    }
    if (_enabled) render();
  }

  function isEnabled() { return _enabled; }

  /**
   * Record diagnostic information for one document.
   */
  function recordDocument(docResult, classification, extractedItems, warnings, ocrAttempted) {
    _records.push({
      name: docResult.name,
      pageCount: docResult.pageCount,
      isScanned: docResult.isScanned,
      classification: classification,
      textLength: docResult.fullText ? docResult.fullText.length : 0,
      rawTextSample: docResult.fullText ? docResult.fullText.substring(0, 2000) : '(no text extracted)',
      textItemCount: docResult.pages ? docResult.pages.reduce(function (s, p) { return s + (p.textItems ? p.textItems.length : 0); }, 0) : 0,
      extractedItems: (extractedItems || []).map(function (it) {
        return { ref: it.reference, confidence: it.confidence, width: it.width, height: it.height, method: it.extractionMethod };
      }),
      warnings: (warnings || []).map(function (w) { return w.message; }),
      ocrAttempted: !!ocrAttempted,
      ocrSuccess: docResult.ocrSuccess || false
    });
    if (_enabled) render();
  }

  function clear() {
    _records = [];
    if (_enabled) render();
  }

  function render() {
    if (!_container) return;
    if (_records.length === 0) {
      _container.innerHTML = '<div class="card-title">\uD83D\uDD2C Extraction Diagnostics</div>' +
        '<div class="diag-empty">No documents processed yet. Upload and analyse documents to see diagnostics.</div>';
      return;
    }

    var html = '<div class="card-title">\uD83D\uDD2C Extraction Diagnostics</div>';
    html += _records.map(function (rec, idx) {
      var cls = rec.classification || { type: 'unknown', confidence: 'low', reason: 'N/A' };
      var confBadge = {
        high: 'diag-badge-success',
        medium: 'diag-badge-warning',
        low: 'diag-badge-danger'
      }[cls.confidence] || 'diag-badge-info';

      var typeBadge = {
        schedule: 'diag-badge-success',
        bq: 'diag-badge-info',
        drawing: 'diag-badge-secondary',
        admin: 'diag-badge-secondary',
        specification: 'diag-badge-info',
        unknown: 'diag-badge-warning'
      }[cls.type] || 'diag-badge-secondary';

      var itemsHtml = rec.extractedItems.length === 0
        ? '<span style="color:var(--text-muted)">None extracted</span>'
        : rec.extractedItems.map(function (it) {
            return '<span class="diag-item-badge diag-badge-' + _esc(it.confidence) + '">' +
              _esc(it.ref) + ' (' + _esc(String(it.width)) + '\xD7' + _esc(String(it.height)) + ', ' + _esc(it.confidence) + ')' +
              '</span>';
          }).join(' ');

      var warningsHtml = rec.warnings.length === 0
        ? '<span style="color:var(--accent-success)">No warnings</span>'
        : rec.warnings.map(function (w) { return '<div class="diag-warning">\u26A0 ' + _esc(w) + '</div>'; }).join('');

      return '<details class="diag-doc" ' + (idx === 0 ? 'open' : '') + '>' +
        '<summary class="diag-doc-summary">' +
        '<span class="diag-doc-name">' + _esc(rec.name) + '</span>' +
        '<span class="diag-badge ' + typeBadge + '">' + _esc(cls.type) + '</span>' +
        '<span class="diag-badge ' + confBadge + '">' + _esc(cls.confidence) + '</span>' +
        (rec.isScanned ? '<span class="diag-badge diag-badge-warning">Scanned</span>' : '') +
        (rec.ocrAttempted ? '<span class="diag-badge ' + (rec.ocrSuccess ? 'diag-badge-success' : 'diag-badge-danger') + '">OCR ' + (rec.ocrSuccess ? '\u2713' : '\u2717') + '</span>' : '') +
        '</summary>' +
        '<div class="diag-doc-body">' +
        '<div class="diag-row"><span class="diag-label">Classification:</span> ' + _esc(cls.type) + ' (' + _esc(cls.confidence) + ' confidence) \u2014 ' + _esc(cls.reason) + '</div>' +
        '<div class="diag-row"><span class="diag-label">Pages:</span> ' + rec.pageCount + '</div>' +
        '<div class="diag-row"><span class="diag-label">Text length:</span> ' + rec.textLength + ' chars</div>' +
        '<div class="diag-row"><span class="diag-label">Text items (with position):</span> ' + rec.textItemCount + '</div>' +
        '<div class="diag-row"><span class="diag-label">Extraction method:</span> ' + (rec.ocrAttempted && rec.ocrSuccess ? 'OCR (Tesseract.js)' : 'PDF.js text layer') + '</div>' +
        '<div class="diag-row"><span class="diag-label">Items extracted (' + rec.extractedItems.length + '):</span><div style="margin-top:4px">' + itemsHtml + '</div></div>' +
        '<div class="diag-row"><span class="diag-label">Warnings:</span><div>' + warningsHtml + '</div></div>' +
        '<details class="diag-raw"><summary>Raw extracted text (first 2000 chars)</summary>' +
        '<pre class="diag-pre">' + _esc(rec.rawTextSample) + '</pre>' +
        '</details>' +
        '</div>' +
        '</details>';
    }).join('');

    _container.innerHTML = html;
  }

  function _esc(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  return {
    init: init,
    toggle: toggle,
    isEnabled: isEnabled,
    recordDocument: recordDocument,
    clear: clear,
    render: render
  };

})();
