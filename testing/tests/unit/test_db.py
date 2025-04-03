import pytest
from unittest.mock import patch, MagicMock
from db import run_sql

@patch("db.psycopg2.connect")
@patch("db.os.getenv")
def test_run_sql_success(mock_getenv, mock_connect):
    """Test run_sql with a successful query."""
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
    mock_cursor.fetchone.side_effect = [
        ("row1_col1", "row1_col2"),
        ("row2_col1", "row2_col2"),
        None  # Simulate end of rows
    ]
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Run the function
    sql = "SELECT col1, col2 FROM test_table"
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
    assert result == [
        {"col1": "row1_col1", "col2": "row1_col2"},
        {"col1": "row2_col1", "col2": "row2_col2"}
    ]

@patch("db.psycopg2.connect")
@patch("db.os.getenv")
def test_run_sql_no_results(mock_getenv, mock_connect):
    """Test run_sql when no rows are returned."""
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
    mock_cursor.fetchone.return_value = None  # Simulate no rows returned
    mock_connection = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_connection

    # Run the function
    sql = "SELECT col1, col2 FROM test_table WHERE col1 = 'nonexistent'"
    columns = ["col1", "col2"]
    result = run_sql(sql, columns)

    # Assertions
    mock_cursor.execute.assert_called_once_with(sql)
    assert result == []  # Expect an empty list when no rows are returned

@patch("db.psycopg2.connect")
@patch("db.os.getenv")
def test_run_sql_connection_error(mock_getenv, mock_connect):
    """Test run_sql when the database connection fails."""
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
    sql = "SELECT col1, col2 FROM test_table"
    columns = ["col1", "col2"]
    with pytest.raises(Exception, match="Connection failed"):
        run_sql(sql, columns)

@patch("db.psycopg2.connect")
@patch("db.os.getenv")
def test_run_sql_query_error(mock_getenv, mock_connect):
    """Test run_sql when the query execution fails."""
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
    sql = "SELECT col1, col2 FROM test_table"
    columns = ["col1", "col2"]
    with pytest.raises(Exception, match="Query failed"):
        run_sql(sql, columns)