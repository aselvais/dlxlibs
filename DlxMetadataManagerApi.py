"""
This class is used to populate the "lake_p01_snapshots" documentation from the metadatamanager into the entity
equivalent within Hue for both tables and fields. This script uses both the metadatamanger API to grab 
documentation as well as the Cloudera Navigator API to update the documentation within Hue.
"""
import urllib, json
from dlxlibs.DlxLogger import DlxLogger
from dlxlibs.DlxAbstractApi import DlxAbstractApi
logger = DlxLogger(handlers="f").get_logger()


class DlxMetadataManagerApi(DlxAbstractApi):
    """
    This class is used to populate the "lake_p01_snapshots" documentation from the metadatamanager into the entity
    equivalent within Hue for both tables and fields. This script uses both the metadatamanger API to grab 
    documentation as well as the Cloudera Navigator API to update the documentation within Hue.

    Returns:
        [type]: [description]
    """

    url_base_metadm = "http://ala01095.deluxe.com:8089/api"
    metadm_accesstoken = "kfLGpKTvVXrEARIp8T0q2D7R8R1dpCLEr4UC9Onz2wvnod2bGDNdpIxUaWeIN7Rw"

    def get_mm_url(self, entity="fields", filter=""):
        """[summary]

        Args:
            entity (str, optional): [description]. Defaults to "fields".
            filter (str, optional): [description]. Defaults to "".

        Returns:
            [type]: [description]
        """
        url = self.url_base_metadm + f"/{entity}?"
        if filter != "":
            filter = urllib.parse.quote(json.dumps(filter))
            url = url + "filter={filter}&"
        url = url + "access_token={self.metadm_accesstoken}"
        return url


    def mm_get_all_schemas(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.get_json_response(self.get_mm_url("schemas"))


    def mm_get_fields_for_table_idh(self, idh):
        """[summary]

        Args:
            idh ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.get_json_response(self.get_mm_url("fields", {"where":{"tables_idh":idh}}))


    def mm_get_tables_for_schema_idh(self, idh):
        """[summary]

        Args:
            idh ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.get_json_response(self.get_mm_url("tables", {"where":{"schemas_idh":idh}}))


    def mm_get_databases_for_database_idh(self, idh):
        """[summary]

        Args:
            idh ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.get_json_response(self.get_mm_url("databases", {"where":{"idh":idh}}))

