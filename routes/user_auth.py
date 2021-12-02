from flask import request
import hashlib
from main import app
import base64
from models import *
import datetime
import jwt


@app.route('/user/new/signup', methods=['POST'])
def user_new_signup():
    json_data = request.get_json()
    if 'username' in json_data and 'password' in json_data and 'email' in json_data:
        # Create New User
        email = json_data['email']
        username = json_data['username']
        password = json_data['password']
        checking_user = check_user_before_sign_up(email)
        if not checking_user and checking_user is not None:
            user_credentials = set_new_user_sign_up(email, username, password)
            if user_credentials:
                return {'code': 200, 'message': "New User Added !!", "token": str(user_credentials)}
        return {'code': 200, 'message': "User already Exists! Please Login Instead "}


@app.route('/user/login', methods=['POST'])
def set_user_login():
    json_data = request.get_json()
    if 'email' in json_data and 'password' in json_data:
        # Create New User
        email = json_data['email']
        password = json_data['password']
        h = hashlib.md5(password.encode())
        check_credentials = res_users.ResUsers().search({'email': email, 'password': h.hexdigest()}, limit=1)

        if check_credentials:
            # user_id = False
            # for element in check_credentials:
            #     user_id = element['_id']
            get_user_access_token = auth_user_key.AuthUsersKeys().search({'user_id': str(check_credentials['_id'])},
                                                                         limit=1)
            if get_user_access_token:
                return {'code': 200, 'token': get_user_access_token['token']}
            else:
                expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=180)
                iat_date = datetime.datetime.utcnow()
                set_token = encode_auth_token(expire_date, iat_date, str(check_credentials['_id']))
                if set_token:
                    shrink_token = base64ToString(set_token)
                    new_auth = auth_user_key.AuthUsersKeys().create(
                        {'user_id': str(check_credentials['_id']), 'token': shrink_token, 'expire_date': expire_date,
                         'iat_date': iat_date})
                    return {'code': 200, 'token': shrink_token}

    return {'code': 200, 'message': "email or password is wrong"}


def encode_auth_token(expire_date, iat_time, user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': expire_date,
            'iat': iat_time,
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def check_user_before_sign_up(email_username):
    if email_username:
        sql_statement = {"$or": [{'username': email_username}, {'email': email_username}]}
        fetched_data = res_users.ResUsers().search(sql_statement)
        if fetched_data and fetched_data is not None:
            data_dict = {}
            for object in fetched_data:
                data_dict[str(object['_id'])] = {'username': object['username'], 'email': object['email']}
            return data_dict
        return False


def set_new_user_sign_up(email, username, password):
    if username and password:
        data_dict = {}
        expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=180)
        # data_dict['expire_date'] = expire_date
        iat_date = datetime.datetime.utcnow()
        # data_dict['iat_date'] = iat_date
        data_dict['email'] = email
        data_dict['username'] = username
        h = hashlib.md5(password.encode())
        data_dict['password'] = h.hexdigest()
        # create New User
        new_user = res_users.ResUsers().create(data_dict)
        if new_user:
            set_token = encode_auth_token(expire_date, iat_date, str(new_user))
            if set_token:
                shrink_token = base64ToString(set_token)
                # check user if exists in token auth table to update it or create new auth record related to this user
                check_auth = auth_user_key.AuthUsersKeys().search({'user_id': str(new_user)}, limit=1)
                if check_auth:
                    auth_user_key.AuthUsersKeys().write(str(check_auth), {'token': shrink_token})
                else:
                    new_auth = auth_user_key.AuthUsersKeys().create(
                        {'user_id': str(new_user), 'token': shrink_token, 'expire_date': expire_date,
                         'iat_date': iat_date})
                return shrink_token
        return False


def stringToBase64(s):
    return base64.encode(s)


def base64ToString(b):
    return b.decode('utf-8')[:36]
