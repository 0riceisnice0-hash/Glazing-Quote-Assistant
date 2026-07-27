# -*- coding: utf-8 -*-
"""Riverside House - AOV smoke vent drawings (house style, A4 landscape).

Draws what Fenster is supplying, dimensioned off A Plus QT51518, with the
client's own smoke-vent note and stairwell locations lifted from the pack
(K1653-11 / K1653-12) so the drawing carries its own evidence.

Everything on the sheet is traceable to a source; anything that is not is
marked TBC and carries an RFI number. Nothing is invented.
"""
import base64
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REN = os.path.join(REPO, "scratchpad", "riverside-render")
OUT_HTML = os.path.join(REPO, "scratchpad", "riverside-drawings.html")
OUT_PDF = os.path.join(REPO, "outputs", "Riverside House - AOV Smoke Vent Drawings.pdf")

S = 0.285  # drawing scale, px per mm


def b64(name):
    p = os.path.join(REN, name)
    with open(p, "rb") as fh:
        return "data:image/png;base64," + base64.b64encode(fh.read()).decode()


# ---- unit geometry, all from QT51518 ------------------------------------
W, H = 1130, 1530          # O/A frame size
FR = 86.5                  # frame section, derived from (1130 - 957) / 2
AW = 957                   # aperture width A1 / A7
A1H, A7H = 590, 591        # aperture heights
TRAN = H - FR - A1H - A7H - FR   # 176mm transom / vent rail zone
SUB = 155                  # 155mm Technal subcill


def elevation(x0, y0):
    """Unit elevation viewed from OUTSIDE. Returns SVG."""
    w, h, fr = W * S, H * S, FR * S
    a1 = A1H * S
    a7 = A7H * S
    tr = TRAN * S
    sub = SUB * S
    aw = AW * S
    g = []
    # outer frame
    g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="frame"/>' % (x0, y0, w, h))
    # upper aperture A1
    ax = x0 + fr
    ay1 = y0 + fr
    g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="glass"/>' % (ax, ay1, aw, a1))
    g.append('<text x="%.1f" y="%.1f" class="ap">A1  957 x 590</text>' % (ax + aw / 2, ay1 + a1 / 2 + 4))
    # transom / vent rail zone
    ty = ay1 + a1
    g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="rail"/>' % (ax, ty, aw, tr))
    g.append('<text x="%.1f" y="%.1f" class="rail-t">transom / vent rail 176 - see note 3</text>'
             % (ax + aw / 2, ty + tr / 2 + 3))
    # lower aperture A7
    ay7 = ty + tr
    g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="glass"/>' % (ax, ay7, aw, a7))
    g.append('<text x="%.1f" y="%.1f" class="ap">A7  957 x 591</text>' % (ax + aw / 2, ay7 + a7 / 2 + 4))
    # subcill
    g.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" class="subcill"/>'
             % (x0 - 6, y0 + h, w + 12, sub))
    g.append('<text x="%.1f" y="%.1f" class="ap">155mm Technal subcill</text>'
             % (x0 + w / 2, y0 + h + sub / 2 + 4))
    # BOTTOM-HUNG opening symbol: apex points at the hinge, which is the cill.
    # Dashed lines run from the two TOP corners down to bottom centre.
    g.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" class="open"/>'
             % (x0 + fr, y0 + fr, x0 + w / 2, y0 + h - fr, x0 + w - fr, y0 + fr))
    g.append('<text x="%.1f" y="%.1f" class="hinge">hinge line - bottom hung, opens out</text>'
             % (x0 + w / 2, y0 + h - fr - 6))
    # actuator body + chain at head (bottom-hung vents are driven from the head)
    axc = x0 + w / 2
    g.append('<rect x="%.1f" y="%.1f" width="52" height="10" class="act"/>' % (axc - 26, y0 + fr + 6))
    g.append('<text x="%.1f" y="%.1f" class="act-c">850mm stroke single chain actuator</text>'
             % (axc, y0 + fr + 26))
    # cable exit right, viewed from outside
    g.append('<path d="M %.1f %.1f h %.1f" class="cable"/>' % (axc + 26, y0 + fr + 11,
                                                              x0 + w + 8 - axc - 26))
    g.append('<text x="%.1f" y="%.1f" class="cable-t">cable exit RIGHT</text>' % (x0 + w + 12, y0 + fr + 9))
    g.append('<text x="%.1f" y="%.1f" class="cable-t">(viewed from outside);</text>' % (x0 + w + 12, y0 + fr + 19))
    g.append('<text x="%.1f" y="%.1f" class="cable-t">~2m flex coiled at vent</text>' % (x0 + w + 12, y0 + fr + 29))

    # ---- dimensions ----
    dl = x0 - 34
    g.append('<path d="M %.1f %.1f V %.1f" class="dim"/>' % (dl, y0, y0 + h))
    g.append('<path d="M %.1f %.1f h 8 M %.1f %.1f h 8" class="dim"/>' % (dl - 4, y0, dl - 4, y0 + h))
    g.append('<text class="dimt" transform="translate(%.1f,%.1f) rotate(-90)">1530 O/A</text>'
             % (dl - 6, y0 + h / 2 + 26))
    db = y0 + h + sub + 26
    g.append('<path d="M %.1f %.1f H %.1f" class="dim"/>' % (x0, db, x0 + w))
    g.append('<path d="M %.1f %.1f v -8 M %.1f %.1f v -8" class="dim"/>' % (x0, db + 4, x0 + w, db + 4))
    g.append('<text x="%.1f" y="%.1f" class="dimt">1130 O/A</text>' % (x0 + w / 2, db + 18))
    # aperture width dim
    dv = y0 - 16
    g.append('<path d="M %.1f %.1f H %.1f" class="dim"/>' % (ax, dv, ax + aw))
    g.append('<path d="M %.1f %.1f v 8 M %.1f %.1f v 8" class="dim"/>' % (ax, dv - 4, ax + aw, dv - 4))
    g.append('<text x="%.1f" y="%.1f" class="dimt">957 daylight</text>' % (ax + aw / 2, dv - 7))
    return "\n".join(g)


