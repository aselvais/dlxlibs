"""

"""
import requests
from dlxlibs.DlxLogger import DlxLogger
logger = DlxLogger(handlers="f").get_logger()


class DlxAbstractApi():
    """

    Returns:
        [type]: [description]
    """

    def get_json_response(self, url="", headers={}, payload={}, method="GET"):
        """[summary]

        Args:
            url (str, optional): [description]. Defaults to "".
            headers (dict, optional): [description]. Defaults to {}.
            payload (dict, optional): [description]. Defaults to {}.
            method (str, optional): [description]. Defaults to "GET".

        Returns:
            [type]: [description]
        """
        logger.debug({"method": method, "url": url, "headers": headers, "data": payload})
        _response = requests.request(method, url, headers=headers, data=payload).json()
        logger.debug(_response)
        return _response


