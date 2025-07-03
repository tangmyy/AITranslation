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
    QAction,
    QComboBox  # 新增语言选择下拉框
)
from PyQt5.QtCore import Qt
from Translator import Do_Trans

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI爱翻译")
        self.resize(600, 700)  # 增大窗口尺寸
        
        # 初始化翻译器
        self.translator = Do_Trans()
        
        # 创建UI
        self.init_ui()
        
    def init_ui(self):
        # 创建菜单栏
        self.create_menu_bar()

        # 主界面组件
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("请输入要翻译的内容...")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("翻译结果将显示在这里...")
        self.send_button = QPushButton("发送")
        
        # 语言选择组件
        self.language_combo = QComboBox()
        languages = self.translator.get_language_table()
        for lang in languages:
            self.language_combo.addItem(lang['language'], lang['short'])
        
        # 默认选择中文
        self.language_combo.setCurrentText('中文（简体）')

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.menu_bar)
        layout.addWidget(self.language_combo)  # 添加语言选择框
        layout.addWidget(self.input_text)
        layout.addWidget(self.send_button)
        layout.addWidget(self.output_text)
        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_message)

    def get_selected_language(self):
        """获取当前选择的语言"""
        return {
            'language': self.language_combo.currentText(),
            'short': self.language_combo.currentData()
        }

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

        # 关于菜单
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
        user_input = self.input_text.toPlainText().strip()
        self.input_text.clear()
        
        if not user_input:
            self.output_text.clear() 
            self.output_text.append("提示：请输入要翻译的内容")
            return
            
        self.output_text.clear()

        try:
            # 获取目标语言
            target_lang = self.get_selected_language()['short']
            
            # 执行翻译
            translated = self.translator.translate(user_input, target_lang)
            
            if isinstance(translated, str):
                if translated.startswith("翻译失败"):
                    self.output_text.append(f"翻译失败: {translated.split(':')[-1]}\n")
                else:
                    self.output_text.append(f"你：{user_input}\n")
                    self.output_text.append(f"翻译结果({target_lang})：{translated}\n")
            else:
            # 处理返回字典的情况
                self.output_text.append(f"你：{user_input}\n")
                self.output_text.append(
                    f"翻译({translated['target_language']})：{translated['translated_text']}\n"
            )
                
        except Exception as e:
             self.output_text.clear()
             self.output_text.append(f"翻译错误：{str(e)}\n")

    def is_english(self, text):
        """简单检测是否为英文"""
        try:
            text.encode('ascii')
            return True
        except UnicodeEncodeError:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ChatApp()
    win.show()
    sys.exit(app.exec_())