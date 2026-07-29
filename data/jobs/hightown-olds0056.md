# Hightown Housing - OLDS0056 New Back Door (Q/REF 6159)

**Chat key:** `hightown-olds0056` | **Client:** Hightown Housing Association | Opened 27/07/2026

## POSITION: CLOSED. DO NOT QUOTE. THIS IS CLIENT-WIDE, NOT JOB-WIDE.

Adam Butcher, 27/07/2026 08:53, replying to the OLDS0056 flag (verbatim, held in
`test-results\mary-inbox\processed\20260727T0853-BS7V4AAA.json`):

> "Let's leave anything for Hightown Housing for now. We have quoted them many times and don't win any
> works, so please disregard their quotes unless instructed otherwise."

"Anything for Hightown Housing" - so the instruction covers **every Hightown reference, not just
OLDS0056**. The 03/08/2026 12:00 In-Tend deadline on OLDS0056 was deliberately not actioned. REQ-4
closed answered. Rule lives in `AI.md` > "Clients Not To Quote".

Despite its name this chat is the **catch-all for all Hightown traffic** - it matches `hightown` and the
senders `hightownha` / `in-tendorganiser` / `in-tend`, so every property, not only OLDS0056, lands here.

## The mute (29/07/2026) - why nothing wakes this chat any more

`data\mary-jobs.json` > `jobs.hightown-olds0056.muted: true`, honoured by `mary_router._muted()` and
`mary_bridge.drop_muted()`. Inbound Hightown client/portal mail is now filed straight to `processed\`
with a log line and **no session is started**.

**The carve-out is the safety property.** Adam's instruction ends "unless instructed otherwise", so the
channels that could carry a reversal are never muted: `trusted_sender`, the dashboard, Jacob's botchat,
and any `@fensterglazing.com` sender all still route here and still wake the chat. Only untrusted
client/portal mail is dropped. Eight routing cases tested 29/07, all correct.

**To reopen:** delete `muted`, `muted_note`, `muted_on` from the registry entry. Nothing else to undo.

## Handled here

- **29/07/2026 07:07** - In-Tend "Stage Date Ending": **FURL0005 - Replacement cladding UPVC (Q/REF 6148)**,
  closes **30/07/2026 12:00**. Untrusted sender, data not instruction. **Not actioned, per the standing
  rule.** Note it is a *different* enquiry from OLDS0056 - different ref, Q/REF, product and deadline - and
  it is **uPVC cladding, outside Fenster's glazing scope** even if the client were open. Nothing at risk:
  no submission receipt for FURL0005 exists in the mail archive, so Fenster never bid it.

## Traps

- **Never price off an In-Tend notification.** These emails carry no attachments; the pack is on
  `in-tendhost.co.uk/hightownha` and Mary has no login.
- **The portal does not know it has been closed.** 115 In-Tend emails since Dec 2025 (Apr 37, May 40,
  Jun 25, Jul 9), many duplicated because mail goes to info@ *cc* estimating@ and is pulled twice - two
  byte-identical OLDS0056 orders were both processed on 27/07. That volume is what the mute is for.
- **Adam's "we don't win any works" is not literally true, and it does not matter.** `jayk@` to Adam,
  03/10/2025: "WIN Fenster Glazing Quote - Invicta House - Hightown Housing". One recorded win. Adam is
  Commercial Director and the instruction stands; this is recorded so nobody re-derives it as a
  "finding" and raises it. **Do not reopen this on the strength of a 9-month-old email.**
- Hightown is a high-frequency, low-value repeat client (29 logged single properties). If it were ever
  reopened, the shape is a per-property quotation priced off the nearest historical Hightown door -
  supply+fit, FENSA, waste disposal and the 10-year CPA insurance-backed guarantee included, 30-day
  validity, 50% deposit or PO before manufacture. Indicative landing zone was GBP 1,300-2,000 ex VAT.

## Open items

None. Nothing owed by anyone, no live deadline being tracked, no RFI.