CSS = """
@page { size: A4 landscape; margin: 9mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; margin:0; color:#1f2a44; font-size:9.5px; }
.sheet { page-break-after: always; height: 192mm; display:flex; flex-direction:column; }
.sheet:last-child { page-break-after: auto; }
h1 { background:#1f2a44; color:#fff; margin:0; padding:7px 12px; font-size:13px; letter-spacing:.4px; }
h1 span { float:right; font-weight:400; font-size:10px; opacity:.85; }
.body { flex:1; display:flex; gap:10px; padding-top:8px; }
.col { display:flex; flex-direction:column; gap:8px; }
.box { border:1px solid #c3cad8; }
.box h2 { background:#eef1f6; margin:0; padding:4px 8px; font-size:9.5px;
          text-transform:uppercase; letter-spacing:.6px; border-bottom:1px solid #c3cad8; }
.box .in { padding:6px 8px; }
table { border-collapse:collapse; width:100%; font-size:8.8px; }
td, th { border-bottom:1px solid #e3e7ee; padding:2.5px 5px; text-align:left; vertical-align:top; }
th { color:#5a657c; font-weight:600; width:112px; }
tr:last-child td, tr:last-child th { border-bottom:none; }
.frame { fill:#f4f6fa; stroke:#1f2a44; stroke-width:2.2; }
.glass { fill:#dce9f5; stroke:#1f2a44; stroke-width:1.2; }
.rail  { fill:#e8ebf1; stroke:#1f2a44; stroke-width:1.2; }
.subcill { fill:#e2e6ee; stroke:#1f2a44; stroke-width:1.4; }
.open { fill:none; stroke:#1f2a44; stroke-width:1; stroke-dasharray:5 3.5; }
.act { fill:#b32d2d; stroke:#7d1c1c; stroke-width:.8; }
.cable { stroke:#b32d2d; stroke-width:1.2; fill:none; }
.dim { stroke:#5a657c; stroke-width:.8; fill:none; }
.dimt { font-size:8px; fill:#5a657c; text-anchor:middle; }
.ap { font-size:8px; fill:#1f2a44; text-anchor:middle; }
.rail-t { font-size:6.6px; fill:#5a657c; text-anchor:middle; }
.act-t, .cable-t { font-size:7.4px; fill:#b32d2d; }
.hinge { font-size:7px; fill:#5a657c; text-anchor:middle; }
.act-c { font-size:7.4px; fill:#b32d2d; text-anchor:middle; }
.note { font-size:8.4px; line-height:1.45; margin:0; padding-left:15px; }
.note li { margin-bottom:3.5px; }
.rfi { background:#fff6e8; border-left:3px solid #d08b16; padding:5px 8px; font-size:8.4px; line-height:1.45; }
.rfi b { color:#8a5a05; }
.flag { background:#fdecec; border-left:3px solid #b32d2d; padding:5px 8px; font-size:8.4px; line-height:1.45; }
img.ex { width:100%; border:1px solid #c3cad8; display:block; }
.cap { font-size:7.6px; color:#5a657c; padding:3px 0 0; }
.tb { display:flex; font-size:8px; border-top:2px solid #1f2a44; padding-top:4px; margin-top:6px; }
.tb div { padding-right:18px; }
.tb b { display:block; color:#5a657c; font-weight:600; font-size:7.2px; text-transform:uppercase; }
.big { font-size:11px; font-weight:700; }
"""

