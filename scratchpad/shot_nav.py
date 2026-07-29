import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
with Hub(height=1400) as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(3)
    print(hub.js("[...document.querySelectorAll('#nav-items > *')].map(x=>x.className+' | '+x.innerText.replace(/\s+/g,' ').trim()).join(' /// ')"))
