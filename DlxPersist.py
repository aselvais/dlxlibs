"""
Generic class for persisting data in JSON format in the file system.
You can use that to "cache" data in files (write and read/retreive).
"""
import decimal, json, re
from dlxlibs.DlxLogger import DlxLogger

logger = DlxLogger().get_logger()


class DecimalEncoder(json.JSONEncoder):
        
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        try:
            return o.toString()
        except:
            pass            
        return super(DecimalEncoder, self).default(o)


class DlxPersist():
    """See file description"""

    """The data foming from another Python module/class we need to persist"""
    _data = None


    def __init__(self, _data = ""):
        """
        Initialization and put data in the class scope

        Args:
            _data (Any): The data foming from another Python module/class we need to persist
        """
        self._data = _data


    def write(self, path: str = "", content: str = ""):
        """
        Write the self.data (or the data passed as content) in the path

        Args:
            path (str): Full path of the file where we want to write the JSON data. Defaults to "".
            content (Any, optional): Data we want to persist; if empty string we use self._data. Defaults to "".
        """
        logger.debug(f"DlxPersist.write({path})")
        if content == "":
            content = self._data
        try:
            json.dump(obj=content, fp=open(path,"w"), indent="\t", ensure_ascii=True, cls=DecimalEncoder)
        except Exception as e:
            logger.error(f"DlxPersist.write({path}, {content})")
            logger.error(e)


    def read(self, path: str = ""):
        """
        Read data from a JSON file and decrypt it in self._data

        Args:
            path (str): The full path of the file. Defaults to "".

        Returns:
            Any: None if error; or the Python list/dict/string from the JSON file
        """
        logger.debug(f"DlxPersist.read({path})")
        try:
            self._data = json.load(open(path,"r"))
            return self._data
        except Exception as e:
            logger.error(f"DlxPersist.read({path})")
            logger.error(e)
            return None
