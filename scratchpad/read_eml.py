import sys, email, email.policy
from email import policy
p = sys.argv[1]
with open(p, "rb") as f:
    msg = email.message_from_binary_file(f, policy=policy.default)
for h in ("From", "To", "Cc", "Date", "Subject"):
    print(f"{h}: {msg.get(h)}")
print("ATTACHMENTS:", [a.get_filename() for a in msg.iter_attachments()])
print("=" * 70)
body = msg.get_body(preferencelist=("plain", "html"))
t = body.get_content() if body else ""
if body and body.get_content_type() == "text/html":
    import re
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"&nbsp;", " ", t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
print(t[:8000])
