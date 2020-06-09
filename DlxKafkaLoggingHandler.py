from logging import StreamHandler
import kafka
from kafka import *
from kafka.errors import *
import ssl
import os
import socket

class DlxKafkaLoggingHandler(StreamHandler):
    """
    kh = DlxKafkaLoggingHandler("localhost", 9092, "logs-apps-dlxc-main")
    #OR
    #kh = DlxKafkaLoggingHandler("localhost", 9092, "logs-apps-dlxc-main")

    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    
    logger.addHandler(kh)
    logger.info("The %s boxing wizards jump %s", 5, "quickly")
    logger.debug("The quick brown %s jumps over the lazy %s", "fox",  "dog")
    try:
        import math
        math.exp(1000)
    except:
        logger.exception("Problem with %s", "math.exp")
    """

    _KAFKA_TOPIC = str('log-loggers')

    def __init__(self):
        """
        """
        StreamHandler.__init__(self)

        _ = os.environ["KRB5_CLIENT_KTNAME"] = "t442512.keytab"
        bootstrap_servers = "ala09035.edp-prod.deluxe.com:9093,ala09036.edp-prod.deluxe.com:9093,ala09037.edp-prod.deluxe.com:9093"
        self.KAFKA_TOPIC = str('log-loggers')
        ssl_context = ssl.create_default_context(cafile='/etc/pki/tls/certs/ca-bundle.crt')
        ssl_context.options |= (ssl.PROTOCOL_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION)
        _hostname = socket.gethostname()

        try:
            self.producer  = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                api_version=None,
                security_protocol='SASL_SSL',
                sasl_mechanism='GSSAPI',
                sasl_kerberos_service_name='kafka',
                ssl_password="changeit",
                ssl_keyfile="/opt/cloudera/security/pki/jks/jssecacerts-java-1.8.jks",
                ssl_context=ssl_context,
                acks=1,
                retries=1,
                api_version_auto_timeout_ms=6000,
                client_id=_hostname,
                receive_buffer_bytes=1024*10,
                send_buffer_bytes=1024*10
            )
        except:
            print('Kafka could not connect')


    def emit(self, record):
        """
        """
        #drop kafka logging to avoid infinite recursion
        if record.name == 'kafka':
            return
        msg = self.format(record)
        self.producer.send(self._KAFKA_TOPIC, msg)
        #record_metadata = future.get(timeout=10)
        '''
        try:
            #use default formatting
            future = self.producer.send(self._KAFKA_TOPIC, msg.encode())
            try:
                record_metadata = future.get(timeout=10)
            except KafkaError:
                # Decide what to do if produce request failed...
                #logging.exception()
                pass
        except:
            print('Could not send msg to kafka')
        '''

    '''
    def close(self):
        """
        """
        #self.producer.stop()
        logging.Handler.close(self)
    '''

