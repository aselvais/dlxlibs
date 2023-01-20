"""
Generic methods and tools for interacting with the Cloudera Navigator API
"""
import json
from dlxlibs.DlxLogger import DlxLogger
from dlxlibs.DlxAbstractApi import DlxAbstractApi
logger = DlxLogger(handlers="f").get_logger()


class DlxClouderaNavigatorApi(DlxAbstractApi):
    """
    Generic methods and tools for interacting with the Cloudera Navigator API

    Returns:
        [type]: [description]
    """
    
    url_base_cn = "https://ala09012.edp-prod.deluxe.com:7187/api/v14"
    cn_authtoken = "dDQ0ODA1NjpDb21ldElzQ3V0ZTEhISE="


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

