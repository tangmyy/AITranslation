import sys
import asyncio
import qasync
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QProgressBar,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from bilibili_api.video import VideoQuality
from bilibili_download import BilibliDownloader
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bilibili 下载器")
        self.setGeometry(300, 300, 500, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 输入框
        self.input_bvid = QLineEdit()
        self.input_bvid.setPlaceholderText("请输入 BVID，例如 BV1xxx 或含 BV 的完整链接")
        layout.addWidget(self.input_bvid)

        # 清晰度下拉框
        self.quality_box = QComboBox()
        self.quality_box.addItems(["360P", "480P", "720P", "1080P", "1080P+", "4K"])
        layout.addWidget(self.quality_box)
        
        # 进度条
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # 封面图显示
        self.cover_label = QLabel("封面预览将在此显示")
        self.cover_label.setAlignment(Qt.AlignCenter)
        self.cover_label.setFixedSize(400, 150)
        layout.addWidget(self.cover_label)

        # 状态栏（文本标签代替）
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        # 查询按钮
        query_btn = QPushButton("查询封面")
        query_btn.clicked.connect(self.query_cover)
        layout.addWidget(query_btn)

        # 下载按钮
        self.download_btn = QPushButton("开始下载")
        self.download_btn.clicked.connect(self.download_video)
        layout.addWidget(self.download_btn)

        self.setLayout(layout)

    # 将清晰度名称转换为 VideoQuality 枚举值
    def get_quality_enum(self, name: str):
        return {
            "360P": VideoQuality._360P,
            "480P": VideoQuality._480P,
            "720P": VideoQuality._720P,
            "1080P": VideoQuality._1080P,
            "1080P+": VideoQuality._1080P_PLUS,
            "4K": VideoQuality._4K
        }.get(name, VideoQuality._360P)

    # 查询封面图（异步任务）
    async def query_cover_async(self):
        bvid = self.parse_bv(self.input_bvid.text())
        if not bvid:
            self.cover_label.setText("无法解析 BVID")
            return
        try:
            dl = BilibliDownloader(bvid)
            await dl.get_vidoe_info(bvid)
            img_data = requests.get(dl.thumnail_url).content
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            self.cover_label.setPixmap(pixmap.scaled(
                self.cover_label.width(), self.cover_label.height(), Qt.KeepAspectRatio
            ))
        except Exception as e:
            self.cover_label.setText(f"获取失败：{e}")

    def query_cover(self):
        asyncio.ensure_future(self.query_cover_async())

    # 开始异步下载视频
    def download_video(self):
        asyncio.ensure_future(self.download_1(self.input_bvid.text()))

    # 异步执行视频下载 + 下载进度更新。
    async def download_1(self, url):
        bvid = self.parse_bv(url)
        if not bvid:
            self.status_label.setText("请输入合法 BVID")
            return
        dl = BilibliDownloader(bvid=bvid)
        selected_quality = self.quality_box.currentText()
        dl.selected_quality = self.get_quality_enum(selected_quality)

        self.status_label.setText("开始下载中...")
        await asyncio.gather(dl.download_by_bvid(bvid), self.update_progress(dl))

    # 不断轮询下载器状态并更新界面上的进度条。
    async def update_progress(self, dl):
        while True:
            await asyncio.sleep(0.3)
            self.progressBar.setValue(int(dl.download_stat))
            if self.progressBar.value() >= 100:
                self.status_label.setText("下载完成！")
                break

    # 从 URL 或 BVID 字符串中提取出 BVID。
    def parse_bv(self, url):
        if url.startswith("BV"):
            return url
        elif "BV" in url:
            parsed_url = urlparse(url)
            path_segments = parsed_url.path.strip("/").split("/")
            try:
                if len(path_segments) >= 2 and path_segments[0] == "video":
                    return path_segments[1]
            except ValueError:
                print("无法从 URL 中提取 BVID")
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    win = MainWindow()
    win.show()
    with loop:
        loop.run_forever()
