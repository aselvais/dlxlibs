"""
Generic class for connecting to sFTP from spark.

You will have to make sure the following jars are available:
    - spark-sftp_2.11-1.1.3.jar
    - sftp.client-1.0.3.jar
    - jsch-0.1.53.jar
"""
from pyspark import SparkContext, SQLContext


class DlxSparkSftp:
    """
    Initialize the class and some required parameters.

    Args:
        host (str, optional): SFTP Host. Defaults to "".
        username (str, optional): SFTP Server Username. Defaults to "".
        password (str, optional): SFTP Server Password. Defaults to "".
        port (str, optional): port: Port in which SFTP server is running. Defaults to 22.
        file_type (str, optional): Type of the file. Supported types are csv, txt, json, avro and parquet. Defaults to "csv".
        delimiter (str, optional): Set the field delimiter. Applicable only for csv fileType. Defaults to ",".
        quote (str, optional): Set the quote character. Applicable only for csv fileType. Defaults to "\"".
        escape (str, optional): Set the escape character. Applicable only for csv fileType. Defaults to "\\".
        multiLine (str, optional): Set the multiline. Applicable only for csv fileType. Defaults to "true".
        infer_schema (str, optional): InferSchema from the file content. Currently applicable only for csv fileType. Defaults to "false".
        header (str, optional): Applicable only for csv fileType. Is the first row in CSV file is header. Defaults to "true".
        pem (str, optional): Location of PEM file. Either pem or password has to be specified. Defaults to "password".
        pemPassphrase (str, optional): Passphrase for PEM file. Defaults to "".
        codec (str, optional):  Applicable only for csv fileType. Compression codec to use when saving to file.
                                Should be the fully qualified name of a class implementing
                                org.apache.hadoop.io.compress.CompressionCodec or one of case-insensitive
                                shorten names (bzip2, gzip, lz4, and snappy). Defaults to no compression
                                when a codec is not specified.
    """

    _sc = None
    _sqlContext = None
    _df = None
    _host = ""
    _username = ""
    _password = ""
    _port = ""
    _file_type = ""
    _delimiter = ""
    _quote = ""
    _escape = ""
    _multiLine = ""
    _infer_schema = ""
    _header = ""
    _file_path = ""
    _pem = ""
    _pem_passphrase = ""
    _codec = ""

    def __init__(self, host="", username="", password="", port='22', file_type="csv", delimiter=",", quote="\"", escape="\\", multiLine="true", infer_schema="false", header="true", pem="password", pem_passphrase="", codec=""):
        """
        Initialize the class and some required parameters.

        Args:
            host (str, optional): SFTP Host. Defaults to "".
            username (str, optional): SFTP Server Username. Defaults to "".
            password (str, optional): SFTP Server Password. Defaults to "".
            port (str, optional): port: Port in which SFTP server is running. Defaults to 22.
            file_type (str, optional): Type of the file. Supported types are csv, txt, json, avro and parquet. Defaults to "csv".
            delimiter (str, optional): Set the field delimiter. Applicable only for csv fileType. Defaults to ",".
            quote (str, optional): Set the quote character. Applicable only for csv fileType. Defaults to "\"".
            escape (str, optional): Set the escape character. Applicable only for csv fileType. Defaults to "\\".
            multiLine (str, optional): Set the multiline. Applicable only for csv fileType. Defaults to "true".
            infer_schema (str, optional): InferSchema from the file content. Currently applicable only for csv fileType. Defaults to "false".
            header (str, optional): Applicable only for csv fileType. Is the first row in CSV file is header. Defaults to "true".
            pem (str, optional): Location of PEM file. Either pem or password has to be specified. Defaults to "password".
            pemPassphrase (str, optional): Passphrase for PEM file. Defaults to "".
            codec (str, optional):  Applicable only for csv fileType. Compression codec to use when saving to file.
                                    Should be the fully qualified name of a class implementing
                                    org.apache.hadoop.io.compress.CompressionCodec or one of case-insensitive
                                    shorten names (bzip2, gzip, lz4, and snappy). Defaults to no compression
                                    when a codec is not specified.
        """
        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._file_type = file_type
        self._delimiter = delimiter
        self._quote = quote
        self._escape = escape
        self._multiLine = multiLine
        self._infer_schema = infer_schema
        self._header = header
        self._pem = pem
        self._pem_passphrase = pem_passphrase
        self._codec = codec

    def connect(self):
        """
        Connect to spark
        """
        self._sc = SparkContext().getOrCreate()
        self._sqlContext = SQLContext(self._sc)

    def get_file(self, file_path="", fileschemas=[], fixed_width_data=[]):
        """
        Get the file from the remote server and store the result in
        a spark dataframe (self._df)

        Args:
            file_path (str, optional): Full path to the file. Defaults to "".
            fileschemas (list, optional): Only useful for fixed width files, contains the schema. Defaults to [].
            fixed_width_data (list, optional): Only used for fixed width, contains the col width definitions. Defaults to [].
        """
        self._file_path = file_path
        df = self._sqlContext\
            .read\
            .format("com.springml.spark.sftp")\
            .option("host", self._host)\
            .option("username", self._username)\
            .option("password", self._password)\
            .option("port", self._port)\
            .option("fileType", self._file_type)\
            .option("delimiter", self._delimiter)\
            .option("quote", self._quote)\
            .option("escape", self._escape)\
            .option("multiLine", self._multiLine)\
            .option("inferSchema", self._infer_schema)\
            .option("header", self._header)\
            .load(self._file_path)
        # .option("pem", self._pem)\
        # .option("pemPassphrase", self._pem_passphrase)\
        # .option("codec", self._codec)\
        if len(fileschemas) == 0:
            self._df = df
        else:
            argss = []
            for ii in range(len(fileschemas)):
                argss.append(df.value.substr(int(fixed_width_data[ii][0]), int(fixed_width_data[ii][1])).alias(fileschemas[ii][2]))
            ddf = df.select(argss)
            self._df = ddf

    def show_df(self):
        """
        Show the Spark dataframe (for debug usually)
        """
        self._df.show()

    def end(self):
        """
        Close the spark session
        """
        self._sc.stop()
