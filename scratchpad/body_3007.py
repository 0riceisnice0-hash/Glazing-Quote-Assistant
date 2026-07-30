# -*- coding: utf-8 -*-
"""READ-ONLY: dump full bodies of specific messages by id."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import mary_graph as mg

IDS = {
    "ADAM-ERRORLOG-2901": ("mary@fensterglazing.com", "AAMkAGUwMmQ3NzE3LTI1YTItNDc0ZS04MTU3LTdmZDVkZjhmYTU0MgBGAAAAAAAfZpegzyDQQZjAfUUulIiHBwD9tQSpL5DiQKayHN7JsAJoAAAAAAEMAAD9tQSpL5DiQKayHN7JsAJoAAACxDIDAAA="),
    "ADAM-REDDITCH-1130": ("mary@fensterglazing.com", "AAMkAGUwMmQ3NzE3LTI1YTItNDc0ZS04MTU3LTdmZDVkZjhmYTU0MgBGAAAAAAAfZpegzyDQQZjAfUUulIiHBwD9tQSpL5DiQKayHN7JsAJoAAAAAAEMAAD9tQSpL5DiQKayHN7JsAJoAAADBhZBAAA="),
    "BSW-GRANGEHILL-1148": ("estimating@fensterglazing.com", "AAMkADBhYWE0ZDllLWYxMmItNDI4Mi05ODBlLTM2MGM0MTkxZTQyMABGAAAAAACXQvrzm9lkQqtiepcBGIRmBwCGW4tRd8n6TrvG_e5XE6uBAAMNPprWAACGW4tRd8n6TrvG_e5XE6uBAAMRPt1CAAA="),
    "ADAM-BROCKSHILL-1319": ("estimating@fensterglazing.com", "AQMkADBhYQE0ZDllLWYxMmItNDI4Mi05ODBlLTM2MGM0MTkxZTQyMABGAAADl0L685vZZEKrYnqXARiEZgcAhluLUXfJ_k67xvnuVxOrgQAAAgEMAAAAhluLUXfJ_k67xvnuVxOrgQADET5KzgAAAA=="),
    "GINTARE-GRANGEHILL-ISSUED-1707": ("estimating@fensterglazing.com", "AQMkADBhYQE0ZDllLWYxMmItNDI4Mi05ODBlLTM2MGM0MTkxZTQyMABGAAADl0L685vZZEKrYnqXARiEZgcAhluLUXfJ_k67xvnuVxOrgQAAAgEJAAAAhluLUXfJ_k67xvnuVxOrgQADET5-sQAAAA=="),
    "VETROSEAL-065209": ("estimating@fensterglazing.com", "AQMkADBhYQE0ZDllLWYxMmItNDI4Mi05ODBlLTM2MGM0MTkxZTQyMABGAAADl0L685vZZEKrYnqXARiEZgcAhluLUXfJ_k67xvnuVxOrgQAAAgEMAAAAhluLUXfJ_k67xvnuVxOrgQADEeqOogAAAA=="),
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bodies-3007.txt")
env = mg.load_env()
token = mg.get_token(env, "READER")
with open(OUT, "w", encoding="utf-8") as fh:
    for tag, (mbox, mid) in IDS.items():
        m = mg.get_message_body(token, mbox, mid)
        body = m.get("body", {})
        txt = body.get("content", "")
        if body.get("contentType") == "html":
            txt = mg.html_to_text(txt)
        fh.write("\n\n" + "=" * 100 + "\n%s | %s | %s\n%s\n" % (
            tag, m.get("receivedDateTime"), m.get("subject"), "=" * 100))
        fh.write(txt[:6000])
print("written", OUT)
