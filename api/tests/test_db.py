import unittest
from unittest.mock import patch, MagicMock
from db import run_sql

class TestRunSQL(unittest.TestCase):
    @patch("db.psycopg2.connect")
    @patch("db.os.getenv")
    def test_run_sql_success(self, mock_getenv, mock_connect):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "test_db",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password"
        }.get(key)

        # Mock database connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [("row1_col1", "row1_col2"), ("row2_col1", "row2_col2")]
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Run the function
        sql = "SELECT * FROM test_table"
        columns = ["col1", "col2"]
        result = run_sql(sql, columns)

        # Assertions
        mock_connect.assert_called_once_with(
            host="localhost",
            port="5432",
            database="test_db",
            user="test_user",
            password="test_password"
        )
        mock_cursor.execute.assert_called_once_with(sql)
        self.assertEqual(result, [{"col1": "row1_col1", "col2": "row1_col2"}, {"col1": "row2_col1", "col2": "row2_col2"}])

    @patch("db.psycopg2.connect")
    @patch("db.os.getenv")
    def test_run_sql_connection_error(self, mock_getenv, mock_connect):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "test_db",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password"
        }.get(key)

        # Simulate connection error
        mock_connect.side_effect = Exception("Connection failed")

        # Run the function and assert exception
        sql = "SELECT * FROM test_table"
        columns = ["col1", "col2"]
        with self.assertRaises(Exception) as context:
            run_sql(sql, columns)
        self.assertEqual(str(context.exception), "Connection failed")

    @patch("db.psycopg2.connect")
    @patch("db.os.getenv")
    def test_run_sql_query_error(self, mock_getenv, mock_connect):
        # Mock environment variables
        mock_getenv.side_effect = lambda key: {
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_NAME": "test_db",
            "DB_USER": "test_user",
            "DB_PASSWORD": "test_password"
        }.get(key)

        # Mock database connection and cursor
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Query failed")
        mock_connection = MagicMock()
        mock_connection.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        # Run the function and assert exception
        sql = "SELECT * FROM test_table"
        columns = ["col1", "col2"]
        with self.assertRaises(Exception) as context:
            run_sql(sql, columns)
        self.assertEqual(str(context.exception), "Query failed")

if __name__ == "__main__":
    unittest.main()