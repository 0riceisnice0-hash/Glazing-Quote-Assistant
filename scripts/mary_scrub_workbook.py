"""Strip third-party traces out of an .xlsx before it can reach a client.

Founded on Riverside House and re-found on Grange Hill, 28/07/2026. The house
template `MASTER PRICING DOC.xlsx` was itself built from somebody else's
workbook, so every document generated from it inherits:

  - docProps/core.xml   dc:creator "Dan Parker;dan.parker@agsurveying.co.uk"
  - docProps/custom.xml a SharePoint ContentTypeId from that firm's site
  - xl/externalLinks/   two live links to "The Datum Group Electrical -
                        TEMPLATE ..." and "Electrical Template - Draft -
                        REV010.xlsx" under C:\\Users\\Parke\\ and
                        C:\\Users\\LiamO'Donnell\\ INetCache paths, with the
                        other firm's cached item catalogue inside them.

All of that is visible in Windows file properties without opening the file.
`mary_checks.check_no_third_party_traces` finds it; this fixes it.

Removing an external link is safe for the pricing document because nothing in
it reads those cached sheets - but any formula that DID would go #REF!, so the
script reports how many formulas referenced them and refuses to write a file
where that count is non-zero unless --force is given.

    python scripts\\mary_scrub_workbook.py "outputs\\Some Doc.xlsx"            # report only
    python scripts\\mary_scrub_workbook.py "outputs\\Some Doc.xlsx" --in-place # not yet issued
    python scripts\\mary_scrub_workbook.py "outputs\\Some Doc.xlsx" --out "...(CLIENT COPY).xlsx"

Use --out, never --in-place, on a file the client already has: the issued file
is the record of what they received.
"""

import argparse
import os
import re
import shutil
import sys
import zipfile

OWNER = "Fenster Glazing"

DROP_PARTS = re.compile(r"^xl/externalLinks/|^docProps/custom\.xml$")


def _clean_core(xml):
    xml = re.sub(r"(<dc:creator[^>]*>)[^<]*(</dc:creator>)", r"\g<1>%s\g<2>" % OWNER, xml)
    xml = re.sub(r"(<cp:lastModifiedBy>)[^<]*(</cp:lastModifiedBy>)", r"\g<1>%s\g<2>" % OWNER, xml)
    xml = re.sub(r"<cp:lastPrinted>[^<]*</cp:lastPrinted>", "", xml)
    return xml


def _strip_external_refs(xml):
    """Remove <externalReferences>...</externalReferences> from workbook.xml."""
    return re.sub(r"<externalReferences>.*?</externalReferences>", "", xml, flags=re.S)


def _strip_rels(xml):
    """Drop relationships pointing at externalLink parts or custom props."""
    return re.sub(
        r'<Relationship\b[^>]*Target="[^"]*(?:externalLink\d+\.xml|docProps/custom\.xml)"[^>]*/>',
        "", xml)


def _strip_content_types(xml):
    return re.sub(
        r'<Override\b[^>]*PartName="/(?:xl/externalLinks/externalLink\d+\.xml'
        r'|docProps/custom\.xml)"[^>]*/>', "", xml)


def _count_external_formulas(z):
    """Formulas of the form [1]Sheet!A1 - a reference into an external book."""
    n = 0
    for name in z.namelist():
        if not (name.startswith("xl/worksheets/") and name.endswith(".xml")):
            continue
        body = z.read(name).decode("utf-8", "replace")
        n += len(re.findall(r"<f[^>]*>[^<]*\[\d+\]", body))
    return n


def scrub(src, dest):
    zin = zipfile.ZipFile(src)
    refs = _count_external_formulas(zin)
    dropped, changed = [], []

    tmp = dest + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            name = item.filename
            if DROP_PARTS.match(name):
                dropped.append(name)
                continue
            data = zin.read(name)
            if name in ("docProps/core.xml", "[Content_Types].xml", "xl/workbook.xml",
                        "xl/workbook.xml.rels", "xl/_rels/workbook.xml.rels",
                        "_rels/.rels"):
                xml = data.decode("utf-8", "replace")
                before = xml
                if name == "docProps/core.xml":
                    xml = _clean_core(xml)
                elif name == "[Content_Types].xml":
                    xml = _strip_content_types(xml)
                elif name == "xl/workbook.xml":
                    xml = _strip_external_refs(xml)
                else:
                    xml = _strip_rels(xml)
                if xml != before:
                    changed.append(name)
                data = xml.encode("utf-8")
            zout.writestr(item, data)
    zin.close()
    shutil.move(tmp, dest)
    return dropped, changed, refs


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--in-place", action="store_true",
                    help="overwrite (only for a file the client has NOT received)")
    ap.add_argument("--out", help="write a cleaned copy here")
    ap.add_argument("--force", action="store_true",
                    help="write even though formulas reference the external books")
    a = ap.parse_args()

    if not os.path.exists(a.path):
        sys.exit("no such file: %s" % a.path)

    zin = zipfile.ZipFile(a.path)
    traces = [n for n in zin.namelist() if DROP_PARTS.match(n)]
    core = zin.read("docProps/core.xml").decode("utf-8", "replace") \
        if "docProps/core.xml" in zin.namelist() else ""
    creator = re.search(r"<dc:creator[^>]*>([^<]*)", core)
    refs = _count_external_formulas(zin)
    zin.close()

    print("%s" % a.path)
    print("  creator            : %s" % (creator.group(1) if creator else "-"))
    print("  parts to drop      : %d" % len(traces))
    for t in traces:
        print("      %s" % t)
    print("  formulas using them: %d" % refs)

    if not a.in_place and not a.out:
        print("\nreport only - pass --in-place or --out to write")
        return

    if refs and not a.force:
        sys.exit("\n%d formula(s) reference the external books - stripping them would "
                 "leave #REF!. Re-run with --force if that is genuinely what you want." % refs)

    dest = a.path if a.in_place else a.out
    if a.in_place:
        backup = a.path + ".pre-scrub"
        if not os.path.exists(backup):
            shutil.copy2(a.path, backup)
            print("\n  backup             : %s" % backup)

    dropped, changed, _ = scrub(a.path, dest)
    print("\n  wrote              : %s" % dest)
    print("  dropped %d part(s), rewrote %d" % (len(dropped), len(changed)))


if __name__ == "__main__":
    main()
