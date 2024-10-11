from flask_restx import Resource
from flask import request, jsonify
from flask_restx import Resource
from flask import request, jsonify
import PyPDF2
import io
from werkzeug.datastructures import FileStorage
import uuid

class ProjectsApi(Resource):
    def __init__(self, api, chroma_client):
        self.chroma_client = chroma_client
        self.api = api

    def post(self):
        """Add a new project."""

        self.collection = self.chroma_client.get_or_create_collection("project1")
        data = request.json
        documents = data['project_description']
        project_id = data['id']
        metadata = {k: v for k, v in data.items() if k not in ['id', 'project_description']}

        # Add project to ChromaDB
        self.collection.add(ids = [project_id], metadatas = [metadata], documents = [documents])
        return jsonify({'status': 'success', 'message': 'Project added successfully.'})

    def get(self):
        """Retrieve all Projects."""
        try:
            # Fetch all data from ChromaDB
            self.collection = self.chroma_client.get_or_create_collection("project1")
            all_projects = self.collection.get()  # Adjust n_results as needed
            if all_projects and len(all_projects) > 0:
                return jsonify(all_projects)  # Return the data with a 200 OK status
            else:
                return jsonify({'status': 'error', 'message': 'No projects found.'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

class ProjectApi(Resource):
    def __init__(self, api, chroma_client):
        self.api = api
        self.chroma_client = chroma_client

    def get(self, project_id):
        """Retrieve a specific project by ID."""

        self.collection = self.chroma_client.get_or_create_collection("project1")
        # Query specific project
        project_data = self.collection.get(ids=project_id)
        if project_data:
            return jsonify(project_data)
        return jsonify({'status': 'error', 'message': 'Project not found.'})

    def delete(self, project_id):
        """Delete a project by ID."""
        # To be implemented
        return jsonify({'status': 'error', 'message': 'Deletion not implemented yet.'})


class DocumentUploadApi(Resource):
    def __init__(self, api, chroma_client):
        self.api = api
        self.chroma_client = chroma_client
        self.collection = self.chroma_client.get_or_create_collection("documents")

    def post(self):
        """Upload a PDF document, embed it, and store with metadata."""
        try:
            # Check if the post request has the file part
            if 'file' not in request.files:
                return jsonify({'status': 'error', 'message': 'No file part in the request'})
            
            file = request.files['file']
            
            # If the user does not select a file, the browser submits an empty file without a filename
            if file.filename == '':
                return jsonify({'status': 'error', 'message': 'No selected file'})
            
            if file and file.filename.lower().endswith('.pdf'):
                pdf_content = file.read()
                
                # Extract text from PDF
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                text_content = ""
                for page in pdf_reader.pages:
                    text_content += page.extract_text()
                
                # Generate a unique ID for the document
                document_id = str(uuid.uuid4())
                
                # Get metadata from the request
                metadata = request.form.to_dict()
                metadata['filename'] = file.filename
                
                # Add document to ChromaDB
                self.collection.add(
                    ids=[document_id],
                    metadatas=[metadata],
                    documents=[text_content]
                )
                
                return jsonify({
                    'status': 'success',
                    'message': 'Document uploaded and embedded successfully',
                    'document_id': document_id
                })
            else:
                return jsonify({'status': 'error', 'message': 'Invalid file format. Please upload a PDF.'})
        
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})