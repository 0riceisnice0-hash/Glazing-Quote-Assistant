import os,re
q=r"test-results\mary-inbox\queue"
out=os.path.join(q,"fd-AAAAhluLUXfJ_k67xvnuVxOrgQADEonTtwAAAA__-att")
try:
    from pypdf import PdfReader
except Exception:
    from PyPDF2 import PdfReader
r=PdfReader(os.path.join(out,"SMD - Brocks Hill Phase 2 Teaching Block Proposal.pdf"))
print("PAGES:",len(r.pages))
t="\n".join((pg.extract_text() or "") for pg in r.pages)
t=re.sub(r"\n{3,}","\n\n",t)
print(t[:9000])
