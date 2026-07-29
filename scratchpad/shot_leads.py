# -*- coding: utf-8 -*-
"""Look at the new Leads register with my own eyes before telling Adam it exists."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub

page = sys.argv[1] if len(sys.argv) > 1 else "leads"
out = sys.argv[2] if len(sys.argv) > 2 else "test-results/leads.png"

with Hub(height=1600) as hub:
    hub.open()
    ok = hub.js("(() => { const b=[...document.querySelectorAll('[data-bot]')]"
                ".find(x=>x.dataset.bot==='jacob'); if(!b) return false; b.click(); return true; })()")
    print("switched to jacob:", ok)
    time.sleep(2)
    print("nav:", hub.js("[...document.querySelectorAll('[data-nav]')].map(x=>x.dataset.nav).join(',')"))
    found = hub.js("(() => { const b=[...document.querySelectorAll('[data-nav]')]"
                   ".find(x=>x.dataset.nav===%r); if(!b) return false; b.click(); return true; })()" % page)
    print("clicked %s:" % page, found)
    time.sleep(2)
    print("title:", hub.js("document.querySelector('#page-title').textContent"))
    print("chars:", hub.js("document.querySelector('#page').innerHTML.length"))
    print("rows :", hub.js("document.querySelectorAll('#page tr[data-jkey]').length"))
    print("errors:", hub.js("window.__err || 'none'"))
    hub.shot(out)
    print("shot:", out)
