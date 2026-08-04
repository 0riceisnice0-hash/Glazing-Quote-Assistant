import os,sys
q=r"test-results\mary-inbox\queue"
out=os.path.join(q,"fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__-att")
sd=os.path.join(q,"fd-4isWAACGW4tRd8n6TrvG_e5XE6uBAAMSif1IAAA_-att")
import hashlib
def h(p): return hashlib.md5(open(p,'rb').read()).hexdigest()[:12]
a=os.path.join(out,"Fenster Glazing - Brocks Hill Phase_SQ218594_Rev1.pdf")
b=os.path.join(sd,"Fenster Glazing - Brocks Hill Phase_SQ218594_Rev1.pdf")
c=os.path.join(sd,"Quote_Fenster Glazing - Brocks Hill Phase_SQ218594_Rev1.pdf")
print("md5 sent-to-client:",h(a)," strongdor-original:",h(b)," IDENTICAL:",h(a)==h(b))
try:
    from pypdf import PdfReader
except Exception:
    from PyPDF2 import PdfReader
for lbl,p in [("A: SENT TO MARTIN (SQ218594_Rev1)",a),("C: Quote_SQ218594_Rev1 (not sent)",c)]:
    print("="*90); print(lbl)
    r=PdfReader(p); print("pages:",len(r.pages))
    t="\n".join((pg.extract_text() or "") for pg in r.pages)
    print(t[:3500])
