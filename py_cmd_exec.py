import logging
from os import setsid
from os import devnull
from sys import exit
import sys
# required for subprocess.communicate()
if sys.version_info < (3, 3):
    raise RuntimeError('unsupported interpreter version, ' +
                       'Python 3.3 or higher required')
if sys.version_info >= (3, 4):
    from os import set_inheritable
else:
    def set_inheritable(fd, switch):
        return switch
if 'Oracle Corporation' in sys.version:
    JYTHON = True
else:
    from os import fork
    from os import execvp
    JYTHON = False
from signal import signal
from signal import SIG_IGN
from signal import SIGCHLD
from subprocess import Popen
from subprocess import PIPE
from subprocess import TimeoutExpired


class CMDExec:
    """Execute external command / program.

       arguments:
         cmd : str or list
           Command to be executed within a container, it can be name of the file,
           relative path or absolute path. All of the list elements after command
            are considered its arguments.

         blocking : bool, optional
           By default execution is blocking and synchronous. For non-blocking behavior
           (AKA "fire and forget"), no return value or output of the command is
           returned / provided to the caller.

         timeout : int, optional
           Timeout for the command execution.

         logger : logging.Logger, optional
           Logger object. Will be autoinitialized in case if not given by the caller.

       returns:
         <command rc>, <command executed>, <command stdout>, <command stderr>

       raises:
         TypeError
           Being raised on invalid arguments / parameters."""

    def __init__(self, cmd, blocking=True, timeout=None, logger=None):
        self.cmd = cmd
        self.blocking = blocking
        self.timeout = timeout or -1
        self.log = logger
        if not logger:
            logging.basicConfig(level=logging.DEBUG)
            self.log = logging.getLogger(__name__)

        if JYTHON and not self.blocking:
            raise RuntimeError('non-blocking execution is not supported for Jython!')
    def _execute(self, args):
        if self.blocking:
            self.log.debug('attempting blocking execution of %s' % (args))
            try:
                # emulate blocking behavior
                proc = Popen(args, stdout=PIPE, stderr=PIPE)
            except OSError as e:
                self.log.error("failed to execute %s:" % (args), exc_info=e)
                return 127, args, None, None
            try:
                _stdout, _stderr = proc.communicate(self.timeout)
            except TimeoutExpired as e:
                self.log.error("failed to execute %s due to a timeout (time limit: %i)"
                               % (args, self.timeout))
                return 1, args, None, None
            return (proc.returncode, args, _stdout.decode('utf8'),
                    _stderr.decode('utf8'))
        else:
            # ignore SIGCHLD because we don't want to wait for its exit status
            signal(SIGCHLD, SIG_IGN)
            self.log.debug('attempting non-blocking execution of %s via fork()'
                           % (args))
            # double fork() to detach / disown
            try:
                self.ret = fork()
            except OSError as e:
                self.log.error("failed to fork:", exc_info=e)
                return 1, args, None, None
            if self.ret != 0:
                return 0, args, None, None
            else:
                setsid()
                sys.stdin.close()
                f = open(devnull, 'w')
                set_inheritable(f.fileno(), True)
                sys.stderr.close()
                sys.stderr = f
                sys.stdout.close()
                sys.stdout = f
                try:
                    self.ret = fork()
                except OSError as e:
                    self.log.error("failed to fork:", exc_info=e)
                    return 1, args, None, None
                if self.ret != 0:
                    exit()
                else:
                    try:
                            execvp(args[0], args)
                    except OSError as e:
                        self.log.error("failed to execute %s" % (args))
                        return 1, args, None, None

    def execute(self):
        self.log.info("executing %s" % (str(self.cmd)))
        return self._execute(self.cmd)
