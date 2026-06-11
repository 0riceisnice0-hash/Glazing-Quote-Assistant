/* js/documentIntake.js - normalise messy tender inputs before extraction */

var DocumentIntake = (function () {
  var IMAGE_RE = /\.(jpe?g|png)$/i;
  var DOCX_RE = /\.docx$/i;
  var EML_RE = /\.eml$/i;
  var MSG_RE = /\.msg$/i;
  var ZIP_RE = /\.zip$/i;

  function processFiles(files, options, onProgress) {
    options = options || {};
    var result = { documents: [], risks: [], supplierEvidence: [], intakeRecords: [] };
    var chain = Promise.resolve();
    Array.from(files || []).forEach(function (file, idx) {
      chain = chain.then(function () {
        if (onProgress) onProgress(idx, files.length, 'Reading ' + file.name);
        return processFile(file, { originalPath: file.webkitRelativePath || file.name, parentArchive: '' }, options);
      }).then(function (entry) {
        mergeResult(result, entry);
      }).catch(function (err) {
        result.risks.push(makeRisk('critical', 'Could not process "' + file.name + '": ' + err.message, {
          sourceDocumentName: file.name,
          suggestedAction: 'Convert the file to PDF/XLSX or process it with the cloud worker.'
        }));
      });
    });
    return chain.then(function () { return result; });
  }

  function processFile(file, context, options) {
    var name = context.originalPath || file.name;
    if (ZIP_RE.test(name)) return processZip(file, context, options);
    if (DOCX_RE.test(name)) return processDocx(file, context, options);
    if (EML_RE.test(name)) return processEml(file, context, options);
    if (MSG_RE.test(name)) return options.cloudEnabled ? processWithCloud(file, context, options) : unsupportedMsg(file, context);
    if (IMAGE_RE.test(name)) return processImage(file, context, options);
    if (typeof isSupportedTenderFile === 'function' && isSupportedTenderFile(file)) {
      return extractTenderInput(file).then(function (doc) {
        doc = normaliseDoc(doc, file, context, inferKind(name));
        var role = inferRole(name, doc.fullText);
        doc.role = role;
        doc.classification = classifyRole(doc);
        return {
          documents: [doc],
          risks: risksForDocument(doc),
          supplierEvidence: extractSupplierEvidence(doc),
          intakeRecords: [recordFor(file, context, doc, 'processed')]
        };
      });
    }
    return Promise.resolve({
      documents: [],
      risks: [makeRisk('warning', 'Unsupported tender file skipped: ' + name, {
        sourceDocumentName: name,
        suggestedAction: 'Convert this file to PDF, Excel, DOCX, EML, JPG or PNG.'
      })],
      supplierEvidence: [],
      intakeRecords: [recordFor(file, context, null, 'unsupported')]
    });
  }

  function processZip(file, context, options) {
    if (typeof JSZip === 'undefined') {
      if (options.cloudEnabled) return processWithCloud(file, context, options);
      return Promise.resolve({
        documents: [],
        risks: [makeRisk('critical', 'ZIP file could not be opened locally because JSZip is unavailable: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Enable cloud document processing or upload the extracted files.'
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'zip-unsupported')]
      });
    }
    return JSZip.loadAsync(file).then(function (zip) {
      var result = { documents: [], risks: [], supplierEvidence: [], intakeRecords: [recordFor(file, context, null, 'zip-opened')] };
      var entries = [];
      zip.forEach(function (relativePath, entry) {
        if (!entry.dir) entries.push({ relativePath: relativePath, entry: entry });
      });
      var chain = Promise.resolve();
      entries.forEach(function (zipEntry) {
        chain = chain.then(function () {
          return zipEntry.entry.async('blob').then(function (blob) {
            var childName = (context.originalPath || file.name) + '/' + zipEntry.relativePath;
            var childFile = new File([blob], zipEntry.relativePath, { type: blob.type || inferMime(zipEntry.relativePath) });
            return processFile(childFile, {
              originalPath: childName,
              parentArchive: context.originalPath || file.name
            }, options);
          }).then(function (childResult) {
            mergeResult(result, childResult);
          });
        });
      });
      return chain.then(function () { return result; });
    }).catch(function (err) {
      if (options.cloudEnabled) return processWithCloud(file, context, options);
      return {
        documents: [],
        risks: [makeRisk('critical', 'ZIP file could not be opened locally: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Extract manually or enable cloud document processing. Error: ' + err.message
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'zip-error')]
      };
    });
  }

  function processDocx(file, context, options) {
    if (typeof JSZip === 'undefined') {
      if (options && options.cloudEnabled) return processWithCloud(file, context, options);
      return Promise.resolve({
        documents: [],
        risks: [makeRisk('critical', 'DOCX file could not be opened locally because JSZip is unavailable: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Enable cloud document processing or save this document as PDF.'
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'docx-unsupported')]
      });
    }
    return JSZip.loadAsync(file).then(function (zip) {
      var docXml = zip.file('word/document.xml');
      if (!docXml) throw new Error('DOCX has no word/document.xml');
      return docXml.async('text');
    }).then(function (xml) {
      var text = extractDocxText(xml);
      var doc = makeTextDocument(file, context, 'docx', text);
      return {
        documents: [doc],
        risks: risksForDocument(doc),
        supplierEvidence: extractSupplierEvidence(doc),
        intakeRecords: [recordFor(file, context, doc, 'processed')]
      };
    }).catch(function (err) {
      if (options && options.cloudEnabled) return processWithCloud(file, context, options);
      return {
        documents: [],
        risks: [makeRisk('critical', 'DOCX file could not be opened locally: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Save this document as PDF or enable cloud document processing. Error: ' + err.message
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'docx-error')]
      };
    });
  }

  function processEml(file, context, options) {
    return file.text().then(function (raw) {
      var parsed = parseEml(raw);
      var doc = makeTextDocument(file, context, 'email', parsed.text);
      var risks = risksForDocument(doc);
      if (/attachment/i.test(raw)) {
        risks.push(makeRisk('warning', 'Email may contain attachments that were not extracted locally: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Upload attachments separately or enable cloud email processing.'
        }));
      }
      return {
        documents: [doc],
        risks: risks,
        supplierEvidence: extractSupplierEvidence(doc),
        intakeRecords: [recordFor(file, context, doc, 'processed')]
      };
    });
  }

  function unsupportedMsg(file, context) {
    return Promise.resolve({
      documents: [],
      risks: [makeRisk('critical', 'MSG email files need cloud processing or manual export: ' + context.originalPath, {
        sourceDocumentName: context.originalPath,
        suggestedAction: 'Save the email as EML/PDF or enable the Cloudflare Worker intake.'
      })],
      supplierEvidence: [],
      intakeRecords: [recordFor(file, context, null, 'msg-unsupported')]
    });
  }

  function processImage(file, context, options) {
    if (typeof Tesseract === 'undefined') {
      if (options && options.cloudEnabled) return processWithCloud(file, context, options);
      return Promise.resolve({
        documents: [],
        risks: [makeRisk('critical', 'Image OCR unavailable for: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Refresh with Tesseract available or enable cloud OCR.'
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'ocr-unavailable')]
      });
    }
    return Tesseract.recognize(file, 'eng', { logger: function () {} }).then(function (result) {
      var text = result && result.data ? (result.data.text || '') : '';
      var doc = makeTextDocument(file, context, 'image', text);
      doc.isScanned = true;
      doc.ocrAttempted = true;
      doc.ocrSuccess = text.trim().length > 50;
      doc.extractionMethod = 'ocr';
      var risks = risksForDocument(doc);
      risks.push(makeRisk('warning', 'Image-derived drawing/text needs estimator review before pricing: ' + context.originalPath, {
        sourceDocumentName: context.originalPath,
        suggestedAction: 'Review OCR text and create/approve drawing takeoff candidates manually.'
      }));
      return {
        documents: [doc],
        risks: risks,
        supplierEvidence: extractSupplierEvidence(doc),
        intakeRecords: [recordFor(file, context, doc, 'ocr')]
      };
    });
  }

  function processWithCloud(file, context, options) {
    var workerUrl = normaliseWorkerUrl(options && options.cloudWorkerUrl);
    if (!workerUrl) {
      return Promise.resolve({
        documents: [],
        risks: [makeRisk('critical', 'Cloud processing is enabled but no Worker URL is configured for: ' + context.originalPath, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Enter the Cloudflare Worker URL or disable cloud processing.'
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'cloud-missing-url')]
      });
    }

    var form = new FormData();
    form.append('files', file, context.originalPath || file.name);

    return fetch(workerUrl.replace(/\/$/, '') + '/process-file', {
      method: 'POST',
      body: form
    }).then(function (response) {
      if (!response.ok) throw new Error('Worker returned HTTP ' + response.status);
      return response.json();
    }).then(function (payload) {
      var result = {
        documents: (payload.documents || []).map(function (doc) { return normaliseCloudDocument(doc, context); }),
        risks: payload.risks || [],
        supplierEvidence: payload.supplierEvidence || [],
        intakeRecords: payload.intakeRecords || []
      };
      result.intakeRecords.push(recordFor(file, context, null, 'processed-cloud'));
      return result;
    }).catch(function (err) {
      return {
        documents: [],
        risks: [makeRisk('critical', 'Cloud processing failed for ' + context.originalPath + ': ' + err.message, {
          sourceDocumentName: context.originalPath,
          suggestedAction: 'Check the Worker URL/deployment or process this file locally/manual.'
        })],
        supplierEvidence: [],
        intakeRecords: [recordFor(file, context, null, 'cloud-error')]
      };
    });
  }

  function normaliseCloudDocument(doc, context) {
    doc = doc || {};
    doc.id = doc.id || generateId();
    doc.name = doc.name || context.originalPath;
    doc.originalPath = doc.originalPath || doc.name;
    doc.parentArchive = doc.parentArchive || context.parentArchive || '';
    doc.kind = doc.kind || 'worker';
    doc.pageCount = doc.pageCount || (doc.pages ? doc.pages.length : 1);
    doc.pages = doc.pages || [{
      pageNum: 1,
      text: doc.fullText || '',
      textItems: [],
      width: 0,
      height: 0
    }];
    doc.fullText = doc.fullText || doc.pages.map(function (page) { return page.text || ''; }).join('\n');
    doc.textItems = doc.textItems || [];
    doc.extractionMethod = doc.extractionMethod || 'worker';
    doc.role = doc.role || inferRole(doc.name, doc.fullText);
    doc.classification = doc.classification || classifyRole(doc);
    doc.provenance = doc.provenance || {
      originalPath: doc.originalPath,
      parentArchive: doc.parentArchive
    };
    return doc;
  }

  function normaliseWorkerUrl(url) {
    url = String(url || '').trim();
    if (!url) return '';
    if (!/^https?:\/\//i.test(url)) url = 'https://' + url;
    return url;
  }

  function makeTextDocument(file, context, kind, text) {
    var doc = {
      id: generateId(),
      name: context.originalPath || file.name,
      originalPath: context.originalPath || file.name,
      parentArchive: context.parentArchive || '',
      kind: kind,
      pageCount: 1,
      pages: [{
        pageNum: 1,
        text: text || '',
        textItems: [],
        width: 0,
        height: 0
      }],
      fullText: text || '',
      textItems: [],
      isScanned: false,
      extractionMethod: kind,
      provenance: {
        fileName: file.name,
        parentArchive: context.parentArchive || '',
        originalPath: context.originalPath || file.name
      }
    };
    doc.role = inferRole(doc.name, doc.fullText);
    doc.classification = classifyRole(doc);
    return doc;
  }

  function normaliseDoc(doc, file, context, kind) {
    doc.id = doc.id || generateId();
    doc.name = context.originalPath || doc.name || file.name;
    doc.originalPath = context.originalPath || file.name;
    doc.parentArchive = context.parentArchive || '';
    doc.kind = kind;
    doc.extractionMethod = doc.extractionMethod || (kind === 'workbook' ? 'sheetjs' : 'pdfjs');
    doc.provenance = {
      fileName: file.name,
      parentArchive: context.parentArchive || '',
      originalPath: context.originalPath || file.name
    };
    return doc;
  }

  function inferKind(name) {
    if (/\.(xlsx|xlsm|xls)$/i.test(name)) return 'workbook';
    if (/\.pdf$/i.test(name)) return 'pdf';
    return 'file';
  }

  function inferRole(name, text) {
    var lowerName = (name || '').toLowerCase();
    var lowerText = (text || '').substring(0, 3000).toLowerCase();
    if (/\bclient quote\b/.test(lowerName) || /\bquotation\b|\bglazing quote\b/.test(lowerName)) return 'client_quote';
    if (/\bsupplier quotes?\b/.test(lowerName) || /\bsupplier\b/.test(lowerName)) return 'supplier_quote';
    if (typeof DataExtractor !== 'undefined') return DataExtractor.classifyDocument(name, text || '').type;
    if (/window\s*schedule|door\s*schedule|glazing\s*schedule/.test(lowerName + ' ' + lowerText)) return 'schedule';
    return 'unknown';
  }

  function classifyRole(doc) {
    if (doc.role === 'supplier_quote' || doc.role === 'client_quote') {
      return { type: 'admin', confidence: 'high', reason: doc.role.replace('_', ' ') + ' excluded from scope extraction' };
    }
    if (typeof DataExtractor !== 'undefined') return DataExtractor.classifyDocument(doc.name, doc.fullText || '');
    return { type: doc.role || 'unknown', confidence: 'low', reason: 'Document intake classification' };
  }

  function risksForDocument(doc) {
    var risks = [];
    if (doc.role === 'client_quote') {
      risks.push(makeRisk('info', 'Client quote excluded from extraction: ' + doc.name, {
        sourceDocumentId: doc.id,
        sourceDocumentName: doc.name
      }));
    }
    if (doc.role === 'supplier_quote') {
      risks.push(makeRisk('info', 'Supplier quote treated as cost evidence only: ' + doc.name, {
        sourceDocumentId: doc.id,
        sourceDocumentName: doc.name
      }));
    }
    if ((doc.kind === 'image' || doc.isScanned) && (!doc.fullText || doc.fullText.trim().length < 50)) {
      risks.push(makeRisk(doc.kind === 'image' ? 'warning' : 'critical', 'OCR produced little or no text for: ' + doc.name, {
        sourceDocumentId: doc.id,
        sourceDocumentName: doc.name,
        suggestedAction: 'Review the source manually or re-upload a clearer PDF/image.'
      }));
    }
    if (doc.role === 'drawing' && (doc.kind === 'image' || doc.isScanned)) {
      risks.push(makeRisk('warning', 'Scanned/image drawing needs human-assisted takeoff: ' + doc.name, {
        sourceDocumentId: doc.id,
        sourceDocumentName: doc.name,
        suggestedAction: 'Confirm refs/dimensions before using this drawing for pricing.'
      }));
    }
    return risks;
  }

  function extractSupplierEvidence(doc) {
    if (doc.role !== 'supplier_quote') return [];
    var evidence = [];
    var lines = (doc.fullText || '').split(/\r?\n/);
    lines.forEach(function (line, idx) {
      var refMatch = line.match(/\b(?:EW|ED|WG|WF|W|D|S|C|SAW|MAW|LAW|SPVC|MPVC|LPVC)[- ]?\d{1,3}[A-Z]?\b/i);
      var moneyMatches = line.match(/(?:£|\bGBP\s*)?\d{1,3}(?:,\d{3})*(?:\.\d{2})/g);
      if (!refMatch || !moneyMatches || !moneyMatches.length) return;
      var amounts = moneyMatches.map(parseMoney).filter(function (n) { return n > 0; });
      if (!amounts.length) return;
      evidence.push({
        id: generateId(),
        supplierName: '',
        sourceDocumentId: doc.id,
        sourceDocumentName: doc.name,
        sourceLocation: 'line ' + (idx + 1),
        matchedItemId: null,
        reference: refMatch[0].replace(/\s+/g, '').toUpperCase(),
        description: line.trim(),
        quantity: 1,
        unitRate: amounts[amounts.length - 1],
        total: amounts[amounts.length - 1],
        matchConfidence: 'low',
        status: 'proposed'
      });
    });
    return evidence;
  }

  function makeRisk(severity, message, extra) {
    return Object.assign({
      id: generateId(),
      type: 'risk',
      severity: severity || 'warning',
      message: message,
      status: 'open',
      suggestedAction: ''
    }, extra || {});
  }

  function recordFor(file, context, doc, status) {
    return {
      id: generateId(),
      name: context.originalPath || file.name,
      parentArchive: context.parentArchive || '',
      kind: doc ? doc.kind : inferKind(context.originalPath || file.name),
      role: doc ? doc.role : '',
      status: status,
      documentId: doc ? doc.id : null
    };
  }

  function mergeResult(target, source) {
    target.documents = target.documents.concat(source.documents || []);
    target.risks = target.risks.concat(source.risks || []);
    target.supplierEvidence = target.supplierEvidence.concat(source.supplierEvidence || []);
    target.intakeRecords = target.intakeRecords.concat(source.intakeRecords || []);
  }

  function extractDocxText(xml) {
    return xml
      .replace(/<\/w:p>/g, '\n')
      .replace(/<\/w:tr>/g, '\n')
      .replace(/<\/w:tc>/g, ' | ')
      .replace(/<[^>]+>/g, '')
      .replace(/&amp;/g, '&')
      .replace(/&lt;/g, '<')
      .replace(/&gt;/g, '>')
      .replace(/&quot;/g, '"')
      .replace(/&#39;/g, "'")
      .replace(/[ \t]+\n/g, '\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  }

  function parseEml(raw) {
    var parts = raw.split(/\r?\n\r?\n/);
    var headers = parts.shift() || '';
    var body = parts.join('\n\n');
    var subject = (headers.match(/^subject:\s*(.+)$/im) || [])[1] || '';
    body = body.replace(/--[A-Za-z0-9'()+_,\-\.\/:=?]+(?:--)?/g, '\n');
    body = body.replace(/Content-[^\n]+\n/gi, '\n');
    return { subject: subject, text: (subject ? 'Subject: ' + subject + '\n\n' : '') + body.trim() };
  }

  function parseMoney(value) {
    return parseFloat(String(value).replace(/[£,\s]|GBP/gi, '')) || 0;
  }

  function inferMime(name) {
    if (/\.pdf$/i.test(name)) return 'application/pdf';
    if (/\.docx$/i.test(name)) return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document';
    if (/\.png$/i.test(name)) return 'image/png';
    if (/\.jpe?g$/i.test(name)) return 'image/jpeg';
    return 'application/octet-stream';
  }

  return {
    processFiles: processFiles,
    processFile: processFile,
    extractSupplierEvidence: extractSupplierEvidence
  };
})();
