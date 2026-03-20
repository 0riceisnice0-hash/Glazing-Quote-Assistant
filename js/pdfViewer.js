/* js/pdfViewer.js — Interactive PDF viewer with detection overlay */

var PDFViewer = (function () {

  var _docResults = [];        // [{name, pageCount, pages, pdfDoc, …}]
  var _items = [];             // detected items (copies with _accepted flag)
  var _currentDocIndex = 0;
  var _currentPageNum = 1;
  var _renderTask = null;      // current PDF.js render task (to cancel if needed)
  var _callbacks = {};
  var _containerEl = null;
  var _scale = 1.5;

  // -----------------------------------------------------------------------
  // Public API
  // -----------------------------------------------------------------------

  function init(docResults, items, containerEl, callbacks) {
    _docResults = (docResults || []).filter(function (d) { return d && d.pdfDoc; });
    _items = (items || []).map(function (item) {
      return Object.assign({}, item, { _accepted: true });
    });
    _currentDocIndex = 0;
    _currentPageNum = 1;
    _containerEl = containerEl;
    _callbacks = callbacks || {};

    _buildShell();
    _renderDocSelector();
    _renderSidebar();
    _renderPage(_currentDocIndex, _currentPageNum);
  }

  function destroy() {
    if (_renderTask) {
      try { _renderTask.cancel(); } catch (e) { /* ignore */ }
      _renderTask = null;
    }
    if (_containerEl) _containerEl.innerHTML = '';
  }

  // -----------------------------------------------------------------------
  // Shell HTML
  // -----------------------------------------------------------------------

  function _buildShell() {
    _containerEl.innerHTML =
      '<div class="pv-layout">' +
        '<div class="pv-left">' +
          '<div class="pv-toolbar" id="pvToolbar">' +
            '<div class="pv-doc-selector-wrap" id="pvDocSelectorWrap"></div>' +
            '<div class="pv-page-nav">' +
              '<button class="btn btn-sm btn-secondary" id="pvPrevPage">&#8592; Prev</button>' +
              '<span class="pv-page-indicator" id="pvPageIndicator">Page 1 / ?</span>' +
              '<button class="btn btn-sm btn-secondary" id="pvNextPage">Next &#8594;</button>' +
            '</div>' +
          '</div>' +
          '<div class="pv-canvas-wrap" id="pvCanvasWrap">' +
            '<div class="pv-canvas-container" id="pvCanvasContainer">' +
              '<div class="pv-loading">Rendering page…</div>' +
            '</div>' +
          '</div>' +
        '</div>' +
        '<div class="pv-right" id="pvSidebar">' +
          '<div class="pv-sidebar-header">Detected Items</div>' +
          '<div class="pv-items-list" id="pvItemsList"></div>' +
          '<div class="pv-confirm-area">' +
            '<div class="pv-legend">' +
              '<span class="pv-legend-dot high"></span> High &nbsp;' +
              '<span class="pv-legend-dot medium"></span> Medium &nbsp;' +
              '<span class="pv-legend-dot low"></span> Low' +
            '</div>' +
            '<button class="btn btn-primary pv-confirm-btn" id="pvConfirmBtn">&#10003; Confirm All &amp; Continue</button>' +
            '<p class="pv-hint">Review detected items, then click Confirm to proceed to the full editor.</p>' +
          '</div>' +
        '</div>' +
      '</div>';

    document.getElementById('pvPrevPage').addEventListener('click', _prevPage);
    document.getElementById('pvNextPage').addEventListener('click', _nextPage);
    document.getElementById('pvConfirmBtn').addEventListener('click', _confirmAll);
  }

  // -----------------------------------------------------------------------
  // Document selector (when multiple PDFs uploaded)
  // -----------------------------------------------------------------------

  function _renderDocSelector() {
    var wrap = document.getElementById('pvDocSelectorWrap');
    if (!wrap) return;
    if (_docResults.length <= 1) {
      wrap.innerHTML = _docResults.length === 1
        ? '<span class="pv-doc-name">' + _escapeHtml(_docResults[0].name) + '</span>'
        : '';
      return;
    }
    var sel = '<select class="pv-doc-select" id="pvDocSelect">' +
      _docResults.map(function (d, i) {
        return '<option value="' + i + '">' + _escapeHtml(d.name) + '</option>';
      }).join('') +
      '</select>';
    wrap.innerHTML = sel;
    document.getElementById('pvDocSelect').addEventListener('change', function (e) {
      _currentDocIndex = parseInt(e.target.value, 10) || 0;
      _currentPageNum = 1;
      _renderPage(_currentDocIndex, _currentPageNum);
      _renderSidebar();
    });
  }

  // -----------------------------------------------------------------------
  // Sidebar — list detected items for the current doc
  // -----------------------------------------------------------------------

  function _renderSidebar() {
    var list = document.getElementById('pvItemsList');
    if (!list) return;

    var docName = _docResults[_currentDocIndex] ? _docResults[_currentDocIndex].name : null;
    var docItems = docName
      ? _items.filter(function (it) { return it.sourceDocument === docName; })
      : _items;

    // If a document has no items mapped to it, show all items
    if (docItems.length === 0) docItems = _items;

    if (docItems.length === 0) {
      list.innerHTML = '<div class="pv-no-items">No items detected in this document.</div>';
      return;
    }

    list.innerHTML = docItems.map(function (item) {
      var accepted = item._accepted !== false;
      var dimStr = (item.width > 0 && item.height > 0)
        ? item.width + ' × ' + item.height + ' mm'
        : '<span class="pv-dim-missing">No dimensions</span>';
      return '<div class="pv-item ' + item.confidence + (accepted ? '' : ' pv-item-rejected') + '" id="pvItem_' + item.id + '">' +
        '<div class="pv-item-header">' +
          '<span class="pv-item-ref">' + _escapeHtml(item.reference) + '</span>' +
          '<span class="badge ' + item.confidence + '">' + item.confidence + '</span>' +
          (accepted ? '' : '<span class="pv-rejected-label">Rejected</span>') +
        '</div>' +
        '<div class="pv-item-meta">' +
          '<span>' + _escapeHtml(item.type) + '</span>' +
          (item.location ? ' &bull; <span>' + _escapeHtml(item.location) + '</span>' : '') +
        '</div>' +
        '<div class="pv-item-dims">' + dimStr + '</div>' +
        '<div class="pv-item-spec">' + _escapeHtml(item.glazingSpec || '') + '</div>' +
        '<div class="pv-item-actions">' +
          '<button class="btn btn-xs ' + (accepted ? 'btn-success' : 'btn-ghost') + ' pv-btn-accept" data-id="' + item.id + '" title="Accept this item">' +
            (accepted ? '&#10003; Accepted' : '&#10003; Accept') +
          '</button>' +
          '<button class="btn btn-xs ' + (accepted ? 'btn-ghost' : 'btn-danger') + ' pv-btn-reject" data-id="' + item.id + '" title="Reject this item">' +
            (accepted ? '&#10007; Reject' : '&#10007; Rejected') +
          '</button>' +
        '</div>' +
      '</div>';
    }).join('');

    // Attach click handlers
    list.querySelectorAll('.pv-btn-accept').forEach(function (btn) {
      btn.addEventListener('click', function () { _setAccepted(btn.dataset.id, true); });
    });
    list.querySelectorAll('.pv-btn-reject').forEach(function (btn) {
      btn.addEventListener('click', function () { _setAccepted(btn.dataset.id, false); });
    });
  }

  function _setAccepted(itemId, accepted) {
    var item = _items.find(function (it) { return it.id === itemId; });
    if (!item) return;
    item._accepted = accepted;
    _renderSidebar();
    // Redraw overlay to reflect new status
    _redrawOverlay();
  }

  // -----------------------------------------------------------------------
  // Page rendering
  // -----------------------------------------------------------------------

  function _renderPage(docIndex, pageNum) {
    var docResult = _docResults[docIndex];
    if (!docResult || !docResult.pdfDoc) {
      _showCanvasError('PDF document not available for rendering.');
      return;
    }

    var container = document.getElementById('pvCanvasContainer');
    if (!container) return;
    container.innerHTML = '<div class="pv-loading">Rendering page ' + pageNum + '…</div>';

    // Cancel any in-progress render
    if (_renderTask) {
      try { _renderTask.cancel(); } catch (e) { /* ignore */ }
      _renderTask = null;
    }

    docResult.pdfDoc.getPage(pageNum).then(function (page) {
      // Fit to the container width (approx 700px target)
      var containerWidth = (container.parentElement ? container.parentElement.clientWidth : 700) || 700;
      var viewport = page.getViewport({ scale: 1 });
      var scale = Math.min((containerWidth - 20) / viewport.width, 2.0);
      scale = Math.max(scale, 0.5);
      _scale = scale;

      var scaledViewport = page.getViewport({ scale: scale });

      // PDF canvas
      var pdfCanvas = document.createElement('canvas');
      pdfCanvas.className = 'pv-pdf-canvas';
      pdfCanvas.width = scaledViewport.width;
      pdfCanvas.height = scaledViewport.height;

      // Overlay canvas (transparent, sits on top)
      var overlayCanvas = document.createElement('canvas');
      overlayCanvas.className = 'pv-overlay-canvas';
      overlayCanvas.width = scaledViewport.width;
      overlayCanvas.height = scaledViewport.height;
      overlayCanvas.id = 'pvOverlayCanvas';

      var wrapper = document.createElement('div');
      wrapper.className = 'pv-canvas-wrapper';
      wrapper.style.width = scaledViewport.width + 'px';
      wrapper.style.height = scaledViewport.height + 'px';
      wrapper.appendChild(pdfCanvas);
      wrapper.appendChild(overlayCanvas);

      container.innerHTML = '';
      container.appendChild(wrapper);

      _renderTask = page.render({
        canvasContext: pdfCanvas.getContext('2d'),
        viewport: scaledViewport
      });

      _renderTask.promise.then(function () {
        _renderTask = null;
        // Draw detection overlays
        var pageItems = _items.filter(function (it) {
          return it.sourceDocument === docResult.name && it.sourcePage === pageNum;
        });
        _drawOverlays(overlayCanvas, pageItems, scaledViewport, scale);
        _updatePageIndicator(docIndex, pageNum);
      }).catch(function (err) {
        if (err && err.name === 'RenderingCancelledException') return;
        _showCanvasError('Render error: ' + (err.message || err));
      });
    }).catch(function (err) {
      _showCanvasError('Could not load page ' + pageNum + ': ' + (err.message || err));
    });
  }

  function _redrawOverlay() {
    var docResult = _docResults[_currentDocIndex];
    if (!docResult) return;
    var overlayCanvas = document.getElementById('pvOverlayCanvas');
    if (!overlayCanvas) return;
    // Re-fetch the current page to get a viewport for position math
    docResult.pdfDoc.getPage(_currentPageNum).then(function (page) {
      var scaledViewport = page.getViewport({ scale: _scale });
      var pageItems = _items.filter(function (it) {
        return it.sourceDocument === docResult.name && it.sourcePage === _currentPageNum;
      });
      var ctx = overlayCanvas.getContext('2d');
      ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);
      _drawOverlays(overlayCanvas, pageItems, scaledViewport, _scale);
    }).catch(function () { /* ignore */ });
  }

  function _drawOverlays(overlayCanvas, pageItems, viewport, scale) {
    if (!pageItems || pageItems.length === 0) return;
    var ctx = overlayCanvas.getContext('2d');
    ctx.clearRect(0, 0, overlayCanvas.width, overlayCanvas.height);

    pageItems.forEach(function (item) {
      var pos = item.textPosition;
      if (!pos) return;

      var accepted = item._accepted !== false;

      // Convert PDF user-space coords to canvas coords
      // PDF origin is bottom-left; canvas origin is top-left
      var cx = pos.x * scale;
      var cy = viewport.height - (pos.y + pos.height) * scale;
      var cw = Math.max(pos.width * scale, 40);
      var ch = Math.max(pos.height * scale, 14);

      // Add a small padding
      cx -= 2;
      cy -= 2;
      cw += 4;
      ch += 4;

      // Choose colour based on confidence & acceptance
      var fillColor, strokeColor;
      if (!accepted) {
        fillColor = 'rgba(220,38,38,0.25)';
        strokeColor = 'rgba(220,38,38,0.85)';
      } else if (item.confidence === 'high') {
        fillColor = 'rgba(22,163,74,0.20)';
        strokeColor = 'rgba(22,163,74,0.80)';
      } else if (item.confidence === 'medium') {
        fillColor = 'rgba(217,119,6,0.20)';
        strokeColor = 'rgba(217,119,6,0.80)';
      } else {
        fillColor = 'rgba(220,38,38,0.20)';
        strokeColor = 'rgba(220,38,38,0.70)';
      }

      ctx.fillStyle = fillColor;
      ctx.fillRect(cx, cy, cw, ch);
      ctx.strokeStyle = strokeColor;
      ctx.lineWidth = 1.5;
      ctx.strokeRect(cx, cy, cw, ch);

      // Label the reference below the box
      ctx.fillStyle = strokeColor;
      ctx.font = 'bold 10px sans-serif';
      ctx.fillText(item.reference, cx, cy + ch + 10);
    });
  }

  function _showCanvasError(msg) {
    var container = document.getElementById('pvCanvasContainer');
    if (container) {
      container.innerHTML = '<div class="pv-loading pv-error">' + _escapeHtml(msg) + '</div>';
    }
  }

  // -----------------------------------------------------------------------
  // Navigation
  // -----------------------------------------------------------------------

  function _prevPage() {
    if (_currentPageNum > 1) {
      _currentPageNum--;
      _renderPage(_currentDocIndex, _currentPageNum);
    }
  }

  function _nextPage() {
    var doc = _docResults[_currentDocIndex];
    if (doc && _currentPageNum < doc.pageCount) {
      _currentPageNum++;
      _renderPage(_currentDocIndex, _currentPageNum);
    }
  }

  function _updatePageIndicator(docIndex, pageNum) {
    var indicator = document.getElementById('pvPageIndicator');
    if (!indicator) return;
    var doc = _docResults[docIndex];
    var total = doc ? doc.pageCount : '?';
    indicator.textContent = 'Page ' + pageNum + ' / ' + total;
  }

  // -----------------------------------------------------------------------
  // Confirm All & Continue
  // -----------------------------------------------------------------------

  function _confirmAll() {
    var accepted = _items.filter(function (it) { return it._accepted !== false; });
    // Strip internal _accepted flag before passing out
    var cleanItems = accepted.map(function (it) {
      var copy = Object.assign({}, it);
      delete copy._accepted;
      return copy;
    });
    if (_callbacks.onConfirm) _callbacks.onConfirm(cleanItems);
  }

  // -----------------------------------------------------------------------
  // Helpers
  // -----------------------------------------------------------------------

  function _escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // -----------------------------------------------------------------------
  // Public
  // -----------------------------------------------------------------------

  return {
    init: init,
    destroy: destroy
  };

})();
