from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from elasticsearch import Elasticsearch
import warnings

# initializes elasticsearch and flask modules

try:
    es = Elasticsearch()
except ImportError:
    warnings.warn('Elasticsearch is not installed.')



# # blueprint for User
elastic = Blueprint('elastic', 'elastic')

# test route 
# @elastic.route('/', methods=['GET'])
# def index():
#     results = es.get(index='contents', doc_type='title', id='my-new-slug')
#     return jsonify(results['_source'])