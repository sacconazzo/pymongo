from flask import Flask, request
from flask_restful import Resource, Api
from bson import json_util, ObjectId
import json
from flask_jsonpify import jsonify
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycollection = mydb['scn']

app = Flask(__name__)
api = Api(app)


class Employees(Resource):
    def get(self):
        x = mycollection.find()
        return json.loads(json_util.dumps(x))
        # return jsonify(x)


class Employees_Filter(Resource):
    def get(self, string_find):
        x = mycollection.find({"name": {'$regex': string_find}})
        return json.loads(json_util.dumps(x))


class Employees_Insert(Resource):
    def get(self, employee_name):
        result = mycollection.insert({"name": employee_name})
        return json.loads(json_util.dumps(result))


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Employees_Filter, '/employees/<string_find>')  # Route_2
api.add_resource(Employees_Insert, '/employee/<employee_name>')  # Route_3


if __name__ == '__main__':
    app.run(port='5002')
