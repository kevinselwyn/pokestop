#!/usr/bin/python
# coding=utf-8
"""Pokéstop API"""

import sys
import argparse
import json
from pokestop import Pokestop
from flask import Flask, jsonify
from flask_restful import Api, reqparse, Resource

#----------------------------------------------------------------#
# Constants

HOSTNAME       = '0.0.0.0'
PORT           = 5000
MIME           = 'application/json'

#----------------------------------------------------------------#
# Utilities

def custom_error(status_code=404, message=''):
    """Returns custom JSON error"""

    response = jsonify({
        'status':  status_code,
        'message': message
    })

    response.status_code = status_code
    response.content_type = MIME

    return response

def get_args(variables=None):
    """Parses data or header arguments"""

    parser = reqparse.RequestParser()

    for variable, val in variables.iteritems():
        parser.add_argument(variable)

    args = parser.parse_args()
    output = {}

    for key, val in args.iteritems():
        output[key] = val

    for key, val in variables.iteritems():
        if not key in output or not output[key]:
            output[key] = val

    return output

def make_response(output):
    response = API.make_response(output, 200)
    response.headers['X-Best-Team'] = 'Team Mystic'

    return response

#----------------------------------------------------------------#
# App

APP = Flask(__name__)
API = Api(APP)

#----------------------------------------------------------------#
# Errors

APP.error_handler_spec[None][404] = lambda x: custom_error(404, 'Invalid endpoint')

#----------------------------------------------------------------#
# Nearby

class NearbyEndpoint(Resource):
    """Nearby endpoint"""

    routes = [
        '/nearby',
        '/nearby'
    ]

    @classmethod
    def get(cls):
        """Gets nearby"""

        args = get_args({
            'SACSID': '<SACSID cookie>',
            'csrftoken': '<csrftoken cookie>',
            'latitude': '',
            'longitude': '',
            'minimum': 0,
            'maximum': 1000,
            'order': 'ASC',
            'limit': 1000
        })

        if not 'SACSID' in args or not args['SACSID'] or not 'csrftoken' in args or not args['csrftoken']:
            return custom_error(401, 'Unauthorized request')

        if not 'latitude' in args or not args['latitude'] or not 'longitude' in args or not args['longitude']:
            return custom_error(404, 'Missing latitude and longitude')

        pokestop = Pokestop(args)
        output = pokestop.entities()
        response = make_response(json.loads(output))

        return response

    @classmethod
    def post(cls):
        """Gets nearby by post"""
        return cls.get()

API.add_resource(NearbyEndpoint, *NearbyEndpoint.routes)

#----------------------------------------------------------------#
# Pokéstop

class PokestopEndpoint(Resource):
    """Pokéstop endpoint"""

    routes = [
        '/pokestop',
        '/pokestop'
    ]

    @classmethod
    def get(cls):
        """Gets Pokéstop"""

        args = get_args({
            'SACSID': '<SACSID cookie>',
            'csrftoken': '<csrftoken cookie>',
            'guid': '',
            'latitude': '',
            'longitude': '',
            'minimum': 0,
            'maximum': 1000,
            'order': 'ASC',
            'limit': 1000
        })

        if not 'SACSID' in args or not args['SACSID'] or not 'csrftoken' in args or not args['csrftoken']:
            return custom_error(401, 'Unauthorized request')

        if not 'guid' in args or not args['guid']:
            return custom_error(404, 'Missing Pokéstop GUID')

        pokestop = Pokestop(args)
        output = pokestop.entity(args['guid'])
        response = make_response(json.loads(output))

        return response

    @classmethod
    def post(cls):
        """Gets Pokéstop by post"""
        return cls.get()

API.add_resource(PokestopEndpoint, *PokestopEndpoint.routes)

#----------------------------------------------------------------#
# Main

def main(argc=0, argv=None):
    """Main function"""

    parser = argparse.ArgumentParser()

    flags = [
        {'short': '-n', 'long': '--host'},
        {'short': '-p', 'long': '--port'},
        {'short': '-d', 'long': '--debug'}
    ]

    arguments = [
        {
            'help':     'Host',
            'required': False,
            'action':   'store',
            'default':  HOSTNAME
        },
        {
            'help':     'Port',
            'required': False,
            'action':   'store',
            'default':  PORT
        },
        {
            'help':     'Debugging',
            'required': False,
            'action':   'store_true',
            'default':  False
        }
    ]

    for i in range(0, len(flags)):
        parser.add_argument(flags[i]['short'], flags[i]['long'], **arguments[i])

    args = parser.parse_args(argv[1:argc])

    APP.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
