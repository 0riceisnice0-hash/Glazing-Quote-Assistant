# Conamar Building Services Ltd

**Slug** `conamar` · **Area** SG/MK/London · `enquiries@conamar.co.uk` · **01438 365142**
Created 30/07/2026, first session that looked at them properly.

## Position

**The largest client in Fenster's history, and until tonight the board could not see them.**

- **16 won contracts, GBP 917,027.91** - 32% of every pound Fenster has ever won
  (GBP 2,835,812 across 204 contracts, `contracts-won.json`). Nobody else is close.
- **Every one of the sixteen was sold by Adam Butcher personally.** Not Jayk, not Harry
  Grover. `LEADSOURCE` on all sixteen is Existing Customer or Existing Commercial - this
  relationship has never once needed a lead source. **It is Adam's own, which is the
  single most useful fact on this page.**
- Continuous from **September 2021 to September 2025** - four unbroken years. Biggest:
  Tottenham Jobcentre **GBP 480,000** (fitted 14/06/2024), Franklin House Flitwick
  GBP 180,055, University of Roehampton GBP 75,000, Brace Street Bedford GBP 59,237.
  Repeat sites: Heals Building three times, Wootton Lower School twice.
- **Then it stopped.** Last order 02/09/2025. Last time Fenster was on their site
  15/12/2025 (Roehampton). Nothing since - no order, no enquiry, no quote.

**State: dormant, with GBP 219,774 of our quotes unanswered.** Not cold, not lost. Nobody
has told Fenster anything and nobody has asked.

## Why the board could not see them (fixed 30/07/2026)

`jacob_dormant.py` excluded Conamar as "mid-conversation - live quote already out". The
test was *does this client appear in the AdminBase pipeline at all*, and under **JAC-14**
(Adam, 29/07) nothing on that backlog ever closes on silence, so all 209 rows read "Live -
Quoted" forever. **The better the client, the more certain they were to be hidden** - and
the largest one in the company was hidden by two quotes whose next-action dates passed in
June 2025, 400 days ago. A quote now only counts as a live conversation while it is younger
than the silence being measured. Conamar came top of the list the moment it was fixed.

## The three quotes sitting with them

| Lead | Project | Ex VAT | Quoted | Silent |
|---|---|---|---|---|
| 6120 | Wootton School Farm, Hall End Rd, Bedford | **GBP 137,245.77** | 11/06/2025 | 414d |
| 6507 | Hollickwood Primary School, Muswell Hill | **GBP 57,260.01** | 05/08/2025 | 359d |
| 6109 | Premier Inn, Thanstead Farm, Loudwater | **GBP 25,268.64** | 09/06/2025 | 416d |

**GBP 219,774.42 in total**, all three still "Live - Quoted" in AdminBase.

**Jayk flagged Hollickwood himself** and it is on the repricing log he emailed on
19/12/2025 (`data/jacob/repricing.json`): *"Very late return. 09/12/2025 chased Simon for
an update. Worth repricing as legacy client."* So the last person to chase this was Jayk,
in December, and he left. Penny-exact value join - log GBP 57,260.01 = lead 6507.

## Named contacts - who actually replies

- **Simon Mead** - `Simon.mead@conamar.co.uk`. On lead 6507 (Hollickwood). The one Jayk
  chased in December. **Start here.**
- **John Ling** - `John.Ling@Conamar.co.uk`. Wootton Lower School. **Last actual message
  from a Conamar person to Fenster: 10/11/2025**, arranging site access for our service
  engineer. Helpful, practical, wrote to Paul.
- **Dean** - Lister Hospital, MHU Glaxo phase 3, 12-month defects snagging.
- **Laurence** - Wootton Lower School invoices.
- **Alex Taylor - LEFT.** Auto-reply on the address since 20/12/2024. Do not use it.
- `enquiries@conamar.co.uk` is the general box and is on two of the three live leads.

## What the mailbox says, against what the CRM says

**`quietDays` is 227 and that is days since WORK, never days since anyone spoke** - the RSR
lesson (`bd.md`). Searched all four mailboxes, all time: 45 hits. The real picture:

- **10/11/2025** John Ling, inbound, site access. The last two-way with a Conamar person.
- **18/11 and 26/11/2025** Adam sending invoices (Wootton, Lister).
- **08/12/2025** Adam chasing outstanding invoices at Wootton School.
- **Nothing since.** The 26/01/2026 and 25/03/2026 hits are not Conamar contact: one is a
  broadcast from info@ about a compromised mailbox, the other is the referral below.

**The money question looks closed, so the call is clean.** Five delivered jobs carry a
balance totalling GBP 6,514.64, and each is 2.5-5% of its contract value - that is the
shape of **retention** on a running defects period, not a disputed invoice. The Wootton
invoices Adam was chasing in December both show a zero balance now, so they were paid.
**Inference from the `balance` column, not a fact - confirm with Adam before leaning on
it**, because opening a "what have you got coming" call with a client who thinks they owe
us money would be the one way to waste this.

## An unanswered referral off the back of a Conamar job

**26/01/2026, Alana Somers, `A.Somers@Gardiner.com`** (Gardiner & Theobald, QS) to info@:
*"Market Testing - Arched Double Glazed Window. We previously worked together on the
University of Roehampton SETEC Project, where you supplied and installed external sash..."*

Perry Giffin forwarded it to commercial@ the same day. **There is no reply anywhere in any
mailbox** - three messages, all 26/01/2026, and that is the whole thread. A national QS
came back to Fenster by name on the strength of a delivered Conamar job and got silence.
Small job, six months cold, and worth one email to find out if it is still live. Note that
Roehampton is the job that generated it - **the GBP 75,000 one, fitted 15/12/2025.**

## Next action and who owns it

1. **Adam rings Simon Mead at Conamar.** Not "how have you been" - **GBP 219,774 of our
   prices have been sitting with them for over a year and nobody has said anything either
   way.** Ask which of the three are still live, what the feedback on the price was, and
   what they have coming in 2026. Adam sold all sixteen jobs himself; this is a call he can
   make without any preamble. **Owner: Adam. Not started.**
2. **Wootton School Farm, GBP 137,245.77, is the one to lead with** - the largest of the
   three and 414 days silent.
3. **Hollickwood needs Mary before it needs a client.** Jayk's note says reprice, and a
   14-month-old figure is not a figure any more. Price is hers and Gintare's, never mine.
4. **Somebody answers Alana Somers at Gardiner** - or decides not to, on purpose.
5. Ask Adam whether the GBP 6,514.64 is retention. It changes how the call opens.

## Standing facts

- Not a supplier. Not on any do-not-approach instruction.
- Nothing about Conamar has ever been said on the bot line or the hub -
  `mary_recall.py --grep conamar` returns one incidental hit. **This page is the first time
  anyone has written the relationship down.**
- Conamar is a main contractor: Fenster is their glazing subcontractor. So the schemes they
  bid are frequently public even when their enquiry list is not (`bd.md`) - worth a
  Contracts Finder and PlanIt sweep on "Conamar" before the call, which nobody has run.
