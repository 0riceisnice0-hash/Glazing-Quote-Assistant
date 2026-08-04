# -*- coding: utf-8 -*-
"""Route job-owned work orders; move settled history and noise to processed."""
import json, io, os, re, glob, shutil

Q = "test-results/mary-inbox/queue"
P = "test-results/mary-inbox/processed"

# file-substring -> owning chat key
ROUTE = {
    # Brocks Hill Phase 2 (SMDT0173, Spacemaker) - live tender, Martin Moore
    "20260730T1052-qOqQ": "brocks-hill", "20260730T1053-rndQ": "brocks-hill",
    "20260730T1056-qOqg": "brocks-hill", "20260730T1102-rndg": "brocks-hill",
    "20260730T1106-qOqw": "brocks-hill", "20260730T1111-qOrA": "brocks-hill",
    "20260730T1114-qOrQ": "brocks-hill", "20260730T1238-rneQ": "brocks-hill",
    "20260730T1242-rneg": "brocks-hill",
    "EonTtQ": "brocks-hill", "EonTtg": "brocks-hill", "EonTtw": "brocks-hill",
    "EonPyw": "brocks-hill", "Sif1I": "brocks-hill", "UmqIS": "brocks-hill",
    # Filwood Broadway (Stepnell, closes 30/07) - issued 12:28, Adam Warner ack 12:35
    "20260730T1021-rndA": "filwood", "20260730T1155-qOrw": "filwood",
    "20260730T1200-rndw": "filwood", "20260730T1228-rneA": "filwood",
    "20260730T1235-R6xP": "filwood",
    # Redditch Library - BSW design back, and the quote to check
    "FSkLYg": "redditch-library", "PmgeAACGW4tRd8n6TrvG": "redditch-library",
    "FSlOHQ": "redditch-library",
    # Vesuvius - Gintare chasing Nick for the supplier quote
    "FSlOHA": "vesuvius",
    # John North Hall - the 5nr SMA doorset RFQ and the site-survey question
    "FJpJWw": "john-north-hall", "FJpg7Q": "john-north-hall",
}

# Settled history and noise - nothing further to do, move out of the way.
CLEAR = [
    # Adam replies from 24-29/07 already acted on and recorded in the job files
    "fd-DAAAAP21BKkvkOJAprIc3smwAmgAAAIFUQAAAA__", "fd-DAAAAP21BKkvkOJAprIc3smwAmgAAAIFUgAAAA__",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAAAJUTaAAA_", "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAABS7V4AAA_",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAABS7V5AAA_", "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAABS7V_AAA_",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAACttVQAAA_", "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAACxDH-AAA_",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAACxDIAAAA_", "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAACxDIBAAA_",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAACxDICAAA_", "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAADBhZAAAA_",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAADBhZBAAA_", "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAADBhZCAAA_",
    "fd-AAEMAAD9tQSpL5DiQKayHN7JsAJoAAADBhZDAAA_",
    # Marketing / bulk / no-action
    "20260730T0900-qOpA",          # Once For All event invite
    "20260730T0918-q51Q",          # Supply2Gov daily alert
    "20260730T1215-qOsQ",          # In-Tend magazine advertising
    "AAGgoITP",                    # Xero statement, Leasium - accounts, not estimating
    # Handled by Adam / closed in-thread
    "UmpoOAAA", "UmpoMAAA", "UmpoLAAA", "FJpg7gAAAA", "FJpg7wAAAA",   # Approved Workforce
    "20260730T1133-qOrg", "20260730T1201-qOsA",                        # Luton - Adam answered
    "AAGgoITd",                    # Door install - Adam handed to commercial
    "FJpJWQAAAA",                  # empty-body internal
    "FSlKJwAAAA",                  # duplicate of the 20 Addison Ave supplier chase
]

routed, cleared, missing = [], [], []
files = glob.glob(os.path.join(Q, "*.json"))

for key, chat in ROUTE.items():
    hits = [f for f in files if key in os.path.basename(f)]
    if not hits:
        missing.append(key); continue
    for f in hits:
        d = json.load(io.open(f, encoding="utf-8"))
        d["route"] = chat
        json.dump(d, io.open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        routed.append("%s -> %s" % (os.path.basename(f)[:34], chat))

for key in CLEAR:
    for f in [x for x in files if key in os.path.basename(x)]:
        if not os.path.exists(f):
            continue
        shutil.move(f, os.path.join(P, os.path.basename(f)))
        att = f[:-5] + "-att"
        if os.path.isdir(att):
            shutil.move(att, os.path.join(P, os.path.basename(att)))
        cleared.append(os.path.basename(f)[:34])

print("ROUTED %d:" % len(routed))
for r in sorted(routed): print("  " + r)
print("\nCLEARED %d" % len(cleared))
print("NO MATCH for keys: %s" % missing)
print("\nSTILL IN QUEUE: %d" % len(glob.glob(os.path.join(Q, "*.json"))))
