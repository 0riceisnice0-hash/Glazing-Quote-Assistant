# -*- coding: utf-8 -*-
"""Rule 20: no client-facing file goes out carrying somebody else's name.

Gordon Court found dc:creator = "Dan Parker;dan.parker@agsurveying.co.uk" in the
docProps of a pricing document that reached Chigwell on 09/07. It replicates on
Riverside because both clone MASTER PRICING DOC.xlsx, created 2018-12-07 - so
that template has carried a named third party's work email as its author for
seven and a half years, and every quote built from it inherits it.

The rule scans the file rather than trusting a manifest field, because the whole
point of the finding is that nobody knew it was there to declare.
"""
import io

P = 'scripts/mary_checks.py'
t = io.open(P, encoding='utf-8').read()

HELPER = '''# Riverside, 28/07, from Gordon Court's docProps finding. Kept deliberately
# narrow - an email address, a Windows or Mac user path, and the two folder
# names that only ever appear in an Outlook attachment cache. Anything looser
# fires on ordinary prose, which is the fault this week's noticeboard has been
# full of.
THIRD_PARTY_TRACE = re.compile(
    rb"[\\w.+-]+@[\\w-]+\\.[\\w.]+"
    rb"|C:\\\\+Users\\\\+[^\\\\\\"<>]+"
    rb"|/Users/[^/\\"<>]+"
    rb"|INetCache|Content\\.Outlook", re.I)

# Parts of an OOXML package that are text stores rather than content. The
# founding case lived in the first of these, and last night's external-link
# clean missed it because it dropped xl/externalLinks/ and nothing else.
METADATA_PARTS = ("docProps/", "externalLink")


def scan_file_for_traces(path, allow=()):
    """Return the traces a file would carry to whoever opens it.

    Reads the raw bytes of every part of an OOXML package, and the whole file
    for anything else. `allow` is a tuple of substrings that are legitimately
    ours - our own domain, for instance.

    Returns (list of (part, trace), error string or None). A file that cannot
    be read returns an error rather than an empty list, because "no traces
    found" and "could not look" must never render the same.
    """
    import os
    import zipfile
    if not os.path.exists(path):
        return [], "file not found"
    hits = []
    try:
        if zipfile.is_zipfile(path):
            z = zipfile.ZipFile(path)
            for n in z.namelist():
                try:
                    raw = z.read(n)
                except Exception:
                    continue
                for m in set(THIRD_PARTY_TRACE.findall(raw)):
                    s = m.decode("utf-8", "ignore")
                    if any(a.lower() in s.lower() for a in allow):
                        continue
                    hits.append((n, s[:90]))
        else:
            with open(path, "rb") as fh:
                raw = fh.read()
            # A compressed or binary file decoded as bytes throws up matches
            # that are not text at all - the Riverside drawings PDF produced
            # six "email addresses" out of 14 FlateDecode streams. Only accept
            # a trace that is printable.
            for m in set(THIRD_PARTY_TRACE.findall(raw)):
                s = m.decode("utf-8", "ignore")
                if not s or not all(32 <= ord(c) < 127 for c in s):
                    continue
                if any(a.lower() in s.lower() for a in allow):
                    continue
                hits.append((os.path.basename(path), s[:90]))
    except Exception as exc:
        return [], "%s: %s" % (type(exc).__name__, exc)
    return hits, None


def check_no_third_party_traces_in_issued_files(m):'''

RULE = '''    """Riverside House, 28/07, from Gordon Court's finding on an already-issued
    document.

    `dc:creator` on their pricing document read "Dan Parker;
    dan.parker@agsurveying.co.uk" - a named person at another company, with his
    work email, recorded as the author of a quotation that went to a client. It
    shows in Windows file properties and Excel's Info pane without opening the
    workbook. Both jobs inherited it from MASTER PRICING DOC.xlsx, created
    2018-12-07.

    This rule opens the files rather than reading a manifest flag, because the
    entire point is that nobody knew the traces were there to declare. It also
    distinguishes "scanned and clean" from "could not be scanned" - a file that
    cannot be opened must never report the same as one that is clean.

    Uses 'issued_documents': [{name, path, is_the_priced_document}] - path
    relative to the repo root."""
    docs = m.get("issued_documents")
    if docs is None:
        return result("no third-party traces in issued files", UNKNOWN,
                      "State the documents that go to the client and where they are: "
                      "'issued_documents': [{name, path, is_the_priced_document}].",
                      "Riverside House",
                      remedy="Add a 'path' to each issued document so it can be opened and read.")
    if isinstance(docs, dict):
        docs = [docs]
    if isinstance(docs, str) or not isinstance(docs, (list, tuple)):
        return result("no third-party traces in issued files", UNKNOWN,
                      "'issued_documents' is %r - it must be a list." % (docs,),
                      "Riverside House", remedy="Rewrite the field as a list.")
    if not docs:
        return result("no third-party traces in issued files", NA,
                      "no issued documents on this job", "Riverside House")
    allow = tuple(m.get("own_domains") or ("fensterglazing.com",))
    dirty, unreadable, scanned = [], [], 0
    for doc in docs:
        if not isinstance(doc, dict):
            unreadable.append("%r is not a document entry" % (doc,))
            continue
        path = doc.get("path")
        name = doc.get("name", path or "?")
        if not path:
            unreadable.append("%s has no path, so it cannot be opened" % name)
            continue
        hits, err = scan_file_for_traces(path, allow)
        if err:
            unreadable.append("%s could not be read (%s)" % (name, err))
            continue
        scanned += 1
        for part, trace in hits:
            dirty.append("%s carries %r in %s" % (name, trace, part))
    if dirty:
        return result("no third-party traces in issued files", FAIL,
                      "A document that would go to the client carries somebody else's name, "
                      "email or file path: " + "; ".join(dirty)
                      + ". This is visible in file properties without opening the document.",
                      "Riverside House",
                      remedy="Rewrite docProps and strip external links on a COPY where the file "
                             "has already been issued - the issued file is the record of what the "
                             "client received - and in place where it has not.")
    if unreadable:
        return result("no third-party traces in issued files", UNKNOWN,
                      "Could not scan every issued document: " + "; ".join(unreadable)
                      + ". Not scanned is not the same as clean.",
                      "Riverside House",
                      remedy="Fix the path or the entry, then re-run.")
    return result("no third-party traces in issued files", PASS,
                  "%d issued document(s) scanned, no third-party name, email or path in any of "
                  "them" % scanned, "Riverside House")


def check_exposures_state_our_recourse(m):'''

assert t.count('def check_exposures_state_our_recourse(m):') == 1
t = t.replace('def check_exposures_state_our_recourse(m):', HELPER + RULE, 1)

OLD = '''    check_exposures_state_our_recourse,
]'''
NEW = '''    check_exposures_state_our_recourse, check_no_third_party_traces_in_issued_files,
]'''
assert t.count(OLD) == 1
t = t.replace(OLD, NEW)

OLD_B = '''        "exposures": None,
    }'''
NEW_B = '''        "exposures": None,
        "own_domains": None,
    }'''
assert t.count(OLD_B) == 1
t = t.replace(OLD_B, NEW_B)

io.open(P, 'w', encoding='utf-8', newline='').write(t)
print('rule 20 added')
