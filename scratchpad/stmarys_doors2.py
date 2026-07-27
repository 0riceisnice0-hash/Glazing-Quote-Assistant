import pdfplumber, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\original-08-07\4.00 - Architectural\2376-08 door schedule.pdf")
with pdfplumber.open(P) as pdf:
    full = "\n".join((p.extract_text() or "") for p in pdf.pages)

# every D.nn entry, with the text that follows it up to the next one
ids = [(m.start(), m.group(1)) for m in re.finditer(r"\b(D\.\d{2})\b", full)]
seen, entries = set(), []
for k, (pos, ref) in enumerate(ids):
    if ref in seen:
        continue
    seen.add(ref)
    end = ids[k + 1][0] if k + 1 < len(ids) else len(full)
    entries.append((ref, full[pos:end]))

print("DOOR REFS FOUND: %d -> %s" % (len(entries), ", ".join(r for r, _ in entries)))
print()
print("THE ONES THAT LOOK EXTERNAL / ALUMINIUM (our package)")
print("=" * 100)
for ref, body in entries:
    if not re.search(r"powder coated aluminium|external|u-value|u value|Secured by Design", body, re.I):
        continue
    size = re.search(r"(\d{3,4}\s*x\s*\d{3,4}(?:\s*\+\s*\d+mm[^\n]*)?)", body)
    print("-" * 96)
    print("  %s   size hint: %s" % (ref, size.group(1) if size else "?"))
    for kw, pat in (("U-VALUE", r"u-?value[^\n]{0,60}"),
                    ("FOB", r"fobbed[^\n]{0,60}"),
                    ("LOCK", r"(no locking mechanism or latch|non-?lockable device)[^\n]{0,40}"),
                    ("BIFOLD", r"bi-?folding[^\n]{0,60}"),
                    ("SBD", r"Secured by Design[^\n]{0,40}"),
                    ("ANTI-LIG", r"[Aa]nti-?[Ll]igature[^\n]{0,70}"),
                    ("HINGE", r"Hinges:[^\n]{0,70}"),
                    ("KICK", r"Kicking plate[^\n]{0,50}"),
                    ("THRESH", r"Threshold[^\n]{0,60}"),
                    ("CLOSER", r"closer[^\n]{0,50}")):
        for m in list(re.finditer(pat, body, re.I))[:2]:
            print("      %-9s %s" % (kw, m.group(0).strip()[:95]))

print()
print("GLOBAL COUNTS ACROSS THE WHOLE SCHEDULE")
print("=" * 100)
for label, pat in (("'fobbed reader'", r"fobbed reader"),
                   ("'u-value of 1.4'", r"u-?value of 1\.4"),
                   ("'No locking mechanism or latch'", r"No locking mechanism or latch"),
                   ("'Non-lockable device'", r"Non-?lockable device"),
                   ("'bi-folding'", r"bi-?folding"),
                   ("'powder coated aluminium'", r"powder coated aluminium"),
                   ("'Anti-Ligature'", r"anti-?ligature"),
                   ("'panic'", r"panic")):
    print("  %-34s %d" % (label, len(re.findall(pat, full, re.I))))
