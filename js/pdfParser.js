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
            return page.getTextContent().then(function (content) {
              const text = content.items.map(function (item) {
                return item.str;
              }).join(' ');
              pages.push({ pageNum: pageNum, text: text });
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
            isScanned: scanned
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
