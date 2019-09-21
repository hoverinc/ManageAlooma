import unittest
import pandas as pd

from unittest.mock import patch
from managealooma.consolidations import Consolidations


class TestConsolidations(unittest.TestCase):
    """ Tests the functions that retrieve and manipulate events from the API
    """

    @patch('managealooma.consolidations.Consolidations')
    def setUp(self, consolidations_class):
        """ Set up the consolidation class and mocked API response with the consolidation list

        :param events_class:
        :return: None
        """
        self.consolidations = Consolidations(api=None)
        self.mock_get_consolidations()

    @patch('managealooma.consolidations.Consolidations.get_scheduled_queries')
    def mock_get_consolidations(self, mock_get_consolidations):
        """ Create the mocked consolidation list of dictionaries

        :param mock_get_mapping:
        :return: The mocked consolidation list
        """

        sample_event_list = [{'id': 12345,
                              'schedule': {'cron': '*/30 * * * *'},
                              'start_time': '2019-01-01T00:00:00.00000Z',
                              'name': 'consolidate_my_account_incremental',
                              'docker_img': 'muppet-consolidation',
                              'docker_tag': 'latest',
                              'docker_cmd': 'python scripts/run_consolidation.py -d my_account-q "incremental" -c \'{"all_ri_fields": ["_metadata.@timestamp"], "ri_field": "_metadata.@timestamp", "ri_column": "_metadata.@timestamp"}\'',
                              'is_active': True,
                              'next_run_time': '2019-08-01T00:30:00.00Z',
                              'is_running': False, 'enqueue_time': '2019-08-25T17:37:23.633727Z',
                              'time_limit': 3600,
                              'service_type': 'alooma_utility',
                              'event_type': 'MY_SCHEMA.A_TABLE',
                              'last_success_time': None,
                              'last_run_start_time': '2019-08-01T00:00:00.00Z',
                              'last_run_end_time': '2019-08-01T00:00:02.00Z',
                              'last_run_return_code': None,
                              'consolidation_query': None,
                              'error_message': None,
                              'query_type': 'incremental',
                              'generated_by': None},
                             {'id': 67890,
                              'schedule': {'cron': '*/30 * * * *'},
                              'start_time': '2018-10-24T23:56:02.033150Z',
                              'name': 'consolidate_my_account_incremental',
                              'docker_img': 'muppet-consolidation',
                              'docker_tag': 'latest',
                              'docker_cmd': 'python scripts/run_consolidation.py -d my_account -q "incremental" -c \'{"all_ri_fields": ["_metadata.consolidation"], "ri_field": "_metadata.consolidation"}\'',
                              'is_active': True,
                              'next_run_time': '2019-08-25T18:00:00Z',
                              'is_running': False,
                              'enqueue_time': '2019-08-25T17:35:50.340959Z',
                              'time_limit': 3600,
                              'service_type': 'alooma_utility',
                              'event_type': 'MY_SCHEMA.ANOTHER_TABLE',
                              'last_success_time': '2019-08-25T17:49:40.803583Z',
                              'last_run_start_time': '2019-08-25T17:35:53.161949Z',
                              'last_run_end_time': '2019-08-25T17:49:40.803583Z',
                              'last_run_return_code': 0,
                              'consolidation_query': """MERGE INTO "MY_SCHEMA"."ANOTHER_TABLE"
                                                        USING (SELECT "_METADATA__TIMESTAMP"
                                                                    , "_METADATA__UUID"
                                                                    , "_METADATA_CONSOLIDATION"
                                                                    , "CREATED_AT", "COLUMN_ONE"
                                                                    , "COLUMN_TWO"
                                                                    , "ID"
                                                                    ,"UPDATED_AT"
                                                                    , "XMIN__TEXT__BIGINT"
                                                                 FROM (SELECT "_METADATA__TIMESTAMP"
                                                                            , "_METADATA__UUID"
                                                                            , "_METADATA_CONSOLIDATION"
                                                                            , "CREATED_AT"
                                                                            , "COLUMN_ONE"
                                                                            , "COLUMN_TWO"
                                                                            , "ID"
                                                                            , "UPDATED_AT"
                                                                            , "XMIN__TEXT__BIGINT"
                                                                            , ROW_NUMBER() OVER (PARTITION BY "ID" ORDER BY "_METADATA_CONSOLIDATION" DESC) AS "row_num"
                                                                         FROM "MY_SCHEMA"."ANOTHER_TABLE")
                                                                        WHERE "row_num"=1) "MY_SCHEMA_ANOTHER_TABLE_LOG" 
                                                                           ON "MY_SCHEMA"."ANOTHER_TABLE"."ID"="MY_SCHEMA_ANOTHER_TABLE_LOG"."ID"
                                                                         WHEN MATCHED AND "MY_SCHEMA"."ANOTHER_TABLE"."_METADATA_CONSOLIDATION" < "MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA_CONSOLIDATION"
                                                                         THEN UPDATE SET "_METADATA__TIMESTAMP"="MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA__TIMESTAMP"
                                                                                       , "_METADATA__UUID"="MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA__UUID"
                                                                                       , "_METADATA_CONSOLIDATION"="MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA_CONSOLIDATION"
                                                                                       , "CREATED_AT"="MY_SCHEMA_ANOTHER_TABLE_LOG"."CREATED_AT"
                                                                                       , "COLUMN_ONE"="MY_SCHEMA_ANOTHER_TABLE_LOG"."COLUMN_ONE"
                                                                                       , "COLUMN_TWO"="MY_SCHEMA_ANOTHER_TABLE_LOG"."COLUMN_TWO"
                                                                                       , "ID"="MY_SCHEMA_ANOTHER_TABLE_LOG"."ID"
                                                                                       , "UPDATED_AT"="MY_SCHEMA_ANOTHER_TABLE_LOG"."UPDATED_AT"
                                                                                       , "XMIN__TEXT__BIGINT"="MY_SCHEMA_ANOTHER_TABLE_LOG"."XMIN__TEXT__BIGINT"
                                                                         WHEN NOT MATCHED THEN INSERT ("_METADATA__TIMESTAMP"
                                                                                                     , "_METADATA__UUID"
                                                                                                     , "_METADATA_CONSOLIDATION"
                                                                                                     , "CREATED_AT"
                                                                                                     , "COLUMN_ONE"
                                                                                                     , "COLUMN_TWO"
                                                                                                     , "ID"
                                                                                                     , "UPDATED_AT"
                                                                                                     , "XMIN__TEXT__BIGINT") 
                                                                        VALUES ("MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA__TIMESTAMP"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA__UUID"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."_METADATA_CONSOLIDATION"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."CREATED_AT"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."COLUMN_ONE"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."COLUMN_TWO"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."ID"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."UPDATED_AT"
                                                                              , "MY_SCHEMA_ANOTHER_TABLE_LOG"."XMIN__TEXT__BIGINT");
                                                        CREATE OR REPLACE VIEW "MY_SCHEMA"."ANOTHER_TABLE_NRT"
                                                        COPY GRANTS AS 
                                                        SELECT "_METADATA__TIMESTAMP"
                                                             , "_METADATA__UUID"
                                                             , "_METADATA_CONSOLIDATION"
                                                             , "CREATED_AT"
                                                             , "COLUMN_ONE"
                                                             , "COLUMN_TWO"
                                                             , "ID"
                                                             , "UPDATED_AT"
                                                             , "XMIN__TEXT__BIGINT"
                                                          FROM (SELECT "_METADATA__TIMESTAMP"
                                                                     , "_METADATA__UUID"
                                                                     , "_METADATA_CONSOLIDATION"
                                                                     , "CREATED_AT"
                                                                     , "COLUMN_ONE"
                                                                     , "COLUMN_TWO"
                                                                     , "ID"
                                                                     , "UPDATED_AT"
                                                                     , "XMIN__TEXT__BIGINT"
                                                                     , ROW_NUMBER() OVER (PARTITION BY "ID" ORDER BY "_METADATA_CONSOLIDATION" DESC) AS "row_num"
                                                                  FROM (SELECT "_METADATA__TIMESTAMP"
                                                                             , "_METADATA__UUID"
                                                                             , "_METADATA_CONSOLIDATION"
                                                                             , "CREATED_AT"
                                                                             , "COLUMN_ONE"
                                                                             , "COLUMN_TWO"
                                                                             , "ID"
                                                                             , "UPDATED_AT"
                                                                             , "XMIN__TEXT__BIGINT"
                                                                          FROM "MY_SCHEMA"."ANOTHER_TABLE_LOG"
                                                                         UNION ALL
                                                                        SELECT "_METADATA__TIMESTAMP"
                                                                             , "_METADATA__UUID"
                                                                             , "_METADATA_CONSOLIDATION"
                                                                             , "CREATED_AT"
                                                                             , "COLUMN_ONE"
                                                                             , "COLUMN_TWO"
                                                                             , "ID"
                                                                             , "UPDATED_AT"
                                                                             , "XMIN__TEXT__BIGINT"
                                                                          FROM "MY_SCHEMA"."ANOTHER_TABLE"))
                                                                 WHERE "row_num"=1;
                                                   GRANT SELECT ON "MY_SCHEMA"."ANOTHER_TABLE" TO ROLE PUBLIC;
                                                   GRANT SELECT ON "MY_SCHEMA"."ANOTHER_TABLE_NRT" TO ROLE PUBLIC;
                                                   DELETE FROM "MY_SCHEMA"."ANOTHER_TABLE_LOG"
                                                         WHERE "_METADATA__TIMESTAMP" < DATEADD(day, -3, CURRENT_TIMESTAMP(0))
                                                            OR "_METADATA__TIMESTAMP" IS NULL;
                                                            """,
                              'error_message': None,
                              'query_type': 'incremental',
                              'generated_by': 'auto-mapper'}
                             ]

        mock_get_consolidations.return_value = sample_event_list
        return mock_get_consolidations.return_value

    # Test 1
    @patch('managealooma.consolidations.Consolidations.get_scheduled_queries', mock_get_consolidations)
    def test_get_scheduled_queries_is_list(self):
        consolidations = self.consolidations.get_scheduled_queries()
        self.assertTrue(isinstance(consolidations, list))

    # Test 2
    @patch('managealooma.consolidations.Consolidations.get_scheduled_queries', mock_get_consolidations)
    def test_get_scheduled_query_table_is_df(self):
        consolidations = self.consolidations.scheduled_query_table()
        self.assertTrue(isinstance(consolidations, pd.DataFrame))

    # Test 3
    @patch('managealooma.consolidations.Consolidations.get_scheduled_queries', mock_get_consolidations)
    def test_get_scheduled_query_table_columns_are_correct(self):
        consolidations = self.consolidations.scheduled_query_table()
        column_list = ['id',
                       'event_name',
                       'error_message',
                       'is_active',
                       'is_running',
                       'schedule',
                       'last_success_time',
                       'last_run_start_time',
                       'last_run_end_time',
                       'last_run_return_code',
                       'start_time',
                       'next_run_time',
                       'generated_by',
                       'query_type',
                       'service_type',
                       'time_limit',
                       'name',
                       'enqueue_time',
                       'docker_tag',
                       'docker_img',
                       'docker_cmd']

        self.assertTrue(column_list, list(consolidations.columns))

    # Test 4
    @patch('managealooma.consolidations.Consolidations.get_scheduled_queries', mock_get_consolidations)
    def test_get_scheduled_query_for_event_is_dict(self):
        consolidations = self.consolidations.get_scheduled_query_for_event(event_name='MY_SCHEMA.ANOTHER_TABLE')
        self.assertTrue(isinstance(consolidations, dict))
