# BilibiliAudioDownloader

## 0. 简介

这是一个用来提取b站视频的音频的工具，支持多线程同时下载多个音频，自动识别视频是否有flac流

~~其实只是为了我自己下歌听用的~~

## 1. 使用：

python版本为3.12.4

1. 你可以前往 `release` 下载我用pyinstaller打包好的exe，或者自行构建python环境
`pip install -r requestments.txt`

2. 在执行目录下新建`links.txt`，在里面一行一个写下你要爬取音频的视频的链接，或者包含其BV号的字符串

3. 运行`main.py`或者我打包的`BilibiliAudioDownloader.exe`，选择多线程模式或者单线程模式
4. 你要下载的音频会出现在`result`文件夹下

## 2. 已知问题

下载的视频标题中的`\`和`/`会被删除

不知道为什么，如果视频标题包含`\`和`/`这两个路径标识符就会爆`no such file or directory`，明明我在下载

但是不用担心，无伤大雅

## 3. 鸣谢

**[SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)** api文档好用，我爱用


