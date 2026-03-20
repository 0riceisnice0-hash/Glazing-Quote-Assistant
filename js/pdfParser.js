/* js/pdfParser.js — PDF upload and text extraction using PDF.js */

function initDropZone(dropZoneEl, fileInputEl, onFilesAdded) {
  if (!dropZoneEl) return;

  dropZoneEl.addEventListener('dragover', function (e) {
    e.preventDefault();
    dropZoneEl.classList.add('drag-over');
  });

  dropZoneEl.addEventListener('dragleave', function (e) {
    if (!dropZoneEl.contains(e.relatedTarget)) {
      dropZoneEl.classList.remove('drag-over');
    }
  });

  dropZoneEl.addEventListener('drop', function (e) {
    e.preventDefault();
    dropZoneEl.classList.remove('drag-over');
    const files = Array.from(e.dataTransfer.files).filter(f => f.type === 'application/pdf' || f.name.toLowerCase().endsWith('.pdf'));
    if (files.length > 0) {
      onFilesAdded(files);
    }
  });

  dropZoneEl.addEventListener('click', function (e) {
    if (e.target !== fileInputEl) {
      fileInputEl.click();
    }
  });

  fileInputEl.addEventListener('change', function () {
    const files = Array.from(fileInputEl.files);
    if (files.length > 0) {
      onFilesAdded(files);
      fileInputEl.value = '';
    }
  });
}

function extractTextFromPDF(file, onProgress) {
  return new Promise(function (resolve, reject) {
    if (typeof pdfjsLib === 'undefined') {
      reject(new Error('PDF.js library not loaded'));
      return;
    }

    const workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    if (!pdfjsLib.GlobalWorkerOptions.workerSrc) {
      pdfjsLib.GlobalWorkerOptions.workerSrc = workerSrc;
    }

    const reader = new FileReader();

    reader.onload = function (e) {
      const typedArray = new Uint8Array(e.target.result);

      pdfjsLib.getDocument({ data: typedArray }).promise.then(function (pdf) {
        const pageCount = pdf.numPages;
        const pages = [];
        let processed = 0;

        if (onProgress) onProgress(0, pageCount, 'Starting extraction…');

        function extractPage(pageNum) {
          return pdf.getPage(pageNum).then(function (page) {
            var viewport = page.getViewport({ scale: 1 });
            return page.getTextContent().then(function (content) {
              // Parse structured items with spatial coordinates from the transform matrix.
              // transform[4] = x (left edge), transform[5] = y (baseline, PDF origin bottom-left)
              // transform[3] = font size (signed; height = |transform[3]|)
              var textItems = content.items.map(function (item) {
                return {
                  str: item.str,
                  x: item.transform[4],
                  y: item.transform[5],
                  width: item.width || 0,
                  height: Math.abs(item.transform[3]) || 10
                };
              });
              var text = textItems.map(function (it) { return it.str; }).join(' ');
              pages.push({
                pageNum: pageNum,
                text: text,
                textItems: textItems,
                width: viewport.width,
                height: viewport.height
              });
              processed++;
              if (onProgress) onProgress(processed, pageCount, 'Reading page ' + pageNum + ' of ' + pageCount);
            });
          });
        }

        const promises = [];
        for (let i = 1; i <= pageCount; i++) {
          promises.push(extractPage(i));
        }

        Promise.all(promises).then(function () {
          pages.sort(function (a, b) { return a.pageNum - b.pageNum; });
          const fullText = pages.map(function (p) { return p.text; }).join('\n');
          const scanned = isLikelyScanned(fullText, pageCount);

          resolve({
            name: file.name,
            pageCount: pageCount,
            pages: pages,
            fullText: fullText,
            isScanned: scanned,
            pdfDoc: pdf
          });
        }).catch(function (err) {
          reject(new Error('Failed to extract pages: ' + err.message));
        });
      }).catch(function (err) {
        reject(new Error('Failed to open PDF: ' + err.message));
      });
    };

    reader.onerror = function () {
      reject(new Error('Failed to read file: ' + file.name));
    };

    reader.readAsArrayBuffer(file);
  });
}

function isLikelyScanned(fullText, pageCount) {
  if (!fullText || fullText.trim().length === 0) return true;
  const cleaned = fullText.replace(/\s+/g, ' ').trim();
  const charsPerPage = pageCount > 0 ? cleaned.length / pageCount : 0;
  if (charsPerPage < 100) return true;
  const words = cleaned.split(' ').filter(function (w) { return w.length > 2; });
  const wordsPerPage = pageCount > 0 ? words.length / pageCount : 0;
  return wordsPerPage < 20;
}

/**
 * Render a PDF page to a canvas element (used for OCR fallback).
 * @param {Object} pdfDoc - PDF.js document object
 * @param {number} pageNum - 1-based page number
 * @param {number} scale - render scale (default 2.0 for good OCR quality)
 * @returns {Promise<HTMLCanvasElement>}
 */
function renderPageToCanvas(pdfDoc, pageNum, scale) {
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
