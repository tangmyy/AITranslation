import re

from google_trans_new import google_translator
from Baidu_Text_transAPI import BaiDu_transAPI


class Do_Translator:
    # 从 lan_table 哈希MAP 中提取语言名称和代码，构造一个字典
    def get_language_table(self):
        lan_table1 = lan_table.strip().replace("'", "")
        names = re.findall(r"[\u4e00-\u9fa5（）]+", lan_table1)
        lans = re.findall(r"[^\u4e00-\u9fa5 \s:（）]+", lan_table1)
        language_table = []
        for language in zip(names, lans):
            item = {}
            item["language"] = language[0]
            item["short"] = language[1]
            language_table.append(item)
        return language_table
    
    # 调用 google_trans_new 模块进行翻译
    def translate(self, text, to_lang):
        try:
            # fy = google_translator().translate(text, language)
            fy = BaiDu_transAPI().BaiDu_trans(text, to_lang)
            return fy
        except Exception as e:
            print(f"出错了：{e}")
            return False

lan_table = """
    '自动选择': 'auto'
    '中文': 'zh'
    '英语': 'en'
    '粤语': 'yue'
    '文言文': 'wyw'
    '繁体中文': 'cht'
    '日语': 'jp'
    '韩语': 'kor'
    '法语': 'fra'
    '西班牙语': 'spa'
    '泰语': 'th'
    '阿拉伯语': 'ara'
    '俄语': 'ru'
    '葡萄牙语': 'pt'
    '德语': 'de'
    '意大利语': 'it'
    '希腊语': 'el'
    '荷兰语': 'nl'
    '波兰语': 'pl'
    '保加利亚语': 'bul'
    '爱沙尼亚语': 'est'
    '丹麦语': 'dan'
    '芬兰语': 'fin'
    '捷克语': 'cs'
    '罗马尼亚语': 'rom'
    '斯洛文尼亚语': 'slo'
    '瑞典语': 'swe'
    '匈牙利语': 'hu'
    '越南语': 'vie'
"""
