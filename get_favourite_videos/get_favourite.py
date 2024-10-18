import math

from biliapis.get_login_user_info import get_login_user_mid
from get_favourite_videos.apis import get_users_all_favourite_collection
from requests_utils.model import console, session


def get_favourite_videos():
    way = input("请选择从自己([s]self)，还是从其他用户([o]others)获取收藏夹内容   default:[s]self\n")
    if way[0] == "o":
        mid = input("请输入用户mid\n")
    else:
        mid = get_login_user_mid()
    get_favourite(mid)

def get_favourite(mid):
    if mid == 0:
        console.print("您尚未登陆")
        return
    collections = get_users_all_favourite_collection(mid)
    mlid, fid = choose_favourite(collections)
    videos = get_all_video_bvids(mlid)
    print("正在写入")

    with open("links.txt", "w", encoding="utf-8") as f:
        f.writelines(videos)

    print("写入完成")

def get_all_video_bvids(mlid):
    result = []
    page_num = 1
    resp = session.get("https://api.bilibili.com/x/v3/fav/resource/list", params={"media_id":mlid, "ps":20, "pn":page_num}).json()
    if resp["data"] is None:
        return result
    total_page = math.ceil(resp["data"]["info"]["media_count"]/20)
    while True:
        print(f"正在解析此收藏夹第{page_num}/{total_page}页")
        resp = session.get("https://api.bilibili.com/x/v3/fav/resource/list", params={"media_id":mlid, "ps":20, "pn":page_num}).json()
        if resp["data"] is None:
            return result

        if not resp["data"]["has_more"]:
            break

        for video in resp["data"]["medias"]:
            if video["attr"] != 0:
                continue
            result.append(f"{video["bv_id"]} <--> {video["title"]}\n")

        page_num += 1
    print("解析完成")
    return result


def choose_favourite(favourite_collections):
    for index, favourite in enumerate(favourite_collections):
        print(f"{index}. 标题：{favourite["title"]}")
        print(f"    视频数量：{favourite["media_count"]}")

    print()
    try:
        arg =  int(input("请选择你想要转换的收藏夹编号，默认选择第0个"))
    except ValueError:
        arg = 0
    return favourite_collections[arg]["id"], favourite_collections[arg]["fid"]