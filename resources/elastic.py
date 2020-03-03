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



# gets all restaurants within approximately 20 miles of the users location
@elastic.route('/restaurants/nearme', methods=['GET'])
def get_restaurants_near_user():

    # gets the users location
    clients_latitude = float(request.args.get('latitude'))
    clients_longitude = float(request.args.get('longitude'))

    results = elasticsearch_client.search(
        index='restaurants',
        body={
            'query': {
                'bool': {
                    'must': {
                        'range': {
                            'latitude': {
                                'lte': str(clients_latitude + 0.3),
                                'gte': str(clients_latitude - 0.3),
                            },
                        }
                    },
                    'must': {
                        'range': {
                            'longitude': {
                                'lte': str(clients_longitude + 0.3),
                                'gte': str(clients_longitude - 0.3)
                            }
                        }
                    }
                }
            }
        }
    ) 

    return jsonify(
        data=results['hits']['hits'],
        status={
            'code': 200,
            'message': 'Successfully found resources'
        }
    )