HEAD = ('<h1>RIVERSIDE HOUSE - AOV SMOKE VENTS<span>FENSTER GLAZING &amp; LOCKS LTD'
        '&nbsp;&nbsp;|&nbsp;&nbsp;%s&nbsp;&nbsp;|&nbsp;&nbsp;27/07/2026&nbsp;&nbsp;|&nbsp;&nbsp;Rev A</span></h1>')

TITLEBLOCK = """
<div class="tb">
  <div><b>Client</b>RRR Group Limited</div>
  <div><b>Site</b>Riverside House, 44 Wedgewood Street, Fairford Leys, Aylesbury HP19 7HL</div>
  <div><b>Planning ref</b>24/02303/PAPCR</div>
  <div><b>Drawing</b>%s</div>
  <div><b>Scale</b>NTS - do not scale</div>
  <div><b>Basis</b>A Plus QT51518, 27/07/2026</div>
</div>
"""

svg_h = (H + SUB) * S + 96   # headroom for the O/A width dimension under the subcill
svg_w = W * S + 150

page1 = """
<div class="sheet">
%s
<div class="body">
  <div class="col" style="flex:0 0 505px;">
    <div class="box" style="flex:1;">
      <h2>AOV.01 &amp; AOV.02 - unit elevation, viewed from outside (2no identical)</h2>
      <div class="in"><svg width="%.0f" height="%.0f">%s</svg></div>
    </div>
  </div>
  <div class="col" style="flex:1;">
    <div class="box">
      <h2>Specification - as quoted, A Plus QT51518</h2>
      <div class="in"><table>
        <tr><th>System</th><td>Sapa DualFrame 75Si casement, style FF, open out, glazed in</td></tr>
        <tr><th>Quantity</th><td>2no - one per stairwell (see sheet 2)</td></tr>
        <tr><th>O/A size</th><td>1130mm x 1530mm</td></tr>
        <tr><th>Colour</th><td>White frame / white sash / white cill (single colour both faces)</td></tr>
        <tr><th>Cill</th><td>155mm subcill (Technal) - <b>Adam's enquiry asked 150mm</b></td></tr>
        <tr><th>Glass</th><td>4-20-4 Clr Tough S Coat 1.2 / 20mm black warm edge</td></tr>
        <tr><th>AOV</th><td>850mm stroke, single chain, 24v DC, actuator colour 9006 satin</td></tr>
        <tr><th>Cable</th><td>Exit right viewed from outside; NOT run through mullions</td></tr>
        <tr><th>Ironmongery</th><td>No handle, no restrictor, no casement locking, no PAS 24</td></tr>
        <tr><th>Free area</th><td><b>Geometric 1.30 m&sup2;</b> per vent, based on a 50mm reveal.
            Aerodynamic free area <b>not stated</b> - see RFI-1</td></tr>
        <tr><th>Supply basis</th><td>Supply only, delivered, glazed. Installation by Fenster.</td></tr>
      </table></div>
    </div>
    <div class="box">
      <h2>Notes</h2>
      <div class="in"><ol class="note">
        <li>Sizes and configuration are taken from A Plus QT51518. The tender pack contains
            <b>no window schedule and no dimensioned opening</b> - the 1130 x 1530 originates from
            Fenster's enquiry of 24/07/2026, not from the architect's drawings.</li>
        <li>Apertures A1 (957 x 590) and A7 (957 x 591) are the glazed apertures stated on the quote,
            confirming a transom-divided frame.</li>
        <li><b>The vent leaf is not identified on the quote.</b> A single 850mm stroke chain actuator
            is quoted against a frame whose individual apertures are ~590mm high, so the opening leaf
            cannot be a single aperture. Vent leaf, rail position and actuator position shown
            indicatively - to be confirmed on A Plus shop drawings before order (RFI-2).</li>
        <li>Actuators are <b>not</b> restrictors. A Plus disclaim liability for damage where a separate
            restrictor is not fitted, set 50mm beyond the actuator stroke. Not in the quoted price.</li>
        <li>Vents below 2.5m from FFL carry a trap-hazard risk under BS EN 60335-2; below 1100mm from
            FFL, Part K anti-fall protection is required and is excluded by A Plus.</li>
        <li>Actuators warranted 15,000 cycles or 12 months, whichever is sooner, and must be powered by
            an SE Controls-approved control system.</li>
        <li>Free area values allow nothing for obstructions, side walls or reveals.</li>
      </ol></div>
    </div>
  </div>
</div>
%s
</div>
""" % (HEAD % "Sheet 1 of 2", svg_w, svg_h, elevation(52, 40), TITLEBLOCK % "FG-RIV-01")

