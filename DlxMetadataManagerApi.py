"""
Generic methods and tools for interacting with the Metadata Manager API
"""
import urllib, json, os
from dlxlibs.DlxLogger import DlxLogger
from dlxlibs.DlxAbstractApi import DlxAbstractApi
logger = DlxLogger(handlers="f").get_logger()

try:
    _key = os.environ["KEY"]
except:
    logger.error('The key is missing, please generate a key and place it in the os KEY env var.')

class DlxMetadataManagerApi(DlxAbstractApi):
    """
    Generic methods and tools for interacting with the Metadata Manager API

    Returns:
        [type]: [description]
    """

    url_base_metadm = "http://ala09006.edp-prod.deluxe.com:8089/api"
    metadm_accesstoken = "7UL3JiC99haQhHfZ0iVj5QZ7fKnOGukXBZloHnmXe4TXKRLJDvqLtXVB0HEIXVZl"

    def get_mm_url(self, entity="fields", filter=""):
        """Returns the URL to query for the metadata manager

        Args:
            entity (str, optional): The collection name in MongoDB. Defaults to "fields".
            filter (dict, optional): The filter as a python dictionary. Defaults to "".

        Returns:
            [type]: [description]
        """
        url = self.url_base_metadm + f"/{entity}?"
        if filter != "":
            filter = urllib.parse.quote(json.dumps(filter))
            url = url + f"filter={filter}&"
        url = url + f"access_token={self.metadm_accesstoken}"
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


    def mm_get_tables_where(self, query={}):
        """[summary]

        Args:
            where (dict, optional): [description]. Defaults to {}.

        Returns:
            [type]: [description]
        """
        return self.get_json_response(self.get_mm_url("tables", query))


    def mm_get_databases_for_database_idh(self, idh):
        """[summary]

        Args:
            idh ([type]): [description]

        Returns:
            [type]: [description]
        """
        return self.get_json_response(self.get_mm_url("databases", {"where":{"idh":idh}}))


    def mm_get_gettableflatfields_for_table_idh(self, idh):
        """[summary]

        Args:
            idh ([type]): [description]

        Returns:
            [type]: [description]
        """
        url = self.url_base_metadm + f"/view4streamsets/gettableflatfields?idh={urllib.parse.quote(idh)}&ks={urllib.parse.quote(_key)}&access_token={self.metadm_accesstoken}"
        r = self.get_json_response(url)
        runtimeParameters = {}
        try:
            idx = 0
            for field in r["data"]:
                if idx == 0:
                    runtimeParameters = {
                        "connection_string": field["databases_jdbc_connection_str"],
                        "username": field["databases_username"],
                        "password" : field["databases_password"],
                        "system" : field["system_name"],
                        "origin" : field["origin_name"],
                        "database" : field["database_name"],
                        "schema": field["schema_name"],
                        "table": field["table_name"],
                        "database_storageengine": field["database_storageengine"],
                        "destination_db": f'{field["database_name"]}__{field["schema_name"]}__{field["table_name"]}'.lower().replace(' ', '_'),
                        # TODO: fix this !!!!!!!!!!!!
                        "lake_name": field["schema_destination_lake"] + '_transformer',
                        "partition_column": "",
                        "mm_columns_info": {},
                        "offset_column_name": ""
                    }
                try:
                    ob = {
                        "_id":          field["_id"] if "_id" in field else "",
                        "idh":          field["idh"] if "idh" in field else "",
                        "name":         field["name"] if "name" in field else "",
                        "datatype":     field["datatype"] if "datatype" in field else "",
                        "tables_idh":   field["tables_idh"] if "tables_idh" in field else "",
                        "to_lower":     field["to_lower"] if "to_lower" in field else "",
                        "is_cdc_field": field["is_cdc_field"] if "is_cdc_field" in field else 0,
                        "is_gdpr":      field["is_gdpr"] if "is_gdpr" in field else 0,
                        "is_pii":       field["is_pii"] if "is_pii" in field else 0,
                        "is_pci":       field["is_pci"] if "is_pci" in field else 0,
                        "is_pk":        field["is_pk"] if "is_pk" in field else 0,
                        "is_fk":        field["is_fk"] if "is_fk" in field else 0,
                        "is_obfuscated":field["is_obfuscated"] if "is_obfuscated" in field else 0,
                        "is_partition": field["is_partition"] if "is_partition" in field else 0,
                    }
                    runtimeParameters["mm_columns_info"][ob["name"].lower()] = ob
                    if ob["is_partition"] == 1:
                        runtimeParameters["partition_column"] = ob["name"]
                    if ob["is_pk"] == 1 and runtimeParameters["partition_column"] == "":
                        runtimeParameters["partition_column"] = ob["name"]
                    if ob["is_pk"] == 1:
                        runtimeParameters["offset_column_name"] = ob["name"]
                except Exception as ee:
                    logger.error(ee)
                idx = idx + 1
            if runtimeParameters["offset_column_name"] == "":
                if runtimeParameters["partition_column"] != "":
                    runtimeParameters["offset_column_name"] = runtimeParameters["partition_column"]
                else:
                    runtimeParameters["offset_column_name"] = r["data"][0]["name"]
        except:
            pass

        return runtimeParameters

