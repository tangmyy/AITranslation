import sys
from urllib.parse import urlparse, parse_qs
import asyncio
import flask
from PyQt5 import QtCore, QtWidgets

from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QWidget,
    QProgressBar,
)
import requests
import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QStyleFactory
from bilibili_download import BilibliDownloader
from PyQt5.QtGui import QIcon, QPixmap


class BirdMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "小鸟下载器"
        screen_geometry = QtWidgets.QApplication.desktop().screenGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()
        # 示例：将窗口居中
        self.width = 500
        self.height = 340
        self.left = (screen_width - self.width) // 2
        self.top = (screen_height - self.height) // 2
        self.initUI()

    def initUI(self):
        # 设置窗口标题与大小
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # 设置中心窗口部件
        self.c_widget = QWidget()
        self.c_widget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setCentralWidget(self.c_widget)
        # ==================== 输入区域 ====================
        self.search_label = QLabel("请输入BV号: ")
        self.search_line_edit = QLineEdit("例如：BV1xxx")
        # 当输入框失焦时更新封面图
        self.search_line_edit.focusOutEvent = lambda event: self.set_thumbnail(
            self.search_line_edit.text()
        )
        # ==================== 缩略图显示 ====================
        self.thumbnail_label = QLabel("thumbnail")
        self.thumbnail_label.setFixedSize(400, 150)

        self.thumbnail = QPixmap(os.getenv("ICON_PATH"))
        if not self.thumbnail.isNull():
            scaled = self.thumbnail.scaled(
                self.thumbnail_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation
            )
            self.thumbnail_label.setPixmap(scaled)
        # ==================== 进度条区域 ====================
        progress_label = QLabel("进度:")
        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        # ==================== 按钮区域 ====================
        self.download_btn = QPushButton("下载")
        self.reset_btn = QPushButton("重置")
        # 绑定按钮事件
        self.download_btn.clicked.connect(lambda: self.run(self.search_line_edit.text()))
        self.reset_btn.clicked.connect(self.reset)
        # ==================== 布局管理 ====================
        layout = QGridLayout()
        layout.addWidget(self.search_label, 0, 0)
        layout.addWidget(self.search_line_edit, 0, 1, 1, 5)
        layout.addWidget(progress_label, 1, 0)
        layout.addWidget(self.progressBar, 1, 1, 1, 5)
        layout.addWidget(self.thumbnail_label, 2, 0, 3, 5)
        layout.addWidget(self.download_btn, 5, 1)
        layout.addWidget(self.reset_btn, 5, 2)
        self.c_widget.setLayout(layout)
        # 显示窗口
        self.show()


    def reset(self):
        self.progressBar.setValue(0)
        self.statusBar().showMessage("")
        self.search_line_edit.setText("")
        self.thumbnail_label.clear()

    def on_click(self):
        a, b = 0, 0
        a = self.textbox_a.text()
        b = self.textbox_b.text()
        answer1 = int(a) + int(b)
        answer2 = int(a) - int(b)
        QtWidgets.QMessageBox.question(
            self,
            "Hahahaa",
            f"Answer1:{answer1}, Answer2:{answer2}",
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Abort,
        )

    # 异步执行视频下载 + 下载进度更新。
    async def download_1(self, url):
        bvid = self.parse_bv(url)
        dl = BilibliDownloader(bvid=bvid)
        await asyncio.gather(dl.download_by_bvid(bvid), self.update_progress(dl))

    # 不断轮询下载器状态并更新界面上的进度条。
    async def update_progress(self, dl):
        while True:
            await asyncio.sleep(0.3)
            self.progressBar.setValue(int(dl.download_stat))
            if self.progressBar.value() >= 100:
                self.statusBar().showMessage(
                    "Download Finished",
                )
                break

    # 运行异步下载函数。
    def run(self, url):
        asyncio.run(main=self.download_1(url))

    # 从 URL 或 BVID 字符串中提取出 BVID。
    def parse_bv(self, url):
        # 解析 BV 号
        if url.startswith("BV"):
            return url
        elif "BV" in url:
            parsed_url = urlparse(url)
            # 提取路径部分（path）
            path_segments = parsed_url.path.strip("/").split("/")
            # 通常 BVID 在路径中的第二个部分
            try:
                if len(path_segments) >= 2 and path_segments[0] == "video":
                    bvid = path_segments[1]
            except ValueError:
                print("无法从 URL 中提取 BVID")
            return bvid
        else:
            return None

    # 获取视频封面图，并在界面中显示。
    def set_thumbnail(self, url):
        bvid = self.parse_bv(url)
        if bvid:
            dl = BilibliDownloader(bvid=bvid)
            asyncio.run(dl.get_vidoe_info(bvid))
            self.thumbnail.loadFromData(requests.get(dl.thumnail_url).content)
            self.thumbnail = self.thumbnail.scaled(
                self.thumbnail_label.width(), self.thumbnail_label.height()
            )
            self.thumbnail_label.setPixmap(self.thumbnail)


if __name__ == "__main__":
    load_dotenv(override=True)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("motif"))  # Fusion, Windows, WindowsVista
    app.setWindowIcon(QIcon(os.getenv("ICON_PATH")))
    with open("code/bilibili/style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())  # qdarkstyle
    # app.setStyleSheet(qss_rc.qss)  # qss_rc
    # app.setStyleSheet(style_sheet_rc.style_sheet)  # style_sheet_rc
    ex = BirdMainWindow()
    # ex=MainWindow()

    sys.exit(app.exec_())
