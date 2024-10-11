from flask_restx import Resource, fields
from sentence_transformers import SentenceTransformer
from flask import request, jsonify


def create_document_string(person_data):
    experience = str(person_data.get('experience', ''))
    projects = ' '.join(person_data.get('projects', []))
    skills = ' '.join(person_data.get('skills', []))
    
    return f"{experience} {projects} {skills}".strip()

class PeopleApi(Resource):
    def __init__(self, api, chroma_client):
        self.chroma_client = chroma_client
        self.api = api

    def post(self):
        """Add a new person."""
        self.collection = self.chroma_client.get_or_create_collection(name = "people1")
        data = request.json
        person_id = data['id']
        documents = create_document_string(data)
        metadata = {k: v for k, v in data.items() if k not in ['id', 'experience', 'projects', 'skills']}
        # Add person to ChromaDB
        self.collection.add(ids = [person_id], metadatas = [metadata], documents = [documents])
        return jsonify({'status': 'success', 'message': 'Person added successfully.'})

    def get(self):
        """Retrieve all people."""
        # Fetch all data from ChromaDB
        self.collection = self.chroma_client.get_or_create_collection(name = "people1")
        all_people = self.collection.get()  # Adjust n_results as needed
        return jsonify(all_people)

class PersonApi(Resource):
    def __init__(self, api, chroma_client):
        self.chroma_client = chroma_client
        self.api = api

    def get(self, person_id):
        """Retrieve a specific person by ID."""

        self.collection = self.chroma_client.get_or_create_collection("people1")
        # Query specific person
        person_data = self.collection.get(ids= person_id)
        
        if person_data and len(person_data) > 0:
            return jsonify(person_data)  # Return the first result
        return jsonify({'status': 'error', 'message': 'Person not found.'})

    
    def delete(self, person_id):
        """Delete a person by ID."""
        # Implement your deletion logic (ChromaDB doesn't support deletion directly)
        return jsonify({'status': 'error', 'message': 'Deletion not implemented yet.'})
