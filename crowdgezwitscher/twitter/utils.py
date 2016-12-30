import os

LOCK_PATH = ".tweets.lock"


def lock_twitter():
    """Must be called before
    """

    if os.path.exists(LOCK_PATH):
        pidfile = open(LOCK_PATH, "r")
        old_pid = pidfile.readline()
        try:
            os.kill(int(old_pid), 0)  # will fail if no process with ID old_pid exists
            return False              # process is still running -> still locked
        except OSError:
            os.remove(LOCK_PATH)      # found orphaned PID file

    pidfile = open(LOCK_PATH, "w")
    pidfile.write("%s" % os.getpid())
    pidfile.close()
    return True


def unlock_twitter():
    if os.path.exists(LOCK_PATH):
        os.remove(LOCK_PATH)
