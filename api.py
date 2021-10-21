from requests import get
from requests import post

BASE_API = "http://f43c-82-215-102-36.ngrok.io/api/"
SECTIONS_API = BASE_API + 'sectors/all'
STORE_RESULT = BASE_API + 'participant/add'
CHECK_USER = BASE_API + 'participant/check'
CHILD_SELECTORS = BASE_API + 'sectors/child_sector/'
REGIONS = BASE_API + 'sectors/region'


def get_categories():
    return get(SECTIONS_API).json()


def store_result(data: dict):
    request = post(STORE_RESULT, data=data)
    print(request.content[:300])

    return request.json()


def check_participant(data: dict):
    request = post(CHECK_USER, data=data)
    return request.json()['success']


def get_child_categories(parent_id: int):
    return get(CHILD_SELECTORS + str(parent_id)).json()


def get_regions():
    return get(REGIONS).json()
