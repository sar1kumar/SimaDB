from flask_restx import Api
from people import PeopleApi, PersonApi
from projects import ProjectsApi, ProjectApi, DocumentUploadApi
from similarity import MatchPeopleToProject, MatchProjectsToPerson, SimilarityScore

def create_routes(api: Api, chroma_client):
    
    api.add_resource(PeopleApi, '/people/', resource_class_args=(chroma_client,))
    api.add_resource(PersonApi, '/people/<person_id>', resource_class_args=(chroma_client,))
    
    # Routes for Projects
    api.add_resource(ProjectsApi, '/projects/', resource_class_args=(chroma_client,))
    api.add_resource(ProjectApi, '/projects/<project_id>', resource_class_args=(chroma_client,))
    

    api.add_resource(DocumentUploadApi, '/upload/', resource_class_args=(chroma_client,))
    
    api.add_resource(MatchPeopleToProject, '/similarity/match-people-to-project', resource_class_args=(chroma_client,))
    api.add_resource(MatchProjectsToPerson, '/similarity/match-projects-to-person', resource_class_args=( chroma_client,))
    api.add_resource(SimilarityScore, '/similarity/similarity-score', resource_class_args=(chroma_client,))
    
    #api.add_resource(DatabaseAPI, '/api/databases')
    #api.add_resource(TableAPI, '/api/tables/<string:database_name>')
    #api.add_resource(Tabledata, '/api/tabledata/<string:database_name>/<string:table_name>')