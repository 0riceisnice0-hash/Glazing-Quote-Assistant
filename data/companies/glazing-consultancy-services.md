# Glazing Consultancy Services (GCS)

Slug: `glazing-consultancy-services`. Written 29/07/2026, from Adam's hub message 40
carrying Darren Trigg's own note, plus the AdminBase lead export.

**Darren Trigg**, `darren@glazingconsultancyservices.co.uk`.

## What they are, and why that matters

A glazing consultancy, not a main contractor and not the client. They specify and procure
glazing packages on somebody else's project, which means **they put Fenster on enquiry
lists**. That is worth more than any single job: in this trade a relationship buys one
thing, being asked to price, and GCS is a relationship whose entire function is asking
people to price.

Darren's own closing line, unprompted (via Adam, 29/07/2026):

> "Currently we are a bit quiet at present but please be assured that we will be sure to
> contact you when we are working on any new projects that we believe may be of interest
> to Fenster."

Read that against Adam's contracts export the same day: **three quarters of every contract
Fenster has ever won came from an existing relationship or from Jayk personally, and three
in the company's history came from a tender portal.** A consultant who volunteers to think
of us is a bigger asset than any feed on the board.

## The two live jobs, and why they are not live

Darren, via Adam, 29/07/2026:

> "Unfortunately both Aylesbury High School and Churchdown School Academy were CIF
> (condition improvement fund) bids and they were unsuccessful in securing funding, please
> keep all information to hand though as they are likely to resubmitted later this year,
> we will be in touch in due course."

**That kills six AdminBase rows, not two**, because Churchdown went out to five different
main contractors and every one of them is a separate lead reading "Live - Quoted":

| Lead | Client | Job | Quoted | Value ex VAT |
|---|---|---|---|---|
| 7009 | Glazing Consultancy Services | Aylesbury High School | 20/10/2025 | GBP 321,273.54 |
| 7098 | Glazing Consultancy Services | Churchdown School | 05/11/2025 | GBP 729,116.85 |
| 7139 | Kemdoc | Churchdown School | 12/11/2025 | GBP 746,616.85 |
| 7159 | Mobius Group | Churchdown School | 14/11/2025 | GBP 746,616.85 |
| 7267 | Roof Estimating Services | Churchdown School Academy | 02/12/2025 | GBP 729,116.85 |
| 7268 | Southern Projects | Churchdown School Academy | 02/12/2025 | GBP 729,116.85 |

Anyone working the chase list would have rung five contractors about a job none of them
has. **An outcome that arrives by email does not reach the CRM** - Darren told us the
funding failed and AdminBase has never heard.

## What CIF is, and what it does to the timing

Condition Improvement Fund is the annual capital pot academies and sixth-form colleges bid
into. It runs on a fixed cycle: bids in the autumn, outcomes the following spring, work
after that. **This is a reading of how the cycle works, not something Darren said** - what
he said is "later this year" and "in touch in due course". Do not quote the cycle back to
him as fact.

The consequence is the useful part. If the resubmission is written this autumn, the price
inside the bid is written this autumn too, and on a CIF bid the number in the submission is
usually the number that gets used. **Being in the bid beats being asked after it.**

## Next action

- **Late September 2026, before the autumn bid window** - Adam or Jacob to call Darren.
  Not "any news": ask to be the glazing number in the resubmission, and ask whether he
  wants the Churchdown pricing refreshed for it.
- Keep the Churchdown information to hand as he asked. It has been priced five times and
  that is the reason Fenster can be quick when it comes back.
- General: he is worth a call every couple of months whether or not there is a job on.
  Nothing is owed and nothing is being chased - the point is to stay on the list he writes
  when he is busy again.

## Position at 04/08/2026 - unchanged

Nothing new from Darren. `mary_recall --grep "Glazing Consultancy Services (GCS)" --days 30`
returns zero, the two CRM rows still read DO NOT CHASE, and the next action is still the
late-September call before the autumn bid window. There is no work to do on GCS right now
and that is the correct state, not a gap.

## This chat receives mail that is nothing to do with GCS

The permanent chat for this relationship is routed on `subject~glazing`, which matches
**"Fenster Glazing"** - our own name - so it catches company-wide correspondence. On 04/08
all four work orders were false positives: Neil Douglas outstanding quotes, a portal digest,
and two Sharnbrook Grain Storage messages. None mentioned GCS.

This is rule 3 of the three hard-won filtering rules in `JACOB-SESSION.md` playing out on our
own router: a single common word throws false positives. **Expect it, work the mail anyway -
it is still Jacob's mail - but do not go looking for a GCS angle that is not there.** The
useful match would be `glazingconsultancyservices` or Darren's address, not `glazing`.

## Open

- Nobody has replied to Darren. Offered Adam a draft on the hub, 29/07; not written unless
  he asks.
- No Companies House check run on GCS. Not needed yet - they are not the payer.
- Raised with Zac on the hub, 04/08: the `subject~glazing` routing rule above.
