import argparse
import queue
import re
from concurrent.futures import ThreadPoolExecutor

from pygments.lexers.sql import re_error
from rich.progress import track

from download_utils.single import download
from get_favourite_videos.get_favourite import get_favourite_videos
from get_seasons_archives.apis import get_seasons
from login.blogin import login
from login.exit_login import exit_login
from requests_utils.model import session, console


def get_bvid(raw_link:str):
    """从url或者其他来源获取BV号"""
    try:
        return re.search(r'(BV.*?).{10}', raw_link).group(0)
    except AttributeError:
        return None

def get_avid(raw_link:str):
    """从url或者其他来源获取AV号"""
    raw_link = raw_link.replace("//", "/")
    raw_links = raw_link.split("/")
    for string in raw_links:
        if "av" in string:
            return string

def translate_avid_2_bvid(raw_link:str):
    avid = get_avid(raw_link)[2:]
    resp = session.get("https://api.bilibili.com/x/web-interface/view", params={"aid": avid}).json()
    return resp["data"]["bvid"]

def main_with_no_command_arg():
    try:
        with open("links.txt", "r", encoding="utf-8") as f:
            links = f.readlines()
    except FileNotFoundError:
        console.print("没有找到links.txt，需要新建一个links.txt [请参阅readme.md]")
        with open("links.txt", "w", encoding="utf-8") as f:
            pass
        return

    videos = queue.Queue()
    for link in track(links,description="正在整理BVID...."):
        bvid = get_bvid(link)
        if bvid is None:
            bvid = translate_avid_2_bvid(link)
            if bvid is None:
                continue
        videos.put(bvid)
    videos.put("STOP")
    way = input(r"请选择使用单线程模式([s]single)\\多线程模式([t]thread)  default:[s]single"+"\n")+"   "
    if way[0] == "t":
        thread_download(videos)
        return

    single_download(videos)



class StopLoopException(Exception):
    pass


def thread_download(videos:queue.Queue):
    try:
        count = int(input("请输入线程数"))
    except ValueError:
        console.print("输入错误，以8线程模式运行")
        count = 8
    pool = ThreadPoolExecutor(max_workers=count)
    futures = []
    for i in range(count):
        futures.append(pool.submit(download, videos))

    try:
        while True:
            for index, future in enumerate(futures):
                if videos.empty():
                    raise StopLoopException
                futures[index] = pool.submit(download, videos)
    except StopLoopException:
        pass

    console.print("下载完成")


def single_download(videos):
    while True:
        res = download(videos)
        if res is None:
            break
    console.print("下载完成")

def re_exit():
    input()
    exit(0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Bilibili音频下载工具\n用于从B站爬取视频")
    parser.add_argument("mode",type=str,help="工具使用的模式，login: 登录工具， down/download：下载模式，默认为下载模式", default="", const=0, nargs='?' )
    args = parser.parse_args()
    if args.mode == "login":
        login()
        exit(0)
    if args.mode == "download" or args.mode == "down":
        main_with_no_command_arg()

    else:
        print("进入登录([l]login)\\下载模式([d]download)\\退出登录([e]exitlogin)")
        print("从收藏夹生成links.txt([f]favourite_to_links)\\从视频合集生成links.txt([s]seasons_archives_to_links)")
        # print("")
        print()
        way = input(r"请选择模式:  default:[d]download"+"\n")+"   "
        if way[0] == "l":
            login()
            re_exit()
        if way[0] == "e":
            exit_login()
            re_exit()
        if way[0] == "f":
            get_favourite_videos()
            re_exit()
        if way[0] == "s":
            get_seasons()

        main_with_no_command_arg()
        re_exit()


