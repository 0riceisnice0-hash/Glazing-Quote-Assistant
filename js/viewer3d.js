/* js/viewer3d.js — Three.js 3D floor plan renderer
 *
 * Completely independent module.  Takes FloorplanParser output and builds an
 * interactive 3D scene.  Opens in a full-screen modal overlay.
 *
 * Dependencies: Three.js (r160+ from CDN), FloorplanParser
 *
 * Usage:
 *   Viewer3D.open(file)          // File object — pass a floor plan PDF
 *   Viewer3D.openFromState(state, pendingFiles) // auto-pick drawing files
 */

var Viewer3D = (function () {

  /* ── constants ──────────────────────────────────────────── */
  var WALL_COLOR    = 0xd1d5db;    // light grey
  var WALL_EDGE     = 0x6b7280;    // dark grey edges
  var WINDOW_COLOR  = 0x60a5fa;    // blue glass
  var WINDOW_FRAME  = 0x374151;    // dark frame
  var DOOR_COLOR    = 0xa16207;    // warm wood
  var DOOR_FRAME    = 0x78350f;
  var GROUND_COLOR  = 0xf3f4f6;    // pale floor
  var GRID_COLOR    = 0xe5e7eb;
  var LABEL_COLOR   = '#1a3a6b';

  var DEFAULT_WALL_HEIGHT = 80;    // in PDF-coordinate units (tuned later)

  /* ── state ──────────────────────────────────────────────── */
  var _scene, _camera, _renderer, _controls, _animId;
  var _overlay, _canvas;
  var _floorplanData;
  var _wallHeight = DEFAULT_WALL_HEIGHT;
  var _labelSprites = [];
  var _raycaster, _mouse, _tooltip;
  var _wallMeshes = [];
  var _baseFileName = '';
  var _candidates = [];         // floor plan File objects for switcher

  /* ===== PUBLIC: open from a file ========================= */

  function open(file, pageNum) {
    _showOverlay('Parsing floor plan…');

    FloorplanParser.parse(file, pageNum).then(function (data) {
      _floorplanData = data;
      _onDataReady(file.name);
    }).catch(function (err) {
      _hideOverlay();
      alert('3D viewer error: ' + err.message);
      console.error(err);
    });
  }

  /* open by scanning the app state for drawing files */
  function openFromState(state, pendingFiles) {
    // find a floor-plan file among pending files
    var candidates = (pendingFiles || []).filter(function (f) {
      var n = f.name.toLowerCase();
      return /floor\s*plan|ground\s*floor|first\s*floor|proposed.*plan/i.test(n)
        || /\.t05|\.t06/i.test(n);
    });
    if (candidates.length === 0) {
      // fall back to any drawing-classified source doc
      var drawingNames = (state.sourceDocuments || [])
        .filter(function (d) { return d.docType === 'drawing'; })
        .map(function (d) { return d.name; });
      candidates = (pendingFiles || []).filter(function (f) {
        return drawingNames.indexOf(f.name) !== -1;
      });
    }
    if (candidates.length === 0) {
      alert('No floor plan PDF found. Please upload a floor plan drawing first.');
      return;
    }
    _candidates = candidates;
    open(candidates[0]);
    // Let user pick if multiple — no longer needed, use toolbar switcher
    open(candidates[0]);
  }

  /* ===== OVERLAY UI ====================================== */

  function _showOverlay(msg) {
    if (_overlay) _hideOverlay();

    _overlay = document.createElement('div');
    _overlay.id = 'viewer3dOverlay';
    _overlay.style.cssText = 'position:fixed;inset:0;background:#0f172a;z-index:9999;display:flex;flex-direction:column;';

    // Toolbar
    var toolbar = document.createElement('div');
    toolbar.style.cssText = 'display:flex;align-items:center;gap:16px;padding:10px 20px;background:#1e293b;color:#fff;font-size:0.9rem;flex-shrink:0;';
    toolbar.innerHTML =
      '<strong style="font-size:1.1rem;">🏗️ 3D Floor Plan</strong>' +
      '<select id="_3dFloorSelect" style="background:#334155;color:#fff;border:1px solid #475569;border-radius:4px;padding:4px 10px;font-size:0.8rem;max-width:280px"></select>' +
      '<span id="_3dFileName" style="color:#94a3b8;font-size:0.8rem"></span>' +
      '<label style="color:#94a3b8;font-size:0.8rem">Wall Height</label>' +
      '<input type="range" id="_3dHeightSlider" min="20" max="200" value="' + _wallHeight + '" style="width:100px">' +
      '<span id="_3dHeightVal" style="color:#94a3b8;font-size:0.8rem;min-width:30px">' + _wallHeight + '</span>' +
      '<label style="color:#94a3b8;font-size:0.8rem">Page</label>' +
      '<select id="_3dPageSelect" style="background:#334155;color:#fff;border:1px solid #475569;border-radius:4px;padding:2px 8px;font-size:0.8rem"></select>' +
      '<button id="_3dLabelsToggle" class="btn btn-secondary" style="padding:4px 12px;font-size:0.8rem">🏷️ Labels</button>' +
      '<button id="_3dResetCam" class="btn btn-secondary" style="padding:4px 12px;font-size:0.8rem">🔄 Reset View</button>' +
      '<button id="_3dClose" style="background:none;border:none;color:#ef4444;font-size:1.5rem;cursor:pointer;padding:4px 8px">✕</button>';
    _overlay.appendChild(toolbar);

    // Status / loading
    var status = document.createElement('div');
    status.id = '_3dStatus';
    status.style.cssText = 'color:#94a3b8;text-align:center;padding:40px;font-size:1rem;flex:1;display:flex;align-items:center;justify-content:center';
    status.textContent = msg || 'Loading…';
    _overlay.appendChild(status);

    // Tooltip
    _tooltip = document.createElement('div');
    _tooltip.style.cssText = 'position:absolute;padding:4px 10px;background:#1e293b;color:#e2e8f0;border-radius:6px;font-size:0.75rem;pointer-events:none;display:none;z-index:10000;';
    _overlay.appendChild(_tooltip);

    document.body.appendChild(_overlay);

    // Wire close
    document.getElementById('_3dClose').addEventListener('click', close);
    // ESC key
    _overlay._escHandler = function (e) { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', _overlay._escHandler);
  }

  function _hideOverlay() {
    if (!_overlay) return;
    if (_animId) cancelAnimationFrame(_animId);
    if (_renderer) { _renderer.dispose(); _renderer = null; }
    if (_controls) { _controls.dispose(); _controls = null; }
    if (_overlay._escHandler) document.removeEventListener('keydown', _overlay._escHandler);
    document.body.removeChild(_overlay);
    _overlay = null;
    _canvas = null;
    _scene = null;
    _camera = null;
    _labelSprites = [];
    _wallMeshes = [];
  }

  function close() { _hideOverlay(); }

  /* ===== BUILD SCENE ===================================== */

  function _onDataReady(fileName) {
    var status = document.getElementById('_3dStatus');
    if (status) status.style.display = 'none';

    // Setup canvas
    _canvas = document.createElement('canvas');
    _canvas.style.cssText = 'flex:1;display:block;cursor:grab;';
    _overlay.appendChild(_canvas);

    // File name
    _baseFileName = fileName;
    var fnEl = document.getElementById('_3dFileName');
    if (fnEl) fnEl.textContent = '';

    // Populate floor plan switcher
    var floorSel = document.getElementById('_3dFloorSelect');
    if (floorSel && _candidates.length > 0) {
      floorSel.innerHTML = '';
      _candidates.forEach(function (f, i) {
        var opt = document.createElement('option');
        opt.value = i;
        // Show a short label: extract the meaningful part of the filename
        var label = f.name.replace(/\.pdf$/i, '').replace(/^\d+\.?/, '');
        opt.textContent = label || f.name;
        if (f.name === fileName) opt.selected = true;
        floorSel.appendChild(opt);
      });
    }

    // Populate page selector
    var pageSel = document.getElementById('_3dPageSelect');
    if (pageSel && _floorplanData.totalPages) {
      for (var p = 1; p <= _floorplanData.totalPages; p++) {
        var opt = document.createElement('option');
        opt.value = p;
        opt.textContent = 'Page ' + p;
        if (p === _floorplanData.currentPage) opt.selected = true;
        pageSel.appendChild(opt);
      }
    }

    // Init Three.js
    _initThree();
    _buildScene();
    _wireControls();
    _animate();
  }

  function _initThree() {
    // Defer size calculation with requestAnimationFrame so the DOM is laid out
    var overlay = _canvas.parentElement;
    var toolbar = overlay.querySelector('div');
    var w = Math.max(overlay.clientWidth, 320);
    var h = Math.max(overlay.clientHeight - (toolbar ? toolbar.offsetHeight : 0), 240);

    _scene = new THREE.Scene();
    _scene.background = new THREE.Color(0x0f172a);
    _scene.fog = new THREE.FogExp2(0x0f172a, 0.0002);

    _camera = new THREE.PerspectiveCamera(55, w / h, 0.1, 100000);
    _renderer = new THREE.WebGLRenderer({ canvas: _canvas, antialias: true, alpha: false });
    _renderer.setSize(w, h);
    _renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    _renderer.shadowMap.enabled = true;
    _renderer.shadowMap.type = THREE.PCFSoftShadowMap;

    // OrbitControls
    _controls = new THREE.OrbitControls(_camera, _canvas);
    _controls.enableDamping = true;
    _controls.dampingFactor = 0.08;
    _controls.maxPolarAngle = Math.PI / 2.05;
    _controls.minDistance = 20;
    _controls.maxDistance = 5000;

    // Raycaster for hover
    _raycaster = new THREE.Raycaster();
    _mouse = new THREE.Vector2();

    // Resize handler
    window.addEventListener('resize', _onResize);
  }

  function _buildScene() {
    var data = _floorplanData;
    if (!data) return;

    // Clear old meshes
    while (_scene.children.length > 0) {
      _scene.remove(_scene.children[0]);
    }
    _labelSprites = [];
    _wallMeshes = [];

    // Auto-scale: calculate wall height relative to building size
    var bw = data.bounds.maxX - data.bounds.minX;
    var bh = data.bounds.maxY - data.bounds.minY;
    var buildingSize = Math.max(bw, bh) || 500;   // fallback if 0
    if (_wallHeight === DEFAULT_WALL_HEIGHT) {
      _wallHeight = Math.max(20, Math.min(120, buildingSize * 0.08));
      var slider = document.getElementById('_3dHeightSlider');
      if (slider) slider.value = Math.round(_wallHeight);
      var valEl = document.getElementById('_3dHeightVal');
      if (valEl) valEl.textContent = Math.round(_wallHeight);
    }

    var cx = (data.bounds.minX + data.bounds.maxX) / 2;
    var cy = (data.bounds.minY + data.bounds.maxY) / 2;
    // Safety: ensure finite values
    if (!isFinite(cx)) cx = 0;
    if (!isFinite(cy)) cy = 0;

    // ── Lighting ──
    var ambient = new THREE.AmbientLight(0xffffff, 0.6);
    _scene.add(ambient);

    var dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
    dirLight.position.set(cx + buildingSize * 0.5, _wallHeight * 3, cy + buildingSize * 0.5);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    var d = buildingSize * 0.8;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    _scene.add(dirLight);

    var hemiLight = new THREE.HemisphereLight(0x87ceeb, 0x444444, 0.3);
    _scene.add(hemiLight);

    // ── Ground plane ──
    var groundSize = buildingSize * 2;
    var groundGeo = new THREE.PlaneGeometry(groundSize, groundSize);
    var groundMat = new THREE.MeshStandardMaterial({
      color: GROUND_COLOR,
      roughness: 0.9,
      metalness: 0
    });
    var ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.position.set(cx, -0.1, cy);
    ground.receiveShadow = true;
    _scene.add(ground);

    // Grid
    var gridHelper = new THREE.GridHelper(groundSize, Math.round(groundSize / 20), GRID_COLOR, GRID_COLOR);
    gridHelper.position.set(cx, 0, cy);
    gridHelper.material.opacity = 0.3;
    gridHelper.material.transparent = true;
    _scene.add(gridHelper);

    // ── Walls ──
    var wallMat = new THREE.MeshStandardMaterial({
      color: WALL_COLOR,
      roughness: 0.7,
      metalness: 0.05
    });
    var wallEdgeMat = new THREE.LineBasicMaterial({ color: WALL_EDGE });

    data.walls.forEach(function (wall) {
      var len = wall.length;
      if (len < 2) return;

      var thick = Math.max(wall.thickness * 1.5, 2);

      // Wall as a box oriented along the line
      var wallGeo = new THREE.BoxGeometry(len, _wallHeight, thick);
      var mesh = new THREE.Mesh(wallGeo, wallMat);

      var mid = midpoint3(wall.p1, wall.p2);
      mesh.position.set(mid.x, _wallHeight / 2, mid.y);

      // Rotate to align with wall direction
      var angle = Math.atan2(wall.p2.y - wall.p1.y, wall.p2.x - wall.p1.x);
      mesh.rotation.y = -angle;

      mesh.castShadow = true;
      mesh.receiveShadow = true;
      _scene.add(mesh);
      _wallMeshes.push(mesh);

      // Edge wireframe
      var edges = new THREE.EdgesGeometry(wallGeo);
      var edgeLine = new THREE.LineSegments(edges, wallEdgeMat);
      edgeLine.position.copy(mesh.position);
      edgeLine.rotation.copy(mesh.rotation);
      _scene.add(edgeLine);
    });

    // ── Windows ── (double-glazed uPVC style, oriented to nearest wall)
    var glassMat = new THREE.MeshStandardMaterial({
      color: 0xADD8E6,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
      roughness: 0,
      metalness: 0
    });
    var outerFrameMat = new THREE.MeshStandardMaterial({
      color: 0xf0f0f0,
      metalness: 0.2,
      roughness: 0.7
    });
    var innerFrameMat = new THREE.MeshStandardMaterial({
      color: 0xe8e8e8,
      metalness: 0.3,
      roughness: 0.6
    });
    var handleMat = new THREE.MeshStandardMaterial({
      color: 0x808080,
      metalness: 0.6,
      roughness: 0.3
    });

    data.windows.forEach(function (win) {
      var winW = 20;
      var winH = _wallHeight * 0.6;
      var fThk = 1.2;                 // frame rail thickness
      var fDepth = 2.5;               // frame depth (Z)
      var outerThk = fThk * 0.5;
      var outerDepth = fDepth + 0.5;
      var mullionW = fThk * 0.8;
      var inset = 0.4;
      var glassGap = 0.3;             // double-glazing air gap

      var group = new THREE.Group();

      // --- Outer surround frame (4 rails) ---
      var otGeo = new THREE.BoxGeometry(winW + outerThk * 2, outerThk, outerDepth);
      var osGeo = new THREE.BoxGeometry(outerThk, winH + outerThk * 2, outerDepth);

      var oTop = new THREE.Mesh(otGeo, outerFrameMat);
      oTop.position.y = (winH + outerThk) / 2;
      group.add(oTop);
      var oBot = new THREE.Mesh(otGeo, outerFrameMat);
      oBot.position.y = -(winH + outerThk) / 2;
      group.add(oBot);
      var oLeft = new THREE.Mesh(osGeo, outerFrameMat);
      oLeft.position.x = -(winW + outerThk) / 2;
      group.add(oLeft);
      var oRight = new THREE.Mesh(osGeo, outerFrameMat);
      oRight.position.x = (winW + outerThk) / 2;
      group.add(oRight);

      // --- Inner frame (top, bottom, left, right rails) ---
      var itGeo = new THREE.BoxGeometry(winW, fThk, fDepth);
      var isGeo = new THREE.BoxGeometry(fThk, winH, fDepth);

      var iTop = new THREE.Mesh(itGeo, innerFrameMat);
      iTop.position.y = (winH - fThk) / 2;
      group.add(iTop);
      var iBot = new THREE.Mesh(itGeo, innerFrameMat);
      iBot.position.y = -(winH - fThk) / 2;
      group.add(iBot);
      var iLeft = new THREE.Mesh(isGeo, innerFrameMat);
      iLeft.position.x = -(winW - fThk) / 2;
      group.add(iLeft);
      var iRight = new THREE.Mesh(isGeo, innerFrameMat);
      iRight.position.x = (winW - fThk) / 2;
      group.add(iRight);

      // --- Central mullion (vertical divider) ---
      var mulGeo = new THREE.BoxGeometry(mullionW, winH - fThk * 2, fDepth);
      var mul = new THREE.Mesh(mulGeo, innerFrameMat);
      group.add(mul);

      // --- Glass panes (left & right of mullion, double-glazed) ---
      var paneW = (winW - fThk * 2 - mullionW) / 2 - inset;
      var paneH = winH - fThk * 2 - inset;
      var paneGeo = new THREE.PlaneGeometry(paneW, paneH);

      // Left pane — outer glass
      var lOuter = new THREE.Mesh(paneGeo, glassMat);
      lOuter.position.set(-(paneW / 2 + mullionW / 2 + inset / 2), 0, fDepth / 2 - 0.1);
      group.add(lOuter);
      // Left pane — inner glass
      var lInner = new THREE.Mesh(paneGeo, glassMat);
      lInner.position.set(-(paneW / 2 + mullionW / 2 + inset / 2), 0, fDepth / 2 - 0.1 - glassGap);
      group.add(lInner);

      // Right pane — outer glass
      var rOuter = new THREE.Mesh(paneGeo, glassMat);
      rOuter.position.set(paneW / 2 + mullionW / 2 + inset / 2, 0, fDepth / 2 - 0.1);
      group.add(rOuter);
      // Right pane — inner glass
      var rInner = new THREE.Mesh(paneGeo, glassMat);
      rInner.position.set(paneW / 2 + mullionW / 2 + inset / 2, 0, fDepth / 2 - 0.1 - glassGap);
      group.add(rInner);

      // --- Sill (slightly wider ledge at bottom) ---
      var sillGeo = new THREE.BoxGeometry(winW + outerThk * 3, outerThk * 0.5, outerDepth + 1);
      var sill = new THREE.Mesh(sillGeo, outerFrameMat);
      sill.position.y = -(winH + outerThk) / 2 - outerThk * 0.25;
      sill.position.z = 0.5;
      group.add(sill);

      // --- Handle (small cylinder on right pane) ---
      var hGeo = new THREE.CylinderGeometry(0.25, 0.25, 2.5, 8);
      var handle = new THREE.Mesh(hGeo, handleMat);
      handle.rotation.z = Math.PI / 2;
      handle.position.set(winW / 2 - fThk - 1, 0, fDepth / 2 + 0.4);
      group.add(handle);

      // Position and orient to nearest wall
      group.position.set(win.x, _wallHeight * 0.55, win.y);
      var wallAngle = _nearestWallAngle(win.x, win.y, data.walls);
      group.rotation.y = -wallAngle;

      group.userData = { ref: win.ref, type: 'window' };
      _scene.add(group);

      _addLabel(win.ref, win.x, _wallHeight + 8, win.y);
    });

    // ── Doors ──
    var doorMat = new THREE.MeshStandardMaterial({
      color: DOOR_COLOR,
      roughness: 0.6,
      metalness: 0.05
    });
    var doorFrameMat = new THREE.MeshStandardMaterial({ color: DOOR_FRAME });

    data.doors.forEach(function (door) {
      var doorW = Math.max(door.swingRadius || 20, 15);
      var doorH = _wallHeight * 0.85;

      var dGroup = new THREE.Group();

      // Door panel
      var doorGeo = new THREE.BoxGeometry(doorW, doorH, 1.5);
      var doorMesh = new THREE.Mesh(doorGeo, doorMat);
      doorMesh.position.y = doorH / 2;
      doorMesh.castShadow = true;
      doorMesh.userData = { ref: door.ref, type: 'door', swingDetected: door.hasSwingDetected };
      dGroup.add(doorMesh);

      // Door frame surround
      var dfTopGeo = new THREE.BoxGeometry(doorW + 2, 1.2, 2.5);
      var dfSideGeo = new THREE.BoxGeometry(1.2, doorH + 1.2, 2.5);
      var dfTop = new THREE.Mesh(dfTopGeo, doorFrameMat);
      dfTop.position.y = doorH + 0.6;
      dGroup.add(dfTop);
      var dfLeft = new THREE.Mesh(dfSideGeo, doorFrameMat);
      dfLeft.position.set(-(doorW / 2 + 0.6), doorH / 2, 0);
      dGroup.add(dfLeft);
      var dfRight = new THREE.Mesh(dfSideGeo, doorFrameMat);
      dfRight.position.set(doorW / 2 + 0.6, doorH / 2, 0);
      dGroup.add(dfRight);

      // Swing arc indicator on the ground
      if (door.hasSwingDetected) {
        var arcGeo = new THREE.RingGeometry(doorW * 0.1, doorW, 32, 1, 0, Math.PI / 2);
        var arcMat2 = new THREE.MeshBasicMaterial({
          color: 0xfbbf24,
          transparent: true,
          opacity: 0.35,
          side: THREE.DoubleSide
        });
        var arcMesh = new THREE.Mesh(arcGeo, arcMat2);
        arcMesh.rotation.x = -Math.PI / 2;
        arcMesh.position.y = 0.2;
        dGroup.add(arcMesh);
      }

      // Position and orient to nearest wall
      dGroup.position.set(door.x, 0, door.y);
      var dAngle = _nearestWallAngle(door.x, door.y, data.walls);
      dGroup.rotation.y = -dAngle;

      _scene.add(dGroup);

      // Label
      var labelText = door.ref + (door.hasSwingDetected ? ' \uD83D\uDEAA' : '');
      _addLabel(labelText, door.x, _wallHeight + 8, door.y);
    });

    // ── Camera position ──
    _camera.position.set(
      cx + buildingSize * 0.6,
      buildingSize * 0.5,
      cy + buildingSize * 0.6
    );
    _controls.target.set(cx, _wallHeight / 2, cy);
    _controls.update();

    // Stats — always set (not append) to prevent duplication on slider rebuild
    var statEl = document.getElementById('_3dFileName');
    if (statEl && data) {
      var swingCount = data.doors.filter(function (d) { return d.hasSwingDetected; }).length;
      statEl.textContent = _baseFileName +
        '  —  ' + data.walls.length + ' walls, ' +
        data.windows.length + ' windows, ' +
        data.doors.length + ' doors' +
        (swingCount > 0 ? ' (' + swingCount + ' swings detected)' : '');
    }
  }

  /* ===== LABELS (CSS2D-style with sprites) =============== */

  function _addLabel(text, x, y, z) {
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    canvas.width = 256;
    canvas.height = 64;
    ctx.fillStyle = 'rgba(255,255,255,0.9)';
    _roundRect(ctx, 0, 0, 256, 64, 10);
    ctx.fill();
    ctx.fillStyle = LABEL_COLOR;
    ctx.font = 'bold 28px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text, 128, 32);

    var texture = new THREE.CanvasTexture(canvas);
    texture.needsUpdate = true;
    var mat = new THREE.SpriteMaterial({ map: texture, transparent: true, depthTest: false });
    var sprite = new THREE.Sprite(mat);
    sprite.position.set(x, y, z);
    sprite.scale.set(30, 8, 1);
    _scene.add(sprite);
    _labelSprites.push(sprite);
  }

  function _roundRect(ctx, x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + w - r, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + r);
    ctx.lineTo(x + w, y + h - r);
    ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
    ctx.lineTo(x + r, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
  }

  /* ===== CONTROLS & ANIMATION ============================ */

  function _wireControls() {
    // Height slider
    var slider = document.getElementById('_3dHeightSlider');
    var valEl = document.getElementById('_3dHeightVal');
    if (slider) {
      slider.addEventListener('input', function () {
        _wallHeight = parseInt(slider.value);
        if (valEl) valEl.textContent = _wallHeight;
        _buildScene();
      });
    }

    // Floor plan switcher
    var floorSel = document.getElementById('_3dFloorSelect');
    if (floorSel) {
      floorSel.addEventListener('change', function () {
        var idx = parseInt(floorSel.value);
        if (_candidates[idx]) {
          _wallHeight = DEFAULT_WALL_HEIGHT;
          var statusEl = document.getElementById('_3dStatus');
          if (statusEl) { statusEl.style.display = 'flex'; statusEl.textContent = 'Loading…'; }
          FloorplanParser.parse(_candidates[idx], 1).then(function (data) {
            _floorplanData = data;
            _baseFileName = _candidates[idx].name;
            if (_overlay) _overlay._currentFile = _candidates[idx];
            // Refresh page selector
            var pageSel2 = document.getElementById('_3dPageSelect');
            if (pageSel2) {
              pageSel2.innerHTML = '';
              for (var p = 1; p <= data.totalPages; p++) {
                var opt = document.createElement('option');
                opt.value = p;
                opt.textContent = 'Page ' + p;
                if (p === data.currentPage) opt.selected = true;
                pageSel2.appendChild(opt);
              }
            }
            _buildScene();
            if (statusEl) statusEl.style.display = 'none';
          });
        }
      });
    }

    // Labels toggle
    var labelsBtn = document.getElementById('_3dLabelsToggle');
    if (labelsBtn) {
      labelsBtn.addEventListener('click', function () {
        var visible = _labelSprites.length > 0 && _labelSprites[0].visible;
        _labelSprites.forEach(function (s) { s.visible = !visible; });
      });
    }

    // Reset camera
    var resetBtn = document.getElementById('_3dResetCam');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        if (!_floorplanData) return;
        var data = _floorplanData;
        var cx = (data.bounds.minX + data.bounds.maxX) / 2;
        var cy = (data.bounds.minY + data.bounds.maxY) / 2;
        var sz = Math.max(data.bounds.maxX - data.bounds.minX, data.bounds.maxY - data.bounds.minY);
        _camera.position.set(cx + sz * 0.6, sz * 0.5, cy + sz * 0.6);
        _controls.target.set(cx, _wallHeight / 2, cy);
        _controls.update();
      });
    }

    // Page selector
    var pageSel = document.getElementById('_3dPageSelect');
    if (pageSel) {
      pageSel.addEventListener('change', function () {
        // Re-parse with new page — need the file again
        // Store it on overlay element
        if (_overlay._currentFile) {
          _wallHeight = DEFAULT_WALL_HEIGHT;
          FloorplanParser.parse(_overlay._currentFile, parseInt(pageSel.value)).then(function (data) {
            _floorplanData = data;
            _buildScene();
          });
        }
      });
    }

    // Hover tooltip
    _canvas.addEventListener('mousemove', function (e) {
      var rect = _canvas.getBoundingClientRect();
      _mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      _mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
      _tooltip.style.left = (e.clientX + 12) + 'px';
      _tooltip.style.top = (e.clientY - 20) + 'px';
    });
  }

  function _animate() {
    _animId = requestAnimationFrame(_animate);

    if (_controls) _controls.update();

    // Hover detection
    if (_raycaster && _camera && _scene) {
      _raycaster.setFromCamera(_mouse, _camera);
      var intersects = _raycaster.intersectObjects(_scene.children, true);
      var found = null;
      for (var i = 0; i < intersects.length; i++) {
        if (intersects[i].object.userData && intersects[i].object.userData.ref) {
          found = intersects[i].object.userData;
          break;
        }
      }
      if (found && _tooltip) {
        _tooltip.style.display = 'block';
        _tooltip.textContent = found.ref + ' (' + found.type + ')' +
          (found.swingDetected ? ' — swing detected' : '');
      } else if (_tooltip) {
        _tooltip.style.display = 'none';
      }
    }

    if (_renderer && _scene && _camera) {
      _renderer.render(_scene, _camera);
    }
  }

  function _onResize() {
    if (!_canvas || !_camera || !_renderer || !_overlay) return;
    var toolbar = _overlay.querySelector('div');
    var w = Math.max(_overlay.clientWidth, 320);
    var h = Math.max(_overlay.clientHeight - (toolbar ? toolbar.offsetHeight : 0), 240);
    _camera.aspect = w / h;
    _camera.updateProjectionMatrix();
    _renderer.setSize(w, h);
  }

  /* ── helpers ─────────────────────────────────────────────── */

  function midpoint3(a, b) { return { x: (a.x + b.x) / 2, y: (a.y + b.y) / 2 }; }

  /** Find the angle of the nearest wall segment to a point (px, py). */
  function _nearestWallAngle(px, py, walls) {
    var bestDist = Infinity;
    var bestAngle = 0;
    walls.forEach(function (wall) {
      var dx = wall.p2.x - wall.p1.x;
      var dy = wall.p2.y - wall.p1.y;
      var len2 = dx * dx + dy * dy;
      if (len2 === 0) return;
      var t = Math.max(0, Math.min(1, ((px - wall.p1.x) * dx + (py - wall.p1.y) * dy) / len2));
      var projX = wall.p1.x + t * dx;
      var projY = wall.p1.y + t * dy;
      var dist = Math.sqrt((px - projX) * (px - projX) + (py - projY) * (py - projY));
      if (dist < bestDist) {
        bestDist = dist;
        bestAngle = Math.atan2(dy, dx);
      }
    });
    return bestAngle;
  }

  function _escapeHtml(text) {
    var div = document.createElement('div');
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  /* ── store file ref for page switching ──────────────────── */
  var _openOriginal = open;
  open = function (file, pageNum) {
    // stash file so page-switch can re-parse
    setTimeout(function () {
      if (_overlay) _overlay._currentFile = file;
    }, 100);
    _openOriginal(file, pageNum);
  };

  /* ===== PUBLIC API ====================================== */
  return {
    open: open,
    openFromState: openFromState,
    close: close
  };

})();
