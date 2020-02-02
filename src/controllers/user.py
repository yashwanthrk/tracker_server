from flask import request, Response
from flask_restful import Resource
from bson.objectid import ObjectId

from datetime import datetime
from io import StringIO
import csv

from src.database.models import USER

from src.helpers.decorators import authorize, authorize_admin, authorize_super_admin
from src.helpers.responses import custom_error_response, success_response_data
from src.utils.time_conversions import timestamp_to_date_month_year, timestamp_to_hour_min_secs
from bson import json_util
import json


class Register(Resource):
    def post(self, *args, **kws):
        # get the post data
        post_data = request.form
        # print(post_data)

        # converting mongo engine to pymongo raw queries
        user_collection = USER._get_collection()
        # check if user already exists
        user = user_collection.find_one({'email': post_data.get('email')})
        # print(user)
        if user:
            return custom_error_response(400, "Email is already taken")

        new_user = USER(email=post_data.get('email'),
                        password=post_data.get('password')).save()
        # user_dict = {'email':post_data.get('email'), 'password':post_data.get('password')}
        # new_user = user_collection.insert(user_dict)

        # generate token now

        token = USER.encode_auth_token(str(new_user['user_id']))
        print(token)
        response = {'token': token}
        return success_response_data(response)


class Login(Resource):
    def post(self, *args, **kws):
        post_data = request.form

        # converting mongo engine to pymongo raw queries
        user_collection = USER._get_collection()

        # check if user already exists
        user = user_collection.find_one({'email': post_data.get('email')})
        # print(user, user.get('password'))

        if not user:
            return custom_error_response(
                400, "Please register to login or check your email")

        # check if email and password are correct
        if not (USER.compare_password(user.get('password'),
                                      post_data.get('password'))):
            return custom_error_response(400, "Password incorrect")

        # generate token now
        print(user)
        token = USER.encode_auth_token(str(user['user_id']))
        print(token)
        response = {'token': token}
        return success_response_data(response)


class Protected(Resource):
    @authorize
    def get(self, *args, **kws):
        user_id = kws['user_id']
        user_collection = USER._get_collection()
        user = user_collection.aggregate([{
            '$match': {
                'user_id': user_id
            }
        }, {
            "$project": {
                '_id': 0,
            }
        }])
        print(user)
        return success_response_data(user)
