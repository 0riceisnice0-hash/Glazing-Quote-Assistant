# Cleaned copies of the pack Chigwell received at 16:07, ready to reissue.
#
# The issued files are the record of what the client got and are NEVER rewritten in place -
# they stay in scratchpad\gh-issued-to-luke-att\ exactly as sent. These are copies.
#
# Nothing here touches a price: the workbook total must still read GBP 39,006.77 afterwards,
# and that is asserted below.
import os
import shutil
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "cip", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "clean_issued_pack.py"))
cip = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cip)

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "scratchpad" / "gh-issued-to-luke-att"
OUT = REPO / "outputs" / "grange-hill-reissue"
OUT.mkdir(parents=True, exist_ok=True)

# --- the workbook: creator, and the externalLinks parts that name the other three firms ---
xl_name = "Chigwell - Grange Hill Methodist Church Ext Pricing.xlsx"
src_xl, out_xl = SRC / xl_name, OUT / xl_name
print("BEFORE  %-14s %d trace(s)" % ("workbook", len(cip.audit(src_xl))))
# No ampersand in the creator - it is written straight into core.xml and a bare & breaks the part.
cip.clean_xlsx(src_xl, out_xl, {}, "Fenster Glazing and Locks Ltd")
print("AFTER   %-14s %d trace(s)" % ("workbook", len(cip.audit(out_xl))))

import openpyxl
ws = openpyxl.load_workbook(out_xl, data_only=True)["Pricing Document "]
total = ws["H24"].value
assert abs(total - 39006.768) < 0.005, "TOTAL MOVED: %r" % total
print("        total unchanged at GBP %s" % format(total, ",.2f"))

# --- the proposal PDF: /Author and the XMP dc:creator both say Nicholas Baker ---
pdf_name = "Chigwell - Grange Hill Methodist Church Ext Proposal.pdf"
src_pdf, out_pdf = SRC / pdf_name, OUT / pdf_name
print("BEFORE  %-14s %d trace(s)" % ("proposal", len(cip.audit(src_pdf))))
try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    from PyPDF2 import PdfReader, PdfWriter
r = PdfReader(str(src_pdf))
w = PdfWriter()
for page in r.pages:
    w.add_page(page)
# add_metadata merges, so the inherited /Author is overwritten rather than appended to.
w.add_metadata({"/Author": "Fenster Glazing & Locks Ltd",
                "/Creator": "Fenster Glazing & Locks Ltd",
                "/Producer": "Fenster Glazing & Locks Ltd"})
with open(out_pdf, "wb") as fh:
    w.write(fh)
print("AFTER   %-14s %d trace(s)" % ("proposal", len(cip.audit(out_pdf))))
print("        %d page(s) carried over" % len(PdfReader(str(out_pdf)).pages))

# The drawings and the two architect's elevations audited clean as issued - copy them through
# so the folder is a complete pack Adam can forward without assembling anything.
for name in ("Window and Door Drawings.pdf",
             "GH 008 (3) - Proposed West Elevation.pdf",
             "GH007 (8) - Proposed Front - (South Elevation).pdf"):
    shutil.copy2(SRC / name, OUT / name)
    print("        copied clean: %s" % name)

print("\nreissue pack: %s" % OUT)
for p in sorted(OUT.iterdir()):
    print("  %9d  %-70s %s" % (p.stat().st_size, p.name,
                               "CLEAN" if not cip.audit(p) else "STILL DIRTY"))
