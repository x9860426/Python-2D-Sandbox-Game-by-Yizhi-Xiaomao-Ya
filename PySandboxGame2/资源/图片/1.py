import os
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime

class FileLister:
    def __init__(self, root):
        self.root = root
        self.root.title("文件夹文件查看器")
        self.root.geometry("800x600")  # 设置窗口初始大小
        
        # 创建按钮框架
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        # 创建选择文件夹按钮
        self.select_btn = tk.Button(btn_frame, text="选择文件夹", command=self.select_folder)
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        # 创建输出到终端按钮
        self.output_btn = tk.Button(btn_frame, text="输出到终端", command=self.output_to_terminal)
        self.output_btn.pack(side=tk.LEFT, padx=5)
        
        # 创建文件信息显示表格
        columns = ("文件名", "大小(KB)", "修改时间")
        self.tree = ttk.Treeview(root, columns=columns, show="headings")
        
        # 设置列标题和宽度
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # 布局表格和滚动条
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # 状态栏显示当前路径
        self.status_var = tk.StringVar()
        self.status_var.set("未选择文件夹")
        self.status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.current_folder = None

    def select_folder(self):
        """选择文件夹并显示其中的文件"""
        folder_path = filedialog.askdirectory(title="选择文件夹")
        if folder_path:
            self.current_folder = folder_path
            self.status_var.set(f"当前文件夹: {folder_path}")
            self.display_files()

    def display_files(self):
        """清空表格并显示当前文件夹中的文件"""
        # 清空现有内容
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if not self.current_folder:
            return
        
        try:
            # 获取文件夹内所有文件
            for filename in os.listdir(self.current_folder):
                file_path = os.path.join(self.current_folder, filename)
                
                # 跳过文件夹（只显示文件）
                if os.path.isdir(file_path):
                    continue
                
                # 获取文件大小（转换为KB）
                file_size = os.path.getsize(file_path) / 1024
                size_str = f"{file_size:.2f}"
                
                # 获取文件修改时间
                modify_time = os.path.getmtime(file_path)
                time_str = datetime.fromtimestamp(modify_time).strftime("%Y-%m-%d %H:%M:%S")
                
                # 添加到表格
                self.tree.insert("", tk.END, values=(filename, size_str, time_str))
        
        except Exception as e:
            self.status_var.set(f"错误: {str(e)}")
    
    def output_to_terminal(self):
        """将当前文件夹中的文件列表输出到终端，方便复制"""
        if not self.current_folder:
            self.status_var.set("错误: 请先选择文件夹")
            return
        
        try:
            print("\n=== 文件夹文件列表 ===")
            print(f"当前文件夹: {self.current_folder}")
            print("-" * 60)
            print(f"{'文件名':<40} {'大小(KB)':<10} {'修改时间':<20}")
            print("-" * 60)
            
            # 遍历并输出所有文件信息
            for filename in os.listdir(self.current_folder):
                file_path = os.path.join(self.current_folder, filename)
                
                # 跳过文件夹
                if os.path.isdir(file_path):
                    continue
                
                # 获取文件信息
                file_size = os.path.getsize(file_path) / 1024
                size_str = f"{file_size:.2f}"
                
                modify_time = os.path.getmtime(file_path)
                time_str = datetime.fromtimestamp(modify_time).strftime("%Y-%m-%d %H:%M:%S")
                
                # 格式化输出，方便复制
                print(f"{filename:<40} {size_str:<10} {time_str:<20}")
            
            print("-" * 60)
            print(f"总计文件数量: {len([f for f in os.listdir(self.current_folder) if os.path.isfile(os.path.join(self.current_folder, f))])}")
            print("=== 输出完成 ===\n")
            
            self.status_var.set("文件列表已输出到终端")
        except Exception as e:
            self.status_var.set(f"输出错误: {str(e)}")
            print(f"错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileLister(root)
    root.mainloop()