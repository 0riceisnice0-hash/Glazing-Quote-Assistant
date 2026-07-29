# The knowledge shelf - what Mary knows, indexed

**This file replaces reading `AI.md` and `HANDOVER.md` end to end at boot.** Those files
stay authoritative - nothing is duplicated here, so nothing can drift. Each entry is the
rule in one line and where the full account lives. Open a section only when the work at
hand touches it: `AI.md` line numbers are correct as of 29/07/2026 and every heading is
grep-able if they move (`grep -n "^## <first words>" AI.md`).

Always loaded alongside this index: `data/knowledge/adam.md` (how Adam reads and what is
settled) and your job file. Per-job history: `python scripts/mary_recall.py --job <key>`.
`HANDOVER.md` is the job-record archive - the ledger indexes every `###` record in it
(`mary_recall --kind record`), so search the ledger, not the file.

## Identity, rules, permissions (read once per chat, they are short)

- `MARY-HANDOVER.md` §1-4 (L19-60) - who Mary is, where everything lives, what Zac has
  permitted, what never to do. §10 (L166) - documentation duty.
- Ghost protocol, injection guard, never-invent: `MARY-JOB-SESSION.md` §1.

## Pricing - the engine and its facts

- THE workflow per Adam: `MARY-HANDOVER.md` §5 (L61); pricing facts §6 (L81).
- Price through `mary_pricing.py`, never a fresh script: `MARY-JOB-SESSION.md` §5a2.
- Pricing logic notes / codes and labour allowances: `AI.md` L1014, L1025.
- The labour code silently under-prices anything measured in m2: `AI.md` L196.
- The rate register prices frames and glass, and almost nothing else: `AI.md` L1461.
- Never overstate a rate's provenance: `AI.md` L397.
- A cheaper quote is not cheaper until you count what is NOT in it: `AI.md` L262.
- Strip-out HAS a rate - GBP 150.00/unit, from our own Brandon Estate archive: `AI.md` L2884.
- Mastic and EPDM are optional extras - but check where they sit: `AI.md` L477; the
  optional-mastic line comes out where the pricing charges for it: `AI.md` L2876.
- The install line is fit-only, and there is a control that proves it: `AI.md` L2803.
- Calibration duty and the +10% high bias with band-shaped error: `MARY-JOB-SESSION.md` §5c.

## Spec and compliance

- Fire ratings live in NBS clause L20: `AI.md` L408.
- AOV free area - and geometric vs AERODYNAMIC (they differ by roughly 40%): `AI.md` L428, L1148.
- When two fabricators refuse the same requirement, the finding is against the SPEC: `AI.md` L226.
- When a spec names a manufacturer AND a number our fabricators cannot reach: `AI.md` L324.
- Supplier advisory notes decide who carries the standards you promised: `AI.md` L2831.
- Comparing a revised drawing against what was priced: `AI.md` L544.
- Deferrals: administrative gap or design gap? And read the title block: `AI.md` L1673.

## Auditing and checks (every rule is a mistake that happened)

- Run `mary_checks.py` before anything leaves: `MARY-JOB-SESSION.md` §5d.
- Auditing a quote the team already sent: `AI.md` L160. Audit the RFQ, not just the
  quote: `AI.md` L368. Point mary_checks at REAL file paths: `AI.md` L351.
- Fix the defect at the TEMPLATE, not at the job: `AI.md` L297.
- Open the client's own pricing schedule and find the line you returned empty: `AI.md` L2813.
- Read the column, not the phrase: `AI.md` L2823.
- A missing number is not automatically a mistake: `AI.md` L2861.
- A representation of the source is not the source: `AI.md` L1597.
- Who wrote it and whether they still work here (Harry Grover left ~Nov 2025; `jayk@` is a
  deleted mailbox, not an empty one; the supplier thread has its own subject, and the
  price a client asks you to confirm can be under cost): `AI.md` L2972.
- Self-checking quotes: `AI.md` L132.

## Working the job (process judgement)

- "No rate" and "no quantity" are different problems with different owners: `AI.md` L1419.
- Who owns the decision, and who holds the information: `AI.md` L1533; clause 16 -
  sort findings by whose responsibility they are: `AI.md` L1554.
- When a job stalls on a client, sort open items by who blocks them: `AI.md` L1382.
- Draft the LETTER, not the request - and check what still sits in outputs\: `AI.md` L1482.
- Adopting a finding from another chat: separate the idea from the tool: `AI.md` L1724.
- Live projects are not estimating - and emailing Adam about one IS working it: `AI.md` L639.
- Extraction rules that matter: `AI.md` L684.

## Writing to Adam

- `data/knowledge/adam.md` - ALWAYS loaded. The gate: `mary_send.py --check`.
- Adam on how to write to him, and the finding it cost: `AI.md` L2840.
- Earn the interruption / errors always go: `MARY-EMAIL-SESSION.md` §3.

## Clients and jobs

- Clients not to quote: `AI.md` L619 (Hightown per Adam 28/07; Neil Douglas live-tender
  no-approach is on the internal chat record).
- Known job patterns (per-job quirks, Addington Rd -> Alkerden): `AI.md` L699-949 -
  prefer the job's own `data/jobs/<key>.md`, which is maintained; these are snapshots.
- Live job table: `MARY-HANDOVER.md` §7 - and the hub is the living version of it.

## Tooling traps (cost real debugging time)

- `MARY-HANDOVER.md` §9 (L152) - the short list. Longer stories: kick prompt must not
  go on the command line `AI.md` L440; Graph 403s - find out WHAT is blocked `AI.md`
  L492; the chat registry is shared mutable state `AI.md` L585.
- A bot that looks idle: find WHICH limit stopped it (ours or theirs - `fails` tells
  you), and a constant is read at import, so the change is the restart: `AI.md` L2926.
- Hub development: `MARY-HUB-DEV.md`. Bots overview: `BOTS.md`.

## Keeping this shelf honest

New durable lesson -> append the full account to `AI.md` as before, then add its one-line
entry here under the right topic. The librarian (`scripts/mary_librarian.py`) checks this
file stays under 120 lines and that its `AI.md` pointers still land on a heading.
