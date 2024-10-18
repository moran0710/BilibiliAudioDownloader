from requests_utils.model import session


def get_login_user_mid():
    resp = session.get("https://api.bilibili.com/x/web-interface/nav").json()
    if resp["code"] == 0:
        return resp["data"]["mid"]
    else:
        return 0