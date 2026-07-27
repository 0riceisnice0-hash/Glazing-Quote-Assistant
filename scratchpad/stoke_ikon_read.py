# -*- coding: utf-8 -*-
"""Read the IKON louvre schedule email and list its attachments."""
import email
import email.policy
import os
import re

P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\2. Projects\Borras"
     r"\Coventry - Stoke Park School\1. Estimating\2. Supplier Quotes\IKON"
     r"\Q26-24329 __ Stoke Park Coventry - Louvre Schedule .eml")

with open(P, "rb") as fh:
    msg = email.message_from_binary_file(fh, policy=email.policy.default)

for h in ("From", "To", "Cc", "Date", "Subject"):
    print("%-8s: %s" % (h, msg.get(h, "")))
print()

body = None
for part in msg.walk():
    if part.get_content_type() == "text/plain" and not part.get_filename():
        body = part.get_content()
        break
if body is None:
    for part in msg.walk():
        if part.get_content_type() == "text/html" and not part.get_filename():
            html = part.get_content()
            body = re.sub(r"<[^>]+>", " ", html)
            body = re.sub(r"&nbsp;", " ", body)
            body = re.sub(r"[ \t]+", " ", body)
            break

print("---- BODY ----")
lines = [l.strip() for l in (body or "").splitlines()]
print("\n".join(l for l in lines if l)[:4000])

print()
print("---- ATTACHMENTS ----")
for part in msg.walk():
    fn = part.get_filename()
    if fn:
        payload = part.get_payload(decode=True) or b""
        print("%-60s %8d bytes" % (fn, len(payload)))
