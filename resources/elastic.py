from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from elasticsearch import Elasticsearch

# initializes elasticsearch and flask modules
es = Elasticsearch()
# app = Flask(__name__)

# # blueprint for User
elastic = Blueprint('elastic', 'elastic')

# test route 
# @elastic.route('/', methods=['GET'])
# def index():
#     results = es.get(index='contents', doc_type='title', id='my-new-slug')
#     return jsonify(results['_source'])