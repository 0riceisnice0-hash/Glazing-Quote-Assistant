/* js/floorplanParser.js — Extract wall geometry, doors & windows from floor plan PDFs
 *
 * Completely independent module.  Reads a PDF File object using PDF.js,
 * walks the operator list to collect vector paths, then classifies walls,
 * door-swings and window openings.
 *
 * Usage:
 *   FloorplanParser.parse(file)          // File object → Promise<FloorplanData>
 *   FloorplanParser.parseFromBytes(u8)   // Uint8Array  → Promise<FloorplanData>
 */

var FloorplanParser = (function () {

  /* ── helpers ─────────────────────────────────────────────── */

  function transformPoint(m, x, y) {
    return {
      x: m[0] * x + m[2] * y + m[4],
      y: m[1] * x + m[3] * y + m[5]
    };
  }

  function multiplyMatrices(a, b) {
    return [
      a[0] * b[0] + a[2] * b[1],
      a[1] * b[0] + a[3] * b[1],
      a[0] * b[2] + a[2] * b[3],
      a[1] * b[2] + a[3] * b[3],
      a[0] * b[4] + a[2] * b[5] + a[4],
      a[1] * b[4] + a[3] * b[5] + a[5]
    ];
  }

  function dist(a, b) {
    var dx = a.x - b.x, dy = a.y - b.y;
    return Math.sqrt(dx * dx + dy * dy);
  }

  function midpoint(a, b) { return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }; }

  function angleDeg(ax, ay, bx, by) {
    return Math.atan2(by - ay, bx - ax) * 180 / Math.PI;
  }

  /* ── PDF operator list walker ───────────────────────────── */

  function walkOperatorList(ops, argsArray) {
    var OPS = pdfjsLib.OPS;

    var segments = [];          // { p1, p2, lineWidth }
    var arcs     = [];          // { centre, radius, startAngle, endAngle, lineWidth }
    var fills    = [];          // closed filled paths
    var path     = [];          // points in current sub-path
    var pathCmds = [];          // 'L' | 'C' commands for current sub-path
    var lineWidth = 1;
    var ctm = [1, 0, 0, 1, 0, 0];
    var stack = [];

    for (var i = 0; i < ops.length; i++) {
      var fn   = ops[i];
      var args = argsArray[i];

      switch (fn) {
        /* graphics-state */
        case OPS.save:
          stack.push({ ctm: ctm.slice(), lineWidth: lineWidth });
          break;
        case OPS.restore:
          if (stack.length) {
            var s = stack.pop();
            ctm = s.ctm;
            lineWidth = s.lineWidth;
          }
          break;
        case OPS.transform:
          ctm = multiplyMatrices(ctm, args);
          break;
        case OPS.setLineWidth:
          lineWidth = args[0];
          break;

        /* path construction */
        case OPS.moveTo:
          path = [transformPoint(ctm, args[0], args[1])];
          pathCmds = [];
          break;
        case OPS.lineTo:
          path.push(transformPoint(ctm, args[0], args[1]));
          pathCmds.push('L');
          break;
        case OPS.curveTo:
          // Cubic Bézier — approximate as arc candidate
          var cp1 = transformPoint(ctm, args[0], args[1]);
          var cp2 = transformPoint(ctm, args[2], args[3]);
          var ep  = transformPoint(ctm, args[4], args[5]);
          path.push(cp1, cp2, ep);
          pathCmds.push('C');
          break;
        case OPS.curveTo2:
          var ccp1 = path.length ? path[path.length - 1] : { x: 0, y: 0 };
          var ccp2 = transformPoint(ctm, args[0], args[1]);
          var cep  = transformPoint(ctm, args[2], args[3]);
          path.push(ccp1, ccp2, cep);
          pathCmds.push('C');
          break;
        case OPS.curveTo3:
          // 'y' operator: cp2 = endpoint
          var dcp1 = transformPoint(ctm, args[0], args[1]);
          var dep  = transformPoint(ctm, args[2], args[3]);
          path.push(dcp1, dep, dep);
          pathCmds.push('C');
          break;
        case OPS.closePath:
          if (path.length) path.push(path[0]);
          pathCmds.push('Z');
          break;
        case OPS.rectangle:
          var rx = args[0], ry = args[1], rw = args[2], rh = args[3];
          var r0 = transformPoint(ctm, rx, ry);
          var r1 = transformPoint(ctm, rx + rw, ry);
          var r2 = transformPoint(ctm, rx + rw, ry + rh);
          var r3 = transformPoint(ctm, rx, ry + rh);
          path = [r0, r1, r2, r3, r0];
          pathCmds = ['L', 'L', 'L', 'Z'];
          break;

        /* path painting */
        case OPS.stroke:
          _harvestPath(segments, arcs, path, pathCmds, lineWidth*Math.abs(ctm[0]), false);
          path = [];
          pathCmds = [];
          break;
        case OPS.fill:
        case OPS.eoFill:
          _harvestPath(segments, arcs, path, pathCmds, lineWidth*Math.abs(ctm[0]), true);
          path = [];
          pathCmds = [];
          break;
        case OPS.fillStroke:
        case OPS.eoFillStroke:
          _harvestPath(segments, arcs, path, pathCmds, lineWidth*Math.abs(ctm[0]), true);
          path = [];
          pathCmds = [];
          break;
        case OPS.endPath:
          path = [];
          pathCmds = [];
          break;
      }
    }

    return { segments: segments, arcs: arcs, fills: fills };
  }

  function _harvestPath(segments, arcs, path, cmds, lw, isFill) {
    if (path.length < 2) return;

    var idx = 0; // index into pathCmds
    var prev = path[0];
    var pi = 1;

    while (pi < path.length && idx < cmds.length) {
      var cmd = cmds[idx];
      if (cmd === 'L' || cmd === 'Z') {
        segments.push({ p1: prev, p2: path[pi], lineWidth: lw, isFill: isFill });
        prev = path[pi];
        pi++;
        idx++;
      } else if (cmd === 'C') {
        // Three points: cp1, cp2, endpoint
        if (pi + 2 < path.length) {
          var cp1 = path[pi];
          var cp2 = path[pi + 1];
          var ep  = path[pi + 2];
          _tryArc(arcs, prev, cp1, cp2, ep, lw);
          prev = ep;
          pi += 3;
        } else {
          pi++;
        }
        idx++;
      } else {
        idx++;
        pi++;
      }
    }
  }

  /* Detect if a cubic Bézier approximates a circular arc (quarter-circle door swing). */
  function _tryArc(arcs, p0, cp1, cp2, p3, lw) {
    // Chord length
    var chord = dist(p0, p3);
    if (chord < 5) return; // too small

    // Estimate centre: for a quarter-circle arc, the centre is at the corner
    // where the two radius lines meet.  For a cubic approx of 90° arc with
    // radius r: cp1 ≈ start + 0.5523*r*tangent, cp2 ≈ end + 0.5523*r*tangent.
    // Quick heuristic: centre ≈ average of the two control-point "extensions"
    var mid = midpoint(p0, p3);
    var cpMid = midpoint(cp1, cp2);
    // For a 90° arc, cpMid is offset from the chord midpoint towards centre
    // Estimate radius from chord length: chord = r*√2 for 90°
    var estRadius = chord / 1.4142;

    // Verify it's roughly circular: control points should be ~0.55r from endpoints
    var d1 = dist(p0, cp1);
    var d2 = dist(p3, cp2);
    var kappa = 0.5523;
    var expected = estRadius * kappa;
    var tolerance = 0.5;
    if (d1 < expected * (1 - tolerance) || d1 > expected * (1 + tolerance)) return;
    if (d2 < expected * (1 - tolerance) || d2 > expected * (1 + tolerance)) return;

    // Estimate centre as the point equidistant from p0 and p3 at distance ~radius
    // Two candidates — pick the one closer to cpMid offset
    var mx = (p0.x + p3.x) / 2;
    var my = (p0.y + p3.y) / 2;
    var dx = p3.x - p0.x;
    var dy = p3.y - p0.y;
    var halfChord = chord / 2;
    // Height from chord midpoint to arc centre
    var h = Math.sqrt(Math.max(0, estRadius * estRadius - halfChord * halfChord));
    var nx = -dy / chord;
    var ny =  dx / chord;
    var c1 = { x: mx + h * nx, y: my + h * ny };
    var c2 = { x: mx - h * nx, y: my - h * ny };

    var centre = dist(c1, cpMid) < dist(c2, cpMid) ? c1 : c2;
    var actualR = (dist(centre, p0) + dist(centre, p3)) / 2;

    // Sweep angle
    var a0 = Math.atan2(p0.y - centre.y, p0.x - centre.x);
    var a1 = Math.atan2(p3.y - centre.y, p3.x - centre.x);
    var sweep = Math.abs(a1 - a0);
    if (sweep > Math.PI) sweep = 2 * Math.PI - sweep;

    // Accept arcs between 60° and 120° (targeting 90° door swings)
    if (sweep < Math.PI / 3 || sweep > 2 * Math.PI / 3) return;

    arcs.push({
      centre: centre,
      radius: actualR,
      startPt: p0,
      endPt: p3,
      startAngle: a0,
      endAngle: a1,
      sweepDeg: sweep * 180 / Math.PI,
      lineWidth: lw
    });
  }

  /* ── text extraction (with positions) ───────────────────── */

  function extractTextItems(textContent, viewport) {
    var items = [];
    textContent.items.forEach(function (item) {
      if (!item.str || !item.str.trim()) return;
      var tx = item.transform;
      // transform: [scaleX, skewY, skewX, scaleY, transX, transY]
      items.push({
        text: item.str.trim(),
        x: tx[4],
        y: tx[5],
        width: item.width,
        height: item.height || Math.abs(tx[3])
      });
    });
    return items;
  }

  /* ── classification: walls, doors, windows ──────────────── */

  function classifyGeometry(segments, arcs, textItems, viewport) {
    // 1. Identify wall line width: most common thick line width
    var widthCounts = {};
    segments.forEach(function (s) {
      if (s.lineWidth < 0.1) return;
      var key = Math.round(s.lineWidth * 10) / 10;
      widthCounts[key] = (widthCounts[key] || 0) + 1;
    });

    // Sort width buckets by count, pick the top one that's "thick"
    var buckets = Object.keys(widthCounts).map(function (k) {
      return { width: parseFloat(k), count: widthCounts[k] };
    }).sort(function (a, b) { return b.count - a.count; });

    // Wall width: most frequent thick width (> 0.3)
    var wallWidth = 0.5;
    for (var i = 0; i < buckets.length; i++) {
      if (buckets[i].width >= 0.3) {
        wallWidth = buckets[i].width;
        break;
      }
    }

    // Allow a tolerance range for wall identification
    var wallThreshold = wallWidth * 0.6;

    // 2. Filter wall segments
    var walls = segments.filter(function (s) {
      return s.lineWidth >= wallThreshold && !s.isFill;
    }).map(function (s) {
      return { p1: s.p1, p2: s.p2, thickness: s.lineWidth, length: dist(s.p1, s.p2) };
    }).filter(function (w) {
      return w.length > 10; // skip tiny segments
    });

    // 3. Find glazing references in text
    var refPattern = /^(EW|ED|EG|ES|EC|W|D|S)\s*(\d{1,3})$/i;
    var refItems = [];
    textItems.forEach(function (t) {
      var m = t.text.match(refPattern);
      if (m) {
        refItems.push({
          ref: m[1].toUpperCase() + (m[1].length === 1 ? '0' : '') + m[2].replace(/^0+/, ''),
          rawRef: t.text,
          type: /^(ED|D)/.test(m[1].toUpperCase()) ? 'door' : 'window',
          x: t.x,
          y: t.y
        });
      }
    });

    // 4. Match door swings to ED references
    var doors = [];
    var usedArcs = new Set();

    refItems.filter(function (r) { return r.type === 'door'; }).forEach(function (ref) {
      // Find the nearest arc (door swing) to this text label
      var bestArc = null;
      var bestDist = Infinity;
      arcs.forEach(function (arc, idx) {
        if (usedArcs.has(idx)) return;
        var d = dist(ref, arc.centre);
        if (d < bestDist && d < arc.radius * 4) { // within 4× radius
          bestDist = d;
          bestArc = idx;
        }
      });
      if (bestArc !== null) usedArcs.add(bestArc);

      var arcData = bestArc !== null ? arcs[bestArc] : null;
      doors.push({
        ref: ref.ref,
        x: ref.x,
        y: ref.y,
        width: arcData ? arcData.radius * 2 : 60,    // door width ≈ arc radius (pdf units)
        swingRadius: arcData ? arcData.radius : 30,
        swingAngle: arcData ? arcData.sweepDeg : 90,
        hasSwingDetected: !!arcData,
        arc: arcData
      });
    });

    // 5. Match windows to EW references
    var windows = [];
    refItems.filter(function (r) { return r.type === 'window'; }).forEach(function (ref) {
      windows.push({
        ref: ref.ref,
        x: ref.x,
        y: ref.y
      });
    });

    // 6. Calculate bounds
    var bounds = { minX: Infinity, minY: Infinity, maxX: -Infinity, maxY: -Infinity };
    walls.forEach(function (w) {
      bounds.minX = Math.min(bounds.minX, w.p1.x, w.p2.x);
      bounds.minY = Math.min(bounds.minY, w.p1.y, w.p2.y);
      bounds.maxX = Math.max(bounds.maxX, w.p1.x, w.p2.x);
      bounds.maxY = Math.max(bounds.maxY, w.p1.y, w.p2.y);
    });

    return {
      walls: walls,
      doors: doors,
      windows: windows,
      bounds: bounds,
      wallWidth: wallWidth,
      viewport: { width: viewport.width, height: viewport.height }
    };
  }

  /* ── public API ─────────────────────────────────────────── */

  function parseFromBytes(uint8Array, pageNum) {
    if (typeof pdfjsLib === 'undefined') {
      return Promise.reject(new Error('PDF.js not loaded'));
    }

    return pdfjsLib.getDocument({ data: uint8Array }).promise.then(function (pdf) {
      var targetPage = pageNum || 1;
      if (targetPage > pdf.numPages) targetPage = 1;

      return pdf.getPage(targetPage).then(function (page) {
        var viewport = page.getViewport({ scale: 1.0 });

        return Promise.all([
          page.getOperatorList(),
          page.getTextContent()
        ]).then(function (results) {
          var opList   = results[0];
          var textContent = results[1];

          var geometry  = walkOperatorList(opList.fnArray, opList.argsArray);
          var textItems = extractTextItems(textContent, viewport);
          var classified = classifyGeometry(geometry.segments, geometry.arcs, textItems, viewport);

          // Also expose all available pages
          classified.totalPages = pdf.numPages;
          classified.currentPage = targetPage;

          return classified;
        });
      });
    });
  }

  function parse(file, pageNum) {
    return new Promise(function (resolve, reject) {
      var reader = new FileReader();
      reader.onload = function (e) {
        var u8 = new Uint8Array(e.target.result);
        parseFromBytes(u8, pageNum).then(resolve).catch(reject);
      };
      reader.onerror = function () { reject(new Error('Failed to read file')); };
      reader.readAsArrayBuffer(file);
    });
  }

  return {
    parse: parse,
    parseFromBytes: parseFromBytes
  };

})();
