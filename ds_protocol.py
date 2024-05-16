# ds_protocol.py

# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# THY TRAN
# THYNT1@UCI.EDU
# 90526048

import json
import time
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
Response = namedtuple("Response", ["type", "message", "token"])

def extract_json(json_msg:str) -> tuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
  
    TODO: replace the pseudo placeholder keys with actual DSP protocol keys
    '''

    ex_dict = json_to_dict(json_msg)
    ex_json = Response(ex_dict["type"], ex_dict["message"], ex_dict["token"])
    return ex_json


def json_to_dict(json_to_decode: str):
    '''

    Decodes a json string to a dictionary

    '''
    try:
        json_obj = json.loads(json_to_decode)

    except json.JSONDecodeError:
        print("Json cannot be decoded.")
        return None

    else:
        json_keys, json_values = get_dict_lists(json_obj)
        json_dict = dict(zip(json_keys, json_values))
        return json_dict


def get_dict_lists(svr_dict: dict):
    keys = []
    values = []

    inner_dict = svr_dict["response"]

    for key in inner_dict:
        keys.append(key)
        values.append(inner_dict[key])
    
    if len(keys) < 3:
        keys.append("token")
        values.append(None)
    
    return keys, values


def get_dict_response(json_dict):
    assert len(json_dict["values"]) == 1 and type(json_dict["values"][0]) is dict #remove later
    print("doing get_dict_response")
    new_json_dict = json_dict["values"][0]

    return new_json_dict


def create_join_msg(username, password):
    msg = (f'{{"join": {{"username": "{username}", ' +
            f'"password": "{password}", "token": ""}}}}')
    return msg


def create_post_msg(post_entry, user_token):
    post_as_str = (f'{{"entry": "{post_entry}", ' +
                   f'"timestamp": "{time.time()}"}}')
    msg = f'{{"token": "{user_token}", "post": {post_as_str}}}'
    return msg

def create_bio_msg(user_bio, user_token):
    bio_pub = f'{{"entry": "{user_bio}", "timestamp": "{time.time()}"}}'
    msg = f'{{"token": "{user_token}", "bio": {bio_pub}}}'
    return msg