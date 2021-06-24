import json
import logging
from datetime import datetime


class Write():
    """

    """
    _type = 'OUTPUT'

    def write(self, *argv):
        """
        """
        vv = [str(datetime.now()), self._type]
        try:
            vv.append(argv[0].get_flat())
        except:
            vv.append(argv)
        print(" - ".join(vv))

    def set_type(self, v):
        """

        Args:
            v ([type]): [description]
        """
        self._type = v


class WriteError(Write):
    """

    Args:
        Write ([type]): [description]
    """

    def __init__(self):
        """[summary]
        """
        super().__init__()
        self.set_type('ERROR')


class Record:
    """

     record.value = 'Hello '                            # Change record root field value to a STRING value
     record.value = { 'V' : 'Hello'}                    # Change record root field value to a MAP value and create an entry
     record.value['X'] = record.value['V'] + ' World'   # Access a MAP entry
     record.value['V'] = 5                              # Modify a MAP entry
     record.value['A'] = [ 'Element 1', 'Element 2' ]   # Create an ARRAY entry
     record.value['B'] = record.value['A'][0]           # Access an ARRAY entry
     record.value['A'][0] = 100                         # Modify an existing ARRAY entry
     record.value['null_int'] = sdc.NULL_INTEGER        # Assign a integer type to a field and value null

     # Check if the field is NULL_INTEGER(Both '==' and 'is' work). If so, assign a value 
     if sdc.getFieldNull(record, '/null_int') == sdc.NULL_INTEGER: 
        record.value['null_int'] = 123

     fieldAttr = record.sdcRecord.get('/value').getAttribute('attr')  # Direct access to the underlying Data Collector Record. Use for read-only operations.

     # Create a new record with map field 
     newRecord = sdc.createRecord(record.sourceId + ':newRecordId')
     newRecord.value = {'field1' : 'val1', 'field2' : 'val2'}
     sdc.output.write(newRecord)

     # Applies if the source uses WHOLE_FILE as data format
     input_stream = record.value['fileRef'].getInputStream()
     try:
       input_stream.read() Process the input stream
     finally:  
       input_stream.close()

     record.attributes['name'] = record.attributes['first_name'] + ' ' + record.attributes['last_name'] # Modify a record header attribute entry

     Get a record header with field names ex. get sourceId and errorCode
     sourceId = record.sourceId
     errorCode = ''
     if record.errorCode:
       errorCode = record.errorCode

    Returns:
        [type]: [description]
    """
    value = None
    attributes = [] # a map of record header attributes.
    #  record.<header name>: get the value of 'header name'.

    def __init__(self, l):
        """[summary]

        Args:
            l ([type]): [description]
        """
        self.value = l

    def get_flat(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return json.dumps(self.value)


class Records:
    """

    """

    NULL_BOOLEAN = None
    NULL_CHAR = None
    NULL_BYTE = None
    NULL_SHORT = None
    NULL_INTEGER = None
    NULL_LONG = None
    NULL_FLOAT = None
    NULL_DOUBLE = None
    NULL_DATE = None
    NULL_DATETIME = None
    NULL_TIME = None
    NULL_DECIMAL = None
    NULL_BYTE_ARRAY = None
    NULL_STRING = None
    NULL_LIST = None
    NULL_MAP = None
    records = [] # array of records to process, depending on Jython processor processing mode it may have 1 record or all the records in the batch.
    output = Write()  # writes a record to processor output
    error = WriteError()  # sends a record to error
    state = [] # dict that is preserved between invocations of this script. Useful for caching bits of data e.g. counters.
    log = logging # use instead of print to send log messages to the log4j log instead of stdout. loglevel is any log4j level: e.g. info, error, warn, trace.

    def getFieldNull(self, record="", field_path='field path'):
        """
        Receive a constant defined above to check if the field is typed 
        field with value null

        Args:
            record (str, optional): [description]. Defaults to "".
            field_path (str, optional): [description]. Defaults to 'field path'.
        """
        pass

    def createRecord(self, recordId=""):
        """
        Creates a new record. Pass a recordId to uniquely identify the record and 
        include enough information to track down the record source.

        Args:
            recordId (str, optional): [description]. Defaults to "".
        """
        pass

    def createMap(self, listMap=""):
        """
        Create a map for use as a field in a record. Pass True to this function 
        to create a list map (ordered map)

        Args:
            listMap (str, optional): [description]. Defaults to "".
        """
        pass

    def createEvent(self, type="", version=""):
        """
        Creates a new event. Create new empty event with standard headers.

        Args:
            type (str, optional): [description]. Defaults to "".
            version (str, optional): [description]. Defaults to "".
        """
        pass

    def toEvent(self, Record=""):
        """
        Send event to event stream Only events created with sdcFunctions.
        createEvent are supported.

        Args:
            Record (str, optional): [description]. Defaults to "".
        """
        pass

    def isPreview(self):
        """
        Determine if pipeline is in preview mode.
        """
        pass

    def userParams(self):
        """
        Dictionary of user-specified keys and values (from UI).
        """
        pass


# ================================================== #

sdc = Records()
