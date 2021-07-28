"""
This class is used to populate the "lake_p01_snapshots" documentation from the metadatamanager into the entity
equivalent within Hue for both tables and fields. This script uses both the metadatamanger API to grab 
documentation as well as the Cloudera Navigator API to update the documentation within Hue.
"""
import requests, urllib, json
from dlxlibs.DlxLogger import DlxLogger
logger = DlxLogger(handlers="f").get_logger()


class DlxMetaDmDocumentation():
    """
    This class is used to populate the "lake_p01_snapshots" documentation from the metadatamanager into the entity
    equivalent within Hue for both tables and fields. This script uses both the metadatamanger API to grab 
    documentation as well as the Cloudera Navigator API to update the documentation within Hue.

    Returns:
        [type]: [description]
    """
    
    url_base_cn = "https://ala09012.edp-prod.deluxe.com:7187/api/v14"
    cn_authtoken = "dDQ0ODA1NjpDb21ldElzQ3V0ZTEhISE="

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


    def cn_get_all_entity_relations(self, entity_id):
        """[summary]

        Args:
            entity_id ([type]): [description]

        Returns:
            [type]: [description]
        """
        url = self.url_base_cn + f"/relations?entityIds={entity_id}&types=PARENT_CHILD&roles=PARENT"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.cn_authtoken}',
            'Cookie': 'NAVIGATOR_JSESSIONID_7187=node0tc6f4uiu6pnj3sbvs0h4f7we210.node0'
        }
        return self.get_json_response(url, headers)


    def cn_get_entity_info(self, entity_id):
        """[summary]

        Args:
            entity_id ([type]): [description]

        Returns:
            [type]: [description]
        """
        url = self.url_base_cn + f"/entities/{entity_id}"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.cn_authtoken}',
            'Cookie': 'NAVIGATOR_JSESSIONID_7187=node016kmaqur2849fvk5fn57qamzm211.node0'
        }
        return self.get_json_response(url, headers)


    def cn_update_entity_description(self, entity_id, description):
        """[summary]

        Args:
            entity_id ([type]): [description]
            description ([type]): [description]
        """
        entity_info = self.cn_get_entity_info(entity_id)
        customProperties = entity_info["customProperties"]
        name = entity_info["name"]
        properties = entity_info["properties"]
        url = self.url_base_cn + f"/entities/{entity_id}"
        payload = json.dumps({
            "customProperties": customProperties,
            "name": name,
            "description": description,
            "tags": None,
            "properties": properties
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {self.cn_authtoken}'
        }
        self.get_json_response(url, headers, payload, "PUT")


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


    def run_process(self, lake_entity_id = "9072149"):
        """[summary]

        Args:
            lake_entity_id (str, optional): [description]. Defaults to "9072149".
        """
        table_entity_relations = self.cn_get_all_entity_relations(lake_entity_id)
        mm_schemas = self.mm_get_all_schemas()

        for i in table_entity_relations:
            table_entity_id = i["children"]["entityIds"][0]
            table_entity_info = self.cn_get_entity_info(table_entity_id)

            if table_entity_info["originalName"].count("__") == 2:
                hue_source_name = table_entity_info["originalName"].split("__")[0]
                hue_schema_name = table_entity_info["originalName"].split("__")[1]
                hue_table_name = table_entity_info["originalName"].split("__")[2]
            else:
                continue

            logger.info(f"""source name:      {hue_source_name}
schema name:      {hue_schema_name}
table name:       {hue_table_name} 
table_entity_id:  {table_entity_id}""")
            # logger.debug(table_entity_info)

            for s in mm_schemas:
                if "schema" in s:
                    if s["schema"].strip().lower() == hue_schema_name.strip().lower():
                        schemas_idh = s["idh"] # database_idh = s["databases_idh"]
                        mm_tables_in_schema = self.mm_get_tables_for_schema_idh(schemas_idh)

                        for t in mm_tables_in_schema:
                            if "name" in t:
                                if t["name"].strip().lower() == hue_table_name.strip().lower():  # [TODO: add regex]
                                    table_idh = t["idh"]
                                    table_description = t["documentation"]

                                    if table_description != "":
                                        logger.warn("updating description for table: " + table_entity_id)
                                        self.cn_update_entity_description(table_entity_id, table_description)

                                        field_entity_relations = self.cn_get_all_entity_relations(table_entity_id)
                                        mm_fields_in_table = self.mm_get_fields_for_table_idh(table_idh)

                                        for f in field_entity_relations:
                                            field_entity_id = f["children"]["entityIds"][0]
                                            field_entity_info = self.cn_get_entity_info(field_entity_id)
                                            hue_field_name = field_entity_info["originalName"]

                                            for mm_f in mm_fields_in_table:
                                                if mm_f["name"].strip().lower() == hue_field_name.strip().lower():
                                                    field_description = mm_f["documentation"]

                                                    if field_description != "":
                                                        logger.warn("updating description for field: " + field_entity_id)
                                                        self.cn_update_entity_description(field_entity_id, field_description)
