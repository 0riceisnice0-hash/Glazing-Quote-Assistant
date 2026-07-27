# -*- coding: utf-8 -*-
"""Read the SUPERSEDED IKON quote Q26-24160 to see what cost the price was built on."""
import email
import email.policy
import re

P = (r"C:\Users\zacpl\OneDrive - Fenster Glazing (1)\Commercial\2. Projects\Borras"
     r"\Coventry - Stoke Park School\1. Estimating\2. Supplier Quotes\IKON\SS"
     r"\Q26-24160 __ Fenster Glazing - Coventry quote.eml")

with open(P, "rb") as fh:
    msg = email.message_from_binary_file(fh, policy=email.policy.default)

for h in ("From", "To", "Date", "Subject"):
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
            body = re.sub(r"<[^>]+>", " ", part.get_content())
            body = re.sub(r"&nbsp;", " ", body)
            break

lines = [l.strip() for l in (body or "").splitlines()]
text = "\n".join(l for l in lines if l)
print(text[:3000])
