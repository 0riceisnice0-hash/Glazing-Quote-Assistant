# -*- coding: utf-8 -*-
"""Adam is on a phone, and on a phone the sidebar is a drawer - which is where
the name went unread in the first place. Check the card and the top-bar chip at
phone width."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub

with Hub(width=430, height=900) as hub:
    hub.open()
    time.sleep(3)
    hub.open()          # first load can serve the edge-cached build
    time.sleep(4)
    print("gate hidden   :", hub.js("document.querySelector('#signin').hidden"))
    print("logo src      :", hub.js("document.querySelector('.signin-logo')?.getAttribute('src')"))
    hub.shot("test-results/signin-phone.png")
    hub.js("[...document.querySelectorAll('.signin-pick')].find(b=>b.dataset.me==='adam').click()")
    time.sleep(2)
    print("chip hidden   :", hub.js("document.querySelector('#who-chip').hidden"))
    print("chip text     :", hub.js("document.querySelector('#who-chip').textContent"))
    print("chip on screen:", hub.js(
        "(() => { const r=document.querySelector('#who-chip').getBoundingClientRect();"
        " return r.width>0 && r.right<=innerWidth; })()"))
    hub.shot("test-results/signin-phone-after.png")
