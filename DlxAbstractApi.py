"""
Abstraction methods and tools for interacting 
with JSON REST APIs
"""
import requests
import json, sys, traceback
from dlxlibs.DlxLogger import DlxLogger
logger = DlxLogger(handlers="f").get_logger()


class DlxAbstractApi():
    """
    Abstraction methods and tools for interacting 
    with JSON REST APIs

    Returns:
        [type]: [description]
    """

    def get_json_response(self, url="", headers={}, payload={}, method="GET"):
        """
        Returns the JSON response data from an API call

        Args:
            url (str, optional): The full URL of the API. Defaults to "".
            headers (dict, optional): The headers to push to the API. Defaults to {}.
            payload (dict, optional): The body/payload. Defaults to {}.
            method (str, optional): The method to use GET|POST. Defaults to "GET".

        Returns:
            dict: The response body as a Python dictionary
        """
        logger.debug({"method": method, "url": url, "headers": headers, "data": payload})
        try:
            _response = requests.request(method, url, headers=headers, data=payload).json()
            logger.debug(_response)
            return _response
        except Exception as e:
            exc_info = sys.exc_info()
            return (''.join(traceback.format_exception(*exc_info)))


