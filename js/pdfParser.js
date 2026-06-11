/* js/pdfParser.js — PDF upload and text extraction using PDF.js */

function isSupportedTenderFile(file) {
  var name = (file && file.name ? file.name : '').toLowerCase();
  return /\.(pdf|xlsx|xlsm|xls|zip|docx|eml|msg|jpe?g|png)$/.test(name) || (file && file.type === 'application/pdf');
}

function isWorkbookFile(file) {
  var name = (file && file.name ? file.name : '').toLowerCase();
  return /\.(xlsx|xlsm|xls)$/.test(name);
}

function getTenderFileName(file) {
  return file.webkitRelativePath || file.name;
}

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
    const files = Array.from(e.dataTransfer.files).filter(isSupportedTenderFile);
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
              // Smart text joining: detect adjacent text items with no visual gap
              // and join them without a space. This fixes PDF.js fragmentation where
              // e.g. "EW" and "19" are separate items but visually contiguous.
              var textParts = [];
              for (var ti = 0; ti < textItems.length; ti++) {
                var curr = textItems[ti];
                if (ti > 0) {
                  var prev = textItems[ti - 1];
                  var prevRightEdge = prev.x + prev.width;
                  var gap = curr.x - prevRightEdge;
                  var sameRow = Math.abs(curr.y - prev.y) < 3;
                  // If items are on the same row and gap is tiny (<2pt), join without space
                  if (sameRow && gap >= -2 && gap < 2) {
                    textParts.push(curr.str);
                  } else {
                    textParts.push(' ' + curr.str);
                  }
                } else {
                  textParts.push(curr.str);
                }
              }
              var text = textParts.join('');
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
            name: getTenderFileName(file),
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

function extractWorkbook(file, onProgress) {
  return new Promise(function (resolve, reject) {
    if (typeof XLSX === 'undefined') {
      reject(new Error('Excel parser library not loaded'));
      return;
    }

    if (onProgress) onProgress(0, 1, 'Reading workbook');

    file.arrayBuffer().then(function (buffer) {
      var workbook = XLSX.read(buffer, { cellDates: false, cellFormula: false, raw: false });
      var pages = workbook.SheetNames.map(function (sheetName, idx) {
        var sheet = workbook.Sheets[sheetName];
        var rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '', raw: false });
        var normalisedRows = rows.map(function (row) {
          return row.map(function (cell) { return String(cell || '').trim(); });
        });
        var textItems = [];
        normalisedRows.forEach(function (row, rowIdx) {
          row.forEach(function (cell, colIdx) {
            if (!cell) return;
            textItems.push({
              str: cell,
              x: colIdx * 120,
              y: (rows.length - rowIdx) * 18,
              width: Math.max(30, cell.length * 7),
              height: 12
            });
          });
        });
        var lines = normalisedRows
          .map(function (row) { return row.filter(Boolean).join(' | '); })
          .filter(Boolean);
        return {
          pageNum: idx + 1,
          sheetName: sheetName,
          text: [sheetName].concat(lines).join('\n'),
          textItems: textItems,
          width: 0,
          height: 0
        };
      });
      var fullText = pages.map(function (page) { return page.text; }).join('\n');
      if (onProgress) onProgress(pages.length, pages.length || 1, 'Workbook extracted');
      resolve({
        name: getTenderFileName(file),
        pageCount: pages.length,
        pages: pages,
        fullText: fullText,
        isScanned: false
      });
    }).catch(function (err) {
      reject(new Error('Failed to read workbook: ' + err.message));
    });
  });
}

function extractTenderInput(file, onProgress) {
  if (isWorkbookFile(file)) {
    return extractWorkbook(file, onProgress);
  }
  return extractTextFromPDF(file, onProgress);
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
