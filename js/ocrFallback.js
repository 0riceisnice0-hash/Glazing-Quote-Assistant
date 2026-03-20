/* js/ocrFallback.js — Client-side OCR fallback for scanned PDFs using Tesseract.js */

var OcrFallback = (function () {

  var _isAvailable = false;

  function checkAvailability() {
    _isAvailable = typeof Tesseract !== 'undefined';
    return _isAvailable;
  }

  /**
   * Process a scanned document using OCR.
   * @param {Object} docResult - Result from extractTextFromPDF (with pdfDoc)
   * @param {Function} onProgress - (pageNum, totalPages, message) callback
   * @returns {Promise<Object>} - Updated docResult with OCR text
   */
  function processScannedDocument(docResult, onProgress) {
    if (!checkAvailability()) {
      return Promise.resolve(Object.assign({}, docResult, {
        ocrAttempted: false,
        ocrError: 'Tesseract.js not loaded'
      }));
    }

    if (!docResult.pdfDoc) {
      return Promise.resolve(Object.assign({}, docResult, {
        ocrAttempted: false,
        ocrError: 'PDF document not available for rendering'
      }));
    }

    var pageCount = docResult.pageCount;
    var ocrPages = [];

    // Process pages sequentially (Tesseract is CPU-intensive)
    var chain = Promise.resolve();
    for (var i = 1; i <= pageCount; i++) {
      (function (pageNum) {
        chain = chain.then(function () {
          if (onProgress) onProgress(pageNum, pageCount, 'OCR processing page ' + pageNum + ' of ' + pageCount + '\u2026');
          return _ocrPage(docResult.pdfDoc, pageNum);
        }).then(function (pageText) {
          ocrPages.push({ pageNum: pageNum, text: pageText, textItems: [], ocrExtracted: true });
        }).catch(function (err) {
          console.warn('OCR failed for page ' + pageNum + ':', err);
          ocrPages.push({ pageNum: pageNum, text: '', textItems: [], ocrExtracted: true, ocrError: err.message });
        });
      })(i);
    }

    return chain.then(function () {
      ocrPages.sort(function (a, b) { return a.pageNum - b.pageNum; });
      var fullOcrText = ocrPages.map(function (p) { return p.text; }).join('\n');

      // Merge OCR pages into docResult, replacing pages that had no text
      var mergedPages = docResult.pages.map(function (origPage) {
        var ocrPage = ocrPages.find(function (op) { return op.pageNum === origPage.pageNum; });
        if (!ocrPage) return origPage;
        // Only use OCR text if it's better than what we had
        var origHasText = origPage.text && origPage.text.trim().length > 50;
        if (origHasText) return origPage;
        return Object.assign({}, origPage, {
          text: ocrPage.text,
          textItems: [],
          ocrExtracted: true
        });
      });

      return Object.assign({}, docResult, {
        pages: mergedPages,
        fullText: fullOcrText || docResult.fullText,
        isScanned: true,
        ocrAttempted: true,
        ocrSuccess: fullOcrText.trim().length > 100,
        extractionMethod: 'ocr'
      });
    });
  }

  function _ocrPage(pdfDoc, pageNum) {
    // Use renderPageToCanvas from pdfParser.js (loaded before this module)
    var renderFn = typeof renderPageToCanvas === 'function' ? renderPageToCanvas : _renderPageToCanvas;
    return renderFn(pdfDoc, pageNum, 2.0).then(function (canvas) {
      return Tesseract.recognize(canvas, 'eng', {
        logger: function () {} // suppress verbose logging
      });
    }).then(function (result) {
      return result.data.text || '';
    });
  }

  // Fallback canvas renderer if pdfParser.js renderPageToCanvas is unavailable
  function _renderPageToCanvas(pdfDoc, pageNum, scale) {
    scale = scale || 2.0;
    return pdfDoc.getPage(pageNum).then(function (page) {
      var viewport = page.getViewport({ scale: scale });
      var canvas = document.createElement('canvas');
      canvas.width = viewport.width;
      canvas.height = viewport.height;
      var ctx = canvas.getContext('2d');
      return page.render({
        canvasContext: ctx,
        viewport: viewport
      }).promise.then(function () {
        return canvas;
      });
    });
  }

  return {
    checkAvailability: checkAvailability,
    processScannedDocument: processScannedDocument,
    isAvailable: function () { return _isAvailable; }
  };

})();
