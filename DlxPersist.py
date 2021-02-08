"""
Generic class for persisting data in JSON format in the file system.
You can use that to "cache" data in files (write and read/retreive).
"""
import decimal, json, re
from dlxlibs.DlxLogger import DlxLogger
from hashlib import md5

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
    _json_data_str = None
    _json_data_md5 = None
    _versioning = False


    def __init__(self, _data = "", versioning = False):
        """
        Initialization and put data in the class scope

        Args:
            _data (Any): The data foming from another Python module/class we need to persist
            versioning (bool, optional): [description]. Defaults to False.
        """
        self._versioning = versioning
        self.set_data(_data)


    def set_data(self, _data=""):
        """[summary]

        Args:
            _data (str, optional): [description]. Defaults to "".
        """
        self._data = _data
        self._data_to_json()
        if self._versioning is True:
            self._json_data_md5 = md5(self._json_data_str.encode()).hexdigest()
    

    def _data_to_json(self):
        """[summary]
        """
        try:
            self._json_data_str = json.dumps(obj=self._data, indent="\t", ensure_ascii=True, cls=DecimalEncoder)
        except Exception as e:
            logger.error(f"error converting to JSON in DlxPersist._data_to_json()")
            logger.error(e)


    def write(self, path: str = "", content: str = ""):
        """
        Write the self.data (or the data passed as content) in the path

        Args:
            path (str): Full path of the file where we want to write the JSON data. Defaults to "".
            content (Any, optional): Data we want to persist; if empty string we use self._data. Defaults to "".
        """
        logger.debug(f"DlxPersist.write({path})")
        if content != "":
            self.set_data(content)
        try:
            # json.dump(obj=content, fp=open(path,"w"), indent="\t", ensure_ascii=True, cls=DecimalEncoder)
            f = open(path, "w")
            f.write(self._json_data_str)
            f.close()
            if self._versioning is True:
                f = open(f"{path}.md5", "w")
                f.write(self._json_data_md5)
                f.close()
    
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
            self.set_data(json.load(open(path,"r")))
            return self._data
        except Exception as e:
            logger.error(f"DlxPersist.read({path})")
            logger.error(e)
            return None
