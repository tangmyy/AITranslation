import threading
from tkinter import Tk, Text, Scrollbar, Menu, StringVar, Toplevel, messagebox, ttk
from tkinter import END, LEFT, RIGHT, VERTICAL, HORIZONTAL
from tkinter.filedialog import askopenfilename

import pyperclip
from Translator import Do_Translator
from Chat_AI import AIChatUI

class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("翻译器-v2.0")
        # 设置窗口尺寸并居中显示
        width = 480
        height = 480
        left = (self.window.winfo_screenwidth() - width) / 2
        top = (self.window.winfo_screenheight() - height) / 2
        self.window.geometry("%dx%d+%d+%d" % (width, height, left, top))  # 设置窗口大小和位置
        self.window.resizable(0, 0)  # 禁止用户调整窗口大小（固定尺寸）

        self.create_widget()   # 创建控件实例
        self.set_widget()      # 配置控件样式/行为
        self.place_widget()    # 控件布局（放置位置）
        self.language = "auto"  # 设置默认目标语言为自动检测
        self.window.mainloop()  # 启动主事件循环（显示窗口）

    # 普通翻译界面
    def open_translate_ui(self):
    # 清除窗口中除菜单栏外的所有控件
        for widget in self.window.winfo_children():
            if not isinstance(widget, Menu):
                widget.destroy()
        self.window.title("翻译器-v2.0")  # 恢复窗口标题
        # 重新创建、设置、放置翻译界面的控件
        self.create_widget()
        self.set_widget()
        self.place_widget()

    # 创建普通翻译界面所有控件
    def create_widget(self):
        self.l1 = ttk.Label(self.window)  # 标签：用于显示“待翻译文本”
        self.l2 = ttk.Label(self.window)  # 标签：用于显示“翻译结果”
        self.t1 = Text(self.window)       # 多行文本框：用于输入原始文本
        self.t2 = Text(self.window)       # 多行文本框：用于显示翻译结果
        self.b1 = ttk.Button(self.window)  # 按钮：清空输入框
        self.b2 = ttk.Button(self.window)  # 按钮：执行翻译
        self.b3 = ttk.Button(self.window)  # 按钮：复制翻译内容
        # 垂直滚动条绑定输入框
        self.Scroll_vertical1 = Scrollbar(self.window, orient=VERTICAL)
        # 垂直滚动条绑定输出框
        self.Scroll_vertical2 = Scrollbar(self.window, orient=VERTICAL)
        # 水平滚动条绑定输出框
        self.Scroll_level = Scrollbar(self.window, orient=HORIZONTAL)
        self.m = Menu(self.window)        # 菜单栏对象
        self.window["menu"] = self.m      # 将菜单绑定到窗口
        self.l3 = ttk.Label(self.window)  # 下位状态栏标签：显示当前目标语言等提示信息
    # 配置控件属性与绑定事件
    def set_widget(self):
        # 设置标签内容与字体
        self.l1.config(text="待翻译文本", font=("宋体", 10))
        self.l2.config(text="翻译结果", font=("宋体", 10))
        # 设置按钮文本与点击事件（使用线程避免卡界面）
        self.b1.config(text="清空输入框", command=lambda: self.thread_it(self.clear_t))
        self.b2.config(text="翻译", command=lambda: self.thread_it(self.do_translate))
        self.b3.config(text="复制翻译内容", command=lambda: self.thread_it(self.copy_t))
        # 输入框绑定垂直滚动条
        self.Scroll_vertical1.config(command=self.t1.yview)
        self.t1["yscrollcommand"] = self.Scroll_vertical1.set
        # 输出框绑定垂直 + 水平滚动条
        self.Scroll_vertical2.config(command=self.t2.yview)
        self.t2["yscrollcommand"] = self.Scroll_vertical2.set
        self.t2["xscrollcommand"] = self.Scroll_level.set
        # 创建菜单栏的三级菜单项（文件、操作、关于）
        self.s1 = Menu(self.m, tearoff=False)
        self.s2 = Menu(self.m, tearoff=False)
        self.s3 = Menu(self.m, tearoff=False)
        self.s4 = Menu(self.m, tearoff=False)
        self.s5 = Menu(self.m, tearoff=False)
        self.s6 = Menu(self.m, tearoff=False)
        # 添加菜单到主菜单栏
        self.m.add_cascade(label="普通翻译", command=self.open_translate_ui)
        self.m.add_cascade(label="操作", menu=self.s2)
        self.m.add_cascade(label="选择语言", command=self.open_topleval)
        self.m.add_cascade(label="AI翻译", menu=self.s4)
        self.m.add_cascade(label="AI对话", command=self.open_ai_chat_ui)
        self.m.add_cascade(label="关于", menu=self.s6)
        # “操作”菜单项配置
        self.s2.add_command(label="打开文本文件", command=self.open_txt)
        self.s2.add_separator()
        self.s2.add_command(label="翻译", command=lambda: self.thread_it(self.do_translate))
        self.s2.add_command(label="清空内容", command=self.clear_t)
        self.s2.add_command(label="复制结果", command=lambda: self.thread_it(self.copy_t))
        self.s2.add_separator()
        self.s2.add_command(label="退出", command=self.quit_window)
        # 状态栏文字绑定变量
        self.l3_var = StringVar()
        self.l3.config(textvariable=self.l3_var, background="lightblue")
        self.l3_var.set("当前[自动选择]目标语言")
        # “关于”菜单项配置
        self.s6.add_command(label="说明", command=self.show_infos)

        # 绑定 ESC 快捷键用于退出
        self.window.bind("<Escape>", self.escape)
        # 输入框绑定回车快捷键触发翻译
        self.t1.bind('<Return>', lambda event: self.thread_it(self.do_translate))
        # 点击关闭窗口触发退出确认
        self.window.protocol("WM_DELETE_WINDOW", self.quit_window)
        # 自定义输入框右键菜单
        self.menubar = Menu(self.t1, tearoff=False)
        self.menubar.add_command(label="粘贴", command=self.do_paste)
        self.t1.bind("<Button-3>", self.paste)
        # 自定义输出框右键菜单
        self.menubar2 = Menu(self.t2, tearoff=False)
        self.menubar2.add_command(label="粘贴", command=self.do_paste2)
        self.t2.bind("<Button-3>", self.paste2)
        # 当前选中的语言索引（默认为第 0 项）
        self.current_select = 0

    # 控件放置布局
    def place_widget(self):
        self.l1.place(x=200, y=5)  # “待翻译文本”标签放上方居中
        self.t1.place(x=10, y=30, height=150, width=450)  # 输入框区域
        self.Scroll_vertical1.place(x=445, y=30, height=150)  # 输入框右侧滚动条
        self.b1.place(x=10, y=200)   # “清空输入框”按钮放左侧
        self.b2.place(x=180, y=200)  # “翻译”按钮放中间
        self.b3.place(x=370, y=200)  # “复制翻译内容”按钮放右侧
        self.l2.place(x=200, y=228)  # “翻译结果”标签
        self.t2.place(x=10, y=250, height=180, width=450)  # 输出框区域
        self.Scroll_vertical2.place(x=445, y=250, height=180)  # 输出框右侧滚动条
        self.Scroll_level.place(x=10, y=430, width=450)  # 输出框底部横向滚动条
        self.l3.place(x=0, y=450, width=480, height=30)  # 状态栏放底部横向占满

    # AI对话界面
    def open_ai_chat_ui(self):
        AIChatUI(self.window)

    # 打开语言选择对话框
    def open_topleval(self):
        # 创建一个新的弹窗窗口（顶层窗口，独立于主窗口）
        self.select_lan_window = Toplevel()
        # 设置弹窗的宽度和高度
        width = 250
        height = 50
        # 计算使窗口在屏幕居中的坐标位置
        left = (self.select_lan_window.winfo_screenwidth() - width) / 2
        top = (self.select_lan_window.winfo_screenheight() - height) / 2
        # 设置窗口大小及位置（格式：宽x高+左+上）
        self.select_lan_window.geometry("%dx%d+%d+%d" % (width, height, left, top))
        # 禁止窗口缩放（固定大小）
        self.select_lan_window.resizable(0, 0)
        # 创建一个字符串变量，用于绑定下拉框选中的值
        self.s_combobox_var = StringVar()
        # 从翻译器类中获取支持语言的列表（每项是一个字典，含语言名和缩写）
        self.language_table = Do_Translator().get_language_table()
        # 创建一个下拉框（Combobox），用于语言选择
        self.s_combobox = ttk.Combobox(
            self.select_lan_window,               # 所属窗口是新弹窗
            textvariable=self.s_combobox_var,     # 绑定的变量，随选择项变化
            justify="center",                     # 内容居中显示
            state="readonly",                     # 用户不能手动输入，只能选择
            width=17,                             # 显示宽度为17字符
            value=[language["language"] for language in self.language_table],  # 所有语言中文名
        )

        # 对当前选中语言进行记录并设置下拉框默认选中项
        if self.current_select == 0:
            # 如果当前还没选过，默认选中第一个语言（index=0）
            self.s_combobox.current(0)
        else:
            # 如果之前选过语言，保持之前的选择
            self.s_combobox.current(self.current_select)
        # 创建“选择”按钮，点击后会调用 self.select_lan 方法处理选中逻辑
        self.s_b1 = ttk.Button(
            self.select_lan_window,
            text="选择",
            command=self.select_lan  # 绑定点击事件处理函数
        )
        self.s_combobox.pack(side=LEFT)     # 将下拉框放置在窗口左侧
        self.s_b1.pack(side=RIGHT)          # 将“选择”按钮放置在窗口右侧
        self.select_lan_window.mainloop()   # 启动当前语言选择窗口的事件循环，使其保持响应
    # 记录当前选择的语言
    def select_lan(self):
        self.current_select = self.s_combobox.current()
        self.now_language = self.language_table[self.s_combobox.current()]["language"]
        messagebox.showinfo("提示", f"当前选择 [{self.now_language}] 作为目标语言")
        self.l3_var.set(f"选择[{self.now_language}]作为目标语言")
        self.now_lan = self.language_table[self.s_combobox.current()]["short"]
        self.select_lan_window.destroy()

    # 核心翻译逻辑
    def do_translate(self):
        # 如果 now_lan 不存在 则抛出 AttributeError 令self.language = "auto"
        try:
            self.aim_language = self.now_lan
        except AttributeError:
            self.aim_language = self.language
        # 删除t2 获取t1
        self.t2.delete("0.0", END)
        text = self.t1.get("0.0", END)

        if len(text) != 1:
            self.l3_var.set("正在翻译...")
            translator = Do_Translator()
            result = translator.translate(text, self.aim_language)

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
            
    # 用线程封装某个函数的执行，避免操作卡住主界面
    def thread_it(self, func, *args):
        t = threading.Thread(target=func, args=args)
        t.setDaemon(True)
        t.start()

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

    # 输入框和输出框粘贴功能
    def paste(self, event):
        self.menubar.post(event.x_root, event.y_root)
    def paste2(self, event):
        self.menubar2.post(event.x_root, event.y_root)
    def do_paste(self):
        self.t1.insert(END, pyperclip.paste())
    def do_paste2(self):
        self.t2.insert(END, pyperclip.paste())

    # 快捷退出绑定 按下 ESC 键调用 quit_window
    def escape(self, event):
        self.quit_window()
    # 退出提示
    def quit_window(self):
        ret = messagebox.askyesno("退出", "是否要退出？")
        if ret:
            self.window.destroy()
    # 弹出一个信息对话框，显示作者信息
    def show_infos(self):
        messagebox.showinfo("说明", "作者：懷淰メ\n二创：脆脆鲨同学")

if __name__ == "__main__":
    a = App()
