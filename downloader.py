import os

from model import session


def download_audio(url:str, title:str, is_flac:bool):
    filename = title+".flac" if is_flac else title+".mp3"

    filename = filename.replace("\\", "")
    filename = filename.replace(r"/", "")

    # 先新建文件

    if not os.path.exists("result"):
        os.mkdir("result")

    with open(os.path.join(".", "result", filename), "wb") as file:
        file.write(session.get(url).content)