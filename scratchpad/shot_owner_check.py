# -*- coding: utf-8 -*-
"""Grange Hill's chase moved from Zac to Adam. Check the deployed board says so
on the pages a human actually opens, not just in the JSON."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub

with Hub(height=1300) as hub:
    hub.open()
    time.sleep(2)
    hub.open()
    time.sleep(4)
    hub.js("[...document.querySelectorAll('.signin-pick')].find(b=>b.dataset.me==='adam').click()")
    time.sleep(1.5)
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2)
    for page in ("chasing", "leads"):
        ok = hub.js("(() => { const b=[...document.querySelectorAll('[data-nav]')]"
                    ".find(x=>x.dataset.nav===%r); if(!b) return false; b.click(); return true; })()" % page)
        if not ok:
            print(page, ": no such page"); continue
        time.sleep(2)
        print(page, "- Grange Hill row mentions:", hub.js(
            "(() => { const rows=[...document.querySelectorAll('#page tr')]"
            ".filter(r=>/Grange Hill/i.test(r.textContent));"
            " return rows.map(r=>({zac:/\\bZac\\b/.test(r.textContent), adam:/\\bAdam\\b/.test(r.textContent)}))"
            ".map(o=>'zac='+o.zac+' adam='+o.adam).join(' | ') || 'no row'; })()"))
    print("page-wide 'ZAC IS CHASING':", hub.js(
        "/ZAC IS CHASING/.test(document.body.textContent)"))
    print("page-wide 'ADAM IS CHASING':", hub.js(
        "/ADAM IS CHASING/.test(document.body.textContent)"))
