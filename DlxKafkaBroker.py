from kafka import KafkaProducer
import json
import os
import ssl
import socket

_ = os.environ["KRB5_CLIENT_KTNAME"] = "t442512.keytab"
ssl_context = ssl.create_default_context(cafile='/etc/pki/tls/certs/ca-bundle.crt')
ssl_context.options |= (ssl.PROTOCOL_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION)


class DlxKafkaBroker(object):

    def __init__(self, bootstrap_servers, json=False):
        """
        Constructor initializing the Kafka connection

        :param bootstrap_servers: List of kafka server to use
        :param json: Boolean (default: False), should we use JSON mode
        """
        self.json = json
        prms = {
                #'value_serializer': (lambda v: json.dumps(v).encode('utf-8')),
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
        if not json:
            self.producer = KafkaProducer(**prms)
        else:
            try:
                self.producer = KafkaProducer(**prms)
            except:
                print('Can not connect to Kafka')


    def send(self, data, topic):
        """
        Send message to Kafka

        :param data: Data to send as a kafka message
        :param topic: Topic to write to
        """
        if self.json:
            result = self.producer.send(topic, key=b'log', value=data)
        else:
            result = self.producer.send(topic, data.encode())

