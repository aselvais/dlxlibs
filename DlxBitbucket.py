"""
\defgroup Version control
Abstraction layer to access Bitbucket from Python. 
"""
from dlxlibs.DlxLogger import DlxLogger
from dlxlibs.DlxBash import DlxBash

_logger = DlxLogger().get_logger()


class DlxBitbucket(DlxBash):

    _username = ""
    _password = ""

    def __init__(self):
        """
        Initialization
        """
        pass

    def set_credentials(self, username="", password=""):
        """

        :param username:
        :param password:
        :return:
        """
        self._username = username
        self._password = password

    def init(self):
        pass

    def status(self):
        """

        :return:
        """
        _logger.debug("Executing git status")
        return self._execute_command("git status")

    def add_all(self):
        """

        :return:
        """
        _logger.debug("Executing git add *")
        return self._execute_command("git add *")

    def commit(self, msg="no commit msg"):
        """

        :return:
        """
        _logger.debug("Executing git commit -m \"" + msg + "\"")
        return self._execute_command("git commit -m \"" + msg + "\"")

    def pull(self):
        """

        :return:
        """
        _logger.debug("Executing git pull")
        return self._execute_command("git pull")

    def push(self):
        """

        :return:
        """
        _logger.debug("Executing git add *")
        # git push https://YOUR_GIT_USERNAME@github.com/YOUR_GIT_USERNAME/yourGitFileName.git
        return self._execute_command("git push")

