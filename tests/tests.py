""""""
import unittest
from app import app
import json


class FlaskTestCase(unittest.TestCase):
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_github_webhook(self):
        tester = app.test_client(self)
        response = tester.post('/github_case_switch', content_type='application/json', data=json.dumps({'issue': 'hello', 'action': None}))
        self.assertNotEqual(response.status_code, 200)

    def test_github_webhook_issue_open(self):
        tester = app.test_client(self)
        response = tester.post('/github_case_switch', content_type='application/json', data=json.dumps({'issue': {'labels': [{'name': 'hello', 'color': 'blue'}], 'title': 'Issue title', 'number': 56156}, 'action': 'open'}))
        self.assertEqual(response.status_code, 200)

    def test_github_webhook_issue_closed(self):
        tester = app.test_client(self)
        response = tester.post('/github_case_switch', content_type='application/json', data=json.dumps({'issue': {'labels': [{'name': 'hello', 'color': 'blue'}], 'title': 'Issue title', 'number': 56156}, 'action': 'closed'}))
        self.assertEqual(response.status_code, 200)

    def test_github_webhook_issue_gibberish(self):
        tester = app.test_client(self)
        response = tester.post('/github_case_switch', content_type='application/json', data=json.dumps({'issue': {'labels': [{'name': 'hello', 'color': 'blue'}], 'title': 'Issue title', 'number': 56156}, 'action': 'afgbasdkhgfkaqegfhakuhf'}))
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
