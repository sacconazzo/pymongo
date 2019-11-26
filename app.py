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
        page_sanitized = json.loads(json_util.dumps(x))
        return page_sanitized
        # return jsonify(x)

class Employees_Filter(Resource):
    def get(self, string_find):
        x = mycollection.find({"name": {'$regex': string_find}})
        page_sanitized = json.loads(json_util.dumps(x))
        return page_sanitized
        # return jsonify(x)

class Employees_Insert(Resource):
    def get(self, employee_name):
        print(employee_name)
        result = mycollection.insert({"name": employee_name})
        page_sanitized = json.loads(json_util.dumps(result))
        return page_sanitized


api.add_resource(Employees, '/employees')  # Route_1
api.add_resource(Employees_Filter, '/employees/<string_find>')  # Route_1
api.add_resource(Employees_Insert, '/employee/<employee_name>')  # Route_3


if __name__ == '__main__':
    app.run(port='5002')
