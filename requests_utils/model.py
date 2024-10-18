import http.cookiejar
import os.path

import requests
from rich.console import Console

session = requests.Session()
console = Console()

session.cookies = http.cookiejar.LWPCookieJar(filename='bcookies.txt')
try:
    session.cookies.load('bcookies.txt', ignore_discard=True, ignore_expires=True)
    console.print("检测到登录状态，自动加载cookie")
except FileNotFoundError:
    pass
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
    'Referer': 'https://www.bilibili.com/'
}
session.headers.update(headers)