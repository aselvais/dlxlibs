"""
Generic class for persisting data in JSON format in the file system.
You can use that to "cache" data in files (write and read/retreive).
"""
import decimal, json, os, time
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
    _data_old = None
    _json_data_str = None
    _json_data_md5 = None
    _json_data_md5_old = None
    _versioning = False
    _has_changed = False


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
            self._compute_md5_hash()


    def _compute_md5_hash(self):
        """[summary]
        """
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
        
        if self._versioning is True:
            try:
                f = open(f"{path}.md5", "r")
                self._json_data_md5_old = f.read()
            except:
                pass
            if self._json_data_md5_old != self._json_data_md5:
                ts = time.time()
                try:
                    # read old data
                    self._data_old = json.load(open(path, "r"))
                    # move old files around
                    os.rename(path, f"{path}.{ts}")
                    self._has_changed = True
                except Exception as e:
                    logger.error(f"DlxPersist.load({path}, {content})")
                    logger.error(e)


        if content != "":
            self.set_data(content)
        try:
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
    

    def get_compared_data_version(self):
        new = self._data['columns_0']
        old = self._data_old['columns_0']
        r = {}

        for i in old:
            kk = f'{i[0]}|{i[1]}|{i[2]}'
            try: r[kk]
            except: r[kk] = {}
            r[kk]['old'] = i
            r[kk]['different'] = True

        for i in new:
            kk = f'{i[0]}|{i[1]}|{i[2]}'
            try: r[kk]
            except: r[kk] = {}
            r[kk]['new'] = i
            r[kk]['different'] = True
            try:
                if r[kk]['new'] == r[kk]['old']:
                    r[kk]['different'] = False
            except:
                pass

        return r

