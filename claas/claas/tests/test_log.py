import sys

import logging
import unittest
from mock import patch

from claas.claas.src.log import Log
import claas.claas.src.log as log_module


class TestLog(unittest.TestCase):
    def test_log_level_debug(self):
        Log(is_debug=True)
        assert logging.getLogger("Log").level == logging.DEBUG

    def test_log_level_info(self):
        Log(is_verbose=True)
        assert logging.getLogger("Log").level == logging.INFO

    def test_log_leveL_default(self):
        Log()
        assert logging.getLogger("Log").level == logging.WARNING

    @patch.object(Log, '_add_file_handler')
    def test_redirect_methods(self, file_method):
        with patch.object(Log, '_touch_file') as touch_method:
            Log(redirect='test.log')
            file_method.assert_called_once()
            touch_method.assert_called_once()

    @patch.object(Log, '_context')
    def test_call_context(self, context_method):
        """
        Ensure that _context() method is called in debug/warning/error/fatal error,
        but is not called in info. Mock sys.exit() for fatal_error()
        """
        log = Log()
        log.info('info message')
        context_method.assert_not_called()

        log.debug('debug message')
        context_method.assert_called_once()

        log.warning('warning message')
        assert context_method.call_count == 2

        log.error('error message')
        assert context_method.call_count == 3

        with patch.object(sys, 'exit'):
            log.fatal_error('fatal error message')
            assert context_method.call_count == 4

    def test_add_file_handler(self):
        log = Log()
        log.redirect = 'test.log'
        log._add_file_handler()
        current_handler = logging.getLogger("Log").handlers[0]
        assert 'RotatingFileHandler' in str(current_handler)
        assert current_handler.maxBytes == log_module.MAXBYTES
        assert current_handler.formatter._fmt == log_module.LOGGING_FORMAT
        assert current_handler.formatter.datefmt == log_module.DATE_FORMAT

    def test_context_in_class(self):
        """
        Context inside TestLog class must show class name and method
        """
        context = Log._context()
        assert 'TestLog:run' in context


def test_context_in_method():
    """
    Context outside must show call method
    """
    context = Log._context()
    assert 'pytest_pyfunc_call' in context


if "__name__" == "__main__":
    testsuite = unittest.TestLoader().discover(pattern="test_*.py", start_dir="")
    unittest.TestRunner().run(testsuite)
