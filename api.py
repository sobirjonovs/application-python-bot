from requests import get
from requests import post

BASE_API = "http://8a12-82-215-102-133.ngrok.io/api/"
SECTIONS_API = BASE_API + 'sectors/all'
STORE_RESULT = BASE_API + 'participant/add'
CHECK_USER = BASE_API + 'participant/check'


def get_categories():
    return get(SECTIONS_API).json()


def store_result(data: dict):
    request = post(STORE_RESULT, data=data)
    return request.json()


def check_participant(data: dict):
    request = post(CHECK_USER, data=data)
    return request.json()['success']
