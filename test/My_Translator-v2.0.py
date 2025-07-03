import threading
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename

import pyperclip
from Translator import Do_Trans

"""
使用combobox进行语言记录
"""


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("翻译器-v2.0")
        width = 480
        height = 480
        left = (self.window.winfo_screenwidth() - width) / 2
        top = (self.window.winfo_screenheight() - height) / 2
        self.window.geometry("%dx%d+%d+%d" % (width, height, left, top))
        self.window.resizable(0, 0)
        self.create_widget()
        self.set_widget()
        self.place_widget()
        self.language = "auto"
        self.window.mainloop()
    # 创建所有控件
    def create_widget(self):
        self.l1 = ttk.Label(self.window)
        self.t1 = Text(self.window)
        self.b1 = ttk.Button(self.window)
        self.b2 = ttk.Button(self.window)
        self.b3 = ttk.Button(self.window)
        self.l2 = ttk.Label(self.window)
        self.t2 = Text(self.window)
        self.Scroll_vertical1 = Scrollbar(self.window, orient=VERTICAL)
        self.Scroll_vertical2 = Scrollbar(self.window, orient=VERTICAL)
        self.Scroll_level = Scrollbar(self.window, orient=HORIZONTAL)
        self.m = Menu(self.window)
        self.window["menu"] = self.m
        self.l3 = ttk.Label(self.window)
    # 配置控件属性与绑定事件
    def set_widget(self):
        self.l1.config(text="待翻译文本", font=("宋体", 10))
        self.b1.config(text="清空输入框", command=lambda: self.thread_it(self.clear_t))
        self.b2.config(text="翻译", command=lambda: self.thread_it(self.do_translate))
        self.b3.config(text="复制翻译内容", command=lambda: self.thread_it(self.copy_t))
        self.l2.config(text="翻译结果", font=("宋体", 10))
        self.Scroll_vertical1.config(command=self.t1.yview)
        self.t1["yscrollcommand"] = self.Scroll_vertical1.set
        self.Scroll_vertical2.config(command=self.t2.yview)
        self.t2["yscrollcommand"] = self.Scroll_vertical2.set
        self.t2["xscrollcommand"] = self.Scroll_level.set
        self.s1 = Menu(self.m, tearoff=False)
        self.s2 = Menu(self.m, tearoff=False)
        self.s3 = Menu(self.m, tearoff=False)
        self.m.add_cascade(label="文件", menu=self.s1)
        self.m.add_cascade(label="操作", menu=self.s2)
        self.m.add_cascade(label="关于", menu=self.s3)
        self.s1.add_command(label="打开文本文件", command=self.open_txt)
        self.s1.add_separator()
        self.s1.add_command(label="退出", command=self.quit_window)
        self.s2.add_command(
            label="翻译", command=lambda: self.thread_it(self.do_translate)
        )
        self.s2.add_command(label="选择语言", command=self.open_topleval)
        self.s2.add_command(label="清空内容", command=self.clear_t)
        self.s2.add_command(
            label="复制结果", command=lambda: self.thread_it(self.copy_t)
        )
        self.s3.add_command(label="说明", command=self.show_infos)
        self.l3_var = StringVar()
        self.l3.config(textvariable=self.l3_var, background="lightblue")
        self.l3_var.set("当前[自动选择]目标语言")
        self.window.bind("<Escape>", self.escape)
        # self.t1.bind("<Return>", lambda: self.thread_it(self.do_translate))
        self.t1.bind('<Return>', lambda event: self.thread_it(self.do_translate))
        self.window.protocol("WM_DELETE_WINDOW", self.quit_window)
        self.menubar = Menu(self.t1, tearoff=False)
        self.menubar.add_command(label="粘贴", command=self.do_paste)
        self.t1.bind("<Button-3>", self.paste)
        self.menubar2 = Menu(self.t2, tearoff=False)
        self.menubar2.add_command(label="粘贴", command=self.do_paste2)
        self.t2.bind("<Button-3>", self.paste2)
        self.current_select = 0
    # 控件放置布局
    def place_widget(self):
        self.l1.place(x=200, y=5)
        self.t1.place(x=10, y=30, height=150, width=450)
        self.Scroll_vertical1.place(x=445, y=30, height=150)
        self.b1.place(x=10, y=200)
        self.b2.place(x=180, y=200)
        self.b3.place(x=370, y=200)
        self.l2.place(x=200, y=228)
        self.t2.place(x=10, y=250, height=180, width=450)
        self.Scroll_vertical2.place(x=445, y=250, height=180)
        self.Scroll_level.place(x=10, y=430, width=450)
        self.l3.place(x=0, y=450, width=480, height=30)
    # 打开语言选择对话框
    def open_topleval(self):
        self.select_lan_window = Toplevel()
        width = 250
        height = 50
        left = (self.select_lan_window.winfo_screenwidth() - width) / 2
        top = (self.select_lan_window.winfo_screenheight() - height) / 2
        self.select_lan_window.geometry("%dx%d+%d+%d" % (width, height, left, top))
        self.select_lan_window.resizable(0, 0)
        self.s_combobox_var = StringVar()
        self.language_table = Do_Trans().get_language_table()
        self.s_combobox = ttk.Combobox(
            self.select_lan_window,
            textvariable=self.s_combobox_var,
            justify="center",
            state="readonly",
            width=17,
            value=[language["language"] for language in self.language_table],
        )
        # 对当前选中语言进行记录
        if self.current_select == 0:
            self.s_combobox.current(0)
        else:
            self.s_combobox.current(self.current_select)
        self.s_b1 = ttk.Button(
            self.select_lan_window, text="选择", command=self.select_lan
        )
        self.s_combobox.pack(side=LEFT)
        self.s_b1.pack(side=RIGHT)
        self.select_lan_window.mainloop()
    # 记录当前选择的语言
    def select_lan(self):
        self.current_select = self.s_combobox.current()
        self.now_language = self.language_table[self.s_combobox.current()]["language"]
        messagebox.showinfo("提示", f"当前选择 [{self.now_language}] 作为目标语言")
        self.l3_var.set(f"选择[{self.now_language}]作为目标语言")
        self.now_lan = self.language_table[self.s_combobox.current()]["short"]
        self.select_lan_window.destroy()
    # 导入 TXT 文本内容
    def open_txt(self):
        txt_path = askopenfilename(
            title="选择一个txt文本文件", filetypes=[("txt source file", "*.txt")]
        )
        if txt_path:
            self.t1.delete("0.0", END)
            with open(txt_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    self.t1.insert(END, line)
            f.close()
    # 核心翻译逻辑
    def do_translate(self):
        try:
            self.aim_language = self.now_lan
        except AttributeError:
            self.aim_language = self.language
        self.t2.delete("0.0", END)
        text = self.t1.get("0.0", END)
        if len(text) != 1:
            self.l3_var.set("正在翻译...")
            t = Do_Trans()
            result = t.translate(text, self.aim_language)
            if result:
                self.l3.config(background="lightblue")
                self.t2.insert(END, result.strip())
                try:
                    self.l3_var.set(f"翻译完成...已翻译为[{self.now_language}]")
                except AttributeError:
                    self.l3_var.set("翻译完成...已[自动选择目标语言]")

            else:
                self.l3_var.set("翻译失败，请检查网络！")
                self.l3.config(background="red")
        else:
            messagebox.showwarning("警告", "请输入内容！")
            self.l3.config(background="red")
            self.l3_var.set("请输入内容")
    # 弹出一个信息对话框，显示作者信息
    def show_infos(self):
        messagebox.showinfo("说明", "作者：懷淰メ")
    # 用线程封装某个函数的执行，避免操作卡住主界面
    def thread_it(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

    # 清空输入框 t1 和输出框 t2
    def clear_t(self):
        self.t1.delete("0.0", END)
        self.t2.delete("0.0", END)
    # 从输出框 t2 获取内容并复制到剪贴板
    def copy_t(self):
        tr_res = self.t2.get("0.0", END)
        pyperclip.copy(tr_res)
        spam = pyperclip.paste()
        if spam:
            self.l3.config(background="lightyellow")
            self.l3_var.set("复制成功！")
    # 粘贴相关函数（右键菜单）
    def paste(self, event):
        self.menubar.post(event.x_root, event.y_root)
    # 快捷退出绑定 按下 ESC 键调用 quit_window
    def do_paste(self):
        self.t1.insert(END, pyperclip.paste())
    # 当用户在 右键点击输出框 t2 时，弹出自定义右键菜单 menubar2
    def paste2(self, event):
        self.menubar2.post(event.x_root, event.y_root)
    # 这是 menubar2 右键菜单中的“粘贴”命令的回调函数
    def do_paste2(self):
        self.t2.insert(END, pyperclip.paste())
    # 绑定键盘上的 ESC 键按下事件
    def escape(self, event):
        self.quit_window()
    # 退出提示
    def quit_window(self):
        ret = messagebox.askyesno("退出", "是否要退出？")
        if ret:
            self.window.destroy()

if __name__ == "__main__":
    a = App()
