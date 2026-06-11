/* js/aiEnrichment.js - OpenAI note review and item prefill */

var AIEnrichment = (function () {
  var DEFAULT_MODEL = 'gpt-5.5';
  var MAX_CONTEXT_CHARS = 42000;

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

  function _documentContext(documents) {
    var remaining = MAX_CONTEXT_CHARS;
    return (documents || []).map(function (doc) {
      var name = doc.name || doc.originalPath || 'Document';
      var classification = doc.classification || {};
      var text = _compactText(doc.fullText || doc.extractedText || '', Math.max(1200, Math.min(remaining, 14000)));
      remaining -= text.length;
      return {
        name: name,
        type: classification.type || doc.docType || doc.kind || '',
        sheetNames: doc.sheetNames || [],
        text: text
      };
    }).filter(function (doc) {
      return doc.text;
    });
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

    var globalProps = {
      frameType: { type: ['string', 'null'] },
      system: { type: ['string', 'null'] },
      colour: { type: ['string', 'null'] },
      finish: { type: ['string', 'null'] },
      glazingSpec: { type: ['string', 'null'] },
      openingType: { type: ['string', 'null'] },
      hardware: { type: ['string', 'null'] },
      missingFields: { type: 'array', items: { type: 'string' } }
    };

    return {
      type: 'object',
      additionalProperties: false,
      required: ['summary', 'items', 'windowDefaults', 'doorDefaults'],
      properties: {
        summary: { type: 'string' },
        windowDefaults: {
          type: 'object',
          additionalProperties: false,
          required: Object.keys(globalProps),
          properties: globalProps
        },
        doorDefaults: {
          type: 'object',
          additionalProperties: false,
          required: Object.keys(globalProps),
          properties: globalProps
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

  function _applyAiResult(items, aiResult) {
    var byId = {};
    var byRef = {};
    (items || []).forEach(function (item) {
      if (item.id) byId[item.id] = item;
      if (item.reference) byRef[String(item.reference).toLowerCase()] = item;
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
        updatedFields: changed,
        notes: row.notes || [],
        reviewedAt: new Date().toISOString()
      };
      item.aiEnriched = changed.length > 0;
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
      task: 'Review the tender notes and BoQ text, verify the parser output, and prefill missing glazing schedule fields. Do not invent values. If the tender docs do not state a value, return null and list that field in missingFields.',
      documents: _documentContext(documents),
      extractedItems: _itemPayload(items)
    };

    return fetch('https://api.openai.com/v1/responses', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + apiKey
      },
      body: JSON.stringify({
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
      })
    }).then(function (response) {
      if (!response.ok) {
        return response.text().then(function (body) {
          throw new Error('OpenAI enrichment failed (' + response.status + '): ' + body.slice(0, 240));
        });
      }
      return response.json();
    }).then(function (data) {
      var text = _extractOutputText(data);
      if (!text) throw new Error('OpenAI returned no enrichment text');
      var aiResult = JSON.parse(text);
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
