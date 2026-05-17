#!/usr/bin/env python3
"""
正则表达式测试工具 - 实时匹配测试
"""
import sys, re, tkinter as tk
from tkinter import messagebox, scrolledtext

class App:
    def __init__(self, root):
        self.root = root
        root.title("正则表达式测试工具 v1.0")
        root.geometry("850x650")
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#6a1b9a", height=50)
        f.pack(fill="x")
        tk.Label(f, text="🔍 正则表达式测试工具", font=("Arial",14,"bold"),
                 fg="white", bg="#6a1b9a").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        # 正则输入
        rf = tk.Frame(main)
        rf.pack(fill="x", pady=5)
        tk.Label(rf, text="正则表达式：", font=("Arial",11,"bold")).pack(side="left")
        self.regex_entry = tk.Entry(rf, font=("Consolas",12), width=50)
        self.regex_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.regex_entry.insert(0, r"\d+")
        
        # 选项
        of = tk.Frame(main)
        of.pack(fill="x", pady=5)
        self.ignore_case = tk.BooleanVar()
        self.multiline = tk.BooleanVar()
        self.dotall = tk.BooleanVar()
        tk.Checkbutton(of, text="忽略大小写 (i)", variable=self.ignore_case).pack(side="left", padx=10)
        tk.Checkbutton(of, text="多行模式 (m)", variable=self.multiline).pack(side="left", padx=10)
        tk.Checkbutton(of, text="点匹配换行 (s)", variable=self.dotall).pack(side="left", padx=10)
        tk.Button(of, text="测试匹配", command=self.test_regex,
                  bg="#6a1b9a", fg="white", font=("Arial",10,"bold"),
                  padx=15).pack(side="right", padx=10)
        
        # 测试文本
        tk.Label(main, text="测试文本：", font=("Arial",10,"bold")).pack(anchor="w", pady=(10,2))
        self.test_txt = scrolledtext.ScrolledText(main, font=("Consolas",10), height=8)
        self.test_txt.pack(fill="x", pady=5)
        self.test_txt.insert(1.0, "Hello 123 World 456\nTest 789 regex")
        
        # 匹配结果
        tk.Label(main, text="匹配结果：", font=("Arial",10,"bold")).pack(anchor="w", pady=(10,2))
        self.result_txt = scrolledtext.ScrolledText(main, font=("Consolas",10),
                                                     height=10, bg="#f3e5f5")
        self.result_txt.pack(fill="both", expand=True)
        
        self.status = tk.Label(main, text="输入正则表达式和测试文本后点击「测试匹配」",
                               font=("Arial",10), fg="gray")
        self.status.pack(anchor="w")
    
    def test_regex(self):
        pattern = self.regex_entry.get().strip()
        text = self.test_txt.get(1.0, "end")
        
        if not pattern:
            messagebox.showwarning("提示", "请输入正则表达式")
            return
        
        try:
            flags = 0
            if self.ignore_case.get():
                flags |= re.IGNORECASE
            if self.multiline.get():
                flags |= re.MULTILINE
            if self.dotall.get():
                flags |= re.DOTALL
            
            matches = list(re.finditer(pattern, text, flags))
            
            if matches:
                result = f"找到 {len(matches)} 个匹配：\n\n"
                for i, m in enumerate(matches, 1):
                    result += f"[{i}] 位置 {m.start()}-{m.end()}: {repr(m.group())}\n"
                    if m.groups():
                        result += f"    分组: {m.groups()}\n"
                self.result_txt.delete(1.0, "end")
                self.result_txt.insert(1.0, result)
                self.status.config(text=f"✅ 找到 {len(matches)} 个匹配")
            else:
                self.result_txt.delete(1.0, "end")
                self.result_txt.insert(1.0, "未找到匹配")
                self.status.config(text="❌ 未找到匹配")
                
        except re.error as e:
            self.result_txt.delete(1.0, "end")
            self.result_txt.insert(1.0, f"正则表达式错误：\n{str(e)}")
            self.status.config(text="❌ 正则表达式无效")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
