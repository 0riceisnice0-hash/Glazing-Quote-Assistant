# -*- coding: utf-8 -*-
"""Archive older noticeboard entries so the kick prompt fits again.

EMERGENCY MITIGATION, 27/07/2026. The bridge passes the kick prompt as a
command-line argument and Windows caps that at 32,767 characters. The fix (prompt
via stdin) is committed but inert until the bridge restarts, and meanwhile EVERY
launch is failing - new chats and resumes alike - so Mary is frozen.

Trimming the board file is a DATA change, so it takes effect for the already
running bridge immediately. Nothing is lost: everything moves to
data/mary-noticeboard-archive.md and the board keeps a pointer to it.

Once the bridge is restarted the ceiling is gone and the board can grow again.
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOARD = os.path.join(REPO, "data", "mary-noticeboard.md")
ARCHIVE = os.path.join(REPO, "data", "mary-noticeboard-archive.md")
TARGET = 12000          # chars of entries to keep live
POINTER = ("> Older entries live in `data/mary-noticeboard-archive.md`. "
           "Read them with `python scripts\\mary_note.py --read` or open the file.\n")


def main():
    raw = open(BOARD, encoding="utf-8").read()
    # Entries start at a line beginning "### "; everything before the first one
    # is the board's own header and must stay.
    parts = re.split(r"(?m)^(?=### )", raw)
    header, entries = parts[0], parts[1:]
    if not entries:
        print("no entries found - leaving alone")
        return

    keep, size = [], 0
    for entry in reversed(entries):          # newest last in the file
        if size + len(entry) > TARGET and keep:
            break
        keep.append(entry)
        size += len(entry)
    keep.reverse()
    move = entries[:len(entries) - len(keep)]

    if not move:
        print("board already fits (%d chars of entries) - nothing archived" % size)
        return

    with open(ARCHIVE, "a", encoding="utf-8") as fh:
        if os.path.getsize(ARCHIVE) == 0 if os.path.exists(ARCHIVE) else True:
            fh.write("# Mary's noticeboard - archive\n\n"
                     "Older entries moved off the live board so the bridge kick prompt stays under\n"
                     "the Windows command-line limit. Newest at the bottom, same as the board.\n\n")
        fh.writelines(move)

    header = re.sub(r"(?m)^> Older entries live in .*\n", "", header)
    if not header.endswith("\n\n"):
        header = header.rstrip("\n") + "\n\n"
    with open(BOARD, "w", encoding="utf-8") as fh:
        fh.write(header + POINTER + "\n" + "".join(keep))

    print("archived %d entries (%d chars), kept %d (%d chars)"
          % (len(move), sum(len(e) for e in move), len(keep), size))


if __name__ == "__main__":
    sys.exit(main())
