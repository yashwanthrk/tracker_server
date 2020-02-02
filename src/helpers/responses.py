from flask import Response
import json
from bson import json_util

def no_auth_header_present():
  return Response(json.dumps({
    "message": "Missing Auth token"
  }), status=400, content_type='application/json')

def invalid_auth_header():
  return Response(json.dumps({
    "message": "Invalid Auth token"
  }), status=403, content_type='application/json')

def access_forbidden():
  return Response(json.dumps({
    "message": "User has no access to this feature"
  }), status=403, content_type='application/json')

def status_500():
  return Response(json.dumps({
    "message": "Something went wrong"
  }), status=500, content_type='application/json')

def custom_error_response(status, message):
  return Response(json.dumps({
    "message": message
  }), status=status, content_type='application/json')

def success_response(body, no_cache=False):
  ''' Expects body parameter to be an object, dumps the body as json while returning it'''
  resp = Response(json_util.dumps(body), status=200, content_type='application/json')
  if no_cache:
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['expires'] = '-1'
    resp.headers['pragma'] = 'no-cache'
  return resp

def success_response_data(body):
  ''' Expects body to be a string or object, adds the body to data key while returning'''
  return Response(json_util.dumps({
    'data': body,
    'status': 'OK'
  }), status=200, content_type='application/json')

def not_found():
  return Response(json.dumps({
    'status': 'Not Found',
    'message': 'Not Found',
  }), status=404, content_type='application/json')

def bad_request():
  return Response(json.dumps({
    'status': 'Bad request',
    'message': 'Bad request'
  }), status=400, content_type='application/json')

class AllowAuth:
  def options(self):
    return Response("", status=200, content_type='application.json', headers={
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization'
    })