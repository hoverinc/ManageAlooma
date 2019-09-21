import unittest

from unittest.mock import patch
from managealooma.mappings import Mappings


class TestMappings(unittest.TestCase):
    """ Tests the functions that alter the mapping dictionary
    """

    @patch('managealooma.mappings.Mappings')
    def setUp(self, mapping_class):
        """ Set up the mapping class and mocked API response with the mapping dictionary

        :param mapping_class:
        :return: None
        """
        self.mappings = Mappings(api=None, event_name='SCHEMA.TABLE', preview_full=False)
        self.mock_get_mapping()

    @patch('managealooma.mappings.Mappings.get_mapping_for_event')
    def mock_get_mapping(self, mock_get_mapping):
        """ Create the mocked mapping list of dictionaries

        :param mock_get_mapping:
        :return: The mocked mapping list
        """

        sample_mapping = {'autoMappingError': None,
                          'consolidation': {'consolidatedSchema': '',
                                            'consolidatedTableName': '',
                                            'consolidationKeys': '',
                                            'viewSchema': None},
                          'fields': [{'fieldName': 'id',
                                      'fields': [],
                                      'mapping': {'columnName': 'ID',
                                                  'columnType': {'nonNull': True,
                                                                 'precision': 38,
                                                                 'scale': 0,
                                                                 'type': 'NUMERIC'},
                                                  'isDiscarded': False,
                                                  'machineGenerated': False,
                                                  'subFields': None}},
                                     {'fieldName': 'name',
                                      'fields': [],
                                      'mapping': {'columnName': 'NAME',
                                                  'columnType': {'length': 16777216,
                                                                 'nonNull': False,
                                                                 'truncate': False,
                                                                 'type': 'VARCHAR'},
                                                  'isDiscarded': False,
                                                  'machineGenerated': False,
                                                  'subFields': None}}
                                     ],
                          'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
                          'mapping': {'isDiscarded': False,
                                      'outputHint': '{"table":"orders","schema":"PUBLIC"}',
                                      'outputId': 'a1s2d3-f4g5h6',
                                      'readOnly': False,
                                      'schema': 'PUBLIC',
                                      'tableName': 'ORDERS'},
                          'mappingMode': 'AUTO_MAP',
                          'name': 'PUBLIC.ORDERS',
                          'origInputLabel': 'production_database',
                          'schemaUrls': ['schema?id=12345-asdfg&schema_object=orders',
                                         'schema?id=d=12345-asdfg&sschema_object=deleted_rows'],
                          'state': 'MAPPED',
                          'usingDefaultMappingMode': False}

        mock_get_mapping.return_value = sample_mapping
        return mock_get_mapping.return_value

    # Test 1
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_view_mapping_without_fields_no_fields_success(self):
        mapping = self.mappings.view_mapping()
        mapping_has_fields = 'fields' not in mapping
        self.assertTrue(mapping_has_fields)

    # Test 2
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_view_mapping_without_fields_no_fields_fail(self):
        mapping = self.mappings.view_mapping(view_field_mappings=True)
        mapping_has_fields = 'fields' not in mapping
        self.assertFalse(mapping_has_fields)

    # Test 3
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_view_mapping_without_fields_has_fields_success(self):
        mapping = self.mappings.view_mapping(view_field_mappings=True)
        mapping_has_fields = 'fields' in mapping
        self.assertTrue(mapping_has_fields)

    # Test 4
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_view_mapping_without_fields_has_fields_failure(self):
        mapping = self.mappings.view_mapping()
        mapping_has_fields = 'fields' in mapping
        self.assertFalse(mapping_has_fields)

    # Test 5
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_mode_success(self):
        change = self.mappings.change_mapping_mode(new_mapping_mode='FLEXIBLE')
        altered_mapping_mode = change['mappingMode']
        self.assertEqual('FLEXIBLE', altered_mapping_mode)

    # Test 6
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_mode_fail(self):
        change = self.mappings.change_mapping_mode(new_mapping_mode='STRICT')
        altered_mapping_mode = change['mappingMode']
        self.assertNotEqual('FLEXIBLE', altered_mapping_mode)

    # Test 7
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_consolidation_settings_suceess(self):
        change = self.mappings.change_mapping_consolidation_settings(consolidation_schema='NEW_SCHEMA', consolidation_table_name="NEW_NAME", consolidation_keys="NEW_KEYS")
        change_consolidation = change['consolidation']

        expected_consolidation = {'consolidatedSchema': 'NEW_SCHEMA', 'consolidatedTableName': 'NEW_NAME', 'consolidationKeys': ['NEW_KEYS'], 'viewSchema': None}

        self.assertEqual(change_consolidation, expected_consolidation)

    # Test 8
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_consolidation_settings_failure(self):
        change = self.mappings.change_mapping_consolidation_settings(consolidation_schema='NEW_SCHEMA', consolidation_table_name="NEW_NAME", consolidation_keys="NEW_KEYS")
        change_consolidation = change['consolidation']

        original_consolidation = {'consolidation': {'consolidatedSchema': 'PUBLIC',
                                                    'consolidatedTableName': 'ORDERS',
                                                    'consolidationKeys': ['ID'],
                                                    'viewSchema': None}}

        self.assertNotEqual(change_consolidation, original_consolidation)

    # Test 9
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_consolidation_key_success(self):
        change = self.mappings.change_mapping_consolidation_key(new_consolidation_key='NEW_KEY')
        altered_mapping_mode = change['consolidation']['consolidationKeys']
        self.assertEqual('NEW_KEY', altered_mapping_mode)

    # Test 10
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_consolidation_key_failure(self):
        change = self.mappings.change_mapping_consolidation_key(new_consolidation_key='NEW_KEY')
        altered_mapping_mode = change['consolidation']['consolidationKeys']
        self.assertNotEqual('ID', altered_mapping_mode)

    # Test 11
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_to_use_log_success(self):
        change = self.mappings.change_mapping_to_use_log()
        altered_mapping_mode = change['mapping']['tableName']
        self.assertEqual('ORDERS_LOG', altered_mapping_mode)

    # Test 12
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_to_use_log_failure(self):
        change = self.mappings.change_mapping_to_use_log()
        altered_mapping_mode = change['mapping']['tableName']
        self.assertNotEqual('ORDERS', altered_mapping_mode)

    # Test 13
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_for_manual_consolidation_creation_success(self):
        change = self.mappings.change_mapping_for_manual_consolidation_creation(consolidation_schema='PUBLIC',
                                                                                consolidation_table_name='ORDERS', consolidation_keys='ID')

        altered_consolidation = change['consolidation']
        altered_mapping = change['mapping']['tableName']

        expected_consolidation_output = {'consolidatedSchema': 'PUBLIC',
                                         'consolidatedTableName': 'ORDERS',
                                         'consolidationKeys': ['ID'],
                                         'viewSchema': None}

        expected_mapping_output = 'ORDERS_LOG'

        self.assertEqual(expected_consolidation_output, altered_consolidation)
        self.assertEqual(expected_mapping_output, altered_mapping)

    # Test 14
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_mapping_for_manual_consolidation_creation_failure(self):
        change = self.mappings.change_mapping_for_manual_consolidation_creation(consolidation_schema='PUBLIC',
                                                                                consolidation_table_name='ORDERS', consolidation_keys='ID')

        altered_consolidation = change['consolidation']
        altered_mapping = change['mapping']['tableName']

        expected_consolidation_output = {'consolidatedSchema': '',
                                         'consolidatedTableName': '',
                                         'consolidationKeys': '',
                                         'viewSchema': None}

        expected_mapping_output = 'ORDERS'

        self.assertNotEqual(expected_consolidation_output, altered_consolidation)
        self.assertNotEqual(expected_mapping_output, altered_mapping)

    # Test 15
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_delete_field_from_mapping_success(self):
        change = self.mappings.delete_field_from_mapping(field_name='NAME')

        field_name_in_fields = False
        for field in change['fields']:
            if field['fieldName'] == 'NAME':
                field_name_in_fields = True

        self.assertFalse(field_name_in_fields)

    # Test 16
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_field_mapping_settings_success(self):
        change = self.mappings.change_field_mapping_settings(field_name='name', new_data_type='NUMERIC', truncate='38', non_null=True)

        change_field = None
        for field in change['fields']:
            if field['fieldName'] == 'name':
                change_field = field

        expected_consolidation_output = {'fieldName': 'name',
                                         'fields': [],
                                         'mapping': {'columnName': 'NAME',
                                                     'columnType': {'length': None,
                                                                    'nonNull': True,
                                                                    'truncate': '38',
                                                                    'type': 'NUMERIC'},
                                                     'isDiscarded': False,
                                                     'machineGenerated': False,
                                                     'subFields': None}}

        self.assertEqual(expected_consolidation_output, change_field)

    # Test 17
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_field_mapping_settings_failure(self):
        change = self.mappings.change_field_mapping_settings(field_name='name', new_data_type='NUMERIC', truncate='38', non_null=True)

        change_field = None
        for field in change['fields']:
            if field['fieldName'] == 'name':
                change_field = field

        original_values = {'fieldName': 'name',
                           'fields': [],
                           'mapping': {'columnName': 'NAME',
                                       'columnType': {'length': 16777216,
                                                      'nonNull': False,
                                                      'truncate': False,
                                                      'type': 'VARCHAR'},
                                       'isDiscarded': False,
                                       'machineGenerated': False,
                                       'subFields': None}}

        self.assertNotEqual(original_values, change_field)

    # Test 18
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_field_varchar_length_success(self):
        change = self.mappings.change_field_varchar_length(field_name='name', new_length=5)

        change_field = None
        for field in change['fields']:
            if field['fieldName'] == 'name':
                change_field = field

        expected_output = {'fieldName': 'name',
                           'fields': [],
                           'mapping': {'columnName': 'NAME',
                                       'columnType': {'length': 5,
                                                      'nonNull': False,
                                                      'truncate': False,
                                                      'type': 'VARCHAR'},
                                       'isDiscarded': False,
                                       'machineGenerated': False,
                                       'subFields': None}}

        self.assertEqual(expected_output, change_field)

    # Test 19
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_field_varchar_length_failure(self):
        change = self.mappings.change_field_varchar_length(field_name='name', new_length=5)

        change_field = None
        for field in change['fields']:
            if field['fieldName'] == 'name':
                change_field = field

        original_values = {'fieldName': 'name',
                           'fields': [],
                           'mapping': {'columnName': 'NAME',
                                       'columnType': {'length': 16777216,
                                                      'nonNull': False,
                                                      'truncate': False,
                                                      'type': 'VARCHAR'},
                                       'isDiscarded': False,
                                       'machineGenerated': False,
                                       'subFields': None}}

        self.assertNotEqual(original_values, change_field)

    # Test 20
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_field_null_constraint_success(self):
        change = self.mappings.change_field_null_constraint(field_name='name', nonnull=True)

        change_field = None
        for field in change['fields']:
            if field['fieldName'] == 'name':
                change_field = field

        expected_output = {'fieldName': 'name',
                           'fields': [],
                           'mapping': {'columnName': 'NAME',
                                       'columnType': {'length': 16777216,
                                                      'nonNull': True,
                                                      'truncate': False,
                                                      'type': 'VARCHAR'},
                                       'isDiscarded': False,
                                       'machineGenerated': False,
                                       'subFields': None}}

        self.assertEqual(expected_output, change_field)

    # Test 21
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_change_field_null_constraint_failure(self):
        change = self.mappings.change_field_null_constraint(field_name='name', nonnull=True)

        change_field = None
        for field in change['fields']:
            if field['fieldName'] == 'name':
                change_field = field

        original_values = {'fieldName': 'name',
                           'fields': [],
                           'mapping': {'columnName': 'NAME',
                                       'columnType': {'length': 16777216,
                                                      'nonNull': False,
                                                      'truncate': False,
                                                      'type': 'VARCHAR'},
                                       'isDiscarded': False,
                                       'machineGenerated': False,
                                       'subFields': None}}

        self.assertNotEqual(original_values, change_field)

    # Test 22
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_check_if_consolidation_uses_log_success(self):
        check = self.mappings.check_if_consolidation_uses_log()
        self.assertFalse(check)

    # Test 23
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_copy_mapping_success(self):
        change = self.mappings.copy_mapping(new_event='NEW_SCHEMA.NEW_TABLE')

        expected_output = {'autoMappingError': None,
                           'consolidation': {'consolidatedSchema': '',
                                             'consolidatedTableName': '',
                                             'consolidationKeys': '',
                                             'viewSchema': None},
                           'fields': [{'fieldName': 'id',
                                       'fields': [],
                                       'mapping': {'columnName': 'ID',
                                                   'columnType': {'nonNull': True,
                                                                  'precision': 38,
                                                                  'scale': 0,
                                                                  'type': 'NUMERIC'},
                                                   'isDiscarded': False,
                                                   'machineGenerated': False,
                                                   'subFields': None}},
                                      {'fieldName': 'name',
                                       'fields': [],
                                       'mapping': {'columnName': 'NAME',
                                                   'columnType': {'length': 16777216,
                                                                  'nonNull': False,
                                                                  'truncate': False,
                                                                  'type': 'VARCHAR'},
                                                   'isDiscarded': False,
                                                   'machineGenerated': False,
                                                   'subFields': None}}
                                      ],
                           'inputObjects': {'12345-asdfg': ['98765-zxcvb']},
                           'mapping': {'isDiscarded': False,
                                       'outputHint': '{"table":"orders","schema":"PUBLIC"}',
                                       'outputId': 'a1s2d3-f4g5h6',
                                       'readOnly': False,
                                       'schema': 'PUBLIC',
                                       'tableName': 'ORDERS'},
                           'mappingMode': 'AUTO_MAP',
                           'name': 'NEW_SCHEMA.NEW_TABLE',
                           'origInputLabel': 'production_database',
                           'schemaUrls': ['schema?id=12345-asdfg&schema_object=orders',
                                          'schema?id=d=12345-asdfg&sschema_object=deleted_rows'],
                           'state': 'MAPPED',
                           'usingDefaultMappingMode': False}

        self.assertEqual(expected_output, change)

    # Test 24
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_copy_mapping_failure(self):
        change = self.mappings.copy_mapping(new_event='NEW_SCHEMA.NEW_TABLE')

        original_event_name = 'PUBLIC.ORDERS'
        self.assertNotEqual('PUBLIC.ORDERS', change['name'])

    # Test 25
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_set_mapping_from_existing_mapping_success(self):
        change = self.mappings.set_mapping_from_existing_mapping(new_event_name='NEW_NAME', new_schema='NEW_SCHEMA', new_table='NEW_TABLE',
                                                                 new_input_label='new_input_label')

        expected_output_consolidation = {'consolidatedSchema': 'NEW_SCHEMA',
                                         'consolidatedTableName': 'NEW_TABLE',
                                         'consolidationKeys': '',
                                         'viewSchema': None}
        expected_output_mapping = {'isDiscarded': False,
                                   'outputHint': None,
                                   'outputId': None,
                                   'readOnly': False,
                                   'schema': 'NEW_SCHEMA',
                                   'tableName': 'NEW_TABLE_LOG'}
        expected_mapping_name = change['name']
        expected_orig_input_label = change['origInputLabel']
        expected_schema_urls = []
        expected_input_objects = change['inputObjects']

        self.assertEqual(expected_output_consolidation, change['consolidation'])
        self.assertEqual(expected_output_mapping, change['mapping'])
        self.assertEqual('NEW_NAME', expected_mapping_name)
        self.assertEqual('new_input_label', expected_orig_input_label)
        self.assertEqual([], expected_schema_urls)
        self.assertIsNone(expected_input_objects)

    # Test 26
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_number_success(self):
        change = self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='NUMBER')

        new_field = None
        for field in change['fields']:
            if field['fieldName'] == 'new_field':
                new_field = field

        expected_new_field = {'fieldName': 'new_field',
                         'fields': [],
                         'mapping': {'columnName': 'NEW_COLUMN',
                                     'columnType': {'nonNull': False,
                                                    'precision': 38,
                                                    'scale': 0,
                                                    'type': 'NUMBER'},
                                     'isDiscarded': False,
                                     'machineGenerated': False,
                                     'subFields': None}}

        self.assertEqual(expected_new_field, new_field)

    # Test 27
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_varchar_success(self):
        change = self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='VARCHAR')

        new_field = None
        for field in change['fields']:
            if field['fieldName'] == 'new_field':
                new_field = field

        expected_new_field = {'fieldName': 'new_field',
                              'fields': [],
                              'mapping': {'columnName': 'NEW_COLUMN',
                                          'columnType': {'length': 16777216,
                                                         'nonNull': False,
                                                         'truncate': False,
                                                         'type': 'VARCHAR'},
                                          'isDiscarded': False,
                                          'machineGenerated': False,
                                          'subFields': None}}

        self.assertEqual(expected_new_field, new_field)

    # Test 28
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_boolean_success(self):
        change = self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='BOOLEAN')

        new_field = None
        for field in change['fields']:
            if field['fieldName'] == 'new_field':
                new_field = field

        expected_new_field = {'fieldName': 'new_field',
                              'fields': [],
                              'mapping': {'columnName': 'NEW_COLUMN',
                                          'columnType': {'nonNull': False,
                                                         'type': 'BOOLEAN'},
                                          'isDiscarded': False,
                                          'machineGenerated': False,
                                          'subFields': None}}

        self.assertEqual(expected_new_field, new_field)

    # Test 29
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_semi_structured_success(self):
        change = self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='VARIANT')

        new_field = None
        for field in change['fields']:
            if field['fieldName'] == 'new_field':
                new_field = field

        expected_new_field = {'fieldName': 'new_field',
                              'fields': [],
                              'mapping': {'columnName': 'NEW_COLUMN',
                                          'columnType': {'nonNull': False,
                                                         'type': 'VARIANT'},
                                          'isDiscarded': False,
                                          'machineGenerated': False,
                                          'subFields': None}}

        self.assertEqual(expected_new_field, new_field)

    # Test 30
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_float_success(self):
        change = self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='FLOAT')

        new_field = None
        for field in change['fields']:
            if field['fieldName'] == 'new_field':
                new_field = field

        expected_new_field = {'fieldName': 'new_field',
                              'fields': [],
                              'mapping': {'columnName': 'NEW_COLUMN',
                                          'columnType': {'nonNull': False,
                                                         'type': 'FLOAT'},
                                          'isDiscarded': False,
                                          'machineGenerated': False,
                                          'subFields': None}}

        self.assertEqual(expected_new_field, new_field)

    # Test 31
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_timestamp_success(self):
        change = self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='TIMESTAMP')

        new_field = None
        for field in change['fields']:
            if field['fieldName'] == 'new_field':
                new_field = field

        expected_new_field = {'fieldName': 'new_field',
                              'fields': [],
                              'mapping': {'columnName': 'NEW_COLUMN',
                                          'columnType': {'nonNull': False,
                                                         'type': 'TIMESTAMP'},
                                          'isDiscarded': False,
                                          'machineGenerated': False,
                                          'subFields': None}}

        self.assertEqual(expected_new_field, new_field)

    # Test 32
    @patch('managealooma.mappings.Mappings.get_mapping_for_event', mock_get_mapping)
    def test_add_field_to_mapping_data_type_exception_success(self):

        with self.assertRaises(BaseException) as cm:
            self.mappings.add_field_to_mapping(field_name='new_field', column_name='NEW_COLUMN', data_type='INT')

        self.assertEqual(str(cm.exception), 'Only SNOWFlAKE data types of NUMBER, VARIANT, BOOLEAN, VARCHAR, FLOAT, TIMESTAMP are allowed')



