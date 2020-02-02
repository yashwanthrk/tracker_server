from flask_mongoengine import MongoEngine
from mongoengine import Document, connect
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt
import uuid

from environs import Env

env = Env()
env.read_env()
bcrypt = Bcrypt()

from mongoengine import (DateTimeField, StringField, ReferenceField, ListField,
                         FileField, ImageField, EmailField, BooleanField,
                         IntField)
# connect(
#     'app12345678',
#     username='heroku',
#     password='a614e68b445d0d9d1c375740781073b4',
#     host='mongodb://<user>:<password>@alex.mongohq.com:10043/app12345678',
#     port=10043
# )

# connect(db="mail_mama", alias='default')
connect(  
    # username='heroku',
    # password='a614e68b445d0d9d1c375740781073b4',
    host='mongodb+srv://yashwanth:J4RHGOlPv8pvR4bb@cluster0-trvai.mongodb.net/MAILMAMA?retryWrites=true&w=majority',
    # port=10043
    )

db = MongoEngine()

# def initialize_db(app):
#     db.init_app(app)


class BaseDocument(Document):
    created_on = IntField(default=int(datetime.now().timestamp() * 1000))
    modified_on = IntField()
    meta = {
        'indexes': ['created_on', 'modified_on'],
        'allow_inheritance': True,
        'abstract': True,
    }


class USER(BaseDocument):
    # email = StringField('email',
    #                     validators=[
    #                         InputRequired(),
    #                         Email(message='Invalid email'),
    #                         Length(max=30)
    #                     ])
    # password = PasswordField(
    #     'password', validators=[InputRequired(),
    #                             Length(min=6, max=20)])
    user_id = StringField(default=str(uuid.uuid4()))
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    first_name = StringField(max_length=20)
    last_name = StringField(max_length=20)
    full_name = StringField(max_length=40)
    mobile_no = StringField(min_length=10, max_length=10)
    role = StringField()
    meta = {'indexes': ['email', 'mobile_no', 'user_id'], 'collection': 'users'}

    def __init__(self, email, password, *args, **kwargs):
        super(USER, self).__init__(*args, **kwargs)
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, int(env('BCRYPT_LOG_ROUNDS'))).decode('utf-8')

    def compare_password(hashed_password, password):
        # print(password, hashed_password)
        return bcrypt.check_password_hash(hashed_password, password)

    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=30),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, env('SECRET_KEY'),
                              algorithm='HS256').decode("utf-8")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        # try:
        payload = jwt.decode(auth_token, env('SECRET_KEY'))
        return payload['sub']
        # is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        # if is_blacklisted_token:
        #     return 'Token blacklisted. Please log in again.'
        # else:
        #     return payload['sub']
        # except jwt.ExpiredSignatureError:
        #     return 'Signature expired. Please log in again.'
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'


# class Post(Document):
#     title = StringField(required=True, max_length=200)
#     content = StringField(required=True)
#     author = StringField(required=True, max_length=50)
#     published = DateTimeField(default=datetime.datetime.now)