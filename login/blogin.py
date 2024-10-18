from time import sleep

import qrcode

from requests_utils.model import session, console


def get_login_qrcode_data():
    resp = session.get("https://passport.bilibili.com/x/passport-login/web/qrcode/generate").json()
    return  resp["data"]

def login():
    login_qrcode_data = get_login_qrcode_data()
    console.print("请扫描此二维码进行登录")
    try:
        show_qrcode_as_img(login_qrcode_data)
    except Exception as e:
        show_qrcode_as_ascii(login_qrcode_data)

    is_login = check_login(login_qrcode_data)
    if is_login:
        console.print("正在保存cookie.....")
        session.cookies.save(ignore_discard=True, ignore_expires=True)
    else:
        console.print("登陆失败")
        return
    print("测试登录成功状态：", test_login())

def test_login():
    resp = session.get("https://api.bilibili.com/x/web-interface/nav").json()
    if resp["code"] == 0:
        return True
    else:
        return False


def check_login(login_qrcode_data:dict):
    while True:
        sleep(1)
        resp = session.get("https://passport.bilibili.com/x/passport-login/web/qrcode/poll", params={"qrcode_key": login_qrcode_data["qrcode_key"]}).json()
        if resp["data"]["code"] == 0:
            console.print("登录成功")
            return True
        elif resp["data"]["code"] == 86038:
            console.print("二维码已经失效")
            return False
        elif resp["data"]["code"] == 86090:
            console.print("等待确认登录...")
        elif resp["data"]["code"] == 86101:
            console.print("等待扫码...")
        else:
            console.print("出现未知原因的失败，已经打印服务器响应信息")
            console.print(resp)
            return False

def show_qrcode_as_img(login_qrcode_data:dict):
    img = qrcode.make(login_qrcode_data["url"])
    img.save("login_qrcode.png")
    img.show()

def show_qrcode_as_ascii(login_qrcode_data:dict):
    img = qrcode.make(login_qrcode_data["url"])
    qr = qrcode.main.QRCode()
    qr.add_data(login_qrcode_data["url"])
    qr.print_ascii()