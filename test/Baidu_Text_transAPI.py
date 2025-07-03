# -*- coding: utf-8 -*-
# 本示例展示了如何将英文文本翻译为简体中文
# 本代码兼容 Python 2.7.x 和 Python 3.x
# 若未安装 requests 库，请运行：pip install requests
# 更多详细接口文档请参考：https://api.fanyi.baidu.com/doc/21

import requests
import random
import json
from hashlib import md5

# 请设置你自己的 appid 和 appkey（可在百度翻译开放平台申请）
appid = '20250703002396120'
appkey = 'mzCie6_X6SvEtmaLcx6_'

# 语言代码参考文档：https://api.fanyi.baidu.com/doc/21
from_lang = 'en'  # 源语言：英文
to_lang = 'zh'    # 目标语言：中文（简体）

# 请求接口地址
endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# 要翻译的文本
query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

# 生成 salt 和签名 sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

salt = random.randint(32768, 65536)
sign = make_md5(appid + query + str(salt) + appkey)

# 构建请求参数
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {
    'appid': appid,
    'q': query,
    'from': from_lang,
    'to': to_lang,
    'salt': salt,
    'sign': sign
}

# 发送请求
r = requests.post(url, params=payload, headers=headers)
result = r.json()

# 显示响应结果
print(json.dumps(result, indent=4, ensure_ascii=False))
