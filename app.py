import pymongo
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util, ObjectId
import json

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycollection = mydb['scn']

app = Flask(__name__)
auth = HTTPBasicAuth()
api = Api(app)

users = {
    "test": generate_password_hash("test"),
    "scn": generate_password_hash("try")
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


class Employees(Resource):
    @auth.login_required
    def get(self):
        x = mycollection.find()
        return json.loads(json_util.dumps(x))
        # return jsonify(x)


class Employees_Filter(Resource):
    @auth.login_required
    def get(self, string_find):
        x = mycollection.find({"name": {'$regex': string_find}})
        return json.loads(json_util.dumps(x))


class Employees_Insert(Resource):
    @auth.login_required
    def get(self, string_name):
        result = mycollection.insert({"name": string_name})
        return json.loads(json_util.dumps(result))


class Employees_Insert_Complete(Resource):
    @auth.login_required
    def post(self):
        result = mycollection.insert(json.loads(request.get_data()))
        return json.loads(json_util.dumps(result))


class Employees_Delete(Resource):
    @auth.login_required
    def delete(self, oid):
        mycollection.delete_one({'_id': ObjectId(oid)})
        return "deleted", 204


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Employees_Filter, '/employees/<string_find>')  # Route_2
api.add_resource(Employees_Insert, '/employee/<string_name>')  # Route_3
api.add_resource(Employees_Insert_Complete, '/employee')  # Route_4
api.add_resource(Employees_Delete, '/employee/<oid>')  # Route_5


if __name__ == '__main__':
    app.run(port='5002')
