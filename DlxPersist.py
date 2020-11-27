import json

class DlxPersist():

    _data = None


    def __init__(self, _data) -> None:
        self._data = _data


    def write(self, path: str = "", content: str = ""):
        if content == "":
            content = self._data
        json.dump(content, open(path,"w"))


    def read(self, path: str = ""):
        try:
            self._data = json.load(open(path,"r"))
            return self._data
        except:
            return None
            
