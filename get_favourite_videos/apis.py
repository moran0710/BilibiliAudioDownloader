from requests_utils.model import session


def get_users_all_favourite_collection(mid:int):
    resp = session.get("https://api.bilibili.com/x/v3/fav/folder/created/list-all", params={"up_mid":mid}).json()
    if resp["code"] == -400:
        return []
    print(resp)
    if not resp["data"]  is None:
        if not resp["data"]["list"] is None:
            favourite_collections = resp["data"]["list"]
            return favourite_collections
