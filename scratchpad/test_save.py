# -*- coding: utf-8 -*-
"""Drive a real save through the panel, then read it back off the API."""
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
KEY = "job:leys-park-changing-pavilion-dagenham"
with Hub(height=1400) as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2)
    hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav==='leads').click()")
    time.sleep(2)
    hub.js("document.querySelector('#page tr[data-jkey=\"%s\"]').click()" % KEY)
    time.sleep(1.5)
    # Click "2 months" exactly as a human would, then type a note and save.
    print("2 months ->", hub.js("[...document.querySelectorAll('#jwhen .opt')]"
                                ".find(x=>x.textContent.trim()==='2 months').click(), "
                                "document.querySelector('#jdate').value"))
    hub.js("document.querySelector('#jnote').value = 'UI round-trip test, 29/07 - delete me.'")
    hub.js("document.querySelector('#jsave').click()")
    time.sleep(3)
    print("panel closed:", hub.js("document.querySelector('#panel').hidden"))
    print("toast:", hub.js("document.querySelector('.toast')?.textContent || 'none'"))
    time.sleep(1)
    print("row date cell:", hub.js(
        "document.querySelector('#page tr[data-jkey=\"%s\"] td:nth-child(5)')?.innerText" % KEY))
    print("row note cell:", hub.js(
        "document.querySelector('#page tr[data-jkey=\"%s\"] .lognote')?.innerText" % KEY))
