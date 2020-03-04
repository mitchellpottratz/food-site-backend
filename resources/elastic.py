from datetime import datetime
from flask import Flask, jsonify, request, Blueprint
from elasticsearch import Elasticsearch
import warnings

elastic = Blueprint('elastic', 'elastic')

elasticsearch_client = Elasticsearch(['http://35.184.144.209:9200/'])


# Ping route
@elastic.route('/restaurants/ping', methods=['GET'])
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


# returns all of the restaurants near a users location
@elastic.route('/restaurants/nearme', methods=['GET'])
def get_restaurants_near_user():

    # gets the users location
    clients_latitude = float(request.args.get('latitude'))
    clients_longitude = float(request.args.get('longitude'))

    results = elasticsearch_client.search(
        index='restaurants',
        body={
            'from': 0,
            'size': 100,
            'query': {
                'bool': {
                    'filter': {
                        'geo_distance': {
                            'distance': "15km",
                            'location': {
                                'lat': clients_latitude,
                                'lon': clients_longitude
                            }
                        }
                    },
                    'must': {
                        'match_all': {}
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









