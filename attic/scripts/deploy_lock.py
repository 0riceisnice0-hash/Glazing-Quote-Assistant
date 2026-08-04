# -*- coding: utf-8 -*-
"""One deploy at a time - a lock, not a queue of bots.

On 29/07 two deploys raced (a dev-session deploy and Mary's close-out deploy)
and last-write-wins shipped the older Functions bundle: a brand-new API route
404'd in production until someone noticed. The historical fix was serialising
the BOTS ("do not deploy while the other is mid-deploy"), which starved Jacob
all morning to protect one wrangler call. This locks the deploy itself, so
Mary, Jacob and any dev session can work fully independently.

Usage in any script that runs `wrangler pages deploy`:

    import deploy_lock
    with deploy_lock.held():        # blocks up to 5 minutes, then raises
        subprocess.run([... wrangler ...])
"""
import contextlib
import os
import time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCKFILE = os.path.join(REPO, "test-results", "deploy.lock")
WAIT_SECONDS = 300
STALE_SECONDS = 600   # a deploy takes ~1 minute; ten means the holder died


@contextlib.contextmanager
def held():
    os.makedirs(os.path.dirname(LOCKFILE), exist_ok=True)
    deadline = time.time() + WAIT_SECONDS
    while True:
        try:
            fd = os.open(LOCKFILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            break
        except FileExistsError:
            try:
                if time.time() - os.path.getmtime(LOCKFILE) > STALE_SECONDS:
                    os.remove(LOCKFILE)   # holder died mid-deploy; reclaim
                    continue
            except OSError:
                pass
            if time.time() > deadline:
                raise RuntimeError(
                    "deploy lock held for over %ds by another process (%s) - "
                    "if nothing is deploying, delete the file"
                    % (WAIT_SECONDS, LOCKFILE))
            time.sleep(5)
    try:
        yield
    finally:
        try:
            os.remove(LOCKFILE)
        except OSError:
            pass
