import pdfplumber, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = (r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\test-results\st-marys-input"
     r"\original-08-07\4.00 - Architectural\2376-08 door schedule.pdf")

with pdfplumber.open(P) as pdf:
    pages = [(i, p.extract_text() or "") for i, p in enumerate(pdf.pages, 1)]
full = "\n".join(t for _, t in pages)
print("2376-08 DOOR SCHEDULE   pages: %d   chars: %d" % (len(pages), len(full)))

PATS = {
 "access control":  r"access control|fob|proximity|card reader|reader",
 "door entry":      r"door entry|intercom|audio|video entry|handset",
 "elec strike/lock": r"electric(al)? (strike|release|lock)|maglock|mag lock|electro",
 "keypad":          r"keypad|code lock|digital lock",
 "push button/exit": r"push (to )?(release|exit)|exit button|break glass|green break",
 "closer/hold open": r"closer|hold[- ]open|free swing",
 "panic/escape":     r"panic|escape|emergency",
 "external alu doors": r"aluminium|alu\b",
 "power/cabling":    r"cabl|wiring|power|24v|12v|transformer|rectifier|transfer hinge|loop",
 "our door types":   r"\bD\.?\d{1,2}\b",
}
for label, pat in PATS.items():
    hits = [(i, m.group(0)) for i, t in pages for m in re.finditer(pat, t, re.I)]
    print("  -- %-20s %d" % (label, len(hits)))

print()
print("FULL TEXT (schedules are usually one or two sheets)")
print("=" * 100)
for i, t in pages:
    print("-" * 92)
    print("PAGE", i)
    print(t[:5000])
