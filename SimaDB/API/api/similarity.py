from flask_restx import Resource, Namespace, fields
from flask import request, jsonify, make_response
#from models import person_model, project_model

class MatchPeopleToProject(Resource):

    def __init__(self, api,chroma_client):
        self.api = api
        self.chroma_client = chroma_client
    

    def post(self):
        """Find the most suitable people for a given project description."""
        self.people_collection = self.chroma_client.get_or_create_collection("people1")
        self.project_collection = self.chroma_client.get_or_create_collection("projects1")
        data = request.json
        project_description = data['project_description']
        n_results = data.get('n_results', 5)

        # Perform similarity search in people collection
        results = self.people_collection.query(
            query_texts = [project_description],
            n_results=100  # Get more results initially for filtering
        )

        matched_people = []
        for i, person_id in enumerate(results['ids'][0]):
            person_data = self.people_collection.get(ids=[person_id])
            person_metadata = person_data['metadatas'][0]

            matched_people.append({
                'id': person_id,
                'name': f"{person_metadata.get('first_name', '')} {person_metadata.get('last_name', '')}".strip(),
                'similarity_score': float(1 - results['distances'][0][i]),  # Convert distance to similarity score
            })

        # Sort by similarity score and limit to n_results
        matched_people.sort(key=lambda x: x['similarity_score'], reverse=True)
        matched_people = matched_people[:n_results]

        response_data = {
            'status': 'success',
            'project_description': project_description,
            'matched_people': matched_people
        }

        response = make_response(jsonify(response_data))
        response.status_code = 200
        return response

class MatchProjectsToPerson(Resource):
    def __init__(self,  api, chroma_client):
        self.api = api
        self.chroma_client = chroma_client
        self.people_collection = self.chroma_client.get_or_create_collection("people1")
        self.project_collection = self.chroma_client.get_or_create_collection("projects1")

    def post(self):
        """Find the most suitable projects for a given person based on similarity and metadata."""
        data = request.json
        person_id = data['person_id']
        n_results = data.get('n_results', 5)
        status_filter = data.get('status')
        max_team_size = data.get('max_team_size')
        max_distance = data.get('max_distance')

        person_data = self.people_collection.get(ids=[person_id])
        if not person_data['ids']:
            return jsonify({'status': 'error', 'message': 'Person not found.'}), 404
        
        person_embedding = person_data['embeddings'][0]
        
        # Perform similarity search in projects collection
        results = self.project_collection.query(
            query_embeddings=[person_embedding],
            n_results=100  # Get more results initially for filtering
        )
        
        matched_projects = []
        for i, project_id in enumerate(results['ids'][0]):
            project_data = self.project_collection.get(ids=[project_id])
            project_metadata = project_data['metadatas'][0]
            
            # Apply metadata filters
            if status_filter and project_metadata.get('status') != status_filter:
                continue
            if max_team_size and len(project_metadata.get('team_members', [])) >= max_team_size:
                continue
            if max_distance and results['distances'][0][i] > max_distance:
                continue
            
            matched_projects.append({
                'id': project_id,
                'title': project_metadata.get('title'),
                'similarity_score': 1 - results['distances'][0][i],  # Convert distance to similarity score
                'status': project_metadata.get('status'),
                'team_size': len(project_metadata.get('team_members', [])),
            })
        
        # Sort by similarity score and limit to n_results
        matched_projects.sort(key=lambda x: x['similarity_score'], reverse=True)
        matched_projects = matched_projects[:n_results]
        
        return jsonify({
            'status': 'success',
            'person_id': person_id,
            #'matched_projects': matched_projects
        })

class SimilarityScore(Resource):
    def __init__(self, api, chroma_client):
        self.api = api
        self.chroma_client = chroma_client
        self.people_collection = self.chroma_client.get_or_create_collection("people")
        self.project_collection = self.chroma_client.get_or_create_collection("projects")

    def post(self):
        """Calculate the similarity score between a specific person and project."""
        data = request.json
        person_id = data['person_id']
        project_id = data['project_id']

        person_data = self.people_collection.get(ids=[person_id])
        project_data = self.project_collection.get(ids=[project_id])

        if not person_data['ids']:
            return jsonify({'status': 'error', 'message': 'Person not found.'}), 404
        if not project_data['ids']:
            return jsonify({'status': 'error', 'message': 'Project not found.'}), 404

        person_embedding = person_data['embeddings'][0]
        project_embedding = project_data['embeddings'][0]

        # Calculate similarity score
        similarity_score = 1 - self.calculate_distance(person_embedding, project_embedding)

        
        response_data = {
                'status': 'success',
                'person_id': person_id,
                'project_id': project_id,
                'similarity_score': float(similarity_score)
            }
        return make_response(response_data)

    def calculate_distance(self, embedding1, embedding2):
        # Implement your distance calculation here (e.g., cosine distance)
        # For simplicity, let's assume we're using Euclidean distance
        return sum((a - b) ** 2 for a, b in zip(embedding1, embedding2)) ** 0.5
