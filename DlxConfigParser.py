"""
\defgroup General
Class for parsing the generic config file.
The config file (if present) is used to pass config parameters to the
DLXlibraries. For example, configuring the logger.

The configuration file name has to be in the root directory of the project and named:
 - dlxconfig-{end}.json
where {env} is the environment name (dev | stage | prod)
"""
import os, sys, json
from pathlib import Path
try:
    _rootpath = os.path.dirname(os.path.abspath(__file__)) + '/..'
except:
    _rootpath = os.getcwd()
sys.path.append(_rootpath)



class DlxConfigParser:
    """
    Class parsing the (optional) configuration file for the DLX modules.

    Example usage:
        _dlxConfigParser = DlxConfigParser()
        config = _dlxConfigParser.get_config("DlxLogger")
    """

    _config = None
    _config_file_name = 'dlxconfig'
    _config_fullpath = None
    _file = None


    def __init__(self, env="dev"):
        """
        Class parsing the (optional) configuration file for the DLX modules.

        Example usage:
            _dlxConfigParser = DlxConfigParser()
            config = _dlxConfigParser.get_config("DlxLogger")

        Args:
            env (str, optional): Part of the log file defining the env (dev|stage|prod). Defaults to "dev".
        """
        self._config_fullpath = os.path.dirname(os.path.realpath(__file__)) + "//..//" + self._config_file_name + '-' + env + '.json'
        self._log(self._config_fullpath)
        self._file = Path(self._config_fullpath)
        if self._file.is_file():
            self._parse_config_file()


    def _log(self, msg):
        """
        Temporary message logger for this class

        Args:
            msg (str): Message to log
        """
        #print(msg)
        pass


    def _parse_config_file(self):
        """
        Parse the JSON config file and stores the result in self._config
        """
        try:
            with open(self._config_fullpath) as f:
                self._config = json.load(f)
        except:
            self._log('Error parsing JSON config file')


    def get_config(self, module_name="DlxLogger"):
        """
        Returns the part of the config file specific to a module (name passed as arg)

        Args:
            module_name (str, optional): Name of the module. Defaults to "DlxLogger".

        Returns:
            Dict: Dictionnary containing the config parameters
        """
        try:
            return self._config[module_name]
        except:
            return None

