"""
\defgroup Logging
Extends the StreamHandler pushing data to Kafka
"""
import os, sys
from logging import StreamHandler
try:
    _rootpath = os.path.dirname(os.path.abspath(__file__)) + '/..'
except:
    _rootpath = os.getcwd()
sys.path.append(_rootpath)
from dlxlibs.DlxKafkaBroker import DlxKafkaBroker

class DlxKafkaLoggingHandler(StreamHandler):
    """
    Logging handler for Kafka streaming

    Args:
        StreamHandler ([type]): [description]
    """


    def __init__(self, bootstrap_servers, topic):
        """
        Init the kafka handler

        Args:
            bootstrap_servers ([type]): Kafka servers to use
            topic ([type]): Topic name
        """
        StreamHandler.__init__(self)
        self.topic = topic
        self._dlxKafkaBroker = DlxKafkaBroker(bootstrap_servers)


    def emit(self, record):
        """
        Management of msg emmition from the logging system

        Args:
            record ([type]): Record
        """
        if record.name == 'kafka':
            return
        msg = self.format(record)
        self._dlxKafkaBroker.send(msg, self.topic)
    
