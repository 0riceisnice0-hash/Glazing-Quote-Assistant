# -*- coding: utf-8 -*-
"""Every Jacob page, every remaining mention of Zac, in context - so a stale
attribution cannot hide on page six. Four of Adam's instructions were filed
under Zac's name; this says whether any of them still is."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub

JS = ("(() => { const t=document.querySelector('#page').textContent; const seen=new Set(); let i=-1;"
      " while((i=t.indexOf('Zac', i+1))>-1) seen.add(t.slice(Math.max(0,i-80), i+60).replace(/\\n+/g,' '));"
      " return [...seen].join('\\n  * ') || '(none)'; })()")

with Hub(height=1200) as hub:
    hub.open(); time.sleep(2)
    hub.open(); time.sleep(4)
    hub.js("[...document.querySelectorAll('.signin-pick')].find(b=>b.dataset.me==='adam').click()")
    time.sleep(1.5)
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2.5)
    pages = hub.js("[...document.querySelectorAll('#nav-items [data-nav]')].map(b=>b.dataset.nav)")
    print("pages:", pages)
    for p in pages:
        hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav===%r)?.click()" % p)
        time.sleep(2)
        print("\n== %s\n  * %s" % (p, hub.js(JS)))
