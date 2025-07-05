# Chat_AI.py

import json
import requests
import X1_http

from tkinter import Text, Scrollbar, END, ttk


class AIChatUI:
    def __init__(self, window):
        self.window = window
        self.chatHistory = []  # ✅ 聊天记录作为类成员变量
        self.build_ui()

    def build_ui(self):
        # 清除窗口中除菜单栏以外的所有控件
        for widget in self.window.winfo_children():
            if not str(widget).startswith(".!menu"):
                widget.destroy()

        self.window.title("翻译器-v2.0---AI对话")
        # 聊天记录显示框（只读）
        self.chat_answer = Text(self.window, state="disabled", wrap="word")
        self.chat_answer.place(x=10, y=10, width=460, height=300)
        # 滚动条
        scroll_chat = Scrollbar(self.window, command=self.chat_answer.yview)
        scroll_chat.place(x=470, y=10, height=300)
        self.chat_answer.config(yscrollcommand=scroll_chat.set)
        # 输入框
        self.input_text = Text(self.window, height=4)
        self.input_text.place(x=10, y=320, width=460, height=80)
        # 发送按钮（功能占位） 
        send_button = ttk.Button(self.window, text="发送", command=self.fake_send)
        send_button.place(x=370, y=410, width=100)
        # 状态栏
        self.chat_status = ttk.Label(self.window, text="AI对话已连接", background="lightgreen")
        self.chat_status.place(x=0, y=450, width=480, height=30) 

    # def fake_send(self):
    #     user_ask = self.input_text.get("1.0", END).strip()
    #     # 解锁插入 → 插入消息 → 再锁定
    #     if user_ask:
    #         # 将聊天记录显示框解锁（normal:可编辑 disabled:不可编辑）
    #         self.chat_answer.config(state="normal")

    #         # 对话
    #         # question = X1_http.checklen(X1_http.getText(chatHistory,"user", user_ask))
    #         question = X1_http.checklen(X1_http.getText(self.chatHistory, "user", user_ask))    
    #         answer = X1_http.get_answer(question)
    #         # 向话历史存储列表中追加一条“AI的回复”
    #         X1_http.getText(self.chatHistory, "assistant", answer)

    #         self.chat_answer.insert(END, f"你：{user_ask}\n")
    #         self.chat_answer.insert(END, f"AI：{answer}\n\n")
    #         # 滚动聊天记录框到底部，使最新消息可见
    #         self.chat_answer.see(END)
    #         # 再次把聊天记录框设置为只读，防止用户手动编辑
    #         self.chat_answer.config(state="disabled")
    #         # 清空输入框内容，准备下一次提问
    #         self.input_text.delete("1.0", END)


    def fake_send(self):
        user_ask = self.input_text.get("1.0", END).strip()
        if not user_ask:
            print("user_ask为空 不可发送!")
            return
        
        # 将聊天记录显示框解锁（normal:可编辑 disabled:不可编辑）
        self.chat_answer.config(state="normal")
        self.chat_answer.insert(END, f"你：{user_ask}\n")
        self.chat_answer.insert(END, f"AI：")
        # 滚动聊天记录框到底部，使最新消息可见
        self.chat_answer.see(END)
        # 再次把聊天记录框设置为只读，防止用户手动编辑
        self.chat_answer.config(state="disabled")
        # 清空输入框内容，准备下一次提问
        self.input_text.delete("1.0", END)

        question = X1_http.checklen(X1_http.getText(self.chatHistory, "user", user_ask))    

        # 开始流式请求并逐帧插入回答
        self.chat_answer.config(state="normal")
        answer = ""         # 存储返回结果
        is_first_chunk = True   # 首帧标识
        for chunk in X1_http.get_answer_stream(question):

            # chunk = chunk.lstrip("\n")  # 去除 chunk 开头多余换行
            if is_first_chunk:
                chunk = chunk.lstrip("\n")  # 仅首帧去除模型多余的换行
                is_first_chunk = False

            self.chat_answer.insert(END, chunk)
            self.chat_answer.see(END)
            self.window.update()  # 强制刷新 UI（关键）
            answer += chunk
        self.chat_answer.insert(END, "\n\n")  # 补换行
        self.chat_answer.config(state="disabled")

        # 向话历史存储列表中追加一条“AI的回复”
        X1_http.getText(self.chatHistory, "assistant", answer)



