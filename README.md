# AITranslation

仓库目前包含两个**分别启动**的 Python 桌面程序，尚未整合为同一个界面。

| 功能 | 入口 | 技术 |
| --- | --- | --- |
| 文本翻译与 AI 对话 | `code/Translator/My_Translator-v2.0.py` | Tkinter、百度翻译、讯飞星火 HTTP |
| B 站视频下载 | `code/Bilibili/bilibili_gui.py` | PyQt5、bilibili-api-python、FFmpeg |

`code/Bilibili/main.py` 和 `mg.py` 是另外两版独立界面；`backend/X1_ws.py` 是单独的星火 WebSocket 示例，均不由上述两个入口调用。

## 准备

在**仓库根目录**打开 PowerShell：

```powershell
uv sync
if (!(Test-Path .env)) { Copy-Item .env.example .env }
```

按需填写 `.env`：翻译需要 `BAIDU_APP_ID`、`BAIDU_APP_KEY`；AI 对话需要 `SPARK_API_KEY`；B 站下载可使用 `SESSDATA`、`BILI_JCT`、`BUVID3`，并检查 `FFMPEG_PATH` 是否指向本机 FFmpeg。现有 `.env` 若已存在，请保留并手动补充变量，不要用示例文件覆盖。

## 分别运行

```powershell
# 翻译器与 AI 对话
uv run python code/Translator/My_Translator-v2.0.py

# B 站视频下载器
uv run python code/Bilibili/bilibili_gui.py
```

两条命令都从仓库根目录执行。也可以先运行 `uv sync`，再用 `.venv\Scripts\python.exe` 替换 `uv run python`。下载的视频写入当前工作目录。

## 当前限制

- 百度翻译接口不接受 `auto` 作为目标语言；使用翻译前先在界面中选择具体目标语言。
- B 站界面中的清晰度选择尚未接入实际下载策略，下载器目前选取接口返回的最佳流。
- 旧的 PyInstaller 配置仍指向已不存在的 `test` 目录，暂不能直接用于打包。