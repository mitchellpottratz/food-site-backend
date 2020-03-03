from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from elasticsearch import Elasticsearch
import warnings

elastic = Blueprint('elastic', 'elastic')

elasticsearch_client = Elasticsearch(['http://35.184.144.209:9200/'])



@elastic.route('/restaurants', methods=['GET'])
def all_restaurants():
    results = elasticsearch_client.search(
        index='restaurants',
        body={
            'from': 0,
            'size': 100,
            'query': {
                'match_all': {}
            }
        }
    )
    return jsonify(results)



