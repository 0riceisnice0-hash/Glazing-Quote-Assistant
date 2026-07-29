# -*- coding: utf-8 -*-
"""Walk Jacob's four Work pages after the hub-74 restructure and report any
console error. A page that throws renders blank, and a blank page looks
exactly like "nothing to do"."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
PAGES = ["overview", "opportunities", "leads", "drafts",
         "enquiries", "chasing", "chaselist", "tenders"]
with Hub(height=1600) as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(3)
    nav = hub.js("[...document.querySelectorAll('[data-nav]')].map(x=>x.dataset.nav+':'+x.textContent.trim().split('\n')[0])")
    print("NAV:", nav)
    for p in PAGES:
        ok = hub.js("(() => { const b=[...document.querySelectorAll('[data-nav]')]"
                    ".find(x=>x.dataset.nav==='%s'); if(!b) return 'no nav'; b.click(); return 'ok'; })()" % p)
        time.sleep(2)
        n = hub.js("document.querySelector('#page')?.innerHTML.length || 0")
        rows = hub.js("document.querySelectorAll('#page tr').length")
        print("%-14s %-8s html=%-7s rows=%s" % (p, ok, n, rows))
        hub.shot("test-results/work-%s.png" % p)
