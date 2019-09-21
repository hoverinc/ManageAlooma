import unittest

from unittest.mock import patch
from managealooma.samples import Samples


class TestSamples(unittest.TestCase):
    """ Tests the functions that retrieve and manipulate samples from the Alooma API, saved files, databases, or other sources
    """

    @patch('managealooma.samples.Samples')
    def setUp(self, samples_class):
        """ Set up the sample class and mocked Alooma API response with a list of samples

        :param samples_class:
        :return: None
        """
        self.samples = Samples(api=None, sample_event_directory=None)
        self.mock_get_samples_from_alooma(event_name='SAMPLE.EVENT')

    @patch('managealooma.samples.Samples.get_samples_for_event_from_alooma_api')
    def mock_get_samples_from_alooma(self, mock_get_samples_from_alooma, event_name='SAMPLE_EVENT'):
        """ Create the mocked mapping dictionary

        :param mock_get_mapping:
        :return: The mocked mapping dictionary
        """

        sample_input_list = [{'sample': {'id': 1,
                                         'created_at': '2019-01-01T00:00:00',
                                         '_metadata': {'@uuid': '1q1q1q-1q1q-1q1q-1q1q-1q1q1q1q',
                                                       'event_type': 'my_sample_event',
                                                       'input_type': 'rest_endpoint'},
                                         'timestamp': 1566162023010,
                                         'status': 'VALID',
                                         'eventType': 'SAMPLE.EVENT'}},
                              {'sample': {'id': 2,
                                          'created_at': '2019-01-02T00:00:00',
                                          '_metadata': {'@uuid': '2w2w2w-2w2w-2w2w-2w2w-2w2w2w2w',
                                                        'event_type': 'my_sample_event',
                                                        'input_type': 'rest_endpoint'},
                                          'timestamp': 1566162023011,
                                          'status': 'VALID',
                                          'eventType': 'SAMPLE.EVENT'}},
                               {'sample': {'id': 3,
                                           'created_at': '2019-01-03T00:00:00',
                                           '_metadata': {'@uuid': '3e3e3e-3e3e-3e3e-3e3e-3e3e3e3e',
                                                         'event_type': 'my_sample_event',
                                                         'input_type': 'rest_endpoint',
                                                         'timestamp': 1566162023012,
                                                         'status': 'VALID',
                                                         'eventType': 'SAMPLE.EVENT'}}}]

        mock_get_samples_from_alooma.return_value = sample_input_list
        return mock_get_samples_from_alooma.return_value

    @patch('managealooma.samples.Samples.get_sample_from_any_api')
    def mock_get_samples_from_api(self, mock_get_samples_from_api):
        """ Create the mocked mapping dictionary

        :param mock_get_mapping:
        :return: The mocked mapping dictionary
        """
        pass

    # Test 1
    @patch('managealooma.samples.Samples.get_samples_for_event_from_alooma_api', mock_get_samples_from_alooma)
    def test_view_samples_for_event_from_alooma_api_is_list(self):
        samples = self.samples.view_samples_for_event_from_alooma_api(event_name='SAMPLE.EVENT')
        self.assertTrue(isinstance(samples, list))

    # Test 2
    @patch('managealooma.samples.Samples.get_samples_for_event_from_alooma_api', mock_get_samples_from_alooma)
    def test_view_samples_for_event_from_alooma_api_list_length_is_three(self):
        samples = self.samples.view_samples_for_event_from_alooma_api(event_name='SAMPLE.EVENT')
        self.assertEqual(3, len(samples))

