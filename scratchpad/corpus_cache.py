# -*- coding: utf-8 -*-
"""Parse the archive once, not once per experiment.

bt.collect() walks the tender directories and opens ~70 workbooks with openpyxl,
which takes about three minutes. Every experiment in this scratchpad starts by
calling it, so a night of six experiments spends twenty minutes re-reading files
that have not changed. The lab session gets killed at its stop wherever it has
got to, so that is twenty minutes of findings lost.

Cache the parsed corpus as JSON. It holds only what parse_doc produced - codes,
sizes, quantities, unit rates and the four component columns - so it is the same
input every experiment was already using, and `--refresh` rebuilds it.

    from corpus_cache import docs          # list of parsed documents
    python scratchpad/corpus_cache.py --refresh
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
import mary_backtest as bt  # noqa: E402

CACHE = os.path.join(HERE, "corpus-cache.json")


def build():
    docs = bt.collect()
    with open(CACHE, "w", encoding="utf-8") as fh:
        json.dump(docs, fh)
    return docs


def load(refresh=False):
    if refresh or not os.path.exists(CACHE):
        return build()
    with open(CACHE, encoding="utf-8") as fh:
        return json.load(fh)


docs = load("--refresh" in sys.argv)

if __name__ == "__main__":
    print("%d documents, %d priced lines, %s"
          % (len(docs), sum(len(d["lines"]) for d in docs), CACHE))
