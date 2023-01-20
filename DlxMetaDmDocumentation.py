"""
This class is used to populate the "lake_p01_snapshots" documentation from the metadatamanager into the entity
equivalent within Hue for both tables and fields. This script uses both the metadatamanger API to grab 
documentation as well as the Cloudera Navigator API to update the documentation within Hue.
"""
from dlxlibs.DlxLogger import DlxLogger
from dlxlibs.DlxMetadataManagerApi import DlxMetadataManagerApi
from dlxlibs.DlxClouderaNavigatorApi import DlxClouderaNavigatorApi
logger = DlxLogger(handlers="f").get_logger()


class DlxMetaDmDocumentation(DlxMetadataManagerApi, DlxClouderaNavigatorApi):
    """
    This class is used to populate the "lake_p01_snapshots" documentation from the metadatamanager into the entity
    equivalent within Hue for both tables and fields. This script uses both the metadatamanger API to grab 
    documentation as well as the Cloudera Navigator API to update the documentation within Hue.

    Returns:
        [type]: [description]
    """

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
