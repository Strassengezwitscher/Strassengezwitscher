import os
import pathlib

LOCK_PATH = pathlib.Path('.tweets.lock')


def lock_twitter():
    """Must be called by TwitterAccount's fetch_tweets method when it starts."""
    if LOCK_PATH.exists():
        old_pid = int(LOCK_PATH.read_text())
        try:
            # Check if process with PID old_pid still exists.
            # The null signal is actually not sent, but error checking is performed, so old_pid is validated.
            # If no process with PID old_pid is found OSError is raised.
            os.kill(old_pid, 0)
            return False  # process is still running -> still locked
        except OSError:
            LOCK_PATH.unlink()  # found orphaned PID file

    with LOCK_PATH.open('w') as pidfile:
        pidfile.write('%d' % os.getpid())
    return True


def unlock_twitter():
    """Must be called by TwitterAccount's fetch_tweets method when it ends."""
    if LOCK_PATH.exists():
        LOCK_PATH.unlink()
