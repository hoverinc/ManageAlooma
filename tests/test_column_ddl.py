import unittest
from managealooma.column_ddl import ColumnDDL

import re


class TestColumnDDL(unittest.TestCase):

    # Test 1
    def test_tuple_to_tuple_list_input_list(self):
        single_tuple = ('schema_name.table_name', 'column_one', 'INT')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple)
        columns = CD.convert_tuple_to_list()
        self.assertTrue(isinstance(columns, list))

    # Test 2
    def test_tuple_to_tuple_list_input_tuple(self):
        tuple_list = [('schema_name.table_name', 'column_one'),
                      ('schema_name.table_name', 'column_two')]
        CD = ColumnDDL(tuple_or_tuple_list=tuple_list)
        columns = CD.convert_tuple_to_list()
        self.assertTrue(isinstance(columns, list))

    # Test 3
    def test_drop_column_no_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'VARCHAR(16777216)')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='drop', has_log=False, case='UPPER')
        query = CD.drop_column(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_to_drop='MY_COLUMN')

        expected_query = """BEGIN TRANSACTION;
                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         DROP COLUMN "MY_COLUMN" CASCADE;

                        COMMIT;"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 4
    def test_drop_column_has_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'VARCHAR(16777216)')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='drop', has_log=True, case='UPPER')
        query = CD.drop_column(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_to_drop='MY_COLUMN')

        expected_query = """BEGIN TRANSACTION;
                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         DROP COLUMN "MY_COLUMN" CASCADE;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                         DROP COLUMN "MY_COLUMN" CASCADE ;

                        COMMIT;"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 5
    def test_create_ddl_statements_drop_two_columns_no_log_lower(self):
        tuple_list = [('schema_name.table_name', 'column_one'),
                      ('schema_name.table_name', 'column_two')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='drop', has_log=False, case='lower')
        query_list = CD.create_ddl_statements()

        expected_query_list = """begin transaction;
                                 alter table "schema_name"."table_name"
                                 drop column "column_one" cascade;

                                  commit;

                                begin transaction;
                                 alter table "schema_name"."table_name"
                                 drop column "column_two" cascade;
                                commit;"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 6
    def test_create_ddl_statements_drop_two_columns_no_log_upper(self):
        tuple_list = [('schema_name.table_name', 'column_one'),
                      ('schema_name.table_name', 'column_two')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='drop', has_log=False, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """BEGIN TRANSACTION;
                         ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                         DROP COLUMN "COLUMN_ONE" CASCADE;

                        COMMIT;
                        BEGIN TRANSACTION;
                         ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                         DROP COLUMN "COLUMN_TWO" CASCADE;

                        COMMIT;"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 7
    def test_create_ddl_statements_drop_two_columns_has_log_upper(self):
        tuple_list = [('schema_name.table_name', 'column_one'),
                      ('schema_name.table_name', 'column_two')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='drop', has_log=True, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """BEGIN TRANSACTION;
                         ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                         DROP COLUMN "COLUMN_ONE" CASCADE;

                         ALTER TABLE "SCHEMA_NAME"."TABLE_NAME_LOG"
                         DROP COLUMN "COLUMN_ONE" CASCADE ;

                        COMMIT;
                        BEGIN TRANSACTION;
                         ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                         DROP COLUMN "COLUMN_TWO" CASCADE;

                         ALTER TABLE "SCHEMA_NAME"."TABLE_NAME_LOG"
                         DROP COLUMN "COLUMN_TWO" CASCADE ;

                        COMMIT;"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 8
    def test_change_column_data_type_no_log_varchar(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'VARCHAR(16777216)')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='data_type', has_log=False, case='UPPER')
        query = CD.change_column_data_type(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_name='MY_COLUMN', new_column_type='VARCHAR(16777216)', new_column_type_no_count='VARCHAR')

        expected_query = """BEGIN TRANSACTION;
                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         RENAME COLUMN "MY_COLUMN" TO "MY_COLUMN_TMP";

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                           ADD COLUMN "MY_COLUMN" VARCHAR(16777216);
                           UPDATE "MY_SCHEMA"."MY_TABLE"
                           SET "MY_COLUMN" = "MY_COLUMN_TMP"::VARCHAR
                           WHERE "MY_COLUMN" IS NULL;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                           DROP COLUMN "MY_COLUMN_TMP" CASCADE;
                        COMMIT;

                        """
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 9
    def test_change_column_data_type_no_log_int(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'INTEGER')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='data_type', has_log=False, case='UPPER')
        query = CD.change_column_data_type(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_name='MY_COLUMN', new_column_type='INTEGER', new_column_type_no_count='INTEGER')

        expected_query = """BEGIN TRANSACTION;
                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         RENAME COLUMN "MY_COLUMN" TO "MY_COLUMN_TMP";

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                           ADD COLUMN "MY_COLUMN" INTEGER;
                           UPDATE "MY_SCHEMA"."MY_TABLE"
                           SET "MY_COLUMN" = "MY_COLUMN_TMP"::INTEGER
                           WHERE "MY_COLUMN" IS NULL;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                           DROP COLUMN "MY_COLUMN_TMP" CASCADE;
                        COMMIT;"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 10
    def test_change_column_data_type_has_log_int(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'INTEGER')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='data_type', has_log=True, case='UPPER')
        query = CD.change_column_data_type(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_name='MY_COLUMN', new_column_type='INTEGER', new_column_type_no_count='INTEGER')

        expected_query = """                     BEGIN TRANSACTION;
                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         RENAME COLUMN "MY_COLUMN" TO "MY_COLUMN_TMP";

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                           ADD COLUMN "MY_COLUMN" INTEGER;
                           UPDATE "MY_SCHEMA"."MY_TABLE"
                           SET "MY_COLUMN" = "MY_COLUMN_TMP"::INTEGER
                           WHERE "MY_COLUMN" IS NULL;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                           DROP COLUMN "MY_COLUMN_TMP" CASCADE;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                         RENAME COLUMN "MY_COLUMN" TO "MY_COLUMN_TMP";

                          ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                           ADD COLUMN "MY_COLUMN" INTEGER;
                           UPDATE "MY_SCHEMA"."MY_TABLE_LOG"
                           SET "MY_COLUMN" = "MY_COLUMN_TMP"::INTEGER
                           WHERE "MY_COLUMN" IS NULL;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                           DROP COLUMN "MY_COLUMN_TMP" CASCADE;
                     COMMIT;
                     """
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 11
    def test_create_ddl_statements_change_data_type_one_column_no_log_upper_int(self):
        single_tuple = ('my_schema.my_table', 'column_one', 'INTEGER')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='data_type', has_log=False, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query = """BEGIN TRANSACTION;
                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                         RENAME COLUMN "COLUMN_ONE" TO "COLUMN_ONE_TMP";

                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                           ADD COLUMN "COLUMN_ONE" INTEGER;
                           UPDATE "MY_TABLE"."MY_SCHEMA"
                           SET "COLUMN_ONE" = "COLUMN_ONE_TMP"::INTEGER
                           WHERE "COLUMN_ONE" IS NULL;

                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                           DROP COLUMN "COLUMN_ONE_TMP" CASCADE;
                        COMMIT;"""
        self.assertEqual(re.sub(r'\W', '', expected_query), re.sub(r'\W', '', query_list))

    # Test 12
    def test_create_ddl_statements_change_data_type_one_column_no_log_lower_int(self):
        single_tuple = ('my_schema.my_table', 'column_one', 'INTEGER')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='data_type', has_log=False, case='lower')
        query_list = CD.create_ddl_statements()

        expected_query = """begin transaction;
                         alter table "my_table"."my_schema"
                         rename column "column_one" to "column_one_tmp";

                         alter table "my_table"."my_schema"
                           add column "column_one" integer;
                           update "my_table"."my_schema"
                           set "column_one" = "column_one_tmp"::integer
                           where "column_one" is null;

                         alter table "my_table"."my_schema"
                           drop column "column_one_tmp" cascade;
                        commit;"""
        self.assertEqual(re.sub(r'\W', '', expected_query), re.sub(r'\W', '', query_list))

    # Test 13
    def test_create_ddl_statements_change_data_type_one_column_no_log_lower_varchar(self):
        single_tuple = ('my_schema.my_table', 'column_one', 'VARCHAR(16777216)')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='data_type', has_log=False, case='lower')
        query_list = CD.create_ddl_statements()

        expected_query = """begin transaction;
                         alter table "my_table"."my_schema"
                         rename column "column_one" to "column_one_tmp";

                         alter table "my_table"."my_schema"
                           add column "column_one" varchar(16777216);
                           update "my_table"."my_schema"
                           set "column_one" = "column_one_tmp"::varchar(16777216)
                           where "column_one" is null;

                         alter table "my_table"."my_schema"
                           drop column "column_one_tmp" cascade;
                        commit;"""
        self.assertEqual(re.sub(r'\W', '', expected_query), re.sub(r'\W', '', query_list))

    # Test 14
    def test_create_ddl_statements_change_data_type_two_column_no_log_lower_int_and_varchar(self):
        tuple_list = [('my_schema.my_table', 'column_one', 'INTEGER'),
                      ('my_schema.my_table', 'column_two', 'VARCHAR(16777216)')]
        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='data_type', has_log=False, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query = """BEGIN TRANSACTION;
                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                         RENAME COLUMN "COLUMN_ONE" TO "COLUMN_ONE_TMP";

                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                           ADD COLUMN "COLUMN_ONE" INTEGER;
                           UPDATE "MY_TABLE"."MY_SCHEMA"
                           SET "COLUMN_ONE" = "COLUMN_ONE_TMP"::INTEGER
                           WHERE "COLUMN_ONE" IS NULL;

                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                           DROP COLUMN "COLUMN_ONE_TMP" CASCADE;
                        COMMIT;

                        BEGIN TRANSACTION;
                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                         RENAME COLUMN "COLUMN_TWO" TO "COLUMN_TWO_TMP";

                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                           ADD COLUMN "COLUMN_TWO" VARCHAR(16777216);
                           UPDATE "MY_TABLE"."MY_SCHEMA"
                           SET "COLUMN_TWO" = "COLUMN_TWO_TMP"::VARCHAR(16777216)
                           WHERE "COLUMN_TWO" IS NULL;

                         ALTER TABLE "MY_TABLE"."MY_SCHEMA"
                           DROP COLUMN "COLUMN_TWO_TMP" CASCADE;
                        COMMIT;"""
        self.assertEqual(re.sub(r'\W', '', expected_query), re.sub(r'\W', '', query_list))

    # Test 15
    def test_add_column_no_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'VARCHAR(16777216)')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='drop', has_log=False, case='UPPER')
        query = CD.add_column(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_to_add='COLUMN_ONE', new_column_type='VARCHAR(16777216)')

        expected_query = """ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         ADD COLUMN "COLUMN_ONE" VARCHAR(16777216);"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 16
    def test_add_column_has_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'column_one', 'VARCHAR(16777216)')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='add', has_log=True, case='UPPER')
        query = CD.add_column(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_to_add='COLUMN_ONE', new_column_type='VARCHAR(16777216)')

        expected_query = """ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         ADD COLUMN "COLUMN_ONE" VARCHAR(16777216);

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                         ADD COLUMN "COLUMN_ONE" VARCHAR(16777216);"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 17
    def test_create_ddl_statements_add_two_columns_no_log_lower(self):
        tuple_list = [('schema_name.table_name', 'column_one', 'VARCHAR(16777216)'),
                      ('schema_name.table_name', 'column_two', 'INTEGER')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='add', has_log=False, case='lower')
        query_list = CD.create_ddl_statements()

        expected_query_list = """alter table "schema_name"."table_name"
                        add column "column_one" varchar(16777216);

                        alter table "schema_name"."table_name"
                        add column "column_two" integer;"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 18
    def test_create_ddl_statements_add_two_columns_no_log_upper(self):
        tuple_list = [('schema_name.table_name', 'column_one', 'VARCHAR(16777216)'),
                      ('schema_name.table_name', 'column_two', 'INTEGER')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='add', has_log=False, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                        ADD COLUMN "COLUMN_ONE" VARCHAR(16777216);

                        ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                        ADD COLUMN "COLUMN_TWO" INTEGER;"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 19
    def test_create_ddl_statements_add_two_columns_has_log_upper(self):
        tuple_list = [('schema_name.table_name', 'column_one', 'VARCHAR(16777216)'),
                      ('schema_name.table_name', 'column_two', 'INTEGER')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='add', has_log=True, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                        ADD COLUMN "COLUMN_ONE" VARCHAR(16777216);

                        ALTER TABLE "SCHEMA_NAME"."TABLE_NAME_LOG"
                        ADD COLUMN "COLUMN_ONE" VARCHAR(16777216);

                        ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                        ADD COLUMN "COLUMN_TWO" INTEGER;

                        ALTER TABLE "SCHEMA_NAME"."TABLE_NAME_LOG"
                        ADD COLUMN "COLUMN_TWO" INTEGER;"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 20
    def test_rename_column_no_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'my_column', 'my_new_column')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='rename', has_log=False, case='UPPER')
        query = CD.rename_column(schema_name='MY_SCHEMA', table_name='MY_TABLE', existing_column_name='MY_COLUMN', new_column_name='MY_NEW_COLUMN')

        expected_query = """ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         RENAME COLUMN "MY_COLUMN" TO "MY_NEW_COLUMN";"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 21
    def test_rename_column_has_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('my_schema.my_table', 'my_column', 'my_new_column')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='rename', has_log=True, case='UPPER')
        query = CD.rename_column(schema_name='MY_SCHEMA', table_name='MY_TABLE', existing_column_name='MY_COLUMN', new_column_name='MY_NEW_COLUMN')

        expected_query = """ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         RENAME COLUMN "MY_COLUMN" TO "MY_NEW_COLUMN";

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                         RENAME COLUMN "MY_COLUMN" TO "MY_NEW_COLUMN";"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 22
    def test_create_ddl_statements_rename_two_columns_no_log_lower(self):
        tuple_list = [('schema_name.table_name', 'column_one', 'new_column_one'),
                      ('schema_name.table_name', 'column_two', 'new_column_two')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='rename', has_log=False, case='lower')
        query_list = CD.create_ddl_statements()

        expected_query_list = """alter table "schema_name"."table_name"
                                rename column "column_one" to "new_column_one";

                                alter table "schema_name"."table_name"
                                 rename column "column_two" to "new_column_two";"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 23
    def test_create_ddl_statements_rename_two_columns_no_log_upper(self):
        tuple_list = [('schema_name.table_name', 'column_one', 'new_column_one'),
                      ('schema_name.table_name', 'column_two', 'new_column_two')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='rename', has_log=False, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                                RENAME COLUMN "COLUMN_ONE" TO "NEW_COLUMN_ONE";

                                ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                                 RENAME COLUMN "COLUMN_TWO" TO "NEW_COLUMN_TWO";"""

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 24
    def test_create_ddl_statements_rename_two_columns_has_log_upper(self):
        tuple_list = [('schema_name.table_name', 'column_one', 'new_column_one'),
                      ('schema_name.table_name', 'column_two', 'new_column_two')]

        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='rename', has_log=True, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                                RENAME COLUMN "COLUMN_ONE" TO "NEW_COLUMN_ONE";

                                ALTER TABLE "SCHEMA_NAME"."TABLE_NAME_LOG"
                                RENAME COLUMN "COLUMN_ONE" TO "NEW_COLUMN_ONE";

                                ALTER TABLE "SCHEMA_NAME"."TABLE_NAME"
                                 RENAME COLUMN "COLUMN_TWO" TO "NEW_COLUMN_TWO";

                                ALTER TABLE "SCHEMA_NAME"."TABLE_NAME_LOG"
                                 RENAME COLUMN "COLUMN_TWO" TO "NEW_COLUMN_TWO";
                                 """

        self.assertEqual(re.sub(r'\W', '', expected_query_list), re.sub(r'\W', '', query_list))

    # Test 25
    def test_combine_columns_no_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('schema_name.table_name', 'my_bad_column', 'my_good_column', 'INT')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='combine', has_log=False, case='UPPER')
        query = CD.combine_columns(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_to_drop='MY_BAD_COLUMN_NAME', column_to_keep='MY_GOOD_COLUMN_NAME', column_to_keep_type='INTEGER')

        expected_query = """BEGIN TRANSACTION;
                         UPDATE TABLE "MY_SCHEMA"."MY_TABLE"
                           SET "MY_GOOD_COLUMN_NAME" = "MY_BAD_COLUMN_NAME"::INTEGER
                           WHERE "MY_GOOD_COLUMN_NAME" IS NULL;

                         ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                         DROP COLUMN "MY_BAD_COLUMN_NAME" CASCADE;
                        COMMIT;"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 26
    def test_combine_column_has_log(self):
        # The tuple is here because it's required by the class. It's not used in this test
        single_tuple = ('schema_name.table_name', 'my_bad_column', 'my_good_column', 'INT')
        CD = ColumnDDL(tuple_or_tuple_list=single_tuple, change_type='combine', has_log=True, case='UPPER')
        query = CD.combine_columns(schema_name='MY_SCHEMA', table_name='MY_TABLE', column_to_drop='MY_BAD_COLUMN_NAME', column_to_keep='MY_GOOD_COLUMN_NAME', column_to_keep_type='INTEGER')

        expected_query = """BEGIN TRANSACTION;
                             UPDATE TABLE "MY_SCHEMA"."MY_TABLE"
                               SET "MY_GOOD_COLUMN_NAME" = "MY_BAD_COLUMN_NAME"::INTEGER
                               WHERE "MY_GOOD_COLUMN_NAME" IS NULL;

                             ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                             DROP COLUMN "MY_BAD_COLUMN_NAME" CASCADE;

                              UPDATE TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                               SET "MY_GOOD_COLUMN_NAME" = "MY_BAD_COLUMN_NAME"::INTEGER
                               WHERE "MY_GOOD_COLUMN_NAME" IS NULL;

                             ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                             DROP COLUMN "MY_BAD_COLUMN_NAME" CASCADE;

                          COMMIT;"""
        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query), re.sub(r'[\n\t\s]*', '', query))

    # Test 27
    def test_create_ddl_statements_combine_two_columns_no_log_lower(self):
        tuple_list = [('my_schema.my_table', 'my_bad_column_name_one', 'my_good_column_name_one', 'INTEGER'),
                      ('my_schema.my_table', 'my_bad_column_name_two', 'my_good_column_name_two', 'VARCHAR(16777216)')]
        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='combine', has_log=False, case='lower')
        query_list = CD.create_ddl_statements()

        expected_query_list = """begin transaction;
                                     update table "my_schema"."my_table"
                                       set "my_good_column_name_one" = "my_bad_column_name_one"::integer
                                       where "my_good_column_name_one" is null;

                                     alter table "my_schema"."my_table"
                                     drop column "my_bad_column_name_one" cascade;
                                commit;

                                begin transaction;
                                     update table "my_schema"."my_table"
                                       set "my_good_column_name_two" = "my_bad_column_name_two"::varchar(16777216)
                                       where "my_good_column_name_two" is null;

                                     alter table "my_schema"."my_table"
                                     drop column "my_bad_column_name_two" cascade;
                                commit;"""

        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query_list), re.sub(r'[\n\t\s]*', '', query_list))

    # Test 28
    def test_create_ddl_statements_combine_two_columns_no_log_upper(self):
        tuple_list = [('my_schema.my_table', 'my_bad_column_name_one', 'my_good_column_name_one', 'INTEGER'),
                      ('my_schema.my_table', 'my_bad_column_name_two', 'my_good_column_name_two', 'VARCHAR(16777216)')]
        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='combine', has_log=False, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """BEGIN TRANSACTION;
                                     UPDATE TABLE "MY_SCHEMA"."MY_TABLE"
                                       SET "MY_GOOD_COLUMN_NAME_ONE" = "MY_BAD_COLUMN_NAME_ONE"::INTEGER
                                       WHERE "MY_GOOD_COLUMN_NAME_ONE" IS NULL;

                                     ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                                     DROP COLUMN "MY_BAD_COLUMN_NAME_ONE" CASCADE;
                                COMMIT;

                                BEGIN TRANSACTION;
                                     UPDATE TABLE "MY_SCHEMA"."MY_TABLE"
                                       SET "MY_GOOD_COLUMN_NAME_TWO" = "MY_BAD_COLUMN_NAME_TWO"::VARCHAR(16777216)
                                       WHERE "MY_GOOD_COLUMN_NAME_TWO" IS NULL;

                                     ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                                     DROP COLUMN "MY_BAD_COLUMN_NAME_TWO" CASCADE;
                                COMMIT;"""

        self.assertEqual(re.sub(r'[\n\t\s]*', '', expected_query_list), re.sub(r'[\n\t\s]*', '', query_list))

    # Test 29
    def test_create_ddl_statements_combine_two_columns_has_log_upper(self):
        tuple_list = [('my_schema.my_table', 'my_bad_column_name_one', 'my_good_column_name_one', 'INTEGER'),
                      ('my_schema.my_table', 'my_bad_column_name_two', 'my_good_column_name_two', 'VARCHAR(16777216)')]
        CD = ColumnDDL(tuple_or_tuple_list=tuple_list, change_type='combine', has_log=True, case='UPPER')
        query_list = CD.create_ddl_statements()

        expected_query_list = """BEGIN TRANSACTION;
                                     UPDATE TABLE "MY_SCHEMA"."MY_TABLE"
                                       SET "MY_GOOD_COLUMN_NAME_ONE" = "MY_BAD_COLUMN_NAME_ONE"::INTEGER
                                       WHERE "MY_GOOD_COLUMN_NAME_ONE" IS NULL;

                                     ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                                     DROP COLUMN "MY_BAD_COLUMN_NAME_ONE" CASCADE;
                                     
                                    UPDATE TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                                       SET "MY_GOOD_COLUMN_NAME_ONE" = "MY_BAD_COLUMN_NAME_ONE"::INTEGER
                                       WHERE "MY_GOOD_COLUMN_NAME_ONE" IS NULL;

                                     ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                                     DROP COLUMN "MY_BAD_COLUMN_NAME_ONE" CASCADE;
                                COMMIT;

                                BEGIN TRANSACTION;
                                     UPDATE TABLE "MY_SCHEMA"."MY_TABLE"
                                       SET "MY_GOOD_COLUMN_NAME_TWO" = "MY_BAD_COLUMN_NAME_TWO"::VARCHAR(16777216)
                                       WHERE "MY_GOOD_COLUMN_NAME_TWO" IS NULL;

                                     ALTER TABLE "MY_SCHEMA"."MY_TABLE"
                                     DROP COLUMN "MY_BAD_COLUMN_NAME_TWO" CASCADE;
                                     
                                     UPDATE TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                                       SET "MY_GOOD_COLUMN_NAME_TWO" = "MY_BAD_COLUMN_NAME_TWO"::VARCHAR(16777216)
                                       WHERE "MY_GOOD_COLUMN_NAME_TWO" IS NULL;

                                     ALTER TABLE "MY_SCHEMA"."MY_TABLE_LOG"
                                     DROP COLUMN "MY_BAD_COLUMN_NAME_TWO" CASCADE;
                                COMMIT;"""
