import logging
import sys
import os
import getpass
import socket
import json
from dlxlibs.DlxLoggingFormatter import DlxLoggingFormatter
from logging.handlers import TimedRotatingFileHandler


class DlxLogger:
    """
    Generic logger class for Deluxe on the EDP

     Usage:
        my_logger = DlxLogger().get_logger()
        my_logger.debug("a debug message")

    other example:
        my_logger = DlxLogger("", "csv", "csv").get_logger()
        my_logger.debug("THIS IS IT ! a debug message")

    This will create a CSV formatted file with a .csv extension

    """

    _app_name = "default"
    _log_format = "json"
    _log_dir = "//..//logs//"
    _log_ext = "log"
    _full_log_file_name = ""
    _formatter = DlxLoggingFormatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")
    _username = ''
    _homedir = ''
    _hostname = ''

    def __init__(self, app_name="", format="json", log_ext="log"):
        """
        Constructor initializing some base vars

        :param app_name: Application/logger name (default: default)
        :param format: sting - csv | json | default - Log format see FORMATTERS (default: json)
        :param log_ext: Log file extension (default: log)
        """
        if app_name == "":
            try:
                caller = sys._getframe(1)
                self._app_name = os.path.basename(caller.f_globals['__file__']).split(".")[0]
            except:
                self._app_name = "default"
        else:
            self._app_name = app_name
        self._log_format = format
        self._log_ext = log_ext
        self._full_log_file_name = os.path.dirname(os.path.realpath(__file__)) + self._log_dir + self._app_name + '.' + self._log_ext
        self._formatter = self._get_format()
        try:
            self._username = getpass.getuser()
        except:
            self._username = ''
        try:
            self._homedir = os.environ['HOME']
        except:
            self._homedir = ''
        try:
            self._hostname = socket.gethostname()
        except:
            self._hostname = ''


    def _get_format(self):
        """
        Get log formatter

        :return: logging.Formatter
        """
        FORMATTERS = {
            'default': "%(asctime)s — %(name)s — %(levelname)s — %(message)s",
            'csv': '"'+'","'.join(self._get_log_schema('values'))+'"',
            'json': json.dumps(self._get_log_schema())
        }
        # return logging.Formatter(fmt=FORMATTERS[self._log_format])
        return DlxLoggingFormatter(FORMATTERS[self._log_format])

    def _get_log_schema(self, type="all"):
        """
        Returns the log schemas in various form according to the type param

        :param type: String - all | values | keys
        :return:
        """
        _ldata = {
            "asctime": '%(asctime)s',                   ## | eg: "asctime": "2020-05-01 08:51:46,374"
            "levelname": '%(levelname)s',               ## | eg: "levelname": "DEBUG"
            "levelno": '%(levelno)s',                   ## | eg: "levelno": "10"
            "message": '%(message)s',                   ## | eg: "message": "a debug message"
            "module": '%(module)s',                     ## | eg: "module": "loggertest"
            "filename": '%(filename)s',                 ## | eg: "filename": "loggertest.py"
            "homedir": self._homedir,                   ## | eg: "homedir": ""
            "pathname": '%(pathname)s',                 ## | eg: "pathname": "C:/Users/T442512/PycharmProjects/spark-template-project/loggertest.py"
            "created": '%(created)f',                   ## | eg: "created": "1588337506.374059"
            "msecs": '%(msecs)d',                       ## | eg: "msecs": "374"
            "relativeCreated": '%(relativeCreated)d',   ## | eg: "relativeCreated": "65"
            "name": '%(name)s',                         ## | eg: "name": "root"
            "username": self._username,                 ## | eg: "username": ""
            "hostname": self._hostname,                 ## | eg: "hostname": ""
            "funcName": '%(funcName)s',                 ## | eg: "funcName": "<module>"
            "lineno": '%(lineno)d',                     ## | eg: "lineno": "6"
            "process": '%(process)d',                   ## | eg: "process": "14744"
            "processName": '%(processName)s',           ## | eg: "processName": "MainProcess"
            "thread": '%(thread)d',                     ## | eg: "thread": "1792"
            "threadName": '%(threadName)s',             ## | eg: "threadName": "MainThread"
            "args": '%(args)s',
            "exc_info": '%(exc_info)s',
            "exc_text": '%(exc_text)s',
            "stack_info": '%(stack_info)s'
        }
        if type == 'values':
            return _ldata.values()
        elif type == 'keys':
            return _ldata.keys()
        else:
            return _ldata


    def _get_console_handler(self):
        """
        Returns the handler for displaying to the console

        :return:
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._formatter)
        return console_handler

    def _get_file_handler(self):
        """
        Returns handler for writing to a file

        :return:
        """
        file_handler = TimedRotatingFileHandler(self._full_log_file_name, when='midnight')
        file_handler.setFormatter(self._formatter)
        return file_handler

    def get_logger(self):
        """
        Returns the logger all configured ready to use

        :return:
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
        logger.addHandler(self._get_console_handler())
        logger.addHandler(self._get_file_handler())
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger
