# -*- coding: utf-8 -*-
"""Does the hub actually ask who you are? A fresh Chrome profile = a device
that has never answered, which is the exact case hub-66 is about.

Checks VISIBILITY, not el.hidden. The first build set el.hidden true and left
the card on screen - `.signin { display: grid }` outranks the UA [hidden] rule -
and the property said everything was fine.
"""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub

SHOWN = ("(() => { const e = document.querySelector('%s');"
         " if (!e) return 'MISSING';"
         " return getComputedStyle(e).display !== 'none' && e.getBoundingClientRect().height > 0; })()")

with Hub(height=900) as hub:
    hub.open()
    time.sleep(2)
    hub.open()          # the first navigation of a session can serve a cached build
    time.sleep(4)
    print("--- fresh device, never answered ---")
    print("card on screen  :", hub.js(SHOWN % "#signin"))
    print("cancel offered  :", hub.js(SHOWN % "#signin-cancel"), "(must be False - cannot be skipped)")
    print("picks           :", hub.js("document.querySelectorAll('#signin .signin-pick').length"))
    print("stored who      :", hub.js("localStorage.getItem('fenster-hub-who')"))
    print("nav name        :", hub.js("document.querySelector('#who-name').textContent"))
    hub.shot("test-results/signin-gate.png")

    hub.js("[...document.querySelectorAll('.signin-pick')].find(b=>b.dataset.me==='adam').click()")
    time.sleep(2)
    print("--- after picking Adam ---")
    print("card on screen  :", hub.js(SHOWN % "#signin"), "(must be False)")
    print("stored who      :", hub.js("localStorage.getItem('fenster-hub-who')"))
    print("nav name        :", hub.js("document.querySelector('#who-name').textContent"))
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2)
    hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav==='jmessages').click()")
    time.sleep(2)
    print("chat hint       :", hub.js("document.querySelector('.chat-hint')?.textContent.trim().slice(0,20)"))
    hub.shot("test-results/signin-after.png")

    hub.open()
    time.sleep(3)
    print("--- reload: a device that HAS answered must not be asked again ---")
    print("card on screen  :", hub.js(SHOWN % "#signin"), "(must be False)")
    print("nav name        :", hub.js("document.querySelector('#who-name').textContent"))

    hub.js("document.querySelector('#who-switch').click()")
    time.sleep(1)
    print("--- switching mid-session ---")
    print("card on screen  :", hub.js(SHOWN % "#signin"))
    print("cancel offered  :", hub.js(SHOWN % "#signin-cancel"), "(must be True - you are already signed in)")
    hub.js("document.querySelector('#signin-cancel').click()")
    time.sleep(0.5)
    print("cancel closes   :", hub.js(SHOWN % "#signin"), "(must be False)")
    print("still Adam      :", hub.js("localStorage.getItem('fenster-hub-who')"))
