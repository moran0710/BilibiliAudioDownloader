from queue import Queue

from biliapi_utils import wbi_sign
from download import download_audio

from model import session, console


def download(videos:Queue):
    next_video = videos.get()
    console.print(f"正在下载{next_video}")
    if next_video == "STOP":
        return
    cid, title = get_title_and_cid(next_video)

    video_download_info = get_video_download_info(cid, next_video)
    if video_download_info is None:
        return ""

    backup_url, base_url, is_flac = get_download_url(video_download_info)

    try:
        download_audio(base_url, title, is_flac)
        return ""

    except Exception as ex:
        console.print(f"Failed to try download audio {next_video}", ex)
        for url in backup_url:
            try:
                download_audio(url, title, is_flac)
                break
            except Exception as e:
                console.print(f"Failed to try download audio {next_video}", e)
        else:
            console.print(f"Failed to download audio {next_video}")
            return ""


def get_download_url(video_download_info):
    flac_info = video_download_info["flac"]
    if flac_info is None or flac_info["audio"] is None:
        base_url, backup_url = video_download_info["audio"][0]["base_url"], video_download_info["audio"][0][
            "backup_url"]
        is_flac = False
    else:
        base_url, backup_url = flac_info["audio"]["base_url"], flac_info["audio"]["backup_url"]
        is_flac = True
    return backup_url, base_url, is_flac


def get_video_download_info(cid, next_video):
    raw_params = {
        "bvid": next_video,
        "cid": cid,
        "fnval": 16
    }
    params = wbi_sign(raw_params)
    video_download_info = session.get(f"https://api.bilibili.com/x/player/wbi/playurl", params=params).json()
    if "v_voucher" in video_download_info["data"].keys():
        console.print("访问被风控")
        return
    video_download_info = video_download_info["data"]["dash"]
    return video_download_info


def get_title_and_cid(next_video):
    raw_params = {"bvid": next_video}
    params = wbi_sign(raw_params)
    info = session.get(f"https://api.bilibili.com/x/web-interface/wbi/view", params=params).json()
    title = info["data"]["title"]
    cid = info["data"]["cid"]
    return cid, title



