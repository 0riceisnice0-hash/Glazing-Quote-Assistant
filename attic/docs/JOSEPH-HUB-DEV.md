# JOSEPH - your own board is yours to build

Zac, 04/08: *"let joseph think about how he wants his dashboard section to look
and code it himself. give him a master prompt type vibe, of like you are the
project manager, so make sure you can do that the best you can and tailor your
code and dashboard for it."*

So this is the brief, not the design. There is a working default in place so
nothing is blocked on you, and **you are expected to replace it** once you have
run a few real jobs and know what you actually reach for.

---

## The brief

**You are the project manager. Build the page you would want open while you
do the job.**

Not a page that describes your work to somebody else - a page you would work
from. If a thing on it does not change what you do next, it does not belong
on it.

The one question it has to answer, in the time it takes to look at it:
**what is going to go wrong, and what do I do about it today?**

---

## What you already have, and can change

`dashboard/public/app.js`, in the `BOTS.joseph` entry. Two pages today:

| Page | What it does |
|---|---|
| `decisions` | What you cannot decide alone - the JOS-n requests |
| `jomessages` | The two-way line with Adam and Zac |

Your *work* lives on **Contracts**, under The work, alongside Leads and
Companies. That is deliberate: a won job is the company's record, not yours,
and three bots reading one record is the whole point of the CRM. Do not
duplicate it. Add what is **yours** - how the delivery is going, what is about
to slip, what you are waiting on.

---

## What you can read

```
python scripts/crm.py --lead <key>        what we quoted, and to whom
python scripts/crm_contract.py --plan <site date>
```
```python
import sys; sys.path.insert(0, "scripts")
import crm, crm_contract
crm.delivery()                    # every task due or late, across live contracts
crm_contract.board("<key>")       # one job: twelve steps, what is done, what is late
crm._call("/api/crm/contracts")   # all of them
```

The API is live and public for reads: `/api/crm/contracts`, `/api/crm/delivery`,
`/api/crm/contract/<key>`. If you need a shape that does not exist, add the
route - `dashboard/functions/api/[[path]].js` - rather than bending the page
around the data.

---

## Before you touch the hub

**Read `MARY-HUB-DEV.md` first.** It is the hard-won part and it is short. The
two that will catch you:

- **Deploy from inside `dashboard/`, never the repo root.** From the root it
  succeeds, silently ships no API, and every route returns the SPA's HTML. The
  tell is a missing "Uploading Functions bundle" line.
- **`styles.css` sets `strong` and headings to `--ink`.** Anything dark on a
  dark surface inherits it and goes invisible.

And two learned since, both from breaking them:

- **`var(--r)` is not a token.** It is `--r-sm`, `--r-md`, `--r-lg`. An
  undefined custom property silently becomes nothing, which is what made every
  control in the CRM panel render with square corners.
- **Never put `-webkit-line-clamp` on a `<td>`.** It takes the cell out of
  table layout and the row height stops being governed by its cells. Clamp a
  span inside it.

Guard your work: `python scripts/mary_hub_guard.py` before you deploy. It is
not Mary's, it is the hub's.

---

## How to judge it

Ask the three questions this system keeps having to re-learn:

1. **Does a number on it mean what a reader will think it means?** 57 live
   contracts with no site date is not "nothing to do", it is "nothing can be
   scheduled" - and the page has to say the second one.
2. **Would somebody act differently because of it?** If not, cut it.
3. **Is it honest when it is empty?** An empty table reads as "nothing to do",
   which is usually a lie. Say why it is empty.

---

## What is not yours to decide

The money half - the chase ladder, applications versus final invoices, where
the invoice figure comes from when there are variations - is waiting on Adam
(D2, D3, D4 in `MASTER-PLAN.md`). Build the page so those slot in when the
answers arrive. Do not invent a chase ladder to fill the space.
