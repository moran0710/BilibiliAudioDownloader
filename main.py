import queue
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from rich.console import Console
from rich.progress import track

from model import console, session
from single import download

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

def main():
    try:
        with open("links.txt", "r", encoding="utf-8") as f:
            links = f.readlines()
    except FileNotFoundError:
        console.print("没有找到links.txt，需要新建一个links.txt [请参阅readme.md]")
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


if __name__ == '__main__':
    main()

