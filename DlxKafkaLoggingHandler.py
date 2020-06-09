from logging import StreamHandler
from dlxlibs.DlxKafkaBroker import DlxKafkaBroker

class DlxKafkaLoggingHandler(StreamHandler):
    """
    Logging handler for Kafka streaming
    """


    def __init__(self, bootstrap_servers, topic):
        """
        Init the kafka handler

        :param bootstrap_servers: Kafka servers to use
        :param topic: Topic name
        """
        StreamHandler.__init__(self)
        self.topic = topic
        self._dlxKafkaBroker = DlxKafkaBroker(bootstrap_servers)


    def emit(self, record):
        """
        Management of msg emmition from the logging system

        :param record: Record
        """
        if record.name == 'kafka':
            return
        msg = self.format(record)
        self._dlxKafkaBroker.send(msg, self.topic)
    
