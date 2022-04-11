"""
\defgroup Logging
Main class for logging.
This class is 100% compatible with the default Python logging class
and make it easy to setup handlers for console, file and kafka.
The Kafka handler should be used in production only if possible.
"""
import logging, sys, os, getpass, socket, json, re
try:
    _rootpath = os.path.dirname(os.path.abspath(__file__)) + '/..'
except:
    _rootpath = os.getcwd()
sys.path.append(_rootpath)

from logging.handlers import TimedRotatingFileHandler
from dlxlibs.DlxLoggingFormatter import DlxLoggingFormatter
from dlxlibs.DlxConfigParser import DlxConfigParser


class DlxLogger:
    """
    Generic logger class for Deluxe on the EDP

    Args:
        app_name (str, optional): Application/logger name. Defaults to "".
        format (str, optional): csv | json | default - Log format see FORMATTERS. Defaults to "json".
        log_ext (str, optional): Log file extension. Defaults to "log".
        handlers (str, optional): Handlers to setup. k=Kafka, f=file, c=console. Defaults to "fc".
        source_system_name (str, optional): Name of the source system or app. Defaults to "logs".
        schema_name (str, optional): Schema name. Defaults to "logs".
        table_name (str, optional): Table name. Defaults to "logs".
        env (str, optional): Environment, dev | prod. Defaults to "dev".

     Usage:
        my_logger = DlxLogger().get_logger()
        my_logger.debug("a debug message")

    other example:
        my_logger = DlxLogger("", "csv", "csv").get_logger()
        my_logger.debug("THIS IS IT ! a debug message", {command: "INSERT", storagename: "logs__logs__testtable", count: 20})

    This will create a CSV formatted file with a .csv extension
    """

    _app_name = "default"
    _log_format = "json"
    _log_dir = "//..//logs//"
    _log_ext = "log"
    _full_log_file_name = ""
    _formatter = DlxLoggingFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    _username = ''
    _homedir = ''
    _hostname = ''
    _handlers = 'fc'
    _source_system_name = "logs"
    _schema_name = "logs"
    _table_name = "logs"
    _env = "dev"

    def __init__(
        self,
        app_name="",
        format="json",
        log_ext="log",
        handlers="fc",
        source_system_name="logs",
        schema_name="logs",
        table_name="logs",
        env="dev"
    ):
        """
        Constructor initializing some base vars
        @todo Make this a singleton
        @todo Use the json config file and override the default params

        Args:
            app_name (str, optional): Application/logger name. Defaults to "".
            format (str, optional): csv | json | default - Log format see FORMATTERS. Defaults to "json".
            log_ext (str, optional): Log file extension. Defaults to "log".
            handlers (str, optional): Handlers to setup. k=Kafka, f=file, c=console. Defaults to "fc".
            source_system_name (str, optional): Name of the source system or app. Defaults to "logs".
            schema_name (str, optional): Schema name. Defaults to "logs".
            table_name (str, optional): Table name. Defaults to "logs".
            env (str, optional): Environment, dev | prod. Defaults to "dev".
        """
        self._source_system_name = source_system_name
        self._schema_name = schema_name
        self._table_name = table_name
        # @todo : get this from the env where it is running
        # The idea is to make it "prod" when it runs in the context of Rundeck
        self._env = env

        # @todo make this effective
        _dlxConfigParser = DlxConfigParser()
        config = _dlxConfigParser.get_config("DlxLogger")

        if app_name == "":
            try:
                caller = sys._getframe(1)
                self._app_name = os.path.basename(
                    caller.f_globals['__file__']).split(".")[0]
            except:
                self._app_name = "default"
        else:
            self._app_name = app_name
        self._log_format = format
        self._log_ext = log_ext
        self._handlers = handlers

        try:
            self._username = os.getlogin()
        except:
            try:
                self._username = getpass.getuser()
            except:
                self._username = ''
        
        self._full_log_file_name = os.path.dirname(os.path.realpath(__file__)) + self._log_dir + self._username + '-' + self._app_name + '.' + self._log_ext
        self._formatter = self._get_format()
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

        Returns:
            DlxLoggingFormatter: logging.Formatter
        """
        FORMATTERS = {
            'default': "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            'csv': '"'+'","'.join(self._get_log_schema('values'))+'"',
            'json': json.dumps(self._get_log_schema())
        }
        return DlxLoggingFormatter(FORMATTERS[self._log_format])

    def _get_log_schema(self, type="all"):
        """
        Returns the log schemas in various form according to the type param

        Args:
            type (str, optional): all | values | keys. Defaults to "all".

        Returns:
            dict: The schema of a log entry
        """
        _ldata = {
            "source_system_name": self._source_system_name,
            "schema_name": self._schema_name,
            "table_name": self._table_name,
            "env": self._env,
            # | eg: "asctime": "2020-05-01 08:51:46,374"
            "asctime": '%(asctime)s',
            "levelname": '%(levelname)s',  # | eg: "levelname": "DEBUG"
            "levelno": '%(levelno)s',  # | eg: "levelno": "10"
            "message": '%(message)s',  # | eg: "message": "a debug message"
            "module": '%(module)s',  # | eg: "module": "loggertest"
            "filename": '%(filename)s',  # | eg: "filename": "loggertest.py"
            "homedir": self._homedir,  # | eg: "homedir": ""
            # | eg: "pathname": "C:/Users/T442512/PycharmProjects/spark-template-project/loggertest.py"
            "pathname": '%(pathname)s',
            "created": '%(created)f',  # | eg: "created": "1588337506.374059"
            "msecs": '%(msecs)d',  # | eg: "msecs": "374"
            # | eg: "relativeCreated": "65"
            "relativeCreated": '%(relativeCreated)d',
            "name": '%(name)s',  # | eg: "name": "root"
            "username": self._username,  # | eg: "username": ""
            "hostname": self._hostname,  # | eg: "hostname": ""
            "funcName": '%(funcName)s',  # | eg: "funcName": "<module>"
            "lineno": '%(lineno)d',  # | eg: "lineno": "6"
            "process": '%(process)d',  # | eg: "process": "14744"
            # | eg: "processName": "MainProcess"
            "processName": '%(processName)s',
            "thread": '%(thread)d',  # | eg: "thread": "1792"
            "threadName": '%(threadName)s',  # | eg: "threadName": "MainThread"
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

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self._formatter)
            return console_handler
        except:
            print('Console handler init failed')
            return None

    def _get_file_handler(self):
        """
        Returns handler for writing to a file
        @todo Add check on the log folder

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        try:
            file_handler = TimedRotatingFileHandler(
                self._full_log_file_name, when='midnight')
            file_handler.setFormatter(self._formatter)
            return file_handler
        except:
            print(
                'File handler init failed. Check that the "logs" directory exists in the root of your project.')
            return None

    def _get_kafka_handler(self):
        """
        Write to Kafka

        Raises:
            Exception: [description]

        Returns:
            [type]: [description]
        """
        try:
            from dlxlibs.DlxKafkaLoggingHandler import DlxKafkaLoggingHandler
            bootstrap_servers = "ala09035.edp-prod.deluxe.com:9093,ala09036.edp-prod.deluxe.com:9093,ala09037.edp-prod.deluxe.com:9093"
            _dlxKafkaLoggingHandler = DlxKafkaLoggingHandler(bootstrap_servers, 'log-loggers')
            _dlxKafkaLoggingHandler.setFormatter(self._formatter)
            return _dlxKafkaLoggingHandler
        except Exception as ee:
            # print(ee)
            print('Kafka handler init failed')
            return None

    def get_logger(self, loggername=""):
        """
        Returns the logger all configured ready to use

        Returns:
            [type]: [description]
        """
        if loggername == "" and self._app_name != "default":
            loggername = self._app_name
        elif loggername == "":
            loggername = __name__
        
        logger = logging.getLogger(loggername)
        logger.setLevel(logging.DEBUG)
        chs = logging.StreamHandler()
        logger.addHandler(chs)

        if re.search('c', self._handlers):
            ch = self._get_console_handler()
            if ch is not None:
                logger.addHandler(ch)

        if re.search('f', self._handlers):
            fh = self._get_file_handler()
            if fh is not None:
                logger.addHandler(fh)

        if re.search('k', self._handlers):
            # kh = self._get_kafka_handler()
            # if kh is not None:
            #     logger.addHandler(kh)
            pass

        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger
