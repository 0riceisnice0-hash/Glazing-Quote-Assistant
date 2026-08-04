# -*- coding: utf-8 -*-
"""Render a Mary body file to standalone HTML so the layout can be screenshot-checked."""
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))
import mary_send

src, dst = sys.argv[1], sys.argv[2]
html = mary_send.build_body(open(src, encoding="utf-8-sig").read())
open(dst, "w", encoding="utf-8").write(
    '<html><body style="background:#ffffff;margin:0;padding:24px;width:720px;">' + html + "</body></html>"
)
print("wrote", dst)
