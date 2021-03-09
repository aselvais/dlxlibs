"""
\defgroup Logging
Kafka broker used by the Kafka Handler class.
It contains the configuration for connecting to Kafka.
Important: You will need to setup the Kerberos authentication to be able to
send data to Kafka.
"""
import os, sys, ssl, socket
from kafka import KafkaProducer
try:
    _rootpath = os.path.dirname(os.path.abspath(__file__)) + '/..'
except:
    _rootpath = os.getcwd()
sys.path.append(_rootpath)


_ = os.environ["KRB5_CLIENT_KTNAME"] = "rundeckadmin.keytab"
ssl_context = ssl.create_default_context(cafile='/etc/pki/tls/certs/ca-bundle.crt')
ssl_context.options |= (ssl.PROTOCOL_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION)


class DlxKafkaBroker(object):

    def __init__(self, bootstrap_servers, json=False):
        """
        Constructor initializing the Kafka connection

        Args:
            bootstrap_servers ([type]): List of kafka server to use
            json (bool, optional): Boolean (default: False), should we use JSON mode. Defaults to False.
        """
        self.json = json
        prms = {
                'bootstrap_servers': bootstrap_servers,
                'api_version': None,
                'security_protocol': 'SASL_SSL',
                'sasl_mechanism': 'GSSAPI',
                'sasl_kerberos_service_name': 'kafka',
                'ssl_password': "changeit",
                'ssl_keyfile': "/opt/cloudera/security/pki/jks/jssecacerts-java-1.8.jks",
                'ssl_context': ssl_context,
                'acks': 1,
                'retries': 1,
                'api_version_auto_timeout_ms': 6000,
                'client_id': socket.gethostname(),
                'receive_buffer_bytes': 1024*10,
                'send_buffer_bytes': 1024*10
        }
        try:
            self.producer = KafkaProducer(**prms)
        except Exception as e:
            print('Can not connect to Kafka')


    def send(self, data, topic):
        """
        Send message to Kafka

        Args:
            data ([type]): Data to send as a kafka message
            topic ([type]): Topic to write to
        """
        if self.json:
            result = self.producer.send(topic, key=b'log', value=data)
        else:
            result = self.producer.send(topic, data.encode())
        try:
            self.producer.flush()
        except:
            pass

