from os import name
from flask import Flask
from flask_restful import Resource, abort, reqparse,fields,marshal_with
from sqlalchemy.orm import session

from .models import Link, db

parser = reqparse.RequestParser()
parser.add_argument('original_url', type=str, help='Original URL')
parser.add_argument('short_url', type=str, help='Short URL')
parser.add_argument('visits', type=int, help='Visits')

resource_fields = {
    'id' : fields.Integer,
    'original_url' : fields.String,
    'short_url' : fields.String,
    'visits' : fields.Integer,
    'date_created' : fields.DateTime
}

class Url(Resource):
    @marshal_with(resource_fields)
    def get(self,url_id):
        result = Link.query.filter_by(id=url_id).first()
        if not result:
            abort(404,message="Url not found")
        return result

    @marshal_with(resource_fields)
    def post(self,url_id):
        args = parser.parse_args()
        result = Link.query.filter_by(id=url_id).first()
        if result:
            abort(409, message="Url already exists")
        link  = Link(id=url_id, original_url=args['original_url'], short_url=args['short_url'])
        db.session.add(link)
        db.session.commit()
        return link, 201

    @marshal_with(resource_fields)
    def put(self,url_id):
        args = parser.parse_args()
        result = Link.query.filter_by(id=url_id).first()
        if not result:
            abort(409, message="Url does not exists")
        
        if args['original_url']:
            result.original_url = args['original_url']
        if args['short_url']:
            result.short_url = args['short_url']
        db.session.commit()
        return result
    
    def delete(self, url_id):
        result = Link.query.filter_by(id=url_id).first()
        if not result:
            abort(409, message="Url does not exists")
        db.session.delete(result)
        db.session.commit()
        return '', 204

class UrlView(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = Link.query.all()
        return result

def initialize_routes(api):
    api.add_resource(Url,'/api/<int:url_id>')
    api.add_resource(UrlView,'/api/')