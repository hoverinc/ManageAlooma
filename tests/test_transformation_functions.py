import unittest
import json

from managealooma.transformation_functions import add_column_based_on_null, add_columns_with_default, add_composite_key, \
    add_duplicate_fields, add_suffix, convert_all_event_fields_to_snake_case, convert_dictionary_fields_to_string, \
    convert_empty_value_to_none, convert_event_type_case, convert_null_to_zero, convert_spaces_and_special_characters_to_underscore, \
    convert_string_to_snake_case, convert_values_to_none, flatten_json, flatten_json_1_level, map_key_in_dictionary_to_value, \
    map_value_in_list_to_dictionary_key, mark_for_delete, parse_list_of_json_and_concat, remove_duplicate_field, remove_outer_key, \
    remove_starting_characters_from_keys, remove_whitespace, rename_fields, split_event_to_multiple_events, split_field_list_to_multiple_events, \
    whitelist_or_blacklist_columns


class TestTransformationFunctions(unittest.TestCase):

    # Test 1
    def test_add_column_based_on_null_when_null(self):
        input = {'last_4': None}
        output = {'last_4': 'N'}
        self.assertEqual(output, add_column_based_on_null(event=input, field='last_4', new_field='last_4', new_value_if_null='N', new_value_if_not_null=None))

    # Test 2
    def test_add_column_based_on_null_when_null_both_params_entered(self):
        input = {'last_4': None}
        output = {'last_4': 'N'}
        self.assertEqual(output, add_column_based_on_null(event=input, field='last_4', new_field='last_4', new_value_if_null='N', new_value_if_not_null='Y'))

    # Test 3
    def test_add_column_based_on_null_when_not_null(self):
        input = {'last_4': 0000}
        output = {'last_4': 'Y'}
        self.assertEqual(output, add_column_based_on_null(event=input, field='last_4', new_field='last_4', new_value_if_null=None, new_value_if_not_null='Y'))

    # Test 4
    def test_add_column_based_on_null_when_not_null_both_params_entered(self):
        input = {'last_4': 0000}
        output = {'last_4': 'Y'}
        self.assertEqual(output, add_column_based_on_null(event=input, field='last_4', new_field='last_4', new_value_if_null='N', new_value_if_not_null='Y'))

    # Test 5
    def test_add_columns_with_default_add_columns(self):
        stuff_to_add = {'add_me': False, 'and_me': 123}

        input_event = {'just_one_key_to_start': 'stuff'}

        expected_output_event = {'add_me': False,
                                 'and_me': 123,
                                 'just_one_key_to_start': 'stuff'}

        self.assertEqual(expected_output_event, add_columns_with_default(input_event, field_and_default_dict=stuff_to_add))

    # Test 6
    def test_add_columns_with_default_add_columns_skip_existing(self):
        stuff_to_add = {'add_me': False, 'skip_me': 123}

        input_event = {'just_one_key_to_start': 'stuff',
                       'skip_me': 'please do not change me'}

        expected_output_event = {'add_me': False,
                                 'skip_me': 'please do not change me',
                                 'just_one_key_to_start': 'stuff'}

        self.assertEqual(expected_output_event, add_columns_with_default(input_event, field_and_default_dict=stuff_to_add))

    # Test 7
    def test_add_composite_key_key(self):
        input_event = {'product_id': 123456,
                       'product_name': 'my_product'}

        expected_output_event = {'product_id': 123456,
                                 'product_name': 'my_product',
                                 'product_id_name': '123456-my_product'}

        self.assertEqual(expected_output_event, add_composite_key(input_event, field_list=['product_id', 'product_name'], key_name='product_id_name'))

    # Test 8
    def test_add_duplicate_fields_single(self):
        suffix_to_add = 'add'

        input_event = {'start_with_me': 123}

        expected_output_event = {'start_with_me': 123,
                                 'start_with_me_add': 123}

        self.assertEqual(expected_output_event, add_duplicate_fields(input_event, field_name='start_with_me', suffix_or_suffix_list=suffix_to_add, keep_original=True))

    # Test 9
    def test_add_duplicate_fields_multiple(self):
        suffixes_to_add = ['add', 'add_me_too']

        input_event = {'start_with_me': 123}

        expected_output_event = {'start_with_me': 123,
                                 'start_with_me_add': 123,
                                 'start_with_me_add_me_too': 123}

        self.assertEqual(expected_output_event, add_duplicate_fields(input_event, field_name='start_with_me', suffix_or_suffix_list=suffixes_to_add, keep_original=True))

    # Test 10
    def test_add_duplicate_fields_multiple_remove_original(self):
        suffixes_to_add = ['add', 'add_me_too']

        input_event = {'start_with_me': 123}

        expected_output_event = {'start_with_me_add': 123,
                                 'start_with_me_add_me_too': 123}

        self.assertEqual(expected_output_event, add_duplicate_fields(input_event, field_name='start_with_me', suffix_or_suffix_list=suffixes_to_add, keep_original=False))

    # Test 11
    def test_add_suffix_single_field_default_separator(self):
        input_event = {'leave_me': 'my_name_stays',
                       'suffix_me': 'I want to be suffix_me_withthis'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'suffix_me_withthis': 'I want to be suffix_me_withthis'}

        self.assertEqual(expected_output_event, add_suffix(input_event, fields='suffix_me', suffix='withthis'))

    # Test 12
    def test_add_suffix_two_fields_default_separator(self):
        input_event = {'leave_me': 'my_name_stays',
                       'suffix_me': 'I want to be suffix_me_withthis',
                       'suffix_me_too': 'I want to be suffix_me_withthis'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'suffix_me_withthis': 'I want to be suffix_me_withthis',
                                 'suffix_me_too_withthis': 'I want to be suffix_me_withthis'}

        self.assertEqual(expected_output_event, add_suffix(input_event, fields=['suffix_me', 'suffix_me_too'], suffix='withthis'))

    # Test 13
    def test_add_suffix_single_field_new_separator(self):
        input_event = {'leave_me': 'my_name_stays',
                       'suffix_me': 'I want to be suffix_me---withthis'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'suffix_me---withthis': 'I want to be suffix_me---withthis'}

        self.assertEqual(expected_output_event, add_suffix(input_event, fields='suffix_me', suffix='withthis', separator='---'))

    # Test 14
    def test_add_suffix_two_fields_new_separator(self):
        input_event = {'leave_me': 'my_name_stays',
                       'suffix_me': 'I want to be suffix_me---withthis',
                       'suffix_me_too': 'I want to be suffix_me---withthis'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'suffix_me---withthis': 'I want to be suffix_me---withthis',
                                 'suffix_me_too---withthis': 'I want to be suffix_me---withthis'}

        self.assertEqual(expected_output_event, add_suffix(input_event, fields=['suffix_me', 'suffix_me_too'], suffix='withthis', separator='---'))

    # Test 15
    def test_add_suffix_field_not_in_event(self):
        input_event = {'leave_me': 'my_name_stays',
                       'suffix_me': 'I want to be suffix_me---withthis'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'suffix_me---withthis': 'I want to be suffix_me---withthis'}

        self.assertEqual(expected_output_event, add_suffix(input_event, fields=['suffix_me', 'skip_me'], suffix='withthis', separator='---'))

    # Test 16
    def test_convert_all_event_fields_to_snake_case(self):
        input_event = {'MakeThisSnakeCase': 'stuff_in_field',
                       'Make This Snake Case': 'stuff_in_field',
                       'keep_this_snake_case': 'stuff_in_field',
                       'makeThisSnakeCase': 'stuff_in_field',
                       'leavemealone': 'left this one alone',
                       '_metadata': {'event_type': 'ObjectName',
                                     'input_label': 'Label',
                                     'input_type': 'salesforce'}}

        output_event = {'make_this_snake_case': 'stuff_in_field',
                        'make_this_snake_case': 'stuff_in_field',
                        'keep_this_snake_case': 'stuff_in_field',
                        'make_this_snake_case': 'stuff_in_field',
                        'leavemealone': 'left this one alone',
                        '_metadata': {'event_type': 'ObjectName',
                                      'input_label': 'Label',
                                      'input_type': 'salesforce'}}

        self.assertEqual(output_event, convert_all_event_fields_to_snake_case(input_event))

    # Test 17
    def test_convert_dictionary_fields_to_string_single_dictionary_is_string(self):
        input_event = {'dump me': {'make me': 'a string',
                                   'change me too': 'into - string'}}
        output_event = convert_dictionary_fields_to_string(input_event, field_or_field_list='dump me')
        self.assertTrue(isinstance(output_event['dump me'], str))

    # Test 18
    def test_convert_dictionary_fields_to_string_single_dictionary_is_not_dict(self):
        input_event = {'dump me': {'make me': 'a string',
                                   'change me too': 'into - string'}}
        output_event = convert_dictionary_fields_to_string(input_event, field_or_field_list='dump me')
        self.assertFalse(isinstance(output_event['dump me'], dict))

    # Test 19
    def test_convert_dictionary_fields_to_string_multiple_dictionary_is_string(self):
        input_event = {'dump me': {'make me': 'a string',
                                   'change me too': 'into - string'},
                       'dump me too': {'make me': 'a string',
                                       'change me too': 'into - string'}
                       }
        output_event = convert_dictionary_fields_to_string(input_event, field_or_field_list=['dump me', 'dump me too'])
        self.assertTrue(isinstance(output_event['dump me'], str) and isinstance(output_event['dump me too'], str))

    # Test 20
    def test_convert_dictionary_fields_to_string_multiple_dictionary_only_first_is_string(self):
        input_event = {'dump me': {'make me': 'a string',
                                   'change me too': 'into - string'},
                       'let me be': {'leave me': 'a dict',
                                     'i do not like': 'to change'}
                       }
        output_event = convert_dictionary_fields_to_string(input_event, field_or_field_list=['dump me'])
        self.assertTrue(isinstance(output_event['dump me'], str))

    # Test 21
    def test_convert_dictionary_fields_to_string_multiple_dictionary_not_specified_is_still_a_dict(self):
        input_event = {'dump me': {'make me': 'a string',
                                   'change me too': 'into - string'},
                       'let me be': {'leave me': 'a dict',
                                     'i do not like': 'to change'}
                       }
        output_event = convert_dictionary_fields_to_string(input_event, field_or_field_list=['dump me'])
        self.assertTrue(isinstance(output_event['let me be'], dict))

    # Test 22
    def test_convert_empty_value_to_none_list_to_null(self):
        input_event = {'empty_list': [],
                       'full_list': ['stuff', 'more_stuff']}

        expected_output_event = {'empty_list': None,
                                 'full_list': ['stuff', 'more_stuff']}

        self.assertEqual(expected_output_event, convert_empty_value_to_none(input_event, key_name='empty_list'))

    # Test 23
    def test_convert_empty_value_to_none_list_string_to_null(self):
        input_event = {'empty_list': '[]',
                       'full_list': ['stuff', 'more_stuff']}

        expected_output_event = {'empty_list': None,
                                 'full_list': ['stuff', 'more_stuff']}

        self.assertEqual(expected_output_event, convert_empty_value_to_none(input_event, key_name='empty_list'))

    # Test 24
    def test_convert_empty_value_to_none_dict_to_null(self):
        input_event = {'empty_dict': {},
                       'full_dict': {'a key': 'a value', 'another_key': 'a value'}}

        expected_output_event = {'empty_dict': None,
                                 'full_dict': {'a key': 'a value', 'another_key': 'a value'}}

        self.assertEqual(expected_output_event, convert_empty_value_to_none(input_event, key_name='empty_dict'))

    # Test 25
    def test_convert_empty_value_to_none_dict_string_to_null(self):
        input_event = {'empty_dict': '{}',
                       'full_dict': {'a key': 'a value', 'another_key': 'a value'}}

        expected_output_event = {'empty_dict': None,
                                 'full_dict': {'a key': 'a value', 'another_key': 'a value'}}

        self.assertEqual(expected_output_event, convert_empty_value_to_none(input_event, key_name='empty_dict'))

    # Test 26
    def test_convert_empty_value_to_none_string(self):
        input = {'winner': ''}
        expected_output = {'winner': None}
        self.assertEqual(expected_output, convert_empty_value_to_none(input, 'winner'))

    # Test 27
    def test_convert_empty_value_to_none_not_empty(self):
        input = {'winner': 'not empty'}
        expected_output = {'winner': 'not empty'}
        self.assertEqual(expected_output, convert_empty_value_to_none(input, 'winner'))

    # Test 28
    def test_convert_empty_value_to_none_string_with_spaces_only_to_none(self):
        input = {'winner': '    '}
        expected_output = {'winner': None}
        self.assertEqual(expected_output, convert_empty_value_to_none(input, 'winner'))

    # test 29
    def test_convert_event_type_case_single_event_force_upper(self):
        input_event = {'_metadata': {'event_type': 'my_schema.my_table'}}

        expected_output_event = {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE'}}

        self.assertEqual(expected_output_event, convert_event_type_case(input_event, case_force_upper=True))

    # test 30
    def test_convert_event_type_case_list_event_force_upper(self):
        input_event = [{'_metadata': {'event_type': 'my_schema.my_table_one'}},
                       {'_metadata': {'event_type': 'My_schema.My_table_Two'}}]

        expected_output_event = [{'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE_ONE'}},
                                 {'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE_TWO'}}]
        self.assertEqual(expected_output_event, convert_event_type_case(input_event, case_force_upper=True))

    # test 31
    def test_convert_event_type_case_single_event_force_lower(self):
        input_event = {'_metadata': {'event_type': 'my_scheMA.my_table'}}

        expected_output_event = {'_metadata': {'event_type':  'my_schema.my_table'}}

        self.assertEqual(expected_output_event, convert_event_type_case(input_event, case_force_upper=False))

    # test 32
    def test_convert_event_type_case_list_event_force_lower(self):
        input_event = [{'_metadata': {'event_type': 'MY_SCHEMA.MY_TABLE_ONE'}},
                       {'_metadata': {'event_type': 'My_scheMA.MY_table_two'}}]

        expected_output_event = [{'_metadata': {'event_type': 'my_schema.my_table_one'}},
                                 {'_metadata': {'event_type': 'my_schema.my_table_two'}}]
        self.assertEqual(expected_output_event, convert_event_type_case(input_event, case_force_upper=False))

    # Test 33
    def test_convert_null_to_zero_list(self):
        input = {'a': None, 'b': None, 'c': 40, 'd': 20}
        expected_output = {'a': None, 'b': 0, 'c': 40, 'd': 20}
        self.assertEqual(expected_output, convert_null_to_zero(input, field_or_field_list=['b', 'c', 'd']))

    # Test 34
    def test_convert_null_to_zero_single_field(self):
        input = {'a': None, 'b': None, 'c': 40, 'd': 20}
        expected_output = {'a': None, 'b': 0, 'c': 40, 'd': 20}
        self.assertEqual(expected_output, convert_null_to_zero(input, field_or_field_list='b'))

    # Test 35
    def test_convert_null_to_zero_single_field_non_zero(self):
        input = {'a': None, 'b': None, 'c': 40, 'd': 20}
        expected_output = {'a': None, 'b': None, 'c': 40, 'd': 20}
        self.assertEqual(expected_output, convert_null_to_zero(input, field_or_field_list='c'))

    # Test 36
    def test_convert_spaces_and_special_characters_to_underscore(self):
        input_string = '$Scr "get-rid^-of-the@" special #characters%&space'
        output_string = '_scr__get_rid__of_the___special__characters__space'
        self.assertEqual(output_string, convert_spaces_and_special_characters_to_underscore(input_string))

    # Test 37
    def test_convert_string_to_snake_case_from_title_case_without_spaces(self):
        input_string = 'MakeThisSnakeCase'
        output_string = 'make_this_snake_case'
        self.assertEqual(output_string, convert_string_to_snake_case(input_string))

    # Test 38
    def test_convert_string_to_snake_case_from_title_case_with_spaces(self):
        input_string = 'Make This Snake Case'
        output_string = 'make_this_snake_case'
        self.assertEqual(output_string, convert_string_to_snake_case(input_string))

    # Test 39
    def test_convert_string_to_snake_case_already_snake_case(self):
        input_string = 'keep_this_snake_case'
        output_string = 'keep_this_snake_case'
        self.assertEqual(output_string, convert_string_to_snake_case(input_string))

    # Test 40
    def test_convert_string_to_snake_case_from_camel_case(self):
        input_string = 'makeThisSnakeCase'
        output_string = 'make_this_snake_case'
        self.assertEqual(output_string, convert_string_to_snake_case(input_string))

    # Test 41
    def test_convert_values_to_none_single_field_all_values(self):
        input_event = {'leave_alone': 1,
                       'change_to_none': 'NaN'}

        output_event = {'leave_alone': 1,
                        'change_to_none': None}

        self.assertEqual(output_event, convert_values_to_none(input_event, field_or_field_list='change_to_none'))

    # Test 42
    def test_convert_values_to_none_multiple_fields_all_values(self):
        input_event = {'leave_alone': 1,
                       'change_to_none': 'NaN',
                       'change_me_too': 5.75}

        output_event = {'leave_alone': 1,
                        'change_to_none': None,
                        'change_me_too': None}

        self.assertEqual(output_event, convert_values_to_none(input_event, field_or_field_list=['change_to_none', 'change_me_too']))

    # Test 43
    def test_convert_values_to_none_single_field_single_value_change(self):
        input_event = {'leave_alone': 1,
                       'change_to_none': 'NaN'}

        output_event = {'leave_alone': 1,
                        'change_to_none': None}

        self.assertEqual(output_event, convert_values_to_none(input_event, field_or_field_list='change_to_none', field_values='NaN'))

    # Test 44
    def test_convert_values_to_none_single_field_single_value_dont_change(self):
        input_event = {'leave_alone': 1,
                       'change_to_none': 'Something Else'}

        output_event = {'leave_alone': 1,
                        'change_to_none': 'Something Else'}

        self.assertEqual(output_event, convert_values_to_none(input_event, field_or_field_list='change_to_none', field_values='NaN'))

    # Test 45
    def test_convert_values_to_none_single_field_value_list_change(self):
        input_event = {'leave_alone': 1,
                       'change_to_none': 'NaN',
                       'also_change_to_none': 2}

        output_event = {'leave_alone': 1,
                        'change_to_none': None,
                        'also_change_to_none': None}

        self.assertEqual(output_event, convert_values_to_none(input_event, field_or_field_list=['change_to_none', 'also_change_to_none'], field_values=['NaN', 2]))

    # test 46
    def test_flatten_json_input_is_list_keep_original_true(self):
        input = {"batters": ['chocolate', 'strawberry', 'vanilla']}

        expected_output = {"batters": ['chocolate', 'strawberry', 'vanilla']}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=True)
        self.assertEqual(expected_output, output_event)

    # test 47
    def test_flatten_json_input_is_list_keep_original_false(self):
        input = {"batters": ['chocolate', 'strawberry', 'vanilla']}
        expected_output = {"batters": ['chocolate', 'strawberry', 'vanilla']}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=False)
        self.assertEqual(expected_output, output_event)

    # test 48
    def test_flatten_json_input_is_empty_dict_keep_original_false(self):
        input = {"batters": {}}
        expected_output = {}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=False)
        self.assertEqual(expected_output, output_event)

    # test 49
    def test_flatten_json_input_is_empty_dict_keep_original_true(self):
        input = {"batters": {}}
        expected_output = {"batters": {}}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=True)
        self.assertEqual(expected_output, output_event)

    # Test 50
    def test_flatten_json_from_string_1_level_keep_original_false_new_keep_as_json(self):
        input = {"cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {'cones_99 flake': '2.4',
                           'cones_cake': {},
                           'cones_sugar': [],
                           'cones_waffle': {"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}}

        output_event = flatten_json(input, field_or_field_list='cones', levels=1, keep_original=False)
        self.assertEqual(expected_output, output_event)

    # Test 51
    def test_flatten_json_from_string_1_level_keep_original_true_new_keep_as_json(self):
        input = {"cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {'cones': {'99 Flake': '2.4',
                                     'cake': {},
                                     'sugar': [],
                                     'waffle': {'chocolate': 'No',
                                                'vanilla': {'extra_charge': '2', 'sprinkles': 'Yes'}}},
                           'cones_99 flake': '2.4',
                           'cones_cake': {},
                           'cones_sugar': [],
                           'cones_waffle': {'chocolate': 'No',
                                            'vanilla': {'extra_charge': '2', 'sprinkles': 'Yes'}}}

        output_event = flatten_json(input, field_or_field_list='cones', levels=1, keep_original=True)
        self.assertEqual(expected_output, output_event)

    # Test 52
    def test_flatten_json_from_string_1_level_keep_original_false_dump_to_string(self):
        input = {"cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {'cones_99 flake': '2.4',
                           'cones_cake': '{}',
                           'cones_sugar': [],
                           'cones_waffle': '{"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}'}

        output_event = flatten_json(input, field_or_field_list='cones', levels=1, keep_original=False, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 53
    def test_flatten_json_from_string_1_level_keep_original_true_dump_to_string(self):
        input = {"cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {'cones': '{"sugar":[],"cake":{},"99 Flake":"2.4","waffle":{"vanilla":{"sprinkles":"Yes","extra_charge":"2"},"chocolate":"No"}}',
                           'cones_99 flake': '2.4',
                           'cones_cake': '{}',
                           'cones_sugar': [],
                           'cones_waffle': '{"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}'}

        output_event = flatten_json(input, field_or_field_list='cones', levels=1, keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 54
    def test_flatten_json_from_dict_1_level_keep_original_false_dump_to_string(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters_blueberry': '{"creaminess": "light", "sweetness": "super"}',
                           'batters_chocolate': '{"creaminess": "moderate", "sweetness": "very"}',
                           'batters_vanilla': '{"creaminess": "very", "sweetness": "medium"}'}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=False, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 55
    def test_flatten_json_from_dict_1_level_keep_original_false_keep_as_json(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters_blueberry': {"creaminess": "light", "sweetness": "super"},
                           'batters_chocolate': {"creaminess": "moderate", "sweetness": "very"},
                           'batters_vanilla': {"creaminess": "very", "sweetness": "medium"}}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=False, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 56
    def test_flatten_json_from_dict_1_level_keep_original_true_dump_to_string(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters': '{"Vanilla": {"creaminess": "very", "sweetness": "medium"}, '
                                      '"Chocolate": {"creaminess": "moderate", "sweetness": "very"}, '
                                      '"Blueberry": {"creaminess": "light", "sweetness": "super"}}',
                           'batters_blueberry': '{"creaminess": "light", "sweetness": "super"}',
                           'batters_chocolate': '{"creaminess": "moderate", "sweetness": "very"}',
                           'batters_vanilla': '{"creaminess": "very", "sweetness": "medium"}'}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 57
    def test_flatten_json_from_dict_1_level_keep_original_true_keep_as_json(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters': {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                                       "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                                       "Blueberry": {"creaminess": "light", "sweetness": "super"}},
                           'batters_blueberry': {"creaminess": "light", "sweetness": "super"},
                           'batters_chocolate': {"creaminess": "moderate", "sweetness": "very"},
                           'batters_vanilla': {"creaminess": "very", "sweetness": "medium"}}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 58
    def test_flatten_json_from_dict_2_level_keep_original_false(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters_blueberry_creaminess': 'light',
                           'batters_blueberry_sweetness': 'super',
                           'batters_chocolate_creaminess': 'moderate',
                           'batters_chocolate_sweetness': 'very',
                           'batters_vanilla_creaminess': 'very',
                           'batters_vanilla_sweetness': 'medium'}

        output_event = flatten_json(input, field_or_field_list='batters', levels=2, keep_original=False)
        self.assertEqual(expected_output, output_event)

    # Test 59
    def test_flatten_json_from_dict_2_level_keep_original_true_as_string(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters': '{"Vanilla": {"creaminess": "very", "sweetness": "medium"}, '
                                      '"Chocolate": {"creaminess": "moderate", "sweetness": "very"}, '
                                      '"Blueberry": {"creaminess": "light", "sweetness": "super"}}',
                           'batters_blueberry_creaminess': 'light',
                           'batters_blueberry_sweetness': 'super',
                           'batters_chocolate_creaminess': 'moderate',
                           'batters_chocolate_sweetness': 'very',
                           'batters_vanilla_creaminess': 'very',
                           'batters_vanilla_sweetness': 'medium'}

        output_event = flatten_json(input, field_or_field_list='batters', levels=2, keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 60
    def test_flatten_json_from_dict_2_level_keep_original_true_keep_as_json(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters': {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                                       "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                                       "Blueberry": {"creaminess": "light", "sweetness": "super"}},
                           'batters_blueberry_creaminess': 'light',
                           'batters_blueberry_sweetness': 'super',
                           'batters_chocolate_creaminess': 'moderate',
                           'batters_chocolate_sweetness': 'very',
                           'batters_vanilla_creaminess': 'very',
                           'batters_vanilla_sweetness': 'medium'}

        output_event = flatten_json(input, field_or_field_list='batters', levels=2, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 61
    def test_flatten_json_list_n_levels_2_fields(self):
        input = {
            "cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}",
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}"
        }
        expected_output = {
            'cones': '{"sugar":[],"cake":{},"99 Flake":"2.4","waffle":{"vanilla":{"sprinkles":"Yes","extra_charge":"2"},"chocolate":"No"}}',
            'cones_99 flake': '2.4',
            'cones_cake': '{}',
            'cones_sugar': [],
            'cones_waffle': '{"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}',
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}",
            "ice_cream_chocolate": 1.99,
            "ice_cream_vanilla": 0.99}

        output_event = flatten_json(input, field_or_field_list=['cones', 'ice_cream'], levels=1,
                                    keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 62
    def test_flatten_json_from_string_3_level_keep_original_false_new(self):
        input = {"cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {'cones_99 flake': 2.4,
                           'cones_sugar': [],
                           'cones_waffle_chocolate': 'No',
                           'cones_waffle_vanilla_extra_charge': '2',
                           'cones_waffle_vanilla_sprinkles': 'Yes'}

        output_event = flatten_json(input, field_or_field_list='cones', levels=3, keep_original=False)
        self.assertEqual(expected_output, output_event)

    # Test 63
    def test_flatten_json_from_string_3_level_keep_original_true_new(self):
        input = {
            "cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {
            'cones': '{"sugar":[],"cake":{},"99 Flake":"2.4","waffle":{"vanilla":{"sprinkles":"Yes","extra_charge":"2"},"chocolate":"No"}}',
            'cones_99 flake': 2.4,
            'cones_sugar': [],
            'cones_waffle_chocolate': 'No',
            'cones_waffle_vanilla_extra_charge': '2',
            'cones_waffle_vanilla_sprinkles': 'Yes'
        }

        output_event = flatten_json(input, field_or_field_list='cones', levels=3, keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 64
    def test_flatten_json_capital_field(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters': '{"Vanilla": {"creaminess": "very", "sweetness": "medium"}, '
                                      '"Chocolate": {"creaminess": "moderate", "sweetness": "very"}, '
                                      '"Blueberry": {"creaminess": "light", "sweetness": "super"}}',
                           'batters_blueberry_creaminess': 'light',
                           'batters_blueberry_sweetness': 'super',
                           'batters_chocolate_creaminess': 'moderate',
                           'batters_chocolate_sweetness': 'very',
                           'batters_vanilla_creaminess': 'very',
                           'batters_vanilla_sweetness': 'medium'}

        output_event = flatten_json(input, field_or_field_list='Batters', levels=2, keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 65
    def test_flatten_json_list_n_levels_1_field(self):
        input = {
            "cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}",
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}"
        }
        expected_output = {
            'cones': '{"sugar":[],"cake":{},"99 Flake":"2.4","waffle":{"vanilla":{"sprinkles":"Yes","extra_charge":"2"},"chocolate":"No"}}',
            'cones_99 flake': '2.4',
            'cones_cake': '{}',
            'cones_sugar': [],
            'cones_waffle': '{"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}',
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}",
        }

        output_event = flatten_json(input, field_or_field_list='cones', levels=1, keep_original=True, dump_to_string=True)
        self.assertEqual(expected_output, output_event)

    # Test 66
    def test_flatten_json_from_string_3_level_keep_original_true_dump_string_false(self):
        input = {
            "cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}"}
        expected_output = {
            'cones': {"sugar": [], "cake": {}, "99 Flake": "2.4", "waffle": {"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}},
            'cones_99 flake': 2.4,
            'cones_sugar': [],
            'cones_waffle_chocolate': 'No',
            'cones_waffle_vanilla_extra_charge': '2',
            'cones_waffle_vanilla_sprinkles': 'Yes'
        }

        output_event = flatten_json(input, field_or_field_list='cones', levels=3, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 67
    def test_flatten_json_input_is_list_keep_original_true_dump_string_false(self):
        input = {"batters": ['chocolate', 'strawberry', 'vanilla']}

        expected_output = {"batters": ['chocolate', 'strawberry', 'vanilla']}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 68
    def test_flatten_json_input_is_empty_dict_keep_original_true_dump_string_false(self):
        input = {"batters": {}}
        expected_output = {"batters": {}}

        output_event = flatten_json(input, field_or_field_list='batters', levels=1, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 69
    def test_flatten_json_capital_field_dump_string_false(self):
        input = {"batters": {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                             "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                             "Blueberry": {"creaminess": "light", "sweetness": "super"}}}

        expected_output = {'batters': {"Vanilla": {"creaminess": "very", "sweetness": "medium"},
                                       "Chocolate": {"creaminess": "moderate", "sweetness": "very"},
                                       "Blueberry": {"creaminess": "light", "sweetness": "super"}},
                           'batters_blueberry_creaminess': 'light',
                           'batters_blueberry_sweetness': 'super',
                           'batters_chocolate_creaminess': 'moderate',
                           'batters_chocolate_sweetness': 'very',
                           'batters_vanilla_creaminess': 'very',
                           'batters_vanilla_sweetness': 'medium'}

        output_event = flatten_json(input, field_or_field_list='Batters', levels=2, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 70
    def test_flatten_json_list_n_levels_1_field_dump_string_false(self):
        input = {
            "cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}",
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}"
        }
        expected_output = {
            'cones': {"sugar": [], "cake": {}, "99 Flake": "2.4", "waffle": {"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}},
            'cones_99 flake': '2.4',
            'cones_cake': {},
            'cones_sugar': [],
            'cones_waffle': {"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"},
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}",
        }

        output_event = flatten_json(input, field_or_field_list='cones', levels=1, keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 71
    def test_flatten_json_list_n_levels_2_fields_dump_string_false(self):
        input = {
            "cones": "{\"sugar\":[],\"cake\":{},\"99 Flake\":\"2.4\",\"waffle\":{\"vanilla\":{\"sprinkles\":\"Yes\",\"extra_charge\":\"2\"},\"chocolate\":\"No\"}}",
            "ice_cream": "{\"chocolate\":1.99,\"vanilla\":0.99}"
        }
        expected_output = {
            'cones': {"sugar": [], "cake": {}, "99 Flake": "2.4", "waffle": {"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"}},
            'cones_99 flake': '2.4',
            'cones_cake': {},
            'cones_sugar': [],
            'cones_waffle': {"vanilla": {"sprinkles": "Yes", "extra_charge": "2"}, "chocolate": "No"},
            "ice_cream": {"chocolate": 1.99, "vanilla": 0.99},
            "ice_cream_chocolate": 1.99,
            "ice_cream_vanilla": 0.99}

        output_event = flatten_json(input, field_or_field_list=['cones', 'ice_cream'], levels=1,
                                    keep_original=True, dump_to_string=False)
        self.assertEqual(expected_output, output_event)

    # Test 72
    def test_flatten_json_1_level_and_dumps_using_ast(self):
        input_event = {'my_field': "{\"a\": None, \"b\": 11, \"c\": 3297, \"d\": 1497, \"e\": 11}"}
        output_event = {'my_field_a': None,
                        'my_field_b': 11,
                        'my_field_c': 3297,
                        'my_field_d': 1497,
                        'my_field_e': 11}
        self.assertEqual(output_event, flatten_json_1_level(event=input_event, field_name='my_field', field_name_underscore='my_field_', dump_to_string=True))

    # Test 73
    def test_map_key_in_dictionary_to_value_clean_transform(self):
        mapping_dict = {1: 'first',
                        2: 'second',
                        3: 'third'}

        input_event = {'number_field': 2,
                       '_metadata': {'event_type': 'event_type_name'}
                       }

        expected_output_event = {'number_field': 2,
                                 'number_field_with_name': 'second',
                                 '_metadata': {'event_type': 'event_type_name'}}

        self.assertEqual(expected_output_event, map_key_in_dictionary_to_value(input_event, mapping_dict, existing_column='number_field', new_column='number_field_with_name', allow_nulls=False))

    # Test 74
    def test_map_key_in_dictionary_to_value_null_allowed(self):
        mapping_dict = {1: 'first',
                        2: 'second',
                        3: 'third'}

        input_event = {'number_field': None,
                       '_metadata': {'event_type': 'event_type_name'}
                       }

        expected_output_event = {'number_field': None,
                                 'number_field_with_name': None,
                                 '_metadata': {'event_type': 'event_type_name'}}

        self.assertEqual(expected_output_event, map_key_in_dictionary_to_value(input_event, mapping_dict, existing_column='number_field', new_column='number_field_with_name', allow_nulls=True))

    # Test 75
    def test_map_key_in_dictionary_to_value_missing_error(self):
        mapping_dict = {1: 'first',
                        2: 'second',
                        3: 'third'}

        input_event = {'number_field': 7,
                       '_metadata': {'event_type': 'event_type_name'}
                       }

        with self.assertRaises(BaseException) as cm:
            map_key_in_dictionary_to_value(input_event, mapping_dict, existing_column='number_field', new_column='number_field_with_name', allow_nulls=False)

        self.assertEqual(str(cm.exception), 'Missing enum transform event_type_name number_field')

    # Test 76
    def test_map_key_in_dictionary_to_value_value_null_error(self):
        mapping_dict = {1: 'first',
                        2: 'second',
                        3: 'third'}

        input_event = {'number_field': None,
                       '_metadata': {'event_type': 'event_type_name'}
                       }

        with self.assertRaises(BaseException) as cm:
            map_key_in_dictionary_to_value(input_event, mapping_dict, existing_column='number_field', new_column='number_field_with_name', allow_nulls=False)

        self.assertEqual(str(cm.exception), 'Missing enum transform event_type_name number_field')

    # Test 77
    def test_map_value_in_list_to_dictionary_key_successful_mapping(self):
        input_event = {"_metadata": {"event_type": "sweets"},
                       "type": "donut"}

        breakfast_item_categories = {"baked good": ["donut", "cake", "croissant"],
                                     "beverages": ["coffee", "tea", "orange juice", "grapefruit juice"]}

        expected_output_event = {'_metadata': {'event_type': 'sweets'},
                                 'breakfast_item_category': 'baked good',
                                 'type': 'donut'}

        self.assertEqual(expected_output_event, map_value_in_list_to_dictionary_key(input_event, mapping_dict_with_lists=breakfast_item_categories,
                                                                                    existing_column='type', new_column='breakfast_item_category',
                                                                                    allow_nulls=False, passthrough=True))

    # Test 78
    def test_map_value_in_list_to_dictionary_key_no_mapping_allow_nulls_false_passthrough_true(self):
        input_event = {"_metadata": {"event_type": "sweets"},
                       "type": "donut"}

        breakfast_item_categories = {"baked good": ["cake", "croissant"],
                                     "beverages": ["coffee", "tea", "orange juice", "grapefruit juice"]}

        expected_output_event = {'_metadata': {'event_type': 'sweets'},
                                 'breakfast_item_category': 'donut',
                                 'type': 'donut'}

        self.assertEqual(expected_output_event,
                         map_value_in_list_to_dictionary_key(input_event, mapping_dict_with_lists=breakfast_item_categories,
                                                             existing_column='type', new_column='breakfast_item_category',
                                                             allow_nulls=False, passthrough=True))

    # Test 79
    def test_map_value_in_list_to_dictionary_key_no_mapping_allow_nulls_false_passthrough_false(self):
        input_event = {"_metadata": {"event_type": "sweets"},
                       "type": "donut",
                       }

        breakfast_item_categories = {"baked_goods": ["cake", "croissant"],
                                     "beverages": ["coffee", "tea", "orange juice", "grapefruit juice"]}

        with self.assertRaises(Exception):
            map_value_in_list_to_dictionary_key(input_event, mapping_dict_with_lists=breakfast_item_categories,
                                                existing_column='type',
                                                new_column='breakfast_item_category',
                                                allow_nulls=False, passthrough=False)

    # Test 80
    def test_map_value_in_list_to_dictionary_key_no_mapping_allow_nulls_true_passthrough_true(self):
        input_event = {"_metadata": {"event_type": "sweets"},
                       "type": "donut"}

        breakfast_item_categories = {"baked good": ["cake", "croissant"],
                                     "beverages": ["coffee", "tea", "orange juice", "grapefruit juice"]}
        expected_output_event = {'_metadata': {'event_type': 'sweets'},
                                 'breakfast_item_category': 'donut',
                                 'type': 'donut'}

        self.assertEqual(expected_output_event, map_value_in_list_to_dictionary_key(input_event, mapping_dict_with_lists=breakfast_item_categories,
                                                                                    existing_column='type', new_column='breakfast_item_category',
                                                                                    allow_nulls=True, passthrough=True))

    # Test 81
    def test_map_value_in_list_to_dictionary_key_no_mapping_allow_nulls_true_passthrough_false(self):
        input_event = {"_metadata": {"event_type": "sweets"},
                       "type": "donut"}

        breakfast_item_categories = {"baked good": ["cake", "croissant"],
                                     "beverages": ["coffee", "tea", "orange juice", "grapefruit juice"]}

        expected_output_event = {'_metadata': {'event_type': 'sweets'},
                                 'breakfast_item_category': None,
                                 'type': 'donut'}

        self.assertEqual(expected_output_event, map_value_in_list_to_dictionary_key(input_event, mapping_dict_with_lists=breakfast_item_categories,
                                                                                    existing_column='type', new_column='breakfast_item_category',
                                                                                    allow_nulls=True, passthrough=False))

    # Test 82
    def test_mark_for_delete(self):
        test_mark_for_delete_input = """{"id": 13,
                                         "table_name": "alooma_test",
                                         "primary_key": "456789",
                                         "old_row_json": {"id":6,
                                                     "name":"User 6",
                                                     "created_at":"2017-08-23T05:01:51.753963",
                                                     "updated_at":"2017-08-26T15:27:13.455902"},
                                      "_metadata": {"event_type": "test"}}"""

        expected_output_event = {'_metadata': {'event_type': 'alooma_test',
                                               'table': 'alooma_test'},
                                 'created_at': '2017-08-23T05:01:51.753963',
                                 'id': 6,
                                 'mark_for_delete': True,
                                 'name': 'User 6',
                                 'updated_at': '2017-08-26T15:27:13.455902'}

        input_event = json.loads(test_mark_for_delete_input)
        input_event["old_row_json"] = json.dumps(input_event["old_row_json"])

        self.assertEqual(expected_output_event, mark_for_delete(input_event))

    # Test 83
    def test_parse_list_of_json_and_concat_keep_original_true(self):
        input_event = {'list_of_dicts': [{'key_to_concat': 123, 'key_to_ignore': 'abc'},
                                         {'key_to_concat': 456, 'key_to_ignore': 'def'},
                                         {'key_to_concat': 789, 'key_to_ignore': 'ghi'}]}

        expected_output_event = {'list_of_dicts': [{'key_to_concat': 123, 'key_to_ignore': 'abc'},
                                                   {'key_to_concat': 456, 'key_to_ignore': 'def'},
                                                   {'key_to_concat': 789, 'key_to_ignore': 'ghi'}],
                                 'list_of_dicts_key_to_concats': [123, 456, 789]}

        self.assertEqual(expected_output_event, parse_list_of_json_and_concat(input_event, field_name='list_of_dicts', keep_original=True, field_to_keep='key_to_concat'))

    # Test 84
    def test_parse_list_of_json_and_concat_keep_original_false(self):
        input_event = {'list_of_dicts': [{'key_to_concat': 123, 'key_to_ignore': 'abc'},
                                         {'key_to_concat': 456, 'key_to_ignore': 'def'},
                                         {'key_to_concat': 789, 'key_to_ignore': 'ghi'}]}

        expected_output_event = {'list_of_dicts_key_to_concats': [123, 456, 789]}

        self.assertEqual(expected_output_event, parse_list_of_json_and_concat(input_event, field_name='list_of_dicts', keep_original=False, field_to_keep='key_to_concat'))

    # Test 85
    def test_remove_duplicate_field_remove(self):
        input_event = {'Im Key': 'I am repeated information',
                       'im_key': 'I am repeated information'}

        expected_output_event = {'Im Key': 'I am repeated information'}

        self.assertEqual(expected_output_event, remove_duplicate_field(input_event, field_to_keep='Im Key', field_to_discard='im_key'))

    # Test 86
    def test_remove_duplicate_field_remove_keep_field_none(self):
        input_event = {'Im Key': None,
                       'im_key': 'I should be kept'}

        expected_output_event = {'im_key': 'I should be kept'}

        self.assertEqual(expected_output_event, remove_duplicate_field(input_event, field_to_keep='Im Key', field_to_discard='im_key'))

    # Test 87
    def test_remove_duplicate_field_missing_a_field_no_discard(self):
        input_event = {'im useless': None,
                       'keep_me': 'I should be kept'}

        expected_output_event = {'im useless': None,
                                 'keep_me': 'I should be kept'}

        self.assertEqual(expected_output_event, remove_duplicate_field(input_event, field_to_keep='keep_me', field_to_discard='discard_me'))

    # Test 88
    def test_remove_duplicate_field_missing_a_field_keep_discard(self):
        input_event = {'im useless': None,
                       'discard_me': 'I stay Anyway'}

        expected_output_event = {'im useless': None,
                                 'discard_me': 'I stay Anyway'}

        self.assertEqual(expected_output_event, remove_duplicate_field(input_event, field_to_keep='keep_me', field_to_discard='discard_me'))

    # Test 89
    def test_remove_outer_key_remove(self):
        input_event = {'a key': 'stuff',
                       'nested_stuff': {'field_one': 1,
                                        'field_two': 2,
                                        'field_three': 3}
                       }

        expected_output_event = {'a key': 'stuff',
                                 'field_one': 1,
                                 'field_two': 2,
                                 'field_three': 3
                                 }

        self.assertEqual(expected_output_event, remove_outer_key(input_event, key_name='nested_stuff'))

    # Test 90
    def test_remove_outer_key_no_dict(self):
        input_event = {'a key': 'stuff',
                       'nested_stuff': {'field_one': 1,
                                        'field_two': 2,
                                        'field_three': 3}
                       }

        expected_output_event = {'a key': 'stuff',
                                 'nested_stuff': {'field_one': 1,
                                                  'field_two': 2,
                                                  'field_three': 3}
                                 }

        self.assertEqual(expected_output_event, remove_outer_key(input_event, key_name='a key'))

    # Test 91
    def test_remove_outer_key_has_key(self):
        input = {'remove_me': {'i want to be top level': 'keep me',
                               'i want to be top level too': 'keep me too'}}

        expected_output = {'i want to be top level': 'keep me',
                           'i want to be top level too': 'keep me too'}

        self.assertEqual(expected_output, remove_outer_key(input, key_name='remove_me'))

    # Test 92
    def test_remove_outer_key_missing_key(self):
        input = {'remove_me': {'i want to be top level': 'keep me',
                               'i want to be top level too': 'keep me too'}}

        expected_output = {'remove_me': {'i want to be top level': 'keep me',
                                         'i want to be top level too': 'keep me too'}}

        self.assertEqual(expected_output, remove_outer_key(input, key_name='i_dont_exist'))

    # Test 93
    def test_remove_outer_key_has_key_and_nest(self):
        input = {'remove_me': {'i want to be top level': 'keep me',
                               'i want to be top level too': 'keep me too',
                               'My children stay nested': {'one down': 'mr one', 'two down': 'ms two', 'has more nest': {'way down': 'mr way', 'way down again': 'ms way'}}}}

        expected_output = {'i want to be top level': 'keep me',
                           'i want to be top level too': 'keep me too',
                           'My children stay nested': {'one down': 'mr one', 'two down': 'ms two', 'has more nest': {'way down': 'mr way', 'way down again': 'ms way'}}}

        self.assertEqual(expected_output, remove_outer_key(input, key_name='remove_me'))

    # Test 94
    def test_remove_starting_characters_from_keys_one_char(self):
        input_event = {'_metadata': {},
                       '$strip_me': 'no more $ in key',
                       '$strip_me_too': 'no more $ in key',
                       '_dont_strip': 'leave my underscore',
                       'nothing_here': 'nothing special'}

        expected_output_event = {'_metadata': {},
                                 '_dont_strip': 'leave my underscore',
                                 'nothing_here': 'nothing special',
                                 'strip_me_too': 'no more $ in key',
                                 'strip_me': 'no more $ in key'}

        self.assertEqual(expected_output_event, remove_starting_characters_from_keys(input_event, starting_characters='$'))

    # Test 95
    def test_remove_starting_characters_from_keys_many_char(self):
        input_event = {'_metadata': {},
                       'MY$-strip_me': 'no more MY$- in key',
                       'MY$-strip_me_too': 'no more MY$- in key',
                       '_dont_strip': 'leave_my_underscore',
                       'nothing_here': 'nothing_special'}

        expected_output_event = {'_metadata': {},
                                 '_dont_strip': 'leave_my_underscore',
                                 'nothing_here': 'nothing_special',
                                 'strip_me': 'no more MY$- in key',
                                 'strip_me_too': 'no more MY$- in key'}

        self.assertEqual(expected_output_event, remove_starting_characters_from_keys(input_event, starting_characters='MY$-'))

    # Test 96
    def test_remove_starting_characters_from_keys_no_keys_present(self):
        input_event = {'_metadata': {},
                       'nothing_here': 'nothing to strip',
                       'nothing_here_either': 'nothing to strip'}

        expected_output_event = {'_metadata': {},
                                 'nothing_here': 'nothing to strip',
                                 'nothing_here_either': 'nothing to strip'}

        self.assertEqual(expected_output_event, remove_starting_characters_from_keys(input_event, starting_characters='$'))

    # Test 97
    def test_remove_starting_characters_from_keys_starts_with_part(self):
        input_event = {'_metadata': {},
                       '$$strip_me': 'starts with two - strimp em',
                       '$strip_me': 'starts with just one - stays here'}

        expected_output_event = {'_metadata': {},
                                 'strip_me': 'starts with two - strimp em',
                                 '$strip_me': 'starts with just one - stays here'}

        self.assertEqual(expected_output_event, remove_starting_characters_from_keys(input_event, starting_characters='$$'))

    # Test 98
    def test_remove_starting_characters_from_sub_field(self):
        input_event = {'$strip_my_subs': {'$strip_me': 'strimp em',
                                          '$and_me': 'strip em too',
                                          'not_me': 'I never change'}}

        expected_output_event = {'$strip_my_subs': {'strip_me': 'strimp em',
                                                    'and_me': 'strip em too',
                                                    'not_me': 'I never change'}}

        self.assertEqual(expected_output_event, remove_starting_characters_from_keys(input_event, starting_characters='$', field_with_json='$strip_my_subs'))

    # Test 99
    def test_remove_starting_characters_from_sub_field_missing_key(self):
        input_event = {'$strip_my_subs': {'$strip_me': 'strimp em',
                                          '$and_me': 'strip em too',
                                          'not_me': 'I never change'}}

        expected_output_event = {'$strip_my_subs': {'$strip_me': 'strimp em',
                                                    '$and_me': 'strip em too',
                                                    'not_me': 'I never change'}}

        self.assertEqual(expected_output_event, remove_starting_characters_from_keys(input_event, starting_characters='$', field_with_json='not_in_event'))

    # Test 100
    def test_trim_whitespace(self):
        input = {'strip': '  this is my example               '}
        output = {'strip': 'this is my example'}
        self.assertEqual(output, remove_whitespace(input, field_or_field_list='strip'))

    # Test 101
    def test_remove_whitespace_list(self):
        input = {'strip': '  this is my example               ',
                 'strip me too': '  this is my example'}
        output = {'strip': 'this is my example',
                  'strip me too': 'this is my example'}
        self.assertEqual(output, remove_whitespace(input, field_or_field_list=['strip', 'strip me too']))

    # Test 102
    def test_remove_whitespace_only_specifiy_one(self):
        input = {'strip': '  this is my example               ',
                 'strip me too': '  this is my example'}
        output = {'strip': 'this is my example',
                  'strip me too': '  this is my example'}
        self.assertEqual(output, remove_whitespace(input, field_or_field_list=['strip']))

    # Test 103
    def test_remove_whitespace_has_an_int(self):
        input = {'strip': 1}
        output = {'strip': 1}
        self.assertEqual(output, remove_whitespace(input, field_or_field_list=['strip']))

    # Test 104
    def test_rename_fields_one_field_in_event(self):
        input_event = {'leave_me': 'my_name_stays',
                       'change_me': 'My new name is: i_changed'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'i_changed': 'My new name is: i_changed'}

        self.assertEqual(expected_output_event, rename_fields(input_event, field_dict={'change_me': 'i_changed'}))

    # Test 105
    def test_rename_fields_one_field_not_in_event(self):
        input_event = {'leave_me': 'my_name_stays',
                       'change_me': 'My new name is: i_changed'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'change_me': 'My new name is: i_changed'}

        self.assertEqual(expected_output_event, rename_fields(input_event, field_dict={'skip_me': 'not_in_event'}))

    # Test 106
    def test_rename_fields_two_fields_in_event(self):
        input_event = {'leave_me': 'my_name_stays',
                       'change_me': 'My new name is: i_changed',
                       'change_me_too': 'My new name is: i_changed_too'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'i_changed': 'My new name is: i_changed',
                                 'i_changed_too': 'My new name is: i_changed_too'}

        self.assertEqual(expected_output_event, rename_fields(input_event, field_dict={'change_me': 'i_changed', 'change_me_too': 'i_changed_too'}))

    # Test 107
    def test_rename_fields_two_fields_one_in_event(self):
        input_event = {'leave_me': 'my_name_stays',
                       'change_me': 'My new name is: i_changed'}

        expected_output_event = {'leave_me': 'my_name_stays',
                                 'i_changed': 'My new name is: i_changed'}

        self.assertEqual(expected_output_event, rename_fields(input_event, field_dict={'change_me': 'i_changed', 'skip_me': 'not_in_event'}))

    # Test 108
    def test_rename_fields_raise_exception(self):
        rename_field_dict = {'im_similar': 'properties_user_id',
                             'imsimilar': 'properties_user_id'}
        input_event = {'im_similar': 2,
                       'imsimilar': 3}

        with self.assertRaises(BaseException):
            rename_fields(input_event, rename_field_dict)

    # Test 109
    def test_split_event_to_multiple_events_skip_for_parent_id(self):
        input_event = {'_metadata': {'event_type': 'schema_name.event_name',
                                     '@parent_uuid': '123'},
                       'a_non_metadata_field': 'some value'}

        expected_output_event = {'_metadata': {'event_type': 'schema_name.event_name',
                                               '@parent_uuid': '123'},
                                 'a_non_metadata_field': 'some value'}

        self.assertEqual(expected_output_event, split_event_to_multiple_events(event=input_event, table_name_list=['one', 'two']))

    # Test 110
    def test_split_event_to_multiple_events_split_into_two(self):
        input_event = {'_metadata': {'event_type': 'schema_name.event_name',
                                     '@parent_uuid': ''},
                       'a_non_metadata_field': 'some value'}

        expected_output_event = [{'_metadata': {'@parent_uuid': '', 'event_type': 'schema_name.table_one'},
                                  'a_non_metadata_field': 'some value'},
                                 {'_metadata': {'@parent_uuid': '', 'event_type': 'schema_name.table_two'},
                                  'a_non_metadata_field': 'some value'}]

        self.assertEqual(expected_output_event, split_event_to_multiple_events(event=input_event, table_name_list=['table_one', 'table_two']))

    # Test 111
    def test_split_event_to_multiple_events_split_into_three(self):
        input_event = {'_metadata': {'event_type': 'schema_name.event_name',
                                     '@parent_uuid': ''},
                       'a_non_metadata_field': 'some value'}

        expected_output_event = [{'_metadata': {'@parent_uuid': '', 'event_type': 'schema_name.table_one'},
                                  'a_non_metadata_field': 'some value'},
                                 {'_metadata': {'@parent_uuid': '', 'event_type': 'schema_name.table_two'},
                                  'a_non_metadata_field': 'some value'},
                                 {'_metadata': {'@parent_uuid': '', 'event_type': 'schema_name.table_three'},
                                  'a_non_metadata_field': 'some value'}]

        self.assertEqual(expected_output_event, split_event_to_multiple_events(event=input_event, table_name_list=['table_one', 'table_two', 'table_three']))

    # Test 112
    def test_split_event_to_multiple_events_throw_exception_if_not_fully_qualified(self):
        input_event = {'_metadata': {'event_type': 'schema_name_event_name',
                                     '@parent_uuid': ''},
                       'a_non_metadata_field': 'some value'}

        with self.assertRaises(BaseException) as cm:
            split_event_to_multiple_events(event=input_event, table_name_list=['table_one', 'table_two', 'table_three'])

        self.assertEqual(str(cm.exception), 'Only fully qualified events can be split. Event type must be schema_name.table_name')

    # Test 113
    def test_split_field_list_to_multiple_events_split(self):
        input = {'id': 1,
                 'names': ['first', 'second'],
                 '_metadata': {'uuid': '1a'}}
        output = [{'id': 1,
                   'name': 'first',
                   'counter': 1,
                   '_metadata': {'uuid': '1a'}},
                  {'id': 1,
                   'name': 'second',
                   'counter': 2,
                   '_metadata': {'uuid': '1a'}}
                  ]
        self.assertEqual(output, split_field_list_to_multiple_events(event=input, fields_to_split=['names'], add_counter=True, counter_name='counter', reverse=False))

    # Test 114
    def test_split_field_list_to_multiple_events_skip_for_parentd_uuid(self):
        input = {'id': 1,
                 'names': ['first', 'second'],
                 '_metadata': {'@parent_uuid': '1a'}}
        output = {'id': 1,
                  'names': ['first', 'second'],
                  '_metadata': {'@parent_uuid': '1a'}}

        self.assertEqual(output, split_field_list_to_multiple_events(event=input, fields_to_split=['names'], add_counter=True, counter_name='counter', reverse=False))

    # Test 115
    def test_whitelist_or_blacklist_columns_whitelist(self):
        input = {"Cookies": None,
                 "cake": None,
                 "brownies": "yum",
                 "iceCream": "mmmm",
                 "_metadata": {"table": "sweets"}}

        expected_output = {"Cookies": None,
                           "cake": None,
                           "iceCream": "mmmm",
                           "_metadata": {"table": "sweets"}}

        self.assertEqual(expected_output, whitelist_or_blacklist_columns(input, field_list=['cookies', 'Cake', 'IceCream'], white_or_black_list='whitelist'))

    # Test 116
    def test_whitelist_or_blacklist_columns_blacklist(self):
        input = {"Cookies": None,
                 "cake": None,
                 "brownies": "yum",
                 "iceCream": "mmmm",
                 "_metadata": {"table": "sweets"}}

        expected_output = {"brownies": "yum",
                           "_metadata": {"table": "sweets"}}

        self.assertEqual(expected_output, whitelist_or_blacklist_columns(input, field_list=['cookies', 'Cake', 'IceCream'], white_or_black_list='blacklist'))








