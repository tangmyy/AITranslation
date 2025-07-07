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
    QHBoxLayout,
    QProgressBar,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
from bilibili_api import video, Credential
from bilibili_api.video import VideoQuality
from dotenv import load_dotenv
import os

load_dotenv()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bilibili 下载器")
        self.setGeometry(300, 300, 500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        # 输入框
        self.input_bvid = QLineEdit()
        self.input_bvid.setPlaceholderText("请输入 BVID，例如 BV1xxx")
        layout.addWidget(self.input_bvid)
        # 清晰度下拉框
        self.quality_box = QComboBox()
        self.quality_box.addItems(["360P", "480P", "720P", "1080P", "1080P+", "4K"])
        layout.addWidget(self.quality_box)
        # ==================== 进度条区域 ====================
        progress_label = QLabel("进度:")
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(progress_label, 1, 0)
        # 封面图显示
        self.cover_label = QLabel("封面预览将在此显示")
        self.cover_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.cover_label)
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

    # 异步：根据 BVID 获取视频信息并显示封面图
    async def query_cover_async(self):
        bvid = self.input_bvid.text().strip()
        if not bvid:
            self.cover_label.setText("请输入 BVID")
            return
        try:
            v = video.Video(bvid=bvid)
            info = await v.get_info()
            pic_url = info["pic"]
            img_data = requests.get(pic_url).content

            # 展示图片
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            self.cover_label.setPixmap(pixmap.scaled(300, 200, Qt.KeepAspectRatio))
        except Exception as e:
            self.cover_label.setText(f"获取失败：{e}")

    # 启动异步封面查询任务（用于按钮绑定）
    def query_cover(self):
        asyncio.ensure_future(self.query_cover_async())

    # 异步：下载视频（根据选中的清晰度）
    async def download_video_async(self):
        from bilibili_download import BilibliDownloader
        bvid = self.input_bvid.text().strip()
        if not bvid:
            return
        downloader = BilibliDownloader(bvid)
        selected_quality = self.quality_box.currentText()
        downloader.selected_quality = self.get_quality_enum(selected_quality)
        await downloader.main()

    # 启动异步下载任务（用于按钮绑定）
    def download_video(self):
        asyncio.ensure_future(self.download_video_async())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    win = MainWindow()
    win.show()

    with loop:
        loop.run_forever()
