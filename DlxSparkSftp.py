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
        host (str, optional): sFTP Host. Defaults to "".
        username (str, optional): sFTP Username. Defaults to "".
        password (str, optional): sFTP password. Defaults to "".
        file_type (str, optional): File type. Defaults to "csv".
        delimiter (str, optional): Delimiter. Defaults to "|".
        quote (str, optional): Are string in quotes. Defaults to "\"".
        escape (str, optional): Escaping character. Defaults to "\\".
        multiLine (str, optional): Is multiline. Defaults to "true".
        infer_schema (str, optional): Do we infer the schema. Defaults to "false".
        header (str, optional): Does the file have a header. Defaults to "true".
    """

    _sc = None
    _sqlContext = None
    _df = None
    _host = ""
    _username = ""
    _password = ""
    _file_type = ""
    _delimiter = ""
    _quote = ""
    _escape = ""
    _multiLine = ""
    _infer_schema = ""
    _header = ""
    _file_path = ""

    def __init__(self, host="", username="", password="", file_type="csv", delimiter=",", quote="\"", escape="\\", multiLine="true", infer_schema="false", header="true"):
        """
        Initialize the class and some required parameters.

        Args:
            host (str, optional): sFTP Host. Defaults to "".
            username (str, optional): sFTP Username. Defaults to "".
            password (str, optional): sFTP password. Defaults to "".
            file_type (str, optional): File type. Defaults to "csv".
            delimiter (str, optional): Delimiter. Defaults to ",".
            quote (str, optional): Are string in quotes. Defaults to "\"".
            escape (str, optional): Escaping character. Defaults to "\\".
            multiLine (str, optional): Is multiline. Defaults to "true".
            infer_schema (str, optional): Do we infer the schema. Defaults to "false".
            header (str, optional): Does the file have a header. Defaults to "true".
        """
        self._host = host
        self._username = username
        self._password = password
        self._file_type = file_type
        self._delimiter = delimiter
        self._quote = quote
        self._escape = escape
        self._multiLine = multiLine
        self._infer_schema = infer_schema
        self._header = header

    def connect(self):
        """
        Connect to spark
        """
        self._sc = SparkContext().getOrCreate()
        self._sqlContext = SQLContext(self._sc)

    def get_file(self, file_path=""):
        """
        Get the file from the remote server and store the result in
        a spark dataframe (self._df)

        Args:
            file_path (str, optional): Full path to the file. Defaults to "".
        """
        self._file_path = file_path
        self._df = self._sqlContext\
            .read\
            .format("com.springml.spark.sftp")\
            .option("host", self._host)\
            .option("username", self._username)\
            .option("password", self._password)\
            .option("fileType", self._file_type)\
            .option("delimiter", self._delimiter)\
            .option("quote", self._quote)\
            .option("escape", self._escape)\
            .option("multiLine", self._multiLine)\
            .option("inferSchema", self._infer_schema)\
            .option("header", self._header)\
            .load(self._file_path)

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
