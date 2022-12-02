# PaperGen

一个简单的试卷生成器
An simple html paper generator for zujuan

## 使用方法/Usage

> 注意/Note
> - 请求头和api来自移动端app，现已支持短信登录，可去除水印（较慢）
> - The headers apis are come from mobile app, and the SMS login module is available.

### xkarticle.py

To get articles from the website.

For example:

To get article from `https://*.*/11pt3205ct8749n230250.html`

Input:
- Url: ...

### paper-gen.py

To generate paper from the article or basket.

The question search ability is based on Baidu. *(While the accuracy is so bad)*

### xkpaper.py

The same as ppg.py.

While the search ability is based on itself, which is limited if you're a free account.
