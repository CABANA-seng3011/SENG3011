import unittest
from unittest.mock import patch, MagicMock
from external_team_routes import (
    query_company,
    query_company_sentiment,
    query_finances_stock_data,
    query_finances_overview,
    query_finances_price,
    query_finances_historical_data,
    query_finances_options_data
)

class TestQueryFunctions(unittest.TestCase):

    @patch('external_team_routes.requests.get')
    def test_query_company_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "events": [
                {"time_object": {"timestamp": "2024-01-01T00:00:00Z"}},
                {"time_object": {"timestamp": "2025-01-01T00:00:00Z"}}
            ]
        }
        mock_get.return_value = mock_response

        data = query_company("AAPL", "fake-api-key", 1, "2020-01-01", "2025-01-01")
        self.assertIn("events", data)
        self.assertEqual(len(data["events"]), 1)
        self.assertEqual(data["events"][0]["time_object"]["timestamp"], "2025-01-01T00:00:00Z")

    @patch('external_team_routes.requests.get')
    def test_query_company_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")
        data = query_company("AAPL", "fake-api-key", 1, "2020-01-01", "2025-01-01")
        self.assertEqual(data, [])

    @patch('external_team_routes.requests.post')
    def test_query_company_sentiment_success(self, mock_post):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"sentiment": "positive"}
        mock_post.return_value = mock_response

        result = query_company_sentiment("AAPL", "fake-api-key")
        self.assertEqual(result, {"sentiment": "positive"})

    @patch('external_team_routes.requests.post')
    def test_query_company_sentiment_failure(self, mock_post):
        mock_response = MagicMock(status_code=400, text="Bad Request")
        mock_post.return_value = mock_response

        result = query_company_sentiment("AAPL", "fake-api-key")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Bad Request")

    @patch('external_team_routes.requests.post')
    def test_query_finances_stock_data_success(self, mock_post):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"price": 150}
        mock_post.return_value = mock_response

        result = query_finances_stock_data("AAPL", "fake-api-key")
        self.assertEqual(result, {"price": 150})

    @patch('external_team_routes.requests.get')
    def test_query_finances_overview_success(self, mock_get):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"overview": "data"}
        mock_get.return_value = mock_response

        result = query_finances_overview("AAPL")
        self.assertEqual(result, {"overview": "data"})

    @patch('external_team_routes.requests.get')
    def test_query_finances_overview_failure(self, mock_get):
        mock_response = MagicMock(status_code=404, text="Not Found")
        mock_get.return_value = mock_response

        result = query_finances_overview("AAPL")
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Not Found")

    @patch('external_team_routes.requests.get')
    def test_query_finances_price_success(self, mock_get):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"price": 170}
        mock_get.return_value = mock_response

        result = query_finances_price("AAPL")
        self.assertEqual(result, {"price": 170})

    @patch('external_team_routes.requests.get')
    def test_query_finances_historical_data_success(self, mock_get):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"historical": []}
        mock_get.return_value = mock_response

        result = query_finances_historical_data("AAPL", "2020-01-01", "2025-01-01", "1d")
        self.assertEqual(result, {"historical": []})

    @patch('external_team_routes.requests.get')
    def test_query_finances_options_data_success(self, mock_get):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = {"options": []}
        mock_get.return_value = mock_response

        result = query_finances_options_data("AAPL")
        self.assertEqual(result, {"options": []})

if __name__ == "__main__":
    unittest.main()