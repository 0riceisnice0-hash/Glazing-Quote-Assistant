# -*- coding: utf-8 -*-
"""Every Riverside deliverable, read for what travels with it rather than in it.

Gordon Court ran the two lines I posted, found the external link on their issued
file - and then found something worse in a store neither of us had looked in:

    dc:creator = Dan Parker;dan.parker@agsurveying.co.uk    docProps/core.xml

A named person at another company, with his work email, recorded as the AUTHOR
of a pricing document that went to a client. It shows in Windows file properties
and Excel's Info pane without opening the workbook.

My own lesson last night was "state where you looked". I moved from cells to
external links and stopped. docProps is a third store, and their sentence for it
is exactly right: my own lesson caught me one level short of where it led.

So this looks everywhere a file can carry text: OOXML docProps (core, app,
custom), PDF trailer info and XMP, and the raw bytes of every part for anything
that looks like a person, a path or an address.
"""
import glob
import os
import re
import zipfile

PERSONAL = re.compile(
    r"[\w.+-]+@[\w-]+\.[\w.]+"                     # any email address
    r"|C:\\+Users\\+[^\\\"<>]+"                    # any windows user path
    r"|/Users/[^/\"<>]+"                           # mac
    r"|INetCache|Content\.Outlook"                 # outlook attachment cache
    r"|AppData", re.I)

DOCPROPS = ['docProps/core.xml', 'docProps/app.xml', 'docProps/custom.xml']

TARGETS = sorted(glob.glob('outputs/Riverside*')) + ['templates/MASTER PRICING DOC.xlsx']

for path in TARGETS:
    if not os.path.exists(path):
        continue
    print("=" * 94)
    print(path)
    print("=" * 94)
    ext = os.path.splitext(path)[1].lower()

    if ext in ('.xlsx', '.docx'):
        z = zipfile.ZipFile(path)
        for p in DOCPROPS:
            try:
                raw = z.read(p).decode('utf-8', 'ignore')
            except KeyError:
                print("  %-22s absent" % p)
                continue
            fields = re.findall(r'<(dc:creator|cp:lastModifiedBy|dc:title|dc:subject|'
                                r'dc:description|cp:keywords|cp:category|Company|Manager|'
                                r'Application|dcterms:created|dcterms:modified)>([^<]*)<', raw)
            for k, v in fields:
                flag = "   <-- PERSONAL" if PERSONAL.search(v) else ""
                print("  %-22s %-22s %s%s" % (p.split('/')[-1], k, v[:60], flag))
        print("  externalLink parts:  %s"
              % ([n for n in z.namelist() if 'externalLink' in n] or 'none'))
        hits = []
        for n in z.namelist():
            try:
                raw = z.read(n).decode('utf-8', 'ignore')
            except Exception:
                continue
            for m in set(PERSONAL.findall(raw)):
                hits.append((n, m[:90]))
        print("  personal/path traces anywhere in the zip: %d" % len(hits))
        for n, m in hits[:12]:
            print("      %-38s %s" % (n, m))

    elif ext == '.pdf':
        import pypdf
        r = pypdf.PdfReader(path)
        meta = r.metadata or {}
        for k, v in meta.items():
            flag = "   <-- PERSONAL" if PERSONAL.search(str(v)) else ""
            print("  %-24s %s%s" % (k, str(v)[:60], flag))
        raw = open(path, 'rb').read().decode('latin-1')
        hits = set(PERSONAL.findall(raw))
        print("  personal/path traces in raw bytes: %d %s" % (len(hits), list(hits)[:6]))

    else:
        body = open(path, encoding='utf-8', errors='ignore').read()
        hits = set(PERSONAL.findall(body))
        print("  plain text. personal/path traces: %d %s" % (len(hits), sorted(hits)[:8]))
    print()
