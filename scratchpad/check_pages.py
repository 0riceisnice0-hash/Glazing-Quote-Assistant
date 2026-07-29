# -*- coding: utf-8 -*-
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
PAGES = ["overview","leads","chasing","drafts","chaselist","enquiries","tenders",
         "opportunities","outcomes","companies","jayk","decisions","sources"]
with Hub() as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2)
    for p in PAGES:
        ok = hub.js("(()=>{const b=[...document.querySelectorAll('[data-nav]')]"
                    ".find(x=>x.dataset.nav===%r); if(!b) return false; b.click(); return true;})()" % p)
        time.sleep(1.2)
        n = hub.js("document.querySelector('#page').innerHTML.length")
        t = hub.js("document.querySelector('#page-title').textContent")
        flag = "  <-- EMPTY" if not n or n < 200 else ""
        print("%-14s nav=%-5s %-22s %6s chars%s" % (p, ok, t, n, flag))
