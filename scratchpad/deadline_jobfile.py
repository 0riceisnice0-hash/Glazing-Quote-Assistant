import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

P = r"C:\Users\zacpl\Desktop\Glazing-Quote-Assistant\data\jobs\st-marys.md"
s = open(P, encoding="utf-8").read()

banner = """# St Mary's Refurbishment, Merthyr Tydfil - E T & S Construction

> ## THE PACKAGE IS RE-OPENED. RETURN DATE **27 JULY 2026** - TODAY. **REQ-25.**
>
> ET&S's Document Register issued with the 24/07 revised drawings carries
> **"Package return date: 27 July 2026"** in its header. The 08/07, 09/07 and 16/07 registers all say
> **17 July 2026** - same package, same package lead (Tom Godfrey). **The 24/07 re-issue moved the
> deadline out by ten days.**
>
> | register | generated | package return date |
> |---|---|---|
> | original-08-07 | 7/8/2026 08:45 | 17 July 2026 |
> | schedule-09-07 | 7/9/2026 08:49 | 17 July 2026 |
> | pci-16-07 | 7/16/2026 11:43 | 17 July 2026 |
> | **revised-24-07** | **7/24/2026 12:10** | **27 JULY 2026** |
>
> We submitted on 17/07 and have treated this as closed and awaiting award ever since. **REQ-5 was right**
> that the addendum changed no scope - it was checked attribute by attribute across the drawings, and the
> return date is in the **register header**, not the drawings. I read that register three times over six
> turns without reading the top of the page.
>
> **If the package really is open until close of play, everything in this file stops being a post-mortem
> on a submitted quote and becomes a corrected tender.** Somebody must establish it with Tom Godfrey
> today - Mary cannot: outbound email is down (REQ-23) and only ever reached adam@/marketing@.
>
> **And our own recorded deadline was never a client date.** The hub carried 16/08, which is the
> BSW/Bellview 30-day quote validity - it had become "the deadline" because it was the only date written
> down. Now corrected to 27/07.

"""

s = s.replace("# St Mary's Refurbishment, Merthyr Tydfil - E T & S Construction\n", banner, 1)
s = s.replace("*Last updated 27/07/2026 (fourth turn).", "*Last updated 27/07/2026 (seventh turn).")
open(P, "w", encoding="utf-8").write(s)
print("job file banner added:", "REQ-25" in s, "| return date line present:", "27 JULY 2026" in s)
