import unittest
import pandas as pd

from unittest.mock import patch
from managealooma.inputs import Inputs


class TestInputs(unittest.TestCase):
    """ Tests the functions that retrieve and manipulate inputs from the API
    """

    @patch('managealooma.inputs.Inputs')
    def setUp(self, inputs_class):
        """ Set up the input class and mocked API response with the list of dictionaries

        :param inputs_class:
        :return: None
        """
        self.inputs = Inputs(api=None)
        self.mock_get_inputs()

    @patch('managealooma.inputs.Inputs.get_all_inputs')
    def mock_get_inputs(self, mock_get_inputs):
        """ Create the mocked input list of dictionaries

        :param mock_get_mapping:
        :return: The mocked input list
        """

        sample_input_list = [{'configuration': {'auto_map': 'true'},
                              'id': '12qw12qw-12qw-12qw-12qw-12qw12qw12qw',
                              'name': 'webhook_input',
                              'type': 'RESTAPI',
                              'validated': True},
                             # For the Mixpanel Engage API you must have separate code that updates the session ID on a schedule for Alooma to get fresh data
                             {'configuration': {'auto_map': 'false',
                                                'base_url': 'https://mixpanel.com/api/2.0/engage',
                                                'cron_expression': '0 */1 * * *',
                                                'data_field': 'results',
                                                'frequency': 240,
                                                'headers': [],
                                                'initial_value': 1,
                                                'input_default_schema': 'PUBLIC',
                                                'page_parameter': 'page',
                                                'pagination_type': 'Incremental',
                                                'parameters': [{'parameter': 'session_id',
                                                                'type': 'Text',
                                                                'value': '1234567869-abcdefghijklmnopqrstuv987'},
                                                               {'parameter': 'where',
                                                                'template': 'properties["$last_seen"]>="%Y-%m-%dT00:00:00"',
                                                                'type': 'Days Past', 'value': 2}],
                                                'primary_keys': [], 'request': 'GET',
                                                'username': '1q2w3e4r5t6y7u8i9o0p'},
                              'created_at': '2019-01-01T00:00:00.000000',
                              'id': '34er34-34er-34er-34er-34er34er34er',
                              'name': 'mixpanel_engage_one',
                              'paused': False,
                              'type': 'REST_INPUT',
                              'validated': True},
                             {'configuration': {'auto_map': 'false',
                                                'base_url': 'https://mixpanel.com/api/2.0/engage',
                                                'cron_expression': '0 */1 * * *',
                                                'data_field': 'results',
                                                'frequency': 240,
                                                'headers': [],
                                                'initial_value': 1,
                                                'input_default_schema': 'PUBLIC',
                                                'page_parameter': 'page',
                                                'pagination_type': 'Incremental'},
                              'created_at': '2019-01-01T00:00:00.000000',
                              'id': '34er34-34er-34er-34er-34er34er34er',
                              'name': 'mixpanel_engage_two',
                              'paused': False,
                              'type': 'REST_INPUT',
                              'validated': True},
                             {'configuration': {'auto_map': 'true',
                                                'fileFormat': '{"type":"excel"}',
                                                'input_default_schema': 'GOOGLE_SHEETS',
                                                'input_type': 'GOOGLE_SHEETS',
                                                'oauth2': '9876poiu9876poiu9876poiu',
                                                'query': "(mimeType='application/vnd.google-apps.spreadsheet' or mimeType='application/vnd.google-apps.folder')",
                                                'root_folder': '10qp10qp10qp10qp10qp'},
                              'created_at': '2019-01-01T00:00:00.000000',
                              'id': '34er34er-34er-34er-34er-34er34er34er',
                              'name': 'a_google_sheet',
                              'paused': False,
                              'type': 'GOOGLE_SHEETS_STORAGE',
                              'validated': True},
                             # For Salesforce the start time should be set to the earliest lastmodifieddata you see on any object
                             {'configuration': {'auto_map': 'true',
                                                'custom_objects': 'Account AccountHistory Opportunity OpportunityHistory Task User UserRole',
                                                'daily_api_calls': 200000,
                                                'daily_bulk_queries': 10000,
                                                'input_default_schema': 'SALESFORCE',
                                                'oauth2': '1234qwer1234qwer1234qwer',
                                                'start_time': '2019-01-01T21:51:11.698503'},
                              'created_at': '2019-01-01T00:00:00.000000',
                              'id': '56ty56ty-56ty-56ty-56ty-56ty56ty56ty',
                              'name': 'salesforce_production',
                              'paused': False,
                              'type': 'SALESFORCE',
                              'validated': True},
                             {'configuration': {'auto_map': 'true',
                                                'batch_size': 100000,
                                                'database': 'my_database',
                                                'db_type': 'psql',
                                                'input_default_schema': 'MY_DATABASE',
                                                'port': 5432,
                                                'replication_type': 'incremental_load',
                                                'schema': 'public',
                                                'server': 'some-address-on-a-cloud.com',
                                                'tables': '{"orders":"xmin::text::bigint","order_items":"xmin::text::bigint","users":"xmin::text::bigint"}',
                                                'user': 'a_user_for_alooma'},
                              'created_at': '2019-01-01T00:00:00.000000',
                              'id': '78ui78ui-78ui-78ui-78ui-78ui78ui78ui',
                              'name': 'my_database',
                              'paused': False,
                              'type': 'ODBC',
                              'validated': True}]

        mock_get_inputs.return_value = sample_input_list
        return mock_get_inputs.return_value

    # Test 1
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_get_all_inputs_is_list(self):
        inputs = self.inputs.get_all_inputs()
        self.assertTrue(isinstance(inputs, list))

    # Test 2
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_get_all_inputs_list_length_is_six(self):
        inputs = self.inputs.get_all_inputs()
        self.assertEqual(6, len(inputs))

    # Test 3
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_get_input_by_name(self):
        single_input = self.inputs.get_input(input_name='webhook_input')

        expected_results = {'configuration': {'auto_map': 'true'},
                            'id': '12qw12qw-12qw-12qw-12qw-12qw12qw12qw',
                            'name': 'webhook_input',
                            'type': 'RESTAPI',
                            'validated': True}

        self.assertEqual(expected_results, single_input)

    # Test 4
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_view_inputs_dataframe(self):
        inputs = self.inputs.view_inputs(print_format='table')
        self.assertTrue(isinstance(inputs, pd.DataFrame))

    # Test 5
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_view_inputs_list_json(self):
        inputs = self.inputs.view_inputs(print_format='json')
        self.assertTrue(isinstance(inputs, list))

    # Test 6
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_view_inputs_single_json(self):
        inputs = self.inputs.view_inputs(print_format='table', single_input='webhook_input')
        self.assertFalse(isinstance(inputs, dict))

    # Test 7
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_list_inputs(self):
        inputs = self.inputs.list_inputs()

        expected_results = ['webhook_input', 'mixpanel_engage_one', 'mixpanel_engage_two', 'a_google_sheet', 'salesforce_production', 'my_database']
        self.assertEqual(expected_results, inputs)

    # Test 8
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_list_tables_success(self):
        tables = self.inputs.list_tables(input_name='my_database')

        expected_results = ['orders', 'order_items', 'users']
        self.assertEqual(expected_results, tables)

    # Test 9
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_list_tables_exception_raised(self):
        with self.assertRaises(BaseException) as cm:
            self.inputs.list_tables(input_name='webhook_input')

        self.assertEqual(str(cm.exception), 'The input webhook_input is of type RESTAPI and not of type ODBC')

    # Test 10
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_create_input_database_input(self):
        new_input = self.inputs.create_input_database(source_credentials={'server': 'server_name',
                                                                          'schema': 'schema_name',
                                                                          'port': 'port',
                                                                          'database': 'database',
                                                                          'db_type': 'psql',
                                                                          'user': 'username',
                                                                          'password': 'password'},
                                                      new_input_name='new_db_input',
                                                      existing_input='my_database',
                                                      tables_dict={'table_one': 'xmin::text::bigint',
                                                                   'table_two': 'xmin::text::bigint'},
                                                      auto_map=True,
                                                      input_default_schema='PUBLIC',
                                                      replication_type='incremental_load',
                                                      batch_size=5000)

        expected_input_config = {'auto_map': True,
                                 'batch_size': 5000,
                                 'database': 'database',
                                 'db_type': 'PUBLIC',
                                 'input_default_schema': 'PUBLIC',
                                 'password': 'password',
                                 'port': 'port',
                                 'replication_type': 'incremental_load',
                                 'schema': 'public',
                                 'server': 'server_name',
                                 'tables': '{"table_one": "xmin::text::bigint", "table_two": "xmin::text::bigint"}',
                                 'user': 'username'}

        self.assertEqual(expected_input_config, new_input)

    # Test 11
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_edit_input_configuration_success(self):
        edited_input = self.inputs.edit_input_configuration(input_name='webhook_input', field_to_edit='auto_map', new_field_value='false')

        expected_edited_input = {'configuration': {'auto_map': 'false'},
                                 'id': '12qw12qw-12qw-12qw-12qw-12qw12qw12qw',
                                 'name': 'webhook_input',
                                 'type': 'RESTAPI',
                                 'validated': True}

        self.assertEqual(expected_edited_input, edited_input)

    # Test 12
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_edit_input_configuration_raise_exception(self):
        with self.assertRaises(BaseException) as cm:
            self.inputs.edit_input_configuration(input_name='webhook_input', field_to_edit='cron_expression', new_field_value='0 */1 * * *')

        self.assertEqual(str(cm.exception), 'The field cron_expression is not in the input webhook_input')

    # Test 13
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_add_table_to_input_success(self):
        edited_input = self.inputs.add_table_to_input(input_name='my_database', new_table_dict={"my_first_new_table": "xmin::text::bigint",
                                                                                                "my_second_new_table": "xmin::text::bigint"})

        expected_edited_input = {'configuration': {'auto_map': 'true',
                                                   'batch_size': 100000,
                                                   'database': 'my_database',
                                                   'db_type': 'psql',
                                                   'input_default_schema': 'MY_DATABASE',
                                                   'port': 5432,
                                                   'replication_type': 'incremental_load',
                                                   'schema': 'public',
                                                   'server': 'some-address-on-a-cloud.com',
                                                   'tables': '{"orders": "xmin::text::bigint", "order_items": "xmin::text::bigint", "users": "xmin::text::bigint", "my_first_new_table": "xmin::text::bigint", "my_second_new_table": "xmin::text::bigint"}',
                                                   'user': 'a_user_for_alooma'},
                                 'created_at': '2019-01-01T00:00:00.000000',
                                 'id': '78ui78ui-78ui-78ui-78ui-78ui78ui78ui',
                                 'name': 'my_database',
                                 'paused': False,
                                 'type': 'ODBC',
                                 'validated': True}

        self.assertEqual(expected_edited_input, edited_input)

    # Test 14
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_add_table_to_input_odbc_exception(self):
        with self.assertRaises(BaseException) as cm:
            self.inputs.add_table_to_input(input_name='mixpanel_engage_one', new_table_dict={"my_first_new_table": "xmin::text::bigint",
                                                                                             "my_second_new_table": "xmin::text::bigint"})

        self.assertEqual(str(cm.exception), 'The input mixpanel_engage_one is of type REST_INPUT and not of type ODBC')

    # Test 15
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_add_table_to_input_table_in_input_exception(self):
        with self.assertRaises(BaseException) as cm:
            self.inputs.add_table_to_input(input_name='my_database', new_table_dict={"orders": "xmin::text::bigint",
                                                                                     "my_second_new_table": "xmin::text::bigint"})

        self.assertEqual(str(cm.exception), 'The table orders is already in the input my_database')

    # Test 16
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_change_auto_mapping_mode_success(self):
        edited_input = self.inputs.change_auto_mapping_mode(input_name='webhook_input', new_mapping_mode='false')

        expected_edited_input = {'configuration': {'auto_map': 'false'},
                                 'id': '12qw12qw-12qw-12qw-12qw-12qw12qw12qw',
                                 'name': 'webhook_input',
                                 'type': 'RESTAPI',
                                 'validated': True}

        self.assertEqual(expected_edited_input, edited_input)

    # Test 17
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_add_template_to_parameter_configuration_success(self):
        edited_input = self.inputs.add_template_to_parameter_configuration(input_name='mixpanel_engage_one',
                                                                           add_to_parameter='session_id',
                                                                           template='properties["$last_seen"]>="%Y-%m-%dT00:00:00"')

        expected_edited_input = {'configuration': {'auto_map': 'false',
                                                   'base_url': 'https://mixpanel.com/api/2.0/engage',
                                                   'cron_expression': '0 */1 * * *',
                                                   'data_field': 'results',
                                                   'frequency': 240,
                                                   'headers': [],
                                                   'initial_value': 1,
                                                   'input_default_schema': 'PUBLIC',
                                                   'page_parameter': 'page',
                                                   'pagination_type': 'Incremental',
                                                   'parameters': [{'parameter': 'session_id', 'type': 'Text', 'value': '1234567869-abcdefghijklmnopqrstuv987'},
                                                                  {'parameter': 'where', 'template': 'properties["$last_seen"]>="%Y-%m-%dT00:00:00"', 'type': 'Days Past', 'value': 2}],
                                                   'primary_keys': [],
                                                   'request': 'GET',
                                                   'username': '1q2w3e4r5t6y7u8i9o0p'},
                                 'created_at': '2019-01-01T00:00:00.000000',
                                 'id': '34er34-34er-34er-34er-34er34er34er',
                                 'name': 'mixpanel_engage_one',
                                 'paused': False,
                                 'type': 'REST_INPUT',
                                 'validated': True}

        self.assertEqual(expected_edited_input, edited_input)

    # Test 18
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_add_template_to_parameter_configuration_no_parameters_exception(self):
        with self.assertRaises(BaseException) as cm:
            self.inputs.add_template_to_parameter_configuration(input_name='mixpanel_engage_two',
                                                                add_to_parameter='where',
                                                                template='properties["$last_seen"]>="%Y-%m-%dT00:00:00"')

        self.assertEqual(str(cm.exception), 'The input mixpanel_engage_two does not have any parameters')

    # Test 19
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_edit_parameter_configuration_success(self):
        edited_input = self.inputs.edit_parameter_configuration(input_name='mixpanel_engage_one',
                                                                parameter_to_edit='where',
                                                                value_to_set='value',
                                                                new_value=3)

        expected_edited_input = {'configuration': {'auto_map': 'false',
                                                   'base_url': 'https://mixpanel.com/api/2.0/engage',
                                                   'cron_expression': '0 */1 * * *',
                                                   'data_field': 'results',
                                                   'frequency': 240,
                                                   'headers': [],
                                                   'initial_value': 1,
                                                   'input_default_schema': 'PUBLIC',
                                                   'page_parameter': 'page',
                                                   'pagination_type': 'Incremental',
                                                   'parameters': [{'parameter': 'session_id',
                                                                   'type': 'Text',
                                                                   'value': '1234567869-abcdefghijklmnopqrstuv987'},
                                                                  {'parameter': 'where',
                                                                   'template': 'properties["$last_seen"]>="%Y-%m-%dT00:00:00"',
                                                                   'type': 'Days Past',
                                                                   'value': 3}],
                                                   'primary_keys': [], 'request': 'GET',
                                                   'username': '1q2w3e4r5t6y7u8i9o0p'},
                                 'created_at': '2019-01-01T00:00:00.000000',
                                 'id': '34er34-34er-34er-34er-34er34er34er',
                                 'name': 'mixpanel_engage_one',
                                 'paused': False,
                                 'type': 'REST_INPUT',
                                 'validated': True}

        self.assertEqual(expected_edited_input, edited_input)

    # Test 20
    @patch('managealooma.inputs.Inputs.get_all_inputs', mock_get_inputs)
    def test_edit_parameter_configuration_no_parameters_exception(self):
        with self.assertRaises(BaseException) as cm:
            self.inputs.edit_parameter_configuration(input_name='mixpanel_engage_two',
                                                     parameter_to_edit='where',
                                                     value_to_set='value',
                                                     new_value=3)

        self.assertEqual(str(cm.exception), 'The input mixpanel_engage_two does not have any parameters')

