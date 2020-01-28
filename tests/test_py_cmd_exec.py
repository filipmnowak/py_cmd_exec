import logging
import unittest
import warnings
from py_cmd_exec import CMDExec as cmdexec
from time import time
from time import sleep
from random import randint
from os import chmod
from os import remove
from stat import S_IEXEC
from stat import S_IREAD


class NullHandler(logging.Handler):

    def emit(self, record):
        pass


class TestUtils(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        self.mute_logger = logging.getLogger().addHandler(NullHandler())

    def test_cli_exec_execute_blocking_timeout_0s(self):
        warnings.simplefilter("ignore", ResourceWarning)
        test_timeout = 0
        test_string = str(time())
        x = cmdexec(['echo', test_string], timeout=test_timeout, blocking=True,
                    logger=self.mute_logger)
        moc_res = (0, ['echo', test_string], test_string + '\n', '')
        res = x.execute()
        self.assertEqual(res, moc_res)

    def test_cli_exec_execute_blocking_timeout_10s(self):
        warnings.simplefilter("ignore", ResourceWarning)
        test_timeout = 10
        test_string = str(time())
        x = cmdexec(['echo', test_string], timeout=test_timeout, blocking=True,
                    logger=self.mute_logger)
        moc_res = (0, ['echo', test_string], test_string + '\n', '')
        res = x.execute()
        self.assertEqual(res, moc_res)

    def test_cli_exec_execute_nonblocking(self):
        warnings.simplefilter("ignore", ResourceWarning)
        test_string = str(time())
        args = ['echo', test_string]
        x = cmdexec(args, blocking=False, logger=self.mute_logger)
        res = x.execute()
        moc_res = (0, args, None, None)
        self.assertEqual(res, moc_res)

    def test_regression_ismiddle1088(self):
        # 1. create a script which prints no. of the args with which it was called
        # 2. redirect its output to a file
        # 3. check the file for the expected output
        warnings.simplefilter("ignore", ResourceWarning)
        test_script = './' + str(time()) + '.ismiddle1088'
        test_script_out = test_script + '_out'
        args = [test_script, '1', '2', '3']
        with open(test_script, 'w') as f:
            f.write('#!/bin/bash\n')
            # we can't rely on stout / stderr
            f.write('echo ${#} > ' + test_script_out + '\n')
        chmod(test_script, S_IEXEC | S_IREAD)
        x = cmdexec(args, blocking=False, logger=self.mute_logger)
        res = x.execute()
        moc_res = (0, args, None, None)
        self.assertEqual(res, moc_res)
        # without sleep test often runs before file is being created
        sleep(3)
        with open(test_script_out, 'r') as f:
            arg_count = int(f.read().rstrip())
        self.assertEqual(arg_count, (len(args) - 1))
        remove(test_script)
        remove(test_script_out)

if __name__ == "__main__":
    unittest.main()
