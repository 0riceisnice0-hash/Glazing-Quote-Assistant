/* js/quoteGenerator.js â€” PDF generation using jsPDF */

var QuoteGenerator = (function () {

  var NAVY = [0, 46, 58];
  var NAVY_LIGHT = [47, 172, 102];
  var GRAY = [107, 114, 128];
  var LIGHT_GRAY = [245, 247, 246];
  var WHITE = [255, 255, 255];
  var BLACK = [17, 24, 39];
  var GREEN = [47, 172, 102];

  function formatCurrency(value) {
    return 'Â£' + Number(value || 0).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }

  function formatDate(dateStr) {
    if (!dateStr) return '';
    var d = new Date(dateStr);
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' });
  }

  function addValidityDate(dateStr, days) {
    if (!dateStr) return '';
    var d = new Date(dateStr);
    if (isNaN(d.getTime())) return '';
    d.setDate(d.getDate() + (parseInt(days, 10) || 30));
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'long', year: 'numeric' });
  }

  function getFensterCompany(company) {
    company = company || {};
    return {
      name: 'Fenster Glazing Ltd',
      address: company.address || '',
      phone: company.phone || '',
      email: company.email || '',
      logoDataUrl: company.logoDataUrl || null,
      logoAsset: company.logoAsset || 'assets/fenster-logo.png'
    };
  }

  function getFensterLogoElement(company) {
    if (company.logoDataUrl) return company.logoDataUrl;
    if (typeof document !== 'undefined') {
      var img = document.getElementById('headerLogo');
      if (img && img.complete && img.naturalWidth > 0) return img;
    }
    return null;
  }

  function addFensterLogo(doc, company, x, y, w, h) {
    var logo = getFensterLogoElement(company);
    if (logo) {
      try {
        doc.addImage(logo, company.logoDataUrl ? 'PNG' : undefined, x, y, w, h);
        return true;
      } catch (e) { /* fall back to text */ }
    }
    doc.setTextColor.apply(doc, NAVY);
    doc.setFontSize(18);
    doc.setFont(undefined, 'bold');
    doc.text('Fenster', x, y + 8);
    doc.setFontSize(9);
    doc.setFont(undefined, 'normal');
    doc.text('GLAZING', x + 27, y + 8);
    return false;
  }
  function generateQuotePDF(state, pricingConfig, options) {
    var jsPDFLib = window.jspdf ? window.jspdf.jsPDF : (window.jsPDF || (typeof jsPDF !== 'undefined' ? jsPDF : null));
    if (!jsPDFLib) throw new Error('jsPDF library not loaded');

    var doc = new jsPDFLib({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    var pageWidth = doc.internal.pageSize.getWidth();
    var pageHeight = doc.internal.pageSize.getHeight();
    var margin = 20;
    var contentWidth = pageWidth - margin * 2;

    var company = getFensterCompany(state.company || {});
    var meta = Object.assign({}, state.metadata || {});
    meta.notes = buildCommercialNotes(state, meta.notes);
    var items = state.items || [];
    var pricing = pricingConfig || state.pricing || {};
    var detailMode = (options && options.detailMode) || 'detailed';
    var presets = state.presets || {};

    var summary = Pricing.getPriceSummary(items, pricing);

    renderPage1(doc, company, meta, pageWidth, pageHeight, margin, contentWidth, summary);

    var groupedItems = groupItemsByType(items);
    var types = Object.keys(groupedItems);

    if (detailMode === 'compact') {
      renderCompactTable(doc, types, groupedItems, margin, contentWidth, company, pageWidth, pageHeight, presets);
    } else {
      renderDetailedSchedule(doc, types, groupedItems, margin, contentWidth, company, pageWidth, pageHeight, presets);
    }

    var finalY = doc.lastAutoTable ? doc.lastAutoTable.finalY + 10 : (doc._lastDetailY || 30) + 10;

    if (finalY > pageHeight - 80) {
      doc.addPage();
      finalY = 25;
    }

    renderPriceSummary(doc, summary, meta, pageWidth, pageHeight, margin, contentWidth, finalY);

    var pagesCount = doc.internal.getNumberOfPages();
    for (var i = 1; i <= pagesCount; i++) {
      doc.setPage(i);
      addPageNumbering(doc, i, pagesCount, pageWidth, pageHeight);
    }

    return doc;
  }

  function buildCommercialNotes(state, existingNotes) {
    var sections = [];
    if (existingNotes) sections.push(existingNotes);

    function accepted(list) {
      return (list || []).filter(function (entry) {
        return entry && (entry.status === 'accepted' || entry.status === 'approved' || entry.status === 'open');
      });
    }

    var assumptions = accepted(state.assumptions);
    var exclusions = accepted(state.exclusions);
    var rfis = accepted(state.rfis);
    var acceptedRisks = (state.risks || []).filter(function (risk) { return risk.status === 'accepted'; });

    if (assumptions.length) {
      sections.push('Assumptions:\n' + assumptions.map(function (a) { return '- ' + a.message; }).join('\n'));
    }
    if (exclusions.length) {
      sections.push('Exclusions:\n' + exclusions.map(function (e) { return '- ' + e.message; }).join('\n'));
    }
    if (rfis.length) {
      sections.push('Clarifications/RFIs:\n' + rfis.map(function (r) { return '- ' + r.message; }).join('\n'));
    }
    if (acceptedRisks.length) {
      sections.push('Estimator accepted risks:\n' + acceptedRisks.map(function (r) { return '- ' + r.message; }).join('\n'));
    }

    return sections.join('\n\n');
  }

  /* ===== COMPACT MODE: traditional 6-column autoTable ===== */
  function renderCompactTable(doc, types, groupedItems, margin, contentWidth, company, pageWidth, pageHeight, presets) {
    var tableBody = [];

    types.forEach(function (type) {
      var typeItems = groupedItems[type];
      var typeLabel = type.charAt(0).toUpperCase() + type.slice(1) + 's';

      tableBody.push([
        { content: typeLabel, colSpan: 6, styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold', fontSize: 9 } }
      ]);

      // Per-type general spec row. Prefer extracted item spec when it conflicts with an old preset.
      var p = getTypeSpecPreset(presets, type, typeItems);
      if (p) {
        var specParts = [];
        if (p.system) specParts.push(p.system);
        if (p.colour) specParts.push(p.colour);
        if (p.glazingMakeup) specParts.push(p.glazingMakeup);
        if (p.hardware) specParts.push(p.hardware);
        if (p.cillType) specParts.push(p.cillType);
        if (p.ventilation) specParts.push(p.ventilation);
        if (p.drainage) specParts.push(p.drainage + ' drainage');
        if (specParts.length > 0) {
          tableBody.push([
            { content: 'Spec: ' + specParts.join('  |  '), colSpan: 6, styles: { fillColor: [239, 246, 255], textColor: GRAY, fontStyle: 'italic', fontSize: 7 } }
          ]);
        }
      }

      var typeTotal = 0;
      typeItems.forEach(function (item) {
        var dims = item.width > 0 && item.height > 0
          ? item.width + ' Ã— ' + item.height + ' mm'
          : 'TBC';
        tableBody.push([
          item.reference || '-',
          (item.description || item.glazingSpec || 'Glazing item').substring(0, 50),
          dims,
          item.quantity || 1,
          formatCurrency(item.unitPrice),
          formatCurrency(item.totalPrice)
        ]);
        typeTotal += item.totalPrice || 0;
      });

      tableBody.push([
        { content: typeLabel + ' Subtotal', colSpan: 5, styles: { fontStyle: 'bold', fontSize: 8, halign: 'right', fillColor: [229, 231, 235] } },
        { content: formatCurrency(typeTotal), styles: { fontStyle: 'bold', fontSize: 8, halign: 'right', fillColor: [229, 231, 235] } }
      ]);
    });

    doc.autoTable({
      startY: 95,
      head: [[
        { content: 'Ref', styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold' } },
        { content: 'Description', styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold' } },
        { content: 'Size', styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold' } },
        { content: 'Qty', styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold', halign: 'center' } },
        { content: 'Unit Price', styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold', halign: 'right' } },
        { content: 'Total', styles: { fillColor: NAVY, textColor: WHITE, fontStyle: 'bold', halign: 'right' } }
      ]],
      body: tableBody,
      theme: 'grid',
      styles: { fontSize: 8, cellPadding: 3, textColor: BLACK, lineColor: [209, 213, 219], lineWidth: 0.3 },
      columnStyles: {
        0: { cellWidth: 18 },
        1: { cellWidth: 'auto' },
        2: { cellWidth: 30 },
        3: { cellWidth: 14, halign: 'center' },
        4: { cellWidth: 26, halign: 'right' },
        5: { cellWidth: 26, halign: 'right' }
      },
      alternateRowStyles: { fillColor: LIGHT_GRAY },
      margin: { left: margin, right: margin },
      didDrawPage: function (data) {
        addPageFooter(doc, company, pageWidth, pageHeight, margin);
        addPageHeader(doc, company, pageWidth, margin);
      }
    });
  }

  /* ===== DETAILED MODE: per-item specification cards ===== */
  function renderDetailedSchedule(doc, types, groupedItems, margin, contentWidth, company, pageWidth, pageHeight, presets) {
    var y = 95;
    var cardH = 32;   // base height for a spec card
    var labelCol = margin + 4;
    var valCol = margin + 32;
    var rightLabelCol = margin + contentWidth / 2 + 4;
    var rightValCol = margin + contentWidth / 2 + 32;
    var priceCol = margin + contentWidth - 4;

    types.forEach(function (type) {
      var typeItems = groupedItems[type];
      var typeLabel = type.charAt(0).toUpperCase() + type.slice(1) + 's';

      // Type heading band
      if (y > pageHeight - 50) {
        doc.addPage();
        addPageHeader(doc, company, pageWidth, margin);
        addPageFooter(doc, company, pageWidth, pageHeight, margin);
        y = 25;
      }

      doc.setFillColor.apply(doc, NAVY);
      doc.rect(margin, y, contentWidth, 8, 'F');
      doc.setTextColor.apply(doc, WHITE);
      doc.setFontSize(9);
      doc.setFont(undefined, 'bold');
      doc.text(typeLabel, margin + 4, y + 5.5);
      y += 12;

      // General spec block for this type
      y = renderTypeSpec(doc, presets, type, typeItems, margin, contentWidth, y, pageWidth, pageHeight, company);

      var typeTotal = 0;

      typeItems.forEach(function (item) {
        var dims = item.width > 0 && item.height > 0
          ? item.width + ' Ã— ' + item.height + ' mm'
          : 'TBC';
        var qty = item.quantity || 1;

        // Build spec rows to render
        var leftSpecs = [];
        var rightSpecs = [];

        if (item.system)       leftSpecs.push(['System:', item.system]);
        if (item.colour)       rightSpecs.push(['Colour:', item.colour]);
        leftSpecs.push(['Size:', dims]);
        rightSpecs.push(['Qty:', String(qty)]);
        if (item.glazingMakeup || item.glazingSpec) leftSpecs.push(['Glazing:', item.glazingMakeup || item.glazingSpec]);
        if (item.glassRequirement) leftSpecs.push(['Glass Req:', item.glassRequirement]);
        if (item.hardware)     rightSpecs.push(['Hardware:', item.hardware]);
        if (item.cillType)     leftSpecs.push(['Cill:', item.cillType]);
        if (item.drainage)     rightSpecs.push(['Drainage:', item.drainage]);
        if (item.openingType && item.openingType !== 'Fixed') leftSpecs.push(['Opening:', item.openingType]);
        if (item.ventilation)  rightSpecs.push(['Vent:', item.ventilation]);
        if (item.escapeWindow === 'Yes') leftSpecs.push(['Escape:', 'Yes']);
        if (item.frameType && item.frameType !== 'Unknown') rightSpecs.push(['Frame:', item.frameType]);
        if (item.securityRequirement) rightSpecs.push(['SBD/PAS24:', item.securityRequirement]);
        if (item.sealantRequirement) leftSpecs.push(['Sealant:', item.sealantRequirement]);
        if (item.windLoadRequirement) rightSpecs.push(['Windload:', item.windLoadRequirement]);
        if (item.fixingRequirement) leftSpecs.push(['Fixing:', item.fixingRequirement]);
        if (item.entranceDoor === 'Yes') rightSpecs.push(['Entrance:', 'Yes']);
        if (item.automationRequirement) leftSpecs.push(['Automation:', item.automationRequirement]);
        if (item.accessControlRequirement) rightSpecs.push(['Access:', item.accessControlRequirement]);
        if (item.handleRequirement) leftSpecs.push(['Handle:', item.handleRequirement]);
        if (item.lockRequirement) rightSpecs.push(['Lock:', item.lockRequirement]);
        if (item.closerRequirement) leftSpecs.push(['Closer:', item.closerRequirement]);

        var rowCount = Math.max(leftSpecs.length, rightSpecs.length);
        var neededH = 10 + rowCount * 4.5 + 4; // header + rows + padding

        if (y + neededH > pageHeight - 20) {
          doc.addPage();
          addPageHeader(doc, company, pageWidth, margin);
          addPageFooter(doc, company, pageWidth, pageHeight, margin);
          y = 25;
        }

        // Card background
        doc.setFillColor(249, 250, 251);
        doc.setDrawColor(209, 213, 219);
        doc.setLineWidth(0.3);
        doc.roundedRect(margin, y, contentWidth, neededH, 1.5, 1.5, 'FD');

        // Reference header line
        doc.setFontSize(8.8);
        doc.setFont(undefined, 'bold');
        doc.setTextColor.apply(doc, NAVY);
        var itemDescription = item.description || item.location || item.glazingSpec || item.type || 'Glazing item';
        var refLabel = (item.reference || '-') + '  ' + itemDescription;
        doc.text(refLabel.substring(0, 86), labelCol, y + 6);

        // Total price on the right of the header
        doc.setFontSize(8.8);
        doc.setFont(undefined, 'bold');
        doc.text('Qty ' + qty + '  |  ' + formatCurrency(item.totalPrice), priceCol, y + 6, { align: 'right' });
        // Spec rows
        var specY = y + 11;
        doc.setFontSize(7.5);

        for (var r = 0; r < rowCount; r++) {
          if (leftSpecs[r]) {
            doc.setFont(undefined, 'bold');
            doc.setTextColor.apply(doc, GRAY);
            doc.text(leftSpecs[r][0], labelCol, specY);
            doc.setFont(undefined, 'normal');
            doc.setTextColor.apply(doc, BLACK);
            doc.text(leftSpecs[r][1].substring(0, 35), valCol, specY);
          }
          if (rightSpecs[r]) {
            doc.setFont(undefined, 'bold');
            doc.setTextColor.apply(doc, GRAY);
            doc.text(rightSpecs[r][0], rightLabelCol, specY);
            doc.setFont(undefined, 'normal');
            doc.setTextColor.apply(doc, BLACK);
            doc.text(rightSpecs[r][1].substring(0, 35), rightValCol, specY);
          }
          specY += 4.5;
        }

        y += neededH + 3;
        typeTotal += item.totalPrice || 0;
      });

      // Subtotal bar for this type
      if (y + 8 > pageHeight - 20) {
        doc.addPage();
        addPageHeader(doc, company, pageWidth, margin);
        addPageFooter(doc, company, pageWidth, pageHeight, margin);
        y = 25;
      }
      doc.setFillColor(229, 231, 235);
      doc.rect(margin, y, contentWidth, 7, 'F');
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.setTextColor.apply(doc, BLACK);
      doc.text(typeLabel + ' Subtotal', margin + contentWidth - 50, y + 5);
      doc.text(formatCurrency(typeTotal), margin + contentWidth - 4, y + 5, { align: 'right' });
      y += 12;
    });

    doc._lastDetailY = y;
  }

  /* ===== PER-TYPE GENERAL SPEC (printed under each type heading) ===== */
  function getTypeSpecPreset(presets, type, items) {
    var p = presets && presets[type] ? Object.assign({}, presets[type]) : {};
    var sample = (items || []).find(function (item) {
      return item && (item.system || item.frameType || item.colour || item.glazingMakeup || item.glazingSpec || item.hardware);
    });
    if (!sample) return p;

    var presetLooksWrong = false;
    if (sample.frameType === 'Aluminium' && /\b(?:PVC|PVCu|Liniar)\b/i.test([p.frameType, p.system].join(' '))) {
      presetLooksWrong = true;
    }
    if (sample.system && p.system && p.system !== sample.system && presetLooksWrong) {
      p.system = sample.system;
    } else if (!p.system && sample.system) {
      p.system = sample.system;
    }
    if (sample.frameType && sample.frameType !== 'Unknown' && (presetLooksWrong || !p.frameType)) p.frameType = sample.frameType;
    if (sample.colour && (presetLooksWrong || !p.colour)) p.colour = sample.colour;
    if ((sample.glazingMakeup || sample.glazingSpec) && (presetLooksWrong || !p.glazingMakeup)) p.glazingMakeup = sample.glazingMakeup || sample.glazingSpec;
    if (sample.hardware && (presetLooksWrong || !p.hardware)) p.hardware = sample.hardware;
    if (sample.drainage && !p.drainage) p.drainage = sample.drainage;
    if (sample.ventilation && !p.ventilation) p.ventilation = sample.ventilation;
    return p;
  }

  function renderTypeSpec(doc, presets, type, items, margin, contentWidth, y, pageWidth, pageHeight, company) {
    var p = getTypeSpecPreset(presets, type, items);
    if (!p) return y;

    var leftLines = [];
    var rightLines = [];
    if (p.system)       leftLines.push(['System:', p.system]);
    if (p.colour)       rightLines.push(['Colour:', p.colour]);
    if (p.glazingMakeup) leftLines.push(['Glazing:', p.glazingMakeup]);
    if (p.hardware)     rightLines.push(['Hardware:', p.hardware]);
    if (p.cillType)     leftLines.push(['Cill/Threshold:', p.cillType]);
    if (p.drainage)     rightLines.push(['Drainage:', p.drainage]);
    if (p.ventilation)  leftLines.push(['Ventilation:', p.ventilation]);

    var rowCount = Math.max(leftLines.length, rightLines.length);
    if (rowCount === 0) return y;

    var neededH = 8 + rowCount * 4.5 + 4;

    if (y + neededH > pageHeight - 30) {
      doc.addPage();
      addPageHeader(doc, company, pageWidth, margin);
      addPageFooter(doc, company, pageWidth, pageHeight, margin);
      y = 25;
    }

    // Spec box background
    doc.setFillColor(239, 246, 255);
    doc.setDrawColor.apply(doc, NAVY_LIGHT);
    doc.setLineWidth(0.3);
    doc.roundedRect(margin, y, contentWidth, neededH, 1.5, 1.5, 'FD');

    // Heading
    doc.setFontSize(8);
    doc.setFont(undefined, 'bold');
    doc.setTextColor.apply(doc, NAVY);
    doc.text('GENERAL SPECIFICATION', margin + 4, y + 6);

    var specY = y + 11;
    var leftLabel = margin + 4;
    var leftVal = margin + 34;
    var rightLabel = margin + contentWidth / 2 + 4;
    var rightVal = margin + contentWidth / 2 + 34;

    doc.setFontSize(7.5);
    for (var r = 0; r < rowCount; r++) {
      if (leftLines[r]) {
        doc.setFont(undefined, 'bold');
        doc.setTextColor.apply(doc, GRAY);
        doc.text(leftLines[r][0], leftLabel, specY);
        doc.setFont(undefined, 'normal');
        doc.setTextColor.apply(doc, BLACK);
        doc.text(leftLines[r][1].substring(0, 40), leftVal, specY);
      }
      if (rightLines[r]) {
        doc.setFont(undefined, 'bold');
        doc.setTextColor.apply(doc, GRAY);
        doc.text(rightLines[r][0], rightLabel, specY);
        doc.setFont(undefined, 'normal');
        doc.setTextColor.apply(doc, BLACK);
        doc.text(rightLines[r][1].substring(0, 40), rightVal, specY);
      }
      specY += 4.5;
    }

    return y + neededH + 4;
  }

  function renderPage1(doc, company, meta, pageWidth, pageHeight, margin, contentWidth, summary) {
    var y = margin;

    doc.setFillColor.apply(doc, WHITE);
    doc.rect(0, 0, pageWidth, pageHeight, 'F');

    addFensterLogo(doc, company, margin, 12, 58, 14.5);

    doc.setTextColor.apply(doc, NAVY);
    doc.setFontSize(23);
    doc.setFont(undefined, 'bold');
    doc.text('QUOTATION', pageWidth - margin, 18, { align: 'right' });
    doc.setFontSize(8.5);
    doc.setFont(undefined, 'normal');
    doc.text(meta.quoteNumber || 'GQ-DRAFT', pageWidth - margin, 25, { align: 'right' });

    doc.setDrawColor.apply(doc, NAVY_LIGHT);
    doc.setLineWidth(1.1);
    doc.line(margin, 34, pageWidth - margin, 34);

    doc.setFillColor.apply(doc, NAVY);
    doc.rect(0, 40, pageWidth, 14, 'F');
    doc.setTextColor.apply(doc, WHITE);
    doc.setFontSize(8.5);
    doc.setFont(undefined, 'bold');
    doc.text('Fenster Glazing Ltd', margin, 48.5);
    doc.setFont(undefined, 'normal');
    var strap = [];
    if (company.phone) strap.push('Tel: ' + company.phone);
    if (company.email) strap.push(company.email);
    doc.text(strap.join('   '), pageWidth - margin, 48.5, { align: 'right' });

    y = 62;

    var cardGap = 8;
    var cardW = (contentWidth - cardGap) / 2;
    drawInfoCard(doc, margin, y, cardW, 38, 'QUOTE DETAILS', [
      ['Quote number', meta.quoteNumber || 'GQ-DRAFT'],
      ['Date', formatDate(meta.quoteDate)],
      ['Valid until', addValidityDate(meta.quoteDate, meta.validityDays || 30)],
      ['Items', String(summary.itemCount || 0)]
    ]);
    drawInfoCard(doc, margin + cardW + cardGap, y, cardW, 38, 'PROJECT', [
      ['Project', meta.projectName || 'N/A'],
      ['Client', meta.clientName || 'N/A'],
      ['Quote value', formatCurrency(summary.total)],
      ['VAT', summary.vatEnabled ? (summary.vatRate + '% included') : 'Not applied']
    ]);

    y += 50;
    doc.setFontSize(8.7);
    doc.setFont(undefined, 'normal');
    doc.setTextColor.apply(doc, BLACK);
    var intro = 'Thank you for the opportunity to provide this quotation. The schedule below sets out the glazing items and commercial allowances extracted from the tender documents. Any scope that is not confirmed in the supplied information should be treated as an assumption, exclusion, or RFI before order.';
    var introLines = doc.splitTextToSize(intro, contentWidth);
    doc.text(introLines, margin, y);
    y += introLines.length * 4.3 + 8;

    doc.setFont(undefined, 'bold');
    doc.setFontSize(10.5);
    doc.setTextColor.apply(doc, NAVY);
    doc.text('ITEMISED SCHEDULE', margin, y);
    doc.setDrawColor.apply(doc, NAVY_LIGHT);
    doc.setLineWidth(0.8);
    doc.line(margin, y + 2.5, margin + 58, y + 2.5);
  }

  function drawInfoCard(doc, x, y, w, h, title, rows) {
    doc.setFillColor(246, 249, 248);
    doc.setDrawColor(210, 222, 219);
    doc.setLineWidth(0.35);
    doc.roundedRect(x, y, w, h, 2, 2, 'FD');
    doc.setFontSize(8);
    doc.setFont(undefined, 'bold');
    doc.setTextColor.apply(doc, NAVY);
    doc.text(title, x + 4, y + 7);
    var rowY = y + 13;
    rows.forEach(function (row) {
      doc.setFontSize(7.4);
      doc.setFont(undefined, 'normal');
      doc.setTextColor.apply(doc, GRAY);
      doc.text(row[0] + ':', x + 4, rowY);
      doc.setFont(undefined, 'bold');
      doc.setTextColor.apply(doc, BLACK);
      doc.text(String(row[1] || '-').substring(0, 30), x + w - 4, rowY, { align: 'right' });
      rowY += 5.5;
    });
  }
  function renderPriceSummary(doc, summary, meta, pageWidth, pageHeight, margin, contentWidth, y) {
    var summaryX = pageWidth - margin - 90;
    var summaryW = 90;

    // Calculate dynamic box height based on line items
    var lineCount = 2; // Subtotal + Total
    if (summary.includeInstallation) lineCount++;
    if (summary.includeEPDM)         lineCount++;
    if (summary.includeMastic)       lineCount++;
    if (summary.quoteExtraAmount !== 0) lineCount++;
    if (summary.discountAmount > 0)  lineCount += 2;
    if (summary.vatEnabled)          lineCount++;
    var boxH = 16 + lineCount * 5.5 + 8;

    doc.setFillColor(239, 246, 255);
    doc.setDrawColor.apply(doc, NAVY_LIGHT);
    doc.setLineWidth(0.3);
    doc.roundedRect(summaryX, y, summaryW, boxH, 2, 2, 'FD');

    doc.setFontSize(8);
    doc.setFont(undefined, 'bold');
    doc.setTextColor.apply(doc, NAVY);
    doc.text('PRICE SUMMARY', summaryX + 4, y + 7);

    doc.setFont(undefined, 'normal');
    doc.setTextColor.apply(doc, BLACK);

    var sy = y + 13;
    var rightCol = summaryX + summaryW - 4;

    doc.text('Product Subtotal:', summaryX + 4, sy);
    doc.text(Pricing.formatCurrency(summary.subtotal), rightCol, sy, { align: 'right' });
    sy += 5.5;

    if (summary.includeInstallation) {
      doc.text('Installation:', summaryX + 4, sy);
      doc.text(Pricing.formatCurrency(summary.installTotal), rightCol, sy, { align: 'right' });
      sy += 5.5;
    }

    if (summary.includeEPDM) {
      doc.text('EPDM:', summaryX + 4, sy);
      doc.text(Pricing.formatCurrency(summary.epdmTotal), rightCol, sy, { align: 'right' });
      sy += 5.5;
    }

    if (summary.includeMastic) {
      doc.text('Mastic:', summaryX + 4, sy);
      doc.text(Pricing.formatCurrency(summary.masticTotal), rightCol, sy, { align: 'right' });
      sy += 5.5;
    }

    if (summary.quoteExtraAmount !== 0) {
      doc.text((summary.quoteExtraLabel || 'Extra costs') + ':', summaryX + 4, sy);
      doc.text(Pricing.formatCurrency(summary.quoteExtraAmount), rightCol, sy, { align: 'right' });
      sy += 5.5;
    }

    if (summary.discountAmount > 0) {
      var discountLabel = summary.discountPercent > 0 && summary.discountFixedAmount > 0
        ? 'Discount (' + summary.discountPercent + '% + fixed):'
        : (summary.discountPercent > 0 ? 'Discount (' + summary.discountPercent + '%):' : 'Fixed Discount:');
      doc.setTextColor(220, 38, 38);
      doc.text(discountLabel, summaryX + 4, sy);
      doc.text('- ' + Pricing.formatCurrency(summary.discountAmount), rightCol, sy, { align: 'right' });
      doc.setTextColor.apply(doc, BLACK);
      sy += 5.5;

      doc.text('After Discount:', summaryX + 4, sy);
      doc.text(Pricing.formatCurrency(summary.afterDiscount), rightCol, sy, { align: 'right' });
      sy += 5.5;
    }

    if (summary.vatEnabled) {
      doc.text('VAT (' + summary.vatRate + '%):', summaryX + 4, sy);
      doc.text(Pricing.formatCurrency(summary.vatAmount), rightCol, sy, { align: 'right' });
      sy += 5.5;
    }

    doc.setLineWidth(0.5);
    doc.setDrawColor.apply(doc, NAVY);
    doc.line(summaryX + 4, sy - 1, rightCol, sy - 1);

    doc.setFontSize(10);
    doc.setFont(undefined, 'bold');
    doc.setTextColor.apply(doc, NAVY);
    doc.text('TOTAL:', summaryX + 4, sy + 4);
    doc.text(Pricing.formatCurrency(summary.total), rightCol, sy + 4, { align: 'right' });

    var termsY = y + boxH + 5;

    doc.setFontSize(7.5);
    doc.setFont(undefined, 'bold');
    doc.setTextColor.apply(doc, NAVY);
    doc.text('TERMS & CONDITIONS', margin, termsY);

    doc.setFont(undefined, 'normal');
    doc.setTextColor.apply(doc, BLACK);
    termsY += 5;

    var terms = [
      '1. This quotation is valid for ' + (meta.validityDays || 30) + ' days from the date of issue.',
      '2. Prices exclude all groundworks, structural alterations, and making good of surrounding finishes.',
      '3. A deposit of 30% is required upon acceptance. Balance payable upon completion.',
      '4. Lead times will be confirmed upon order. Any delays caused by others are not our responsibility.',
      '5. All works are subject to site survey. Final pricing may vary if site conditions differ from drawings.',
      '6. All glazing shall comply with BS 6262 and relevant Building Regulations.',
      '7. Warranty: 10 years on sealed units, 5 years on frames from date of installation.'
    ];

    terms.forEach(function (term) {
      var tLines = doc.splitTextToSize(term, contentWidth - 95);
      doc.text(tLines, margin, termsY);
      termsY += tLines.length * 4 + 1;
    });

    var sigY = Math.max(termsY + 8, y + boxH + 25);
    if (sigY > pageHeight - 30) {
      doc.addPage();
      sigY = 30;
    }

    doc.setFont(undefined, 'bold');
    doc.setFontSize(8);
    doc.setTextColor.apply(doc, NAVY);
    doc.text('ACCEPTANCE', margin, sigY);
    doc.setFont(undefined, 'normal');
    doc.setTextColor.apply(doc, BLACK);
    doc.setFontSize(8);
    doc.text('To accept this quotation, please sign and return a copy with your deposit payment.', margin, sigY + 5);

    var slY = sigY + 15;
    doc.setDrawColor(150, 150, 150);
    doc.setLineWidth(0.3);
    doc.line(margin, slY, margin + 70, slY);
    doc.line(margin + 90, slY, margin + 150, slY);
    doc.setFontSize(7);
    doc.text('Authorised Signature', margin, slY + 4);
    doc.text('Date', margin + 90, slY + 4);

    if (meta.notes) {
      var notesY = slY + 15;
      doc.setFontSize(8);
      doc.setFont(undefined, 'bold');
      doc.setTextColor.apply(doc, NAVY);
      doc.text('ADDITIONAL NOTES', margin, notesY);
      doc.setFont(undefined, 'normal');
      doc.setTextColor.apply(doc, BLACK);
      var noteLines = doc.splitTextToSize(meta.notes, contentWidth);
      doc.text(noteLines, margin, notesY + 5);
    }
  }

  function addPageHeader(doc, company, pageWidth, margin) {
    var currentPage = doc.internal.getCurrentPageInfo().pageNumber;
    if (currentPage <= 1) return;

    doc.setFillColor.apply(doc, NAVY);
    doc.rect(0, 0, pageWidth, 12, 'F');
    doc.setTextColor.apply(doc, WHITE);
    doc.setFontSize(7);
    doc.setFont(undefined, 'bold');
    doc.text((company.name || 'Glazing Quote'), margin, 8);
    doc.setFont(undefined, 'normal');
    doc.text('QUOTATION â€” Continued', pageWidth - margin, 8, { align: 'right' });
  }

  function addPageFooter(doc, company, pageWidth, pageHeight, margin) {
    doc.setDrawColor(209, 213, 219);
    doc.setLineWidth(0.3);
    doc.line(margin, pageHeight - 12, pageWidth - margin, pageHeight - 12);
    doc.setFontSize(7);
    doc.setFont(undefined, 'normal');
    doc.setTextColor.apply(doc, GRAY);
    doc.text(company.name || 'Glazing Quote Assistant', margin, pageHeight - 7);
    if (company.email) {
      doc.text(company.email, pageWidth / 2, pageHeight - 7, { align: 'center' });
    }
  }

  function addPageNumbering(doc, pageNum, totalPages, pageWidth, pageHeight) {
    doc.setFontSize(7);
    doc.setFont(undefined, 'normal');
    doc.setTextColor.apply(doc, GRAY);
    doc.text('Page ' + pageNum + ' of ' + totalPages, pageWidth - 20, pageHeight - 7, { align: 'right' });
  }

  function groupItemsByType(items) {
    var groups = {};
    items.forEach(function (item) {
      var type = item.type || 'other';
      if (!groups[type]) groups[type] = [];
      groups[type].push(item);
    });
    var ordered = {};
    ['window', 'door', 'screen', 'curtain wall', 'other'].forEach(function (t) {
      if (groups[t] && groups[t].length) ordered[t] = groups[t];
    });
    Object.keys(groups).forEach(function (t) {
      if (!ordered[t]) ordered[t] = groups[t];
    });
    return ordered;
  }

  return {
    generateQuotePDF: generateQuotePDF
  };
})();

