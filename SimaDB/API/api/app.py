from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from chromadb import PersistentClient
from routes import create_routes

app = Flask(__name__)

api = Api(app, version='1.0', title='SimiDB API', description='SimiDB')

# Initialize ChromaDB client
chroma_client = PersistentClient(path='./chromadb_data')

# Init API and routes
create_routes(api=api, chroma_client=chroma_client)


if __name__ == '__main__':
    app.run(debug=True)
