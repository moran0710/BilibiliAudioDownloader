import hashlib
import urllib
from time import time
from urllib import parse

from requests_utils.model import session


def wbi_sign(raw_params:dict):
    raw_params = raw_params.copy()
    raw_params["wts"]=round(time())
    raw_params = dict(sorted(raw_params.items()))
    query = urllib.parse.urlencode(raw_params)
    sign = hashlib.md5((query+mixin_key).encode()).hexdigest()
    raw_params["w_rid"] = sign
    return raw_params

def get_mixin_key():

    resp = session.get('https://api.bilibili.com/x/web-interface/nav')
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    return img_key+ sub_key

def remake_key():
    raw = get_mixin_key()
    map_lst = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]
    result = ""
    for i in map_lst:
        result += raw[i]
    return result

mixin_key = get_mixin_key()