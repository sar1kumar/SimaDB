import unittest
from flask import Flask, json
from flask_restx import Api
from similarity import ns as similarity_namespace


class TestSimilarityAPI(unittest.TestCase):

    def setUp(self):
        """Setup the Flask app and test client."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.api = Api(self.app)
        self.api.add_namespace(similarity_namespace)

        self.client = self.app.test_client()

        # Example payload data for API requests
        self.people_payload = {
            'project_id': 'project_1',
            'n_results': 5,
            'min_experience': 3,
            'required_skills': ['python'],
            'max_distance': 0.5
        }

        self.projects_payload = {
            'person_id': 'person_1',
            'n_results': 5,
            'status': 'active',
            'max_team_size': 10,
            'max_distance': 0.5
        }

        self.similarity_payload = {
            'person_id': 'person_1',
            'project_id': 'project_1'
        }

    def test_match_people_to_project_success(self):
        """Test the /match-people-to-project endpoint with valid input."""
        response = self.client.post(
            '/similarity/match-people-to-project',
            data=json.dumps(self.people_payload),
            content_type='application/json'
        )

        # Validate response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['project_id'], 'project_1')
        self.assertIn('matched_people', data)

    def test_match_people_to_project_project_not_found(self):
        """Test the /match-people-to-project endpoint with a non-existent project."""
        response = self.client.post(
            '/similarity/match-people-to-project',
            data=json.dumps({
                'project_id': 'invalid_project',
                'n_results': 5,
                'min_experience': 3,
                'required_skills': ['python'],
                'max_distance': 0.5
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Project not found.')

    def test_match_projects_to_person_success(self):
        """Test the /match-projects-to-person endpoint with valid input."""
        response = self.client.post(
            '/similarity/match-projects-to-person',
            data=json.dumps(self.projects_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['person_id'], 'person_1')
        self.assertIn('matched_projects', data)

    def test_match_projects_to_person_person_not_found(self):
        """Test the /match-projects-to-person endpoint with a non-existent person."""
        response = self.client.post(
            '/similarity/match-projects-to-person',
            data=json.dumps({
                'person_id': 'invalid_person',
                'n_results': 5,
                'status': 'active',
                'max_team_size': 10,
                'max_distance': 0.5
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'Person not found.')

    def test_similarity_score_calculation(self):
        """Test the /similarity-score endpoint."""
        response = self.client.post(
            '/similarity/similarity-score',
            data=json.dumps(self.similarity_payload),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['person_id'], 'person_1')
        self.assertEqual(data['project_id'], 'project_1')
        self.assertIn('similarity_score', data)


if __name__ == '__main__':
    unittest.main()
