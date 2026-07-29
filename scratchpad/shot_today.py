import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from mary_hub_shot import Hub
with Hub(height=1700) as hub:
    hub.open()
    hub.js("[...document.querySelectorAll('[data-bot]')].find(x=>x.dataset.bot==='jacob').click()")
    time.sleep(3)
    for p in (sys.argv[1:] or ["overview"]):
        hub.js("[...document.querySelectorAll('[data-nav]')].find(x=>x.dataset.nav==='%s').click()" % p)
        time.sleep(2.5)
        print(p, "stats:", hub.js("[...document.querySelectorAll('#page .stat')].map(x=>x.innerText.replace(/\n/g,' ~ ')).join(' | ')"))
        print(p, "heads:", hub.js("[...document.querySelectorAll('#page h3, #page summary')].map(x=>x.innerText.slice(0,80)).join(' // ')"))
        hub.shot("test-results/w-%s.png" % p)
