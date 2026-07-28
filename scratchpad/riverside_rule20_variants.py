# -*- coding: utf-8 -*-
"""Variants for rule 20, written before it shipped and self-contained.

Built on synthetic files in a temp directory rather than on repo paths, so the
suite does not break the day somebody cleans the template it was founded on.

Seven that must fire or ask, seven that must not - including the two shapes this
week has proved are the real risks: a compressed file whose bytes throw up
"email addresses" that are not text (the Riverside drawings PDF produced six out
of fourteen FlateDecode streams), and a file that cannot be read, which must
never report the same as a file that is clean.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

BLOCK = '''def selftest_trace_variants():
    """Recall test for check_no_third_party_traces_in_issued_files.

    Synthetic files, built and destroyed here, so the suite survives the
    template it was founded on being cleaned.
    """
    import shutil
    import tempfile
    import zipfile
    d = tempfile.mkdtemp(prefix="mary-trace-")
    try:
        def ooxml(name, core):
            p = os.path.join(d, name)
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("docProps/core.xml", core)
                z.writestr("xl/worksheets/sheet1.xml", "<sheet><v>5990.22</v></sheet>")
            return p

        def flat(name, body):
            p = os.path.join(d, name)
            with open(p, "wb") as fh:
                fh.write(body)
            return p

        dirty = ooxml("dirty.xlsx", "<cp><dc:creator>Dan Parker;"
                                    "dan.parker@agsurveying.co.uk</dc:creator></cp>")
        clean = ooxml("clean.xlsx", "<cp><dc:creator>Fenster Glazing &amp; Locks Ltd"
                                    "</dc:creator></cp>")
        ours = ooxml("ours.xlsx", "<cp><dc:creator>adam@fensterglazing.com</dc:creator></cp>")
        path = ooxml("path.xlsx", "<cp><x>C:\\\\Users\\\\LiamO'Donnell\\\\AppData\\\\Local"
                                  "\\\\Microsoft\\\\Windows\\\\INetCache</x></cp>")
        plain = flat("plain.txt", b"Riverside House - nothing personal in here at all.")
        email = flat("email.txt", b"contact hayley@hdplanning.co.uk about the approval")
        # binary that is NOT text - the shape that produced six false "emails"
        # out of the drawings PDF before the printable guard went in
        binary = flat("binary.pdf", bytes(range(256)) * 40)

        VARIANTS = [
            ("field absent",            None,                                       UNKNOWN),
            ("empty list",              [],                                         NA),
            ("clean ooxml",             [{"name": "c", "path": clean}],             PASS),
            ("our own domain allowed",  [{"name": "o", "path": ours}],              PASS),
            ("plain text, nothing",     [{"name": "p", "path": plain}],             PASS),
            ("binary, no real text",    [{"name": "b", "path": binary}],            PASS),
            ("third-party email in docProps",
                                        [{"name": "d", "path": dirty}],             FAIL),
            ("windows user path",       [{"name": "w", "path": path}],              FAIL),
            ("third-party email in a txt",
                                        [{"name": "e", "path": email}],             FAIL),
            ("one clean one dirty",     [{"name": "c", "path": clean},
                                         {"name": "d", "path": dirty}],             FAIL),
            ("no path given",           [{"name": "x"}],                            UNKNOWN),
            ("path does not exist",     [{"name": "x", "path": os.path.join(d, "nope.xlsx")}],
                                                                                    UNKNOWN),
            ("entry is not a dict",     ["clean.xlsx"],                             UNKNOWN),
            ("a dict, not a list",      {"name": "c", "path": clean},               PASS),
            ("a bare string",           "clean.xlsx",                               UNKNOWN),
        ]

        bad = []
        for name, value, expect in VARIANTS:
            m = {} if value is None else {"issued_documents": value}
            try:
                got = check_no_third_party_traces_in_issued_files(m)["status"]
            except Exception as exc:
                got = "EXCEPTION %s: %s" % (type(exc).__name__, exc)
            if got != expect:
                bad.append("%s: expected %s, got %s" % (name, expect, got))
        print("  %-22s %d/%d trace variants behave as intended%s"
              % ("third-party traces", len(VARIANTS) - len(bad), len(VARIANTS),
                 "" if not bad else "  MISSED: " + "; ".join(bad)))
        return not bad
    finally:
        shutil.rmtree(d, ignore_errors=True)


def selftest_exposure_variants():'''

anchor = 'def selftest_exposure_variants():'
assert t.count(anchor) == 1
t = t.replace(anchor, BLOCK)

OLD = '''    if not selftest_exposure_variants():
        ok = False'''
NEW = '''    if not selftest_exposure_variants():
        ok = False
    if not selftest_trace_variants():
        ok = False'''
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('variants added')
