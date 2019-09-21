Getting Started
==============================

This document will take you through setting up a local repo, testing your transformations locally, using the transformation functions in the managealooma package, and using one of management classes in the managealooma package.

.. _installation:

Installation
------------

This package is available from the `Python Package Index
<http://pypi.python.org/pypi/managealooma>`_. If you have `pip
<https://pip.pypa.io/>`_ you should be able to do::

    $ pip install managealooma


.. _local_configuration:

Local Configuration
-------------------

1. Create a workspace for your Alooma code

.. code-block:: bash

    $ mkdir -p alooma/code
    $ touch alooma/event_sample.py alooma/event_test.py alooma/manage.py alooma/code/__init__.py alooma/code/code_engine.py


2. Check that your files match this directory structure:

.. code-block:: bash

    alooma/
        alooma_code/
            __init__.py
            code_engine.py
        event_sample.py
        event_test.py
        manage.py


.. _test_an_event:

Test an Event
-------------

1. Each Alooma event is a dictionary. Alooma takes your data and adds `_metadata` fields that help you manage the data. Add the following sample event to :file:`event_sample.py`:

.. code-block:: python

    event = {"myField": "stuff",
             "createdAt": "2019-08-01 00:00:00",
             "xmin::text::bigint": 123456789,
             "aNumber": 6,
             "id": 1,
             "aDictionary": {"one": "Some Stuff",
                             "two": "More Stuff",
                             "three": {"Another dict": {"Inside Three": 3.3,
                                                        "More Inside Three": 3.4}
                                       },
                             },
             "_metadata": {
                 "@uuid": "1a1a1a-2b2b-3c3c-4d4d-5e5e5e5e5e",
                 "event_type": "my_schema.my_table",
                 "input_label": "my_input",
                 "@parent_uuid": ""
             }
             }

2. Each of these samples will run through the code you have in :file:`code_engine.py` file.  Let's add this code to :file:`code_engine.py` to change the keys of the sample event from camelCase to snake_case.

.. code-block:: python

    from managealooma import convert_all_event_fields_to_snake_case

    def transform(event):

        # Converts the all keys of the event dictionary to snake_case
        event = convert_all_event_fields_to_snake_case(event)

        return event

3. Now we need code that will run the event in :file:`event_sample.py` through the code in :file:`code_engine.py`. Add the code below to :file:`event_test.py`

.. code-block:: python

    # The TransformationTest class takes an event and run it through your transformation code
    from managealooma import TransformationTest

    # Imports your local transformation code. It will also import any submodules in the directory.
    import code.code_engine as ce

    # This imports the sample event for testing.
    from event_sample import event

    # Instantiate the TransformationTest class and test a single event
    T = TransformationTest(api=None, code_package=ce, preview_full_events=True, preview_difference_dicts=False, local_or_api='local')
    T.test_single_event(sample=event)

4. Now run the file and the event will print to your console before and after the transformation

.. code-block:: bash

    $ python event_test.py

5. You can change the params in TransformationTest to summarize the diffs in the event instead of viewing the entire before and after

.. code-block:: python

    T = TransformationTest(api=None, code_package=ce, preview_full_events=False, preview_difference_dicts=True, local_or_api='local')

6. You can add as many transformations as you want to :file:`code_engine.py`.  Let's add more transformations from `managealooma.transformation_functions`.  Change your :file:`code_engine.py` to this:

.. code-block:: python

    from managealooma import convert_all_event_fields_to_snake_case, add_composite_key, map_value_in_list_to_dictionary_key, flatten_json

    def transform(event):
        # Converts the all keys of the event dictionary to snake_case
        event = convert_all_event_fields_to_snake_case(event)

        # More transformations. Read the docs to see all the options or write your own!
        event = flatten_json(event, field_list='a_dictionary', levels=1, keep_original=False, dump_to_string=True)
        event = add_composite_key(event, field_list=['id', 'created_at'], key_name='id_created_datetime')
        event = map_value_in_list_to_dictionary_key(event, mapping_dict_with_lists={'one_to_three': [1, 2, 3], 'four_to_six': [4, 5, 6]}, existing_column='a_number', new_column='number_category', allow_nulls=True, passthrough=True)

        return event

7. Run that file 1 more time to see the transformations

.. code-block:: bash

    $ python event_test.py



.. _use_the_API:

Use the API
-----------

Alooma has a robust API that will let you programmatically manage the tool.  The `managealooma` package contains main functions to help utilize these features. Typical usage will often mean running the code with `apply_changes=False` to visually inspect your changes first. Then you can set `apply_changes=True` to execute your adjustments.  This example will walk you through changing the mapping mode for an event.

In this example we'll only edit the  :file:`manage.py` file.
1. Add imports for `alooma`, `os`, and the mappings class from `managealooma`

.. code-block:: python

    import alooma
    from managealooma import Mappings
    from os import environ

2. Add your credentials for Alooma and instantiate the `api`.

.. code-block:: python

    alooma_credentials = {'account_name': environ.get('ALOOMA_ACCOUNT_NAME'),
                          'api_key': environ.get('ALOOMA_API_KEY')}

    api = alooma.Client(api_key=alooma_credentials["api_key"], account_name=alooma_credentials["account_name"])

3.  Add code to instantiate the `Mapping` class and use the `change_mapping_mode` function. Change `MY_EVENT.NAME` to the name of one of your events.


.. code-block:: python

    M = Mappings(api=api, event_name='MY_EVENT.NAME', preview_full=True, preview_changes=False, apply_changes=False, pprint_indent=2, pprint_width=250, pprint_depth=5)
    M.change_mapping_mode(new_mapping_mode='STRICT')

4. Now your file should be complete like this:


.. code-block:: python


    import alooma
    from managealooma import Mappings
    from os import environ

    alooma_credentials = {'account_name': environ.get('ALOOMA_ACCOUNT_NAME'),
                          'api_key': environ.get('ALOOMA_API_KEY')}

    api = alooma.Client(api_key=alooma_credentials["api_key"], account_name=alooma_credentials["account_name"])

    M = Mappings(api=api, event_name='MY_EVENT.NAME', preview_full=True, preview_changes=False, apply_changes=False, pprint_indent=2, pprint_width=250, pprint_depth=5)
    M.change_mapping_mode(new_mapping_mode='STRICT')

5. Run the file and you'll see the full mapping printed with before and after changes.

.. code-block:: bash

    $ python manage.py

6. It's a little hard to see the mapping moode in the mapping dictionaries. Let's change the print parameters to only see the changes.

.. code-block:: python

    M = Mappings(api=api, event_name='MY_EVENT.NAME', preview_full=False, preview_changes=True, apply_changes=False, pprint_indent=2, pprint_width=250, pprint_depth=5)

7. Now make sure to change the mapping mode to a new value

.. code-block:: python

    # The mapping code can be AUTO_MAP, STRICT, or FLEXIBLE. Try changing the value to a different value than the current setting
    M.change_mapping_mode(new_mapping_mode='STRICT')

8. Finally, if you want to execute these changes then sett `apply_changes=True`

.. code-block:: python

    M = Mappings(api=api, event_name='MY_EVENT.NAME', preview_full=False, preview_changes=True, apply_changes=True, pprint_indent=2, pprint_width=250, pprint_depth=5)


