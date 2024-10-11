from flask_restx import fields

project_model = {
    'id': fields.String(required=True, description='Unique identifier for the project'),
    'title': fields.String(required=True, description='Title of the project'),
    'description': fields.String(required=True, description='Detailed description of the project'),
    'start_date': fields.Date(required=True, description='Project start date'),
    'end_date': fields.Date(description='Project end date (if applicable)'),
    'status': fields.String(required=True, enum=['planning', 'in_progress', 'completed', 'on_hold'], description='Current status of the project'),
    'skills_required': fields.List(fields.String, description='List of skills required for the project'),
    'team_members': fields.List(fields.String, description='List of person IDs associated with the project')
}


person_model = {
    'id': fields.String(required=True, description='Unique identifier for the person'),
    'name': fields.String(required=True, description='Full name of the person'),
    'email': fields.String(required=True, description='Email address of the person'),
    'skills': fields.List(fields.String, description='List of skills'),
    'experience': fields.Integer(description='Years of experience'),
    'bio': fields.String(description='Short biography'),
    'projects': fields.List(fields.String, description='List of project IDs the person is associated with')
}

