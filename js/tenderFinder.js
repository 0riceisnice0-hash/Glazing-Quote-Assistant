/* js/tenderFinder.js - live tender source strategy and opportunity scoring */

var TenderFinder = (function () {
  var KEYWORDS = [
    'commercial windows',
    'aluminium windows',
    'aluminium doors',
    'windows and doors',
    'curtain walling',
    'glazing works',
    'replacement windows',
    'external doors',
    'louvre panels',
    'facade glazing'
  ];

  var CPV_CODES = [
    { code: '44221000', label: 'Windows, doors and related items' },
    { code: '45421100', label: 'Installation of doors, windows and related components' },
    { code: '45441000', label: 'Glazing work' },
    { code: '45443000', label: 'Facade work' }
  ];

  var SOURCES = [{
    id: 'find-tender',
    name: 'Find a Tender',
    type: 'Official public procurement',
    coverage: 'UK above-threshold public sector opportunities',
    cadence: 'Daily',
    searchUrl: 'https://www.find-tender.service.gov.uk/Search/Results?Keywords={query}',
    notes: 'Best for larger public-sector projects and frameworks.'
  }, {
    id: 'contracts-finder',
    name: 'Contracts Finder',
    type: 'Official public procurement',
    coverage: 'UK public contracts over lower thresholds',
    cadence: 'Daily',
    searchUrl: 'https://www.contractsfinder.service.gov.uk/Search/Results?searchCriteria={query}',
    notes: 'Best for smaller public-sector works and below-threshold notices.'
  }, {
    id: 'bidstats',
    name: 'Bidstats',
    type: 'Public tender index',
    coverage: 'Aggregated UK public procurement notices',
    cadence: 'Weekly check',
    searchUrl: 'https://bidstats.uk/tenders/?q={query}',
    notes: 'Useful for quick historic/live keyword checks and market sizing.'
  }, {
    id: 'barbour-abi',
    name: 'Barbour ABI',
    type: 'Paid construction lead platform',
    coverage: 'Planning, pre-tender, tender and awarded UK construction leads',
    cadence: 'Demo / subscription',
    searchUrl: 'https://barbour-abi.com/',
    notes: 'Good fit if Fenster wants earlier-stage private-sector construction leads, not only public tender portals.'
  }, {
    id: 'glenigan',
    name: 'Glenigan',
    type: 'Paid construction lead platform',
    coverage: 'Construction sales leads, marketing data and market analysis',
    cadence: 'Demo / subscription',
    searchUrl: 'https://www.glenigan.com/',
    notes: 'Comparable to Barbour ABI; worth benchmarking against ABI for lead quality and workflow.'
  }];

  function getSources() {
    return SOURCES.slice();
  }

  function getKeywords() {
    return KEYWORDS.slice();
  }

  function getCpvCodes() {
    return CPV_CODES.slice();
  }

  function buildSearchLinks(query) {
    query = query || 'windows doors glazing';
    return SOURCES.map(function (source) {
      return {
        sourceId: source.id,
        name: source.name,
        url: source.searchUrl.replace('{query}', encodeURIComponent(query)),
        type: source.type,
        notes: source.notes
      };
    });
  }

  function scoreOpportunity(text) {
    text = String(text || '').toLowerCase();
    var score = 0;
    var reasons = [];
    function hit(pattern, points, reason) {
      if (pattern.test(text)) {
        score += points;
        reasons.push(reason);
      }
    }
    hit(/\baluminium|aluminum|curtain\s*wall|facade|shopfront/, 20, 'Commercial aluminium/facade language');
    hit(/\bwindow|glazing|door|louvre|screen/, 20, 'Core Fenster product keywords');
    hit(/\bcommercial|school|hospital|care\s*home|council|housing|framework|public\s*sector/, 15, 'Commercial/public-sector context');
    hit(/\bsupply\s+and\s+install|installation|replacement|refurbishment/, 15, 'Supply/install scope');
    hit(/\btender|procurement|framework|opportunity|contract/, 10, 'Procurement language');
    hit(/\bfire\s*rated|pas\s*24|secured\s+by\s+design|u[-\s]?value|part\s*l/, 10, 'Spec-driven opportunity');
    if (/\bwindow\s+cleaning|cleaning\s+of\s+windows|blind[s]?\b/.test(text)) {
      score -= 35;
      reasons.push('Likely not a glazing supply/install opportunity');
    }
    var status = score >= 60 ? 'High fit' : (score >= 35 ? 'Possible fit' : 'Low fit');
    return { score: Math.max(0, Math.min(100, score)), status: status, reasons: reasons };
  }

  function buildResearchSummary() {
    return {
      answer: 'Yes. The practical route is a monitored tender-finder that checks official portals and paid construction lead platforms, scores opportunities, and feeds promising packs into the quote assistant.',
      officialSources: SOURCES.filter(function (s) { return /Official/.test(s.type); }),
      paidSources: SOURCES.filter(function (s) { return /Paid/.test(s.type); }),
      keywords: getKeywords(),
      cpvCodes: getCpvCodes(),
      nextSteps: [
        'Create saved searches and email alerts on Find a Tender and Contracts Finder.',
        'Trial Barbour ABI and Glenigan against the same Fenster keyword/region filters.',
        'Log opportunities into the bot with source URL, deadline, buyer, location, scope, value and documents.',
        'Score each opportunity before spending estimator time.',
        'When tender documents are available, run them through Project Hail Mary intake for scope/supplier/pricing review.'
      ]
    };
  }

  function buildAdamReply() {
    return [
      'Hi Adam,',
      '',
      'Research is going well. Short answer: yes, there can be a bot/workflow for this, but the best version is not just blindly scraping the internet.',
      '',
      'The sensible setup is:',
      '- monitor official sources like Find a Tender and Contracts Finder;',
      '- track paid construction lead platforms like Barbour ABI and Glenigan for earlier-stage private/commercial leads;',
      '- search against Fenster-specific keywords and CPV codes such as windows, doors, glazing works, curtain walling, aluminium windows, external doors and louvres;',
      '- score each lead for fit before anyone spends time pricing it;',
      '- pull any tender documents into the estimating bot for scope review, supplier quote checks, RFIs, exclusions and pricing.',
      '',
      'The Barbour ABI examples are useful because they show the type of commercial project lead data they provide, but the attached PDF is image-based, so the bot needs OCR/project-example ingestion rather than normal text parsing.',
      '',
      'My recommendation is that we test free/public alerts first, then trial Barbour ABI or Glenigan properly and compare lead quality, not just headline number of projects.',
      '',
      'Zac'
    ].join('\n');
  }

  return {
    getSources: getSources,
    getKeywords: getKeywords,
    getCpvCodes: getCpvCodes,
    buildSearchLinks: buildSearchLinks,
    scoreOpportunity: scoreOpportunity,
    buildResearchSummary: buildResearchSummary,
    buildAdamReply: buildAdamReply
  };
})();
