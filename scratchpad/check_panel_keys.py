# -*- coding: utf-8 -*-
"""Every key type on the board should open its panel. Until 29/07 only lead: did."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
PAGES = ["leads","chasing","chaselist","tenders","drafts","companies","enquiries","opportunities"]
with Hub() as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2)
    seen = {}
    for p in PAGES:
        hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav===%r).click()" % p)
        time.sleep(1.2)
        keys = hub.js("[...document.querySelectorAll('#page [data-jkey]')]"
                      ".map(x=>x.dataset.jkey).slice(0,400)") or []
        for k in keys:
            pre = k.split(":")[0]
            seen.setdefault(pre, (p, k))
    print("key types on the board:", sorted(seen))
    bad = []
    for pre, (p, k) in sorted(seen.items()):
        hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav===%r).click()" % p)
        time.sleep(1.0)
        hub.js("document.querySelector('#page [data-jkey=\"%s\"]').click()" % k)
        time.sleep(1.0)
        hidden = hub.js("document.querySelector('#panel').hidden")
        title = hub.js("document.querySelector('#panel-body h2')?.textContent")
        toast = hub.js("document.querySelector('.toast')?.textContent || ''")
        ok = (hidden is False) and bool(title)
        if not ok: bad.append(pre)
        print("%-8s %-13s %-6s %s" % (pre, p, "OPENS" if ok else "FAILS",
                                      (title or toast or "")[:55]))
        hub.js("document.querySelector('#panel-veil')?.click()")
        time.sleep(0.4)
    print("FAILING KEY TYPES:", bad or "none")
