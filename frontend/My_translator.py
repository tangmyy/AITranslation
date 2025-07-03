import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Translator import Do_Trans
from about_author import About_Author_dialog
from language_select import Language_Select_Form
from translate_ui import Ui_MainWindow

class language_select_window(QWidget,Language_Select_Form):
    def __init__(self):
        # 信号的定义
        super().__init__()
        self.setupUi(self)


class about_author_window(QWidget,About_Author_dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

class My_Translate(QMainWindow):
    message_single=pyqtSignal(int,str)
    def __init__(self):
        super(My_Translate, self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()
        self.ui.action_open_txt.triggered.connect(self.open_txt_file)
        self.ui.action_quit.triggered.connect(lambda :self.close())
        self.ui.action_translate.triggered.connect(self.do_translate)
        self.ui.action_select_aim_language.triggered.connect(self.select_aim_language)
        self.ui.action_clear_input.triggered.connect(self.clear_input)
        self.ui.action_copy_result.triggered.connect(self.copy_result)
        self.ui.action_set_font.triggered.connect(self.set_plaineidt_font)
        self.ui.action_about.triggered.connect(lambda :self.about_ui.show())
        self.ui.action_infos.triggered.connect(lambda :QMessageBox.information(self,'关于作者','作者：懷淰メ\nBy:PyQt5'))
        self.ui.pushButton.clicked.connect(self.clear_input)
        self.ui.pushButton_2.clicked.connect(self.do_translate)
        self.ui.pushButton_3.clicked.connect(self.copy_result)
        self.message_single.connect(self.show_message)


    def init(self):
        self.about_ui = about_author_window()
        self.lan_select_ui = language_select_window()
        self.current_aim_language = '自动选择'
        self.current_aim_language_short = 'auto'
        self.t = Do_Trans()
        language_table=self.t.get_language_table()
        self.languages=[lan['language'] for lan in language_table]
        self.language_table=[lan['short'] for lan in language_table]
        self.ui.label_3.setText(f'目标语言：<a style=color:"blue">{self.current_aim_language}</a>')

    def set_plaineidt_font(self):
        font,ok=QFontDialog.getFont()
        if ok :
            self.ui.plainTextEdit.setFont(font)
            self.ui.plainTextEdit_2.setFont(font)

    @pyqtSlot(int,str)
    def show_message(self,type,message):
        """
        使用信号槽将messagebox信号处理
        :param type:
        :param message:
        :return:
        """
        if type==1:
            QMessageBox.information(self,"提示",message)
        elif type==2:
            QMessageBox.warning(self,"警告",message)
        elif type==3:
            QMessageBox.critical(self,"错误",message)

    def open_txt_file(self):
        """
        打开一个文本文件，将文本文件内容输入到输入框中
        :return:
        """
        aim_txt_file_path,_=QFileDialog.getOpenFileName(self,"打开一个文本文件",".",'文本文件(*.txt)')
        if aim_txt_file_path:
            file =open(aim_txt_file_path,'r',encoding='utf-8')
            data=file.readlines()
            file.close()
            self.ui.plainTextEdit.setPlainText(''.join(data))
        else:
            pass

    def do_translate(self):
        """
        翻译
        :return:
        """
        aim_trans=self.ui.plainTextEdit.toPlainText()
        if aim_trans=="":
            self.message_single.emit(1,'请输入内容！')
        else:
            self.ui.plainTextEdit_2.clear()
            trans_result=self.t.translate(aim_trans,self.current_aim_language_short)
            if trans_result:
                self.ui.plainTextEdit_2.setPlainText(trans_result)
            else:
                self.message_single.emit(3,'发生了一个错误！')

    def select_aim_language(self):
        """
        选择翻译目标语言
        :return:
        """
        current_language_index=self.language_table.index(self.current_aim_language_short)
        self.lan_select_ui.comboBox.addItems(self.languages)
        self.lan_select_ui.comboBox.setCurrentIndex(current_language_index)
        self.lan_select_ui.pushButton.clicked.connect(self.do_select_language)
        self.lan_select_ui.show()

    def do_select_language(self):
        """
        选择语言
        :return:
        """
        index=self.lan_select_ui.comboBox.currentIndex()
        self.current_aim_language=self.languages[index]
        self.current_aim_language_short=self.language_table[index]
        self.ui.label_3.setText(f'目标语言：<a style=color:"blue">{self.current_aim_language}</a>')
        self.lan_select_ui.hide()

    def clear_input(self):
        """
        清空两个输入框
        :return:
        """
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit_2.clear()
        self.ui.statusbar.showMessage("清空输入框成功！",3000)

    def copy_result(self):
        """
        复制翻译结果
        :return:
        """
        trans_result=self.ui.plainTextEdit_2.toPlainText()
        clipbord=QApplication.clipboard()
        clipbord.setText(trans_result)
        self.ui.statusbar.showMessage("复制翻译结果成功！",3000)


    def closeEvent(self,event):
        ret=QMessageBox.question(self,"退出",'确定要退出？',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if ret==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ui=My_Translate()
    ui.show()
    sys.exit(app.exec_())

