from biliapis.sign import wbi_sign
from requests_utils.model import session


def get_seasons_bvids(sid:int):
    resp = session.get("https://api.bilibili.com/x/polymer/web-space/seasons_archives_list", params=wbi_sign({
        "season_id":sid,
        "mid":114,
        "page_size":100
    })).json()
    print(resp)
    videos = resp["data"]["archives"]
    total = resp["data"]["page"]["total"]
    result = []
    while True:
        resp = session.get("https://api.bilibili.com/x/polymer/web-space/seasons_archives_list", params=wbi_sign({
            "season_id":sid,
            "mid":114,
            "page_size":100
        })).json()
        videos = resp["data"]["archives"]
        if len(result) >= total:
            break
        for video in videos:
            result.append(f"{video["bvid"]} <--> {video['title']}\n")
    return result

def get_seasons():
    mode = input("请选择使用合集链接模式([l]link)\\合集sid模式([s]sid)  default:[l]links")
    result = input("请输入查询参数")
    if mode[0] != "s":
        sid = get_sid_from_link(result)
    else:
        try:
            sid = int(result)
        except ValueError:
            print("sid错误")
            return
    videos = get_seasons_bvids(sid)
    print("正在写入")
    with open("links.txt", "w", encoding="utf-8") as f:
        f.writelines(videos)
    print("写入完成")


def get_sid_from_link(link:str):
    raw = link.split("/")
    for arg in raw:
        if "collectiondetail" in arg:
            arg = arg.replace("?", "")
            arg = arg.replace("collectiondetail", "")
            arg = arg.split("&")
            for sd in arg:
                if "sid" in sd:
                    return int(sd[4:])


