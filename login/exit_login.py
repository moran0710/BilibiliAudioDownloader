import os
from json import JSONDecodeError

import requests

from requests_utils.model import session, console


def exit_login():
    try:
        resp = session.post("https://passport.bilibili.com/login/exit/v2",
                            data={"biliCSRF":requests.utils.dict_from_cookiejar(session.cookies)["bili_jct"]}).json()
    except JSONDecodeError as e:
        console.print("退出登录失败：您还未登录")
        return

    if resp["code"] == 0:
        console.print("请求成功，已经退出登录，正在删除cookie文件")
        os.remove("bcookies.txt")
        return
    else:
        console.print("退出登录失败，正在打印响应")
        console.print(resp)
        return