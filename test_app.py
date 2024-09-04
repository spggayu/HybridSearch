import unittest
import requests
import json

class TestHybridSearchAPI(unittest.TestCase):
    
    BASE_URL = 'https://ubiquitous-carnival-q7v7696rwwq5f46pw-6543.app.github.dev/search'  # Adjust this URL based on your setup

    def test_search_with_query(self):
        payload = {
            "query": "text",
            "vector": None
        }
        response = requests.post(self.BASE_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        self.assertIn("keyword_results", response.json())
        self.assertNotIn("vector_results", response.json())

    def test_search_with_vector(self):
        payload = {
            "query": None,
            "vector": [0.1, 0.2, 0.3, 0.4]
        }
        response = requests.post(self.BASE_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("keyword_results", response.json())
        self.assertIn("vector_results", response.json())

    def test_search_with_both(self):
        payload = {
            "query": "example search term",
            "vector": [0.1, 0.2, 0.3, 0.4]
        }
        response = requests.post(self.BASE_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        self.assertIn("keyword_results", response.json())
        self.assertIn("vector_results", response.json())

    def test_search_with_invalid_content_type(self):
        headers = {"Content-Type": "text/plain"}
        payload = {
            "query": "example search term",
            "vector": [0.1, 0.2, 0.3, 0.4]
        }
        response = requests.post(self.BASE_URL, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 415)
        self.assertIn("error", response.json())

    def test_search_with_missing_query_and_vector(self):
        payload = {}
        response = requests.post(self.BASE_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

if __name__ == '__main__':
    unittest.main()
