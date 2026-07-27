import pdfplumber, glob, os
root = 'test-results/vesuvius-input/full-pack'
out = 'scratchpad/vesuvius-text'
os.makedirs(out, exist_ok=True)
for f in sorted(glob.glob(root + '/**/*.pdf', recursive=True)):
    rel = os.path.relpath(f, root).replace(os.sep, '__')
    try:
        with pdfplumber.open(f) as pdf:
            t = '\n'.join((p.extract_text() or '') for p in pdf.pages)
    except Exception as e:
        t = 'ERROR ' + str(e)
    open(os.path.join(out, rel + '.txt'), 'w', encoding='utf-8').write(t)
    print('%7d  %s' % (len(t), rel))
