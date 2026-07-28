# -*- coding: utf-8 -*-
"""Gordon Court's measurement, run here: which sentences have I NEVER quoted?

They probed all nine sentences of BSW's footer block against four outputs, the
job file and the manifest, and found four mined and five never read - out of one
six-line paragraph.

Same probe on A Plus's advisory notes and AOV notes: every bullet, against every
letter, the job file, the manifest and the terms document. A bullet counts as
QUOTED if a distinctive run of words from it appears anywhere in my output.
"""
import io, os, re, glob

SRC = ['scratchpad/aplus_advisory_2019.txt', 'scratchpad/qt51518_full.txt']

TARGETS = (glob.glob('outputs/Riverside House*.txt')
           + ['data/jobs/riverside.md', 'data/job-checks/riverside-house-aov.json'])

def norm(s):
    s = s.replace(u'’', "'").replace(u'‘', "'")
    s = s.replace(u'“', '"').replace(u'”', '"')
    s = s.replace(u'–', '-').replace(u'—', '-')
    return re.sub(r'\s+', ' ', s).lower().strip()

haystack = ''
for p in TARGETS:
    if os.path.exists(p):
        haystack += ' ' + norm(io.open(p, encoding='utf-8', errors='replace').read())

# every bullet from the advisory notes, plus every sentence of the AOV notes
bullets = []
adv = io.open(SRC[0], encoding='utf-8').read()
for line in adv.split('\n'):
    line = line.strip()
    if line.startswith(u'•') or line.startswith('o ') or line.startswith(u'▪'):
        bullets.append(('advisory', line.lstrip(u'•o▪ ').strip()))

full = io.open(SRC[1], encoding='utf-8').read()
aov = full[full.index('AOV Notes:'):]
aov = aov[:aov.index('Maintenance:')] if 'Maintenance:' in aov else aov
buf = ''
for line in aov.split('\n')[1:]:
    buf += ' ' + line.strip()
for sent in re.split(r'(?<=\.)\s+', buf):
    sent = sent.strip()
    if len(sent) > 40:
        bullets.append(('aov', sent))

def quoted(text):
    """A distinctive run of 7 consecutive words appearing in my output."""
    words = norm(text).split()
    if len(words) < 7:
        return norm(text) in haystack
    for i in range(len(words) - 6):
        if ' '.join(words[i:i + 7]) in haystack:
            return True
    return False

hit, miss = [], []
for src, b in bullets:
    (hit if quoted(b) else miss).append((src, b))

print('A PLUS: %d bullets/sentences, %d quoted somewhere, %d NEVER QUOTED ANYWHERE'
      % (len(bullets), len(hit), len(miss)))
print('\n--- NEVER QUOTED ANYWHERE ---')
for src, b in miss:
    print('  [%s] %s' % (src, b[:150]))
