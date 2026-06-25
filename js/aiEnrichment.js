/* js/aiEnrichment.js - OpenAI note review and item prefill */

var AIEnrichment = (function () {
  var DEFAULT_MODEL = 'gpt-4o-mini';
  var MAX_CONTEXT_CHARS = 18000;
  var OPENAI_TIMEOUT_MS = 60000;

  var UPDATE_FIELDS = [
    'frameType',
    'system',
    'colour',
    'finish',
    'openingType',
    'glazingSpec',
    'glassRequirement',
    'glazingMakeup',
    'hardware',
    'cillType',
    'ventilation',
    'drainage',
    'doorGlazing',
    'fireRating',
    'entranceDoor',
    'automationRequirement',
    'accessControlRequirement',
    'handleRequirement',
    'lockRequirement',
    'closerRequirement',
    'ironmongery'
  ];

  function _clean(value) {
    return String(value == null ? '' : value).trim();
  }

  function _compactText(text, limit) {
    text = _clean(text).replace(/\s+/g, ' ');
    if (text.length <= limit) return text;
    var head = text.slice(0, Math.floor(limit * 0.65));
    var tail = text.slice(text.length - Math.floor(limit * 0.35));
    return head + '\n...\n' + tail;
  }

  function _refPattern(items) {
    var refs = (items || []).map(function (item) { return _clean(item.reference); })
      .filter(Boolean)
      .filter(function (ref, idx, arr) { return arr.indexOf(ref) === idx; })
      .slice(0, 120);
    if (!refs.length) return null;
    refs.sort(function (a, b) { return b.length - a.length; });
    return new RegExp('\\b(' + refs.map(function (ref) {
      return ref.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }).join('|') + ')\\b', 'gi');
  }

  function _snippetsForRefs(text, pattern, limit) {
    if (!pattern) return '';
    text = _clean(text).replace(/\s+/g, ' ');
    var snippets = [];
    var seen = {};
    var match;
    pattern.lastIndex = 0;
    while ((match = pattern.exec(text)) && snippets.join('\n').length < limit) {
      var start = Math.max(0, match.index - 260);
      var end = Math.min(text.length, match.index + 520);
      var snippet = text.slice(start, end).trim();
      var key = snippet.slice(0, 120);
      if (!seen[key]) {
        seen[key] = true;
        snippets.push(snippet);
      }
      if (pattern.lastIndex === match.index) pattern.lastIndex += 1;
    }
    return snippets.join('\n---\n').slice(0, limit);
  }

  function _snippetsForTenderTerms(text, limit) {
    text = _clean(text).replace(/\s+/g, ' ');
    if (!text) return '';
    var terms = /(door|doors|doorset|window|windows|opening|entrance|reception|lobby|automatic|access control|colour|color|ral|ppc|powder|paint|finish|handle|lock|closer|ironmongery|hardware|chartwell|anthracite|grey|gray|white|black)/ig;
    var snippets = [];
    var seen = {};
    var match;
    terms.lastIndex = 0;
    while ((match = terms.exec(text)) && snippets.join('\n').length < limit) {
      var start = Math.max(0, match.index - 220);
      var end = Math.min(text.length, match.index + 520);
      var snippet = text.slice(start, end).trim();
      var key = snippet.slice(0, 140);
      if (!seen[key]) {
        seen[key] = true;
        snippets.push(snippet);
      }
      if (terms.lastIndex === match.index) terms.lastIndex += 1;
    }
    return snippets.join('\n---\n').slice(0, limit);
  }

  function _documentContext(documents, items) {
    var remaining = MAX_CONTEXT_CHARS;
    var refPattern = _refPattern(items);
    return (documents || []).map(function (doc) {
      var name = doc.name || doc.originalPath || 'Document';
      var classification = doc.classification || {};
      var type = classification.type || doc.docType || doc.kind || '';
      var rawText = doc.fullText || doc.extractedText || '';
      var isCoreDoc = /schedule|bq|bill|workbook/i.test(type + ' ' + name);
      var text = _snippetsForRefs(rawText, refPattern, Math.min(remaining, isCoreDoc ? 6000 : 2500));
      var termText = _snippetsForTenderTerms(rawText, Math.min(remaining - text.length, isCoreDoc ? 3500 : 2500));
      if (termText) text = [text, termText].filter(Boolean).join('\n---\n');
      if (!text && isCoreDoc) text = _compactText(rawText, Math.min(remaining, 3500));
      if (!text) return null;
      remaining -= text.length;
      return {
        name: name,
        type: type,
        sheetNames: doc.sheetNames || [],
        text: text
      };
    }).filter(Boolean);
  }

  function _itemPayload(items) {
    return (items || []).map(function (item) {
      return {
        id: item.id || '',
        reference: item.reference || '',
        type: item.type || '',
        description: item.description || item.location || '',
        sourceDocument: item.sourceDocument || '',
        quantity: item.quantity || 1,
        width: item.width || null,
        height: item.height || null,
        frameType: item.frameType || '',
        system: item.system || '',
        colour: item.colour || '',
        finish: item.finish || '',
        openingType: item.openingType || '',
        glazingSpec: item.glazingSpec || item.glassRequirement || '',
        hardware: item.hardware || item.ironmongery || '',
        notes: item.notes || []
      };
    });
  }

  function _schema() {
    var updateProps = {};
    UPDATE_FIELDS.forEach(function (field) {
      updateProps[field] = { type: ['string', 'null'] };
    });

    var windowDefaultProps = {
      frameType: { type: ['string', 'null'] },
      system: { type: ['string', 'null'] },
      colour: { type: ['string', 'null'] },
      finish: { type: ['string', 'null'] },
      glazingSpec: { type: ['string', 'null'] },
      openingType: { type: ['string', 'null'] },
      hardware: { type: ['string', 'null'] },
      missingFields: { type: 'array', items: { type: 'string' } }
    };
    var doorDefaultProps = Object.assign({}, windowDefaultProps, {
      entranceRef: { type: ['string', 'null'] },
      doorColour: { type: ['string', 'null'] },
      handle: { type: ['string', 'null'] },
      lock: { type: ['string', 'null'] },
      closer: { type: ['string', 'null'] },
      ironmongeryNotes: { type: ['string', 'null'] }
    });

    return {
      type: 'object',
      additionalProperties: false,
      required: ['summary', 'items', 'windowDefaults', 'doorDefaults'],
      properties: {
        summary: { type: 'string' },
        windowDefaults: {
          type: 'object',
          additionalProperties: false,
          required: Object.keys(windowDefaultProps),
          properties: windowDefaultProps
        },
        doorDefaults: {
          type: 'object',
          additionalProperties: false,
          required: Object.keys(doorDefaultProps),
          properties: doorDefaultProps
        },
        items: {
          type: 'array',
          items: {
            type: 'object',
            additionalProperties: false,
            required: ['id', 'reference', 'confirmed', 'confidence', 'updates', 'missingFields', 'notes'],
            properties: {
              id: { type: 'string' },
              reference: { type: 'string' },
              confirmed: { type: 'boolean' },
              confidence: { type: 'number' },
              updates: {
                type: 'object',
                additionalProperties: false,
                required: UPDATE_FIELDS,
                properties: updateProps
              },
              missingFields: { type: 'array', items: { type: 'string' } },
              notes: { type: 'array', items: { type: 'string' } }
            }
          }
        }
      }
    };
  }

  function _extractOutputText(data) {
    if (!data) return '';
    if (data.output_text) return data.output_text;
    var chunks = [];
    (data.output || []).forEach(function (part) {
      (part.content || []).forEach(function (content) {
        if (content.text) chunks.push(content.text);
        if (content.type === 'output_text' && content.text) chunks.push(content.text);
      });
    });
    return chunks.join('\n');
  }

  function _parseJsonObject(text) {
    text = _clean(text).replace(/^```(?:json)?/i, '').replace(/```$/i, '').trim();
    try {
      return JSON.parse(text);
    } catch (firstErr) {
      var start = text.indexOf('{');
      if (start === -1) throw firstErr;
      var depth = 0;
      var inString = false;
      var escaped = false;
      for (var i = start; i < text.length; i++) {
        var ch = text.charAt(i);
        if (escaped) {
          escaped = false;
          continue;
        }
        if (ch === '\\') {
          escaped = true;
          continue;
        }
        if (ch === '"') {
          inString = !inString;
          continue;
        }
        if (inString) continue;
        if (ch === '{') depth += 1;
        if (ch === '}') {
          depth -= 1;
          if (depth === 0) {
            return JSON.parse(text.slice(start, i + 1));
          }
        }
      }
      throw firstErr;
    }
  }

  function _fetchJsonWithTimeout(url, request, timeoutMs) {
    var controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
    var timer = controller ? setTimeout(function () { controller.abort(); }, timeoutMs || OPENAI_TIMEOUT_MS) : null;
    if (controller) request.signal = controller.signal;
    return fetch(url, request).then(function (response) {
      if (timer) clearTimeout(timer);
      if (!response.ok) {
        return response.text().then(function (body) {
          throw new Error('OpenAI enrichment failed (' + response.status + '): ' + body.slice(0, 240));
        });
      }
      return response.json();
    }).catch(function (err) {
      if (timer) clearTimeout(timer);
      if (err && err.name === 'AbortError') {
        throw new Error('OpenAI enrichment timed out after ' + Math.round((timeoutMs || OPENAI_TIMEOUT_MS) / 1000) + ' seconds');
      }
      throw err;
    });
  }

  function _applyAiResult(items, aiResult) {
    var byId = {};
    var byRef = {};
    (items || []).forEach(function (item) {
      if (item.id) byId[item.id] = item;
      if (item.reference) byRef[String(item.reference).toLowerCase()] = item;
    });

    function setIfMissing(item, field, value, changed) {
      value = _clean(value);
      if (!value || item[field]) return;
      item[field] = value;
      if (changed && changed.indexOf(field) === -1) changed.push(field);
    }
    function addAiNote(item, note) {
      note = _clean(note);
      if (!note) return;
      if (!item.notes) item.notes = [];
      if (item.notes.indexOf(note) === -1) item.notes.push(note);
    }
    function applyDefaults(item) {
      var defaults = item.type === 'door' ? (aiResult.doorDefaults || {}) : (item.type === 'window' ? (aiResult.windowDefaults || {}) : null);
      if (!defaults) return [];
      var changed = [];
      setIfMissing(item, 'frameType', defaults.frameType, changed);
      setIfMissing(item, 'system', defaults.system, changed);
      setIfMissing(item, 'colour', defaults.doorColour || defaults.colour, changed);
      setIfMissing(item, 'finish', defaults.finish, changed);
      setIfMissing(item, 'openingType', defaults.openingType, changed);
      setIfMissing(item, 'glazingSpec', defaults.glazingSpec, changed);
      if (defaults.glazingSpec && !item.glassRequirement) item.glassRequirement = defaults.glazingSpec;
      if (item.type === 'door') {
        setIfMissing(item, 'handleRequirement', defaults.handle, changed);
        setIfMissing(item, 'lockRequirement', defaults.lock, changed);
        setIfMissing(item, 'closerRequirement', defaults.closer, changed);
        setIfMissing(item, 'ironmongery', defaults.ironmongeryNotes || defaults.hardware, changed);
        if (item.ironmongery && !item.hardware) item.hardware = item.ironmongery;
        if (defaults.entranceRef && item.reference && String(defaults.entranceRef).toLowerCase() === String(item.reference).toLowerCase()) {
          item.entranceDoor = 'Yes';
          addAiNote(item, 'AI identified as entrance door');
        }
        if (defaults.entranceRef) {
          item.aiEntranceRef = defaults.entranceRef;
        }
      } else {
        setIfMissing(item, 'hardware', defaults.hardware, changed);
      }
      return changed;
    }

    (items || []).forEach(function (item) {
      var defaultFields = applyDefaults(item);
      if (defaultFields.length) {
        item.aiEnriched = true;
        item.aiDefaultedFields = defaultFields;
      }
    });

    (aiResult.items || []).forEach(function (row) {
      var item = byId[row.id] || byRef[String(row.reference || '').toLowerCase()];
      if (!item) return;
      var changed = [];
      UPDATE_FIELDS.forEach(function (field) {
        var value = row.updates ? _clean(row.updates[field]) : '';
        if (!value) return;
        item[field] = value;
        if (field === 'glazingMakeup' && !item.glazingSpec) item.glazingSpec = value;
        if (field === 'glazingSpec' && !item.glassRequirement) item.glassRequirement = value;
        if (field === 'ironmongery' && !item.hardware) item.hardware = value;
        changed.push(field);
      });
      if (!item.notes) item.notes = [];
      (row.notes || []).forEach(function (note) {
        note = _clean(note);
        if (note && item.notes.indexOf(note) === -1) item.notes.push(note);
      });
      item.aiReview = {
        confirmed: !!row.confirmed,
        confidence: typeof row.confidence === 'number' ? row.confidence : 0,
        missingFields: row.missingFields || [],
        updatedFields: changed.concat(item.aiDefaultedFields || []),
        notes: row.notes || [],
        reviewedAt: new Date().toISOString()
      };
      item.aiEnriched = changed.length > 0 || !!item.aiEnriched;
      item.aiMissingFields = row.missingFields || [];
    });

    return items;
  }

  function enrichItems(documents, items, options) {
    options = options || {};
    var apiKey = _clean(options.apiKey);
    if (!options.enabled || !apiKey || !items || items.length === 0) {
      return Promise.resolve({
        items: items || [],
        skipped: true,
        reason: !apiKey ? 'Missing OpenAI API key' : 'AI enrichment disabled'
      });
    }

    var payload = {
      task: 'Review the tender notes and BoQ text, verify the parser output, and prefill missing glazing schedule fields. Prioritise fields marked [RED_TEXT] and fill doorColour, entranceDoor, handleRequirement, lockRequirement, closerRequirement, and ironmongery when stated. If an external materials schedule states a colour to match windows and doors, use that as the door/window colour. If main entrance/reception/lobby automatic doors are stated, identify the relevant entrance reference or explain if the extracted item refs do not include it. Do not invent values. If the tender docs do not state a value, return null and list that field in missingFields.',
      documents: _documentContext(documents, items),
      extractedItems: _itemPayload(items)
    };

    var openaiRequest = {
      model: options.model || DEFAULT_MODEL,
      store: false,
      input: [
        {
          role: 'system',
          content: [{ type: 'input_text', text: 'You are a commercial glazing estimator. Return only schema-valid JSON. Prefer exact notes from BoQs, Excel remarks, specifications, and drawing labels over guesses.' }]
        },
        {
          role: 'user',
          content: [{ type: 'input_text', text: JSON.stringify(payload) }]
        }
      ],
      text: {
        format: {
          type: 'json_schema',
          name: 'glazing_item_enrichment',
          strict: true,
          schema: _schema()
        }
      }
    };

    var proxyUrl = _clean(options.proxyUrl).replace(/\/+$/, '');
    var requestUrl = proxyUrl ? proxyUrl + '/openai-enrich' : 'https://api.openai.com/v1/responses';
    var request = proxyUrl ? {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ apiKey: apiKey, openaiRequest: openaiRequest })
    } : {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey
      },
      body: JSON.stringify(openaiRequest)
    };

    return _fetchJsonWithTimeout(requestUrl, request, options.timeoutMs || OPENAI_TIMEOUT_MS).then(function (data) {
      var text = _extractOutputText(data);
      if (!text) throw new Error('OpenAI returned no enrichment text');
      var aiResult = _parseJsonObject(text);
      return {
        items: _applyAiResult(items, aiResult),
        summary: aiResult.summary || '',
        windowDefaults: aiResult.windowDefaults || {},
        doorDefaults: aiResult.doorDefaults || {},
        raw: aiResult
      };
    });
  }

  return {
    enrichItems: enrichItems,
    DEFAULT_MODEL: DEFAULT_MODEL
  };
})();
