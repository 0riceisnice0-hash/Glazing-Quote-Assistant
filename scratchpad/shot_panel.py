# -*- coding: utf-8 -*-
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
with Hub(height=1400) as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(2)
    hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav==='leads').click()")
    time.sleep(2)
    key = sys.argv[1] if len(sys.argv) > 1 else "job:leys-park-changing-pavilion-dagenham"
    ok = hub.js("(() => { const r=document.querySelector('#page tr[data-jkey=\"%s\"]');"
                " if(!r) return 'row not on page'; r.click(); return 'clicked'; })()" % key)
    print("row:", ok)
    time.sleep(1.5)
    print("panel hidden:", hub.js("document.querySelector('#panel').hidden"))
    print("panel h2   :", hub.js("document.querySelector('#panel-body h2')?.textContent"))
    print("date input :", hub.js("!!document.querySelector('#jdate')"))
    print("date value :", hub.js("document.querySelector('#jdate')?.value"))
    print("quick btns :", hub.js("document.querySelectorAll('#jwhen .opt').length"))
    print("note box   :", hub.js("!!document.querySelector('#jnote')"))
    print("toast      :", hub.js("document.querySelector('.toast')?.textContent || 'none'"))
    hub.shot(sys.argv[2] if len(sys.argv) > 2 else "test-results/panel.png")
    print("shot done")
