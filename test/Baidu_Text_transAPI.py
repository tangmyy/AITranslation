# -*- coding: utf-8 -*-
# 本示例展示了如何将英文文本翻译为简体中文
# 本代码兼容 Python 2.7.x 和 Python 3.x
# 若未安装 requests 库，请运行：pip install requests
# 更多详细接口文档请参考：https://api.fanyi.baidu.com/doc/21
# 语言代码参考文档：https://api.fanyi.baidu.com/doc/21

import requests
import random
import json
from hashlib import md5

# q	string	是	请求翻译query	UTF-8编码，完成个人/企业认证后上限为6000字符
# from	string	是	翻译源语言	可设置为auto（自动检测语言）
# to	string	是	翻译目标语言	不可设置为auto
# appid	string	是	APPID	可在开发者信息查看
# salt	string	是	随机数	可为字母或数字的字符串
# sign	string	是	签名	appid+q+salt+密钥的MD5值


class BaiDu_transAPI:

    def BaiDu_trans(self, text, to_lang):
        # 请设置你自己的 appid 和 appkey（可在百度翻译开放平台申请）
        appid = '20250703002396120'
        appkey = 'mzCie6_X6SvEtmaLcx6_'
        from_lang = 'auto'  # 源语言：自动

        # 请求接口地址
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path

        # 要翻译的文本
        # text = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

        # 制作字符串 s 的 MD5 签名的方法
        def make_md5(s, encoding='utf-8'):
            return md5(s.encode(encoding)).hexdigest()
        salt = random.randint(32768, 65536)
        sign = make_md5(appid + text + str(salt) + appkey)

        # 构建请求参数
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            'appid': appid,
            'q': text,
            'from': from_lang,
            'to': to_lang,
            'salt': salt,
            'sign': sign,
        }
        
        try:
            # 发送请求
            request = requests.post(
                url, 
                params=payload, 
                headers=headers
            )
            # result 是 Python 字典
            result = request.json()
            tr_text = result["trans_result"][0]["dst"]
            # # ✅ 美化查看用
            print(tr_text)
            # print(json.dumps(result, indent=4, ensure_ascii=False))
            # print(f"from_lang参数: " +from_lang)
            # print(f"to_lang参数: " +to_lang)
            return tr_text
        except Exception as e:
            print(f"出错了：{e}")
            return False



