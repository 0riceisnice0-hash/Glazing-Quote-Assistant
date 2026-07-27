# -*- coding: utf-8 -*-
"""Look at the hub with your own eyes before shipping it.

mary-dashboard.pages.dev is blocked in the Browser pane, so this drives
headless Chrome over CDP instead. Two real bugs shipped because the code was
correct and the page was not: Mary's own text rendered navy-on-navy and was
invisible, and the Won/Lost buttons were being swallowed by another click
handler. Neither was visible in a diff.

  python scripts/mary_hub_shot.py                       # overview
  python scripts/mary_hub_shot.py scoreboard out.png    # a specific page
  python scripts/mary_hub_shot.py messages out.png --contrast   # unreadable text

Chrome quirks worth keeping: 111+ refuses the devtools websocket unless
--remote-allow-origins is set and the client suppresses its Origin header, and
passing the URL as an argv means the page target is not there yet when you
look - so launch on about:blank and navigate after attaching.
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

URL = os.environ.get("MARY_HUB_URL", "https://mary-dashboard.pages.dev")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


class Hub:
    def __init__(self, port=9350, width=1500, height=1100):
        self.port, self.width, self.height = port, width, height
        self.proc = self.ws = None
        self._id = 0

    def __enter__(self):
        profile = tempfile.mkdtemp(prefix="mary-cdp-")
        self.proc = subprocess.Popen(
            [CHROME, "--headless=new", "--remote-debugging-port=%d" % self.port,
             "--remote-allow-origins=*", "--user-data-dir=" + profile, "--no-first-run",
             "--no-default-browser-check", "--window-size=%d,%d" % (self.width, self.height),
             "about:blank"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        import websocket
        last = None
        for _ in range(40):
            try:
                with urllib.request.urlopen("http://localhost:%d/json" % self.port, timeout=5) as r:
                    pages = [t for t in json.load(r) if t["type"] == "page"]
                if pages:
                    self.ws = websocket.create_connection(pages[0]["webSocketDebuggerUrl"],
                                                          timeout=45, suppress_origin=True)
                    break
            except Exception as e:
                last = e
            time.sleep(1)
        if not self.ws:
            raise RuntimeError("could not attach to Chrome: %s" % last)
        self.cmd("Runtime.enable")
        self.cmd("Page.enable")
        return self

    def __exit__(self, *_):
        try:
            if self.ws:
                self.ws.close()
        finally:
            if self.proc:
                self.proc.kill()

    def cmd(self, method, **params):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                return msg.get("result", {})

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            return "JS ERROR: %s" % r["exceptionDetails"].get("text", "")
        return r.get("result", {}).get("value")

    def open(self, page=None, settle=7):
        self.cmd("Page.navigate", url=URL)
        for _ in range(40):
            if self.js("!!document.querySelector('[data-nav]')"):
                break
            time.sleep(1)
        time.sleep(settle)
        if page:
            found = self.js("(() => { const b = [...document.querySelectorAll('[data-nav]')]"
                            ".find(x => x.dataset.nav === %r); if (!b) return false; b.click();"
                            " return true; })()" % page)
            if not found:
                raise RuntimeError("no such page: %r" % page)
            time.sleep(2)
        return self

    def shot(self, path):
        self.cmd("Emulation.setDeviceMetricsOverride", width=self.width, height=self.height,
                 deviceScaleFactor=1, mobile=False)
        time.sleep(0.4)
        data = self.cmd("Page.captureScreenshot", format="png")["data"]
        with open(path, "wb") as fh:
            fh.write(base64.b64decode(data))
        return path

    def contrast_report(self):
        """Catch text that cannot be read against what is behind it - the exact
        failure that made Mary's chat replies invisible."""
        return self.js("""(() => {
          const lum = (c) => { const m = c.match(/\\d+/g); if (!m) return null;
            const [r,g,b] = m.map(Number).map(v => { v/=255; return v <= .03928 ? v/12.92 : Math.pow((v+.055)/1.055, 2.4); });
            return .2126*r + .7152*g + .0722*b; };
          // Keep walking up through transparent AND semi-transparent layers -
          // a 5% white overlay on navy is still navy, and stopping at it
          // reports the whole sidebar as unreadable.
          const solid = (c) => { const m = c && c.match(/rgba?\\(([^)]+)\\)/);
            if (!m) return false; const p = m[1].split(',').map(s => parseFloat(s));
            return p.length < 4 || p[3] >= 0.9; };
          // A gradient has no single colour we can compare against, so bail
          // rather than invent one - the nav is painted with one, and guessing
          // reported the whole sidebar as unreadable.
          const bgOf = (el) => { let n = el; while (n && n !== document.body) {
            const s = getComputedStyle(n);
            if (s.backgroundImage && s.backgroundImage !== 'none') return null;
            if (solid(s.backgroundColor)) return s.backgroundColor;
            n = n.parentElement; }
            const b = getComputedStyle(document.body).backgroundColor;
            return solid(b) ? b : 'rgb(255,255,255)'; };
          const bad = [];
          document.querySelectorAll('#page *, .nav *').forEach(el => {
            if (!el.textContent || !el.textContent.trim() || el.children.length) return;
            const bgc = bgOf(el); if (bgc === null) return;
            const fg = lum(getComputedStyle(el).color), bg = lum(bgc);
            if (fg === null || bg === null) return;
            const ratio = (Math.max(fg,bg) + .05) / (Math.min(fg,bg) + .05);
            if (ratio < 2.5) bad.push({text: el.textContent.trim().slice(0,40),
              tag: el.tagName, color: getComputedStyle(el).color, on: bgc, ratio: +ratio.toFixed(2)});
          });
          return JSON.stringify(bad.slice(0, 12), null, 1);
        })()""")

    def console_errors(self):
        return self.js("window.__errs ? JSON.stringify(window.__errs) : '[]'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", default=None)
    ap.add_argument("out", nargs="?", default="hub.png")
    ap.add_argument("--contrast", action="store_true", help="report unreadable text")
    args = ap.parse_args()

    with Hub() as hub:
        hub.open(args.page)
        title = hub.js("document.querySelector('#page-title').textContent")
        rendered = hub.js("document.querySelector('#page').innerHTML.length")
        print("page      : %s (%s chars rendered)" % (title, rendered))
        if not rendered or rendered < 50:
            print("WARNING: this page rendered almost nothing")
        if args.contrast:
            print("contrast  : %s" % hub.contrast_report())
        hub.shot(args.out)
        print("screenshot: %s" % args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
