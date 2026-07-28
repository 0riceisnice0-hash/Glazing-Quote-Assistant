# -*- coding: utf-8 -*-
"""Rule 20 reported 'ff@C.0' as a third-party trace on Gordon Court's proposal.

It is not an address. It is bytes out of a compressed stream - the same
FlateDecode false positive Riverside caught in its own audit and added a
printable-character guard for. The guard does not cover this shape, because
every character in 'ff@C.0' is printable.

Two changes:

  1. The pattern now requires a domain label of at least two characters and a
     TLD that is alphabetic and at least two long. 'ff@C.0' fails on both -
     domain "C" is one character, TLD "0" is not alphabetic. Every real address
     on either job still matches: dan.parker@agsurveying.co.uk,
     hayley@hdplanning.co.uk, drawingoffice@aol.com, adam@fensterglazing.com,
     estimating@aplusaluminium.co.uk.

  2. For a PDF, read the EXTRACTED TEXT rather than the raw bytes. A tightened
     pattern narrows the odds; reading the text instead of the compression
     removes the class of error rather than the instance of it. Falls back to
     raw bytes if the text cannot be extracted, and says so - because "could not
     read" must never render as "clean".
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

OLD_PAT = '''THIRD_PARTY_TRACE = re.compile(
    rb"[\\w.+-]+@[\\w-]+\\.[\\w.]+"
    rb"|C:\\\\+Users\\\\+[^\\\\\\"<>]+"
    rb"|/Users/[^/\\"<>]+"
    rb"|INetCache|Content\\.Outlook", re.I)'''

NEW_PAT = '''# Gordon Court, 28/07: this reported `ff@C.0` on their proposal PDF, which is
# bytes out of a compressed stream rather than an address. Riverside's printable
# guard does not cover it - every character in it is printable. So the address
# arm now requires a domain label of two or more characters and an ALPHABETIC
# TLD of two or more. Checked against every real address on both jobs:
# dan.parker@agsurveying.co.uk, hayley@hdplanning.co.uk, drawingoffice@aol.com,
# adam@fensterglazing.com, estimating@aplusaluminium.co.uk - all still match.
THIRD_PARTY_TRACE = re.compile(
    rb"[\\w.+-]+@[\\w-]{2,}(?:\\.[\\w-]{2,})*\\.[A-Za-z]{2,}"
    rb"|C:\\\\+Users\\\\+[^\\\\\\"<>]+"
    rb"|/Users/[^/\\"<>]+"
    rb"|INetCache|Content\\.Outlook", re.I)'''

assert t.count(OLD_PAT) == 1, 'pattern anchor'
t = t.replace(OLD_PAT, NEW_PAT)

OLD_BODY = '''        else:
            with open(path, "rb") as fh:
                raw = fh.read()'''
NEW_BODY = '''        else:
            with open(path, "rb") as fh:
                raw = fh.read()
            # A PDF is compression, not text. Tightening the pattern narrows the
            # odds of a false hit; reading the extracted text instead removes
            # the class of error. Only fall back to the bytes if the text cannot
            # be had - and if neither works, say so rather than return clean.
            if raw[:5] == b"%PDF-":
                try:
                    import pypdf
                    rd = pypdf.PdfReader(path)
                    raw = "".join((pg.extract_text() or "") for pg in rd.pages).encode(
                        "utf-8", "ignore")
                except Exception as exc:
                    return [], ("PDF text could not be extracted (%s: %s) - not scanned is "
                                "not the same as clean" % (type(exc).__name__, exc))'''
assert t.count(OLD_BODY) == 1, 'body anchor'
t = t.replace(OLD_BODY, NEW_BODY)

# persist their case and the guards
OLD_V = '''        VARIANTS = [
            ("field absent",            None,                                       UNKNOWN),'''
NEW_V = '''        # Gordon Court's exact false positive, and the shapes either side of it.
        ffat = flat("ffat.txt", b"noise ff@C.0 more noise")
        short_tld = flat("shorttld.txt", b"someone@example.c")
        numeric_tld = flat("numtld.txt", b"someone@example.11")
        real = flat("real.txt", b"write to dan.parker@agsurveying.co.uk about it")

        VARIANTS = [
            ("Gordon Court's 'ff@C.0' - not an address",
                                        [{"name": "f", "path": ffat}],              PASS),
            ("one-character TLD",       [{"name": "s", "path": short_tld}],         PASS),
            ("numeric TLD",             [{"name": "n", "path": numeric_tld}],       PASS),
            ("a real third-party address still fires",
                                        [{"name": "r", "path": real}],              FAIL),
            ("field absent",            None,                                       UNKNOWN),'''
assert t.count(OLD_V) == 1, 'variant anchor'
t = t.replace(OLD_V, NEW_V)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule 20 tightened')
