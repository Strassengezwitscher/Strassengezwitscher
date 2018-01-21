import os
from unittest import mock

from django.test import TestCase

from twitter import utils


class TwitterUtilTests(TestCase):

    def test_unlock_removes_file(self):
        utils.LOCK_PATH.touch()
        self.assertTrue(utils.LOCK_PATH.exists())
        utils.unlock_twitter()
        self.assertFalse(utils.LOCK_PATH.exists())

    def test_lock_writes_pid_to_file_and_returns_true(self):
        self.assertTrue(utils.lock_twitter())
        with utils.LOCK_PATH.open() as pidfile:
            pid_from_file = int(pidfile.read())
        self.assertEqual(pid_from_file, os.getpid())
        utils.unlock_twitter()

    @mock.patch('os.kill')
    def test_lock_on_already_locked_still_active(self, os_kill):
        with utils.LOCK_PATH.open('w') as pidfile:
            pidfile.write('%i' % -4)
        self.assertFalse(utils.lock_twitter())
        os_kill.assert_called_once_with(-4, 0)
        utils.unlock_twitter()

    def test_lock_removes_corrupt_file(self):
        utils.LOCK_PATH.touch()  # we have an invalid (empty) lock file now
        self.assertTrue(utils.lock_twitter())
        pid_from_file = int(utils.LOCK_PATH.read_text())
        self.assertEqual(pid_from_file, os.getpid())
        utils.unlock_twitter()

    @mock.patch('os.kill', mock.Mock(side_effect=OSError()))
    def test_lock_on_already_locked_orphaned(self):
        with utils.LOCK_PATH.open('w') as pidfile:
            pidfile.write('%i' % -4)
        self.assertTrue(utils.lock_twitter())
        pid_from_file = int(utils.LOCK_PATH.read_text())
        self.assertEqual(pid_from_file, os.getpid())
        utils.unlock_twitter()
