from django.test import TestCase

import mock
from mock import patch
import os

from twitter import utils

class TwitterUtilTests(TestCase):

    def test_unlock_removes_file(self):
        pidfile = open(utils.LOCK_PATH, 'w')
        self.assertTrue(os.path.exists(utils.LOCK_PATH))
        utils.unlock_twitter()
        self.assertFalse(os.path.exists(utils.LOCK_PATH))

    def test_lock_writes_pid_to_file_and_returns_true(self):
        self.assertTrue(utils.lock_twitter())
        pidfile = open(utils.LOCK_PATH, 'r')
        pid_from_file = int(pidfile.read())
        pidfile.close()
        self.assertEqual(pid_from_file, os.getpid())
        utils.unlock_twitter()

    @mock.patch('os.kill')
    def test_lock_on_already_locked_still_active(self, os_kill):
        pidfile = open(utils.LOCK_PATH, 'w')
        pidfile.write("%d" % -4)
        pidfile.close()
        self.assertFalse(utils.lock_twitter())
        os_kill.assert_called_once_with(-4, 0)
        utils.unlock_twitter()

    @mock.patch('os.kill', mock.Mock(side_effect=OSError()))
    def test_lock_on_already_locked_orphaned(self):
        pidfile = open(utils.LOCK_PATH, 'w')
        pidfile.write("%d" % -4)
        pidfile.close()
        self.assertTrue(utils.lock_twitter())
        pidfile = open(utils.LOCK_PATH, 'r')
        pid_from_file = int(pidfile.read())
        pidfile.close()
        self.assertEqual(pid_from_file, os.getpid())
        utils.unlock_twitter()
