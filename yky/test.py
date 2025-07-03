# test_translate.py

from Translator import Do_Trans

def test_translation(text, target_lang):
    translator = Do_Trans()
    result = translator.translate(text, target_lang)

    print(f"原文: {text}")
    print(f"目标语言: {target_lang}")
    print("翻译结果:")

    if isinstance(result, dict):
        if result.get('translated_text') is None:
            print(f"❌ 翻译失败: {result.get('error')}")
        else:
            print(f"✅ {result['translated_text']}")
    else:
        print(f"⚠️ 未知返回: {result}")


if __name__ == "__main__":
    # 测试用例 1：中文翻译成英文
    test_translation("你好，世界", "en")

    # 测试用例 2：英文翻译成日语
    test_translation("Good morning", "ja")

    # 测试用例 3：中文翻译成中文（测试无效果的情况）
    test_translation("早上好", "zh")

    # 测试用例 4：非法语言代码
    test_translation("hello", "xyz")
