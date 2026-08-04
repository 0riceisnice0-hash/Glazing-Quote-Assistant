"""Shots of Joseph's pages. mary_hub_shot clicks [data-nav] in the CURRENT bot's
nav, and Joseph's pages are not in it until his sidebar card is clicked - so this
wraps it with that click and then walks his pages."""
import sys, time
sys.path.insert(0, "scripts")
import mary_hub_shot as H

PAGES = sys.argv[1:] or ["delivery", "josteps", "jowaiting", "jomoney"]

with H.Hub() as hub:
    hub.open()
    # The "who is this?" modal blurs every page behind it, so answer it once.
    hub.js("localStorage.setItem('fenster-hub-who','zac'); location.reload(); true")
    time.sleep(9)
    ok = hub.js("(() => { const b = document.querySelector('[data-bot=\"joseph\"]');"
                " if (!b) return false; b.click(); return true; })()")
    print("switched to joseph:", ok)
    time.sleep(3)
    print("nav:", hub.js("[...document.querySelectorAll('[data-nav]')]"
                         ".map(x => x.dataset.nav).join(',')"))
    for p in PAGES:
        found = hub.js("(() => { const b = [...document.querySelectorAll('[data-nav]')]"
                       ".find(x => x.dataset.nav === %r); if (!b) return false; b.click();"
                       " return true; })()" % p)
        if not found:
            print(p, "NO SUCH PAGE"); continue
        time.sleep(2)
        n = hub.js("document.querySelector('#page').innerHTML.length")
        err = hub.js("(window.__errs || []).join(' | ')")
        out = "scratchpad/jos-%s.png" % p
        hub.shot(out)
        print("%-10s %6s chars -> %s %s" % (p, n, out, err or ""))
        bad = hub.contrast_report()
        if bad and bad.strip() not in ("[]", ""):
            print("   UNREADABLE:", bad)