page2 = """
<div class="sheet">
%s
<div class="body">
  <div class="col" style="flex:0 0 300px;">
    <div class="box">
      <h2>The client's requirement, as drawn</h2>
      <div class="in">
        <img class="ex" src="%s">
        <div class="cap">Extract, drawings K1653-11 (first floor) and K1653-12 (second floor),
          Campbell Ark, CONSTRUCTION ISSUE. The identical note appears on both sheets.</div>
      </div>
    </div>
    <div class="box">
      <h2>Free area - requirement against quote</h2>
      <div class="in"><table>
        <tr><th>Required (drawings)</th><td class="big">1.00 m&sup2; free area</td></tr>
        <tr><th>Basis</th><td>Per stairwell. The note appears once per stairwell, at that
            stairwell's top storey.</td></tr>
        <tr><th>Quoted (A Plus)</th><td class="big">1.30 m&sup2; geometric</td></tr>
        <tr><th>Position</th><td>Complies on a <b>geometric</b> reading, with 0.30 m&sup2; to spare.</td></tr>
        <tr><th>If aerodynamic</th><td>A Plus's aerodynamic figures run <b>60-62%% of geometric</b> on the
            same product (QT51516, Towcester Vale: 0.49/0.81 and 0.54/0.87). On that ratio 1.30 m&sup2;
            geometric is roughly <b>0.78-0.81 m&sup2; aerodynamic</b> - about 20%% short of 1.00 m&sup2;.
            Indicative only: different sizes, and a 900mm stroke against 850mm here.</td></tr>
      </table></div>
    </div>
    <div class="flag"><b>The one question that decides this.</b> "Free area of 1m&sup2;" is not qualified
      on the drawing. On a geometric reading the vents as quoted comply comfortably. On an aerodynamic
      reading they do not, and nor would A Plus's own proposed 1235 x 1583. A Plus must state the
      aerodynamic figure for the actual Riverside sizes, and the fire strategy must confirm which
      basis applies.</div>
  </div>
  <div class="col" style="flex:1;">
    <div class="box" style="flex:1;">
      <h2>Locations - one vent per stairwell, at that stairwell's top storey</h2>
      <div class="in" style="display:flex; gap:9px;">
        <div style="flex:1;">
          <img class="ex" src="%s">
          <div class="cap"><b>AOV.01 - Stairwell 1, SECOND FLOOR</b> (top storey of the corner block).
            Drawing K1653-12, note leader 7.</div>
        </div>
        <div style="flex:1;">
          <img class="ex" src="%s">
          <div class="cap"><b>AOV.02 - Stairwell 2, FIRST FLOOR</b> (top storey of this wing).
            Drawing K1653-11, note leader 3.</div>
        </div>
      </div>
    </div>
    <div class="box">
      <h2>Excluded from this drawing and from the price</h2>
      <div class="in"><ol class="note">
        <li><b>The AOV control system in its entirety</b> - smoke control panel, mains and battery-backed
            supply, cabling and containment from panel to vent, the fire brigade override at ground floor
            access level required by the note above, interfacing, commissioning and the O&amp;M / EN 12101
            documentation. A Plus fix the actuator, test it on local batteries and leave ~2m of flex
            coiled at the vent. <b>The drawing's requirement cannot be met by the window alone.</b></li>
        <li>Window restrictors (note 4).</li>
        <li>Builder's work - forming, adapting or making good openings, lintels, internal finishes.
            Understood to sit with PHDB under the building works package.</li>
        <li>Access equipment / scaffold to top-storey level.</li>
        <li>Ongoing maintenance of the life-safety system, which is a legal duty of the occupier or agent
            under the Regulatory Reform (Fire Safety) Order 2005.</li>
      </ol></div>
    </div>
    <div class="rfi">
      <b>RFI-1</b> - A Plus to state the <b>aerodynamic</b> free area for 1130 x 1530 at 850mm stroke.
      QT51518 gives geometric only; their QT51516 states both on every line.<br>
      <b>RFI-2</b> - A Plus to confirm the vent leaf, rail position and actuator position on shop drawings.<br>
      <b>RFI-3</b> - Client / fire strategy to confirm whether the 1m&sup2; on K1653-11 and K1653-12 is
      geometric or aerodynamic free area, and to confirm the source of the 1.5m&sup2; figure in
      Fenster's enquiry of 24/07/2026, which does not appear anywhere in the pack.<br>
      <b>RFI-4</b> - Who is carrying the AOV control system, cabling and fire brigade override?<br>
      <b>RFI-5</b> - Confirm cill height above FFL at each vent (BS EN 60335-2 trap hazard below 2.5m,
      Part K anti-fall below 1100mm), and confirm 155mm subcill is acceptable against the 150mm enquired.
    </div>
  </div>
</div>
%s
</div>
""" % (HEAD % "Sheet 2 of 2", b64("K11_NOTE.png"), b64("LOC_S1.png"), b64("LOC_S2.png"),
       TITLEBLOCK % "FG-RIV-02")

html = "<!doctype html><html><head><meta charset='utf-8'><style>%s</style></head><body>%s%s</body></html>" % (
    CSS, page1, page2)

with open(OUT_HTML, "w", encoding="utf-8") as fh:
    fh.write(html)
print("html:", OUT_HTML)
print("pdf target:", OUT_PDF)
