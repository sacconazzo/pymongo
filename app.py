from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import pymongo

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['mydatabase']
mycollection = mydb['scn']

app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def get(self):
        x = mycollection.count()
        return jsonify(x)

class Employees_Name(Resource):
    def get(self, employee_name):
        print(employee_name)
        result = mycollection.insert_one({"name" : employee_name})
        return jsonify(employee_name)
        

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Employees_Name, '/employees/<employee_name>') # Route_3


if __name__ == '__main__':
     app.run(port='5002')
