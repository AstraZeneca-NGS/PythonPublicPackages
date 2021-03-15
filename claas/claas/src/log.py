import inspect
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

BACKUPCOUNT = 1000
MAXBYTES = 10_000_000
SEP = "\t"
LOGGING_FORMAT = "%(asctime)s{0}%(levelname)s{0}%(message)s".format(SEP)
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _create_logger():
    """ logger set up """
    logging.basicConfig(format=LOGGING_FORMAT, datefmt=DATE_FORMAT, stream=sys.stderr, level=logging.WARNING)
    return logging.getLogger("Log")


logger = _create_logger()


class Log:
    """
    Should be used as a singleton, default logging level is WARNING
    If is_debug is True DEBUG level is set
    If is_verbose is True INFO level is set
    If redirect is passed log messages are appended to the file specified
    """
    def __init__(self, **kwargs):
        self.is_debug = kwargs.get("is_debug", False)
        self.is_verbose = kwargs.get("is_verbose", False)
        self.redirect = kwargs.get("redirect")

        if self.is_debug:
            logger.setLevel(logging.DEBUG)
        elif self.is_verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        if self.redirect is not None:
            try:
                self._touch_file()
            except IOError as io_error:
                sys.exit(repr(io_error))
            except Exception as e:
                sys.exit(repr(e))
            self._add_file_handler()

    def _touch_file(self):
        """
        Create folders needed to keep logs if path does not exist, add file
        if does not exist and set access/modified as current time.
        """
        folder = os.path.abspath(os.path.dirname(self.redirect))
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        with open(self.redirect, "a"):
            os.utime(self.redirect, None)

    @staticmethod
    def _context(frame_number: int = 2) -> str:
        """
        Returns a string with filename:line number and function or class and method called
        """
        frame = inspect.stack()[frame_number]
        class_name = ''
        check_class = frame[0].f_locals.get("self")
        if check_class is not None:
            class_name = check_class.__class__.__name__ + ':'
        return f"{frame.filename}:{frame.lineno}{SEP}{class_name}{frame.function}"

    def _add_file_handler(self):
        """
        Adds a file handler to append log messages.
        Will create a new log ~ each 10Mb.
        Keep 1000 log files in the folder.
        """
        file_handler = RotatingFileHandler(self.redirect, maxBytes=MAXBYTES, backupCount=BACKUPCOUNT)
        file_handler.setFormatter(logging.Formatter(fmt=LOGGING_FORMAT, datefmt=DATE_FORMAT))
        logger.addHandler(file_handler)

    def info(self, msg: str):
        """
        Shows msg to STDOUT if we are in 'verbose' mode
        If redirect is defined, also append message to the file
        """
        logger.info(f"{msg}")
        sys.stdout.flush()

    def debug(self, msg: str):
        """
        Shows msg to STDERR if we are in 'debug' mode
        If redirect is defined, also append message to the file
        """
        logger.debug(f"{self._context()}{SEP}{msg}")
        sys.stderr.flush()

    def warning(self, msg: str):
        """
        Shows msg to STDERR
        If redirect is defined, also append message to the file
        Same message structure as debug
        """
        logger.warning(f"{self._context()}{SEP}{msg}")
        sys.stderr.flush()

    def error(self, msg):
        """
        Shows msg to STDERR
        If redirect is defined, also append message to the file
        Same message structure as debug
        """
        logger.error(f"{self._context()}{SEP}{msg}")
        sys.stderr.flush()

    def fatal_error(self, msg: str):
        """
        Shows msg to STDERR
        If redirect is defined, also append message to the file
        Same message structure as debug
        Exit with code 1
        """
        logger.error(f"{self._context()}{SEP}{msg}")
        sys.stderr.flush()
        sys.exit(1)
