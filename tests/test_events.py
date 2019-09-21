import unittest
import pandas as pd

from unittest.mock import patch
from managealooma.events import Events


class TestEvents(unittest.TestCase):
    """ Tests the functions that retrieve and manipulate events from the API
    """

    @patch('managealooma.events.Events')
    def setUp(self, events_class):
        """ Set up the event class and mocked API response with the event list

        :param events_class:
        :return: None
        """
        self.events = Events(api=None)
        self.mock_get_events()

    @patch('managealooma.events.Events.get_all_events')
    def mock_get_events(self, mock_get_events):
        """ Create the mocked event list of dictionaries

        :param mock_get_mapping:
        :return: The mocked event list
        """

        sample_event_list = [{'name': 'SOURCE_ONE.TABLE_ONE',
                              'mappingMode': 'AUTO_MAP',
                              'mapping': {'isDiscarded': False,
                                          'outputHint': None,
                                          'outputId': '12345-a1a1-b2b2-c2c2-12345asdf',
                                          'tableName': 'TABLE_ONE',
                                          'schema': 'SOURCE_ONE',
                                          'readOnly': False},
                              'consolidation': {'consolidatedTableName': None,
                                                'consolidatedSchema': None,
                                                'viewSchema': None, 'consolidationKeys': []},
                              'stats': {'count': 10},
                              'state': 'MAPPED',
                              'usingDefaultMappingMode': False,
                              'schemaUrls': [],
                              'origInputLabel': 'source_one',
                              'inputObjects': {},
                              'autoMappingError': None},
                             {'name': 'SOURCE_ONE.TABLE_TWO',
                              'mappingMode': 'STRICT',
                              'mapping': {'isDiscarded': False,
                                          'outputHint': None,
                                          'outputId': '98765-z9z9-4aa9-ba47-27274891c496',
                                          'tableName': 'TABLE_TWO',
                                          'schema': 'SOURCE_ONE',
                                          'readOnly': False},
                              'consolidation': {'consolidatedTableName': None,
                                                'consolidatedSchema': None,
                                                'viewSchema': None,
                                                'consolidationKeys': None},
                              'stats': None,
                              'state': 'MAPPED',
                              'usingDefaultMappingMode': True,
                              'schemaUrls': ['schema?id=43l43l-9876-543l-kjh1-1234asdf12&schema_object=two'],
                              'origInputLabel': 'source_one',
                              'inputObjects': {},
                              'autoMappingError': None},
                             {'name': 'SOURCE_TWO.TABLE_ONE',
                              'mappingMode': 'STRICT',
                              'mapping': {'isDiscarded': False,
                                          'outputHint': None,
                                          'outputId': '201dd975-a7e1-4aa9-ba47-27274891c496',
                                          'tableName': 'TABLE_ONE_LOG',
                                          'schema': 'SOURCE_TWO',
                                          'readOnly': False},
                              'consolidation': {'consolidatedTableName': 'TABLE_ONE',
                                                'consolidatedSchema': 'SOURCE_TWO',
                                                'viewSchema': None,
                                                'consolidationKeys': ['ID']},
                              'stats': {'count': 5763},
                              'state': 'MAPPED',
                              'usingDefaultMappingMode': True,
                              'schemaUrls': ['schema?id=afd6e39c-2045-4fab-8f75-673cab5a3846&schema_object=three'],
                              'origInputLabel': 'source_tWO',
                              'inputObjects': {'opiuyt-l4l4-p3p3-9876-asdf1234tr': ['qwer98-2l2l-1234-2345-aa99akjlh']},
                              'autoMappingError': None}
                             ]

        mock_get_events.return_value = sample_event_list
        return mock_get_events.return_value

    # Test 1
    @patch('managealooma.events.Events.get_all_events', mock_get_events)
    def test_view_events_dataframe_success(self):
        events = self.events.view_events()
        self.assertTrue(isinstance(events, pd.DataFrame))

    # Test 2
    @patch('managealooma.events.Events.get_all_events', mock_get_events)
    def test_view_events_dataframe_failure(self):
        events = self.events.view_events(print_format='json')
        self.assertFalse(isinstance(events, pd.DataFrame))

    # Test 3
    @patch('managealooma.events.Events.get_all_events', mock_get_events)
    def test_view_events_json_success(self):
        events = self.events.view_events(print_format='json')
        self.assertTrue(isinstance(events, list))

    # Test 4
    @patch('managealooma.events.Events.get_all_events', mock_get_events)
    def test_view_events_json_failure(self):
        events = self.events.view_events(print_format='table')
        self.assertFalse(isinstance(events, list))

    # Test 5
    @patch('managealooma.events.Events.get_all_events', mock_get_events)
    def test_list_events_all_inputs(self):
        event_list = self.events.list_events()

        expected_list = ['SOURCE_ONE.TABLE_ONE', 'SOURCE_ONE.TABLE_TWO', 'SOURCE_TWO.TABLE_ONE']
        self.assertEqual(expected_list, event_list)

    # Test 6
    @patch('managealooma.events.Events.get_all_events', mock_get_events)
    def test_list_events_single_input(self):
        event_list = self.events.list_events(input_labels='source_one')

        expected_list = ['SOURCE_ONE.TABLE_ONE', 'SOURCE_ONE.TABLE_TWO']
        self.assertEqual(expected_list, event_list)




