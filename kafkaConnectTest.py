#
# ktutil 
# addent -password -p t442512@DELUXE.COM -k 1 -e RC4-HMAC
# wkt /tmp/keytabs/t442512.keytab
# exit
#
# ------------------------------------------------------------------------------------- #

import os
import socket
import gssapi
import logging
import ssl
import socket
from datetime import datetime as dt
import kafka
from kafka import *
from kafka.errors import *


logging.basicConfig(level=logging.INFO)
_ = os.environ["KRB5_CLIENT_KTNAME"] = "t442512.keytab"
bootstrap_servers = "ala09035.edp-prod.deluxe.com:9093,ala09036.edp-prod.deluxe.com:9093,ala09037.edp-prod.deluxe.com:9093"
KAFKA_TOPIC = str('log-loggers')
ssl_context = ssl.create_default_context(cafile='/etc/pki/tls/certs/ca-bundle.crt')
ssl_context.options |= (ssl.PROTOCOL_TLSv1 | ssl.OP_NO_TLSv1_1 | ssl.OP_NO_TLSv1_2 | ssl.OP_NO_COMPRESSION)

producer = KafkaProducer(
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
    client_id=socket.gethostname(),
    receive_buffer_bytes=1024*10,
    send_buffer_bytes=1024*10
)

producer.config

# Asynchronous by default
future = producer.send('log-loggers', b'raw_bytes')

# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    #logging.exception()
    pass

print('------ END -----')

