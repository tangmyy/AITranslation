import sys
import requests
from PyQt5.QtWidgets import (
  QApplication,
  QWidget,
  QTextEdit,
  QPushButton,
  QVBoxLayout,
  QMenuBar,
  QMenu,
  QAction)
from PyQt5.QtCore import Qt

class ChatApp(QWidget):
  def __init__(self):
      super().__init__()
      self.setWindowTitle("AI爱翻译")
      self.resize(500, 600)

      # 创建菜单栏
      self.create_menu_bar()

      # 主界面组件
      self.input_text = QTextEdit()
      self.output_text = QTextEdit()
      self.output_text.setReadOnly(True)
      self.send_button = QPushButton("发送")

      # 布局
      layout = QVBoxLayout()
      layout.addWidget(self.menu_bar)  # 添加菜单栏
      layout.addWidget(self.input_text)
      layout.addWidget(self.send_button)
      layout.addWidget(self.output_text)
      self.setLayout(layout)

      self.send_button.clicked.connect(self.send_message)

  def create_menu_bar(self):
      """创建菜单栏"""
      self.menu_bar = QMenuBar()

      # 普通翻译菜单
      normal_translate_menu = QMenu("普通翻译", self)
      self.menu_bar.addMenu(normal_translate_menu)

      # AI翻译菜单
      ai_translate_menu = QMenu("AI翻译", self)
      self.menu_bar.addMenu(ai_translate_menu)

      # AI对话菜单
      ai_speak_menu = QMenu("AI对话", self)
      self.menu_bar.addMenu(ai_speak_menu)

      # 关于菜单（带下拉选项）
      about_menu = QMenu("关于", self)
      self.menu_bar.addMenu(about_menu)

      # 关于软件
      about_action = QAction("关于软件", self)
      about_action.triggered.connect(self.show_about)
      about_menu.addAction(about_action)

      # 联系我们
      contact_action = QAction("联系我们", self)
      contact_action.triggered.connect(self.show_contact)
      about_menu.addAction(contact_action)

  def show_about(self):
      """显示关于软件信息"""
      self.output_text.append("\n=== 关于软件 ===")
      self.output_text.append("版本: 1.0.0")
      self.output_text.append("功能: 提供普通翻译和AI翻译功能")
      self.output_text.append("开发团队: AI助手开发组\n")

  def show_contact(self):
      """显示联系信息"""
      self.output_text.append("\n=== 联系我们 ===")
      self.output_text.append("邮箱: support@aiassistant.com")
      self.output_text.append("电话: 400-123-4567\n")

  def send_message(self):
      user_input = self.input_text.toPlainText()
      self.input_text.clear()
      self.output_text.append(f"你：{user_input}")

      try:
          resp = requests.post(
              "http://127.0.0.1:8000/chat",
              json={"content": user_input}
          )
          data = resp.json()
          reply = data['choices'][0]['message']['content']
          self.output_text.append(f"AI：{reply}\n")
      except Exception as e:
          self.output_text.append(f"错误：{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChatApp()
    win.show()
    sys.exit(app.exec_())