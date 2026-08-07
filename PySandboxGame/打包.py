import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import subprocess
import os
import sys
import threading
import platform
from queue import Queue, Empty


class PyToExeConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Python 转 EXE 工具 - PNG自动扫描")
        self.root.geometry("700x600")
        self.root.resizable(True, True)

        # 确保中文显示正常
        self.setup_fonts()

        # 状态变量
        self.selected_file = tk.StringVar()
        self.resource_dir = tk.StringVar()  # 资源目录
        self.save_dir = tk.StringVar(value=os.path.join(os.getcwd(), "dist"))  # 保存目录
        self.png_files = []  # 存储扫描到的PNG文件
        self.is_converting = False

        # 消息队列
        self.message_queue = Queue()

        # 创建界面
        self.create_widgets()

        # 检查PyInstaller
        threading.Thread(target=self.check_pyinstaller, daemon=True).start()

        # 处理消息
        self.process_messages()

    def setup_fonts(self):
        if sys.platform.startswith('win'):
            default_font = ('Microsoft YaHei UI', 10)
        else:
            default_font = ('SimHei', 10)
        self.root.option_add("*Font", default_font)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 1. 选择Python文件
        ttk.Label(main_frame, text="Python文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=0, column=1, sticky=tk.EW, pady=5)
        ttk.Entry(file_frame, textvariable=self.selected_file, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                                                              padx=(0, 5))
        ttk.Button(file_frame, text="浏览...", command=self.browse_file).pack(side=tk.RIGHT)

        # 2. 资源目录选择
        ttk.Label(main_frame, text="资源目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        resource_frame = ttk.Frame(main_frame)
        resource_frame.grid(row=1, column=1, sticky=tk.EW, pady=5)
        ttk.Entry(resource_frame, textvariable=self.resource_dir, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                                                                 padx=(0, 5))
        ttk.Button(resource_frame, text="浏览...", command=self.browse_resource_dir).pack(side=tk.RIGHT)
        ttk.Button(resource_frame, text="扫描PNG", command=self.scan_png_files).pack(side=tk.RIGHT, padx=5)

        # 3. PNG文件列表
        ttk.Label(main_frame, text="PNG图片列表:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        png_frame = ttk.LabelFrame(main_frame, text="扫描到的PNG文件（自动打包）")
        png_frame.grid(row=2, column=1, sticky=tk.NSEW, pady=5)
        self.png_listbox = tk.Listbox(png_frame, height=4)
        self.png_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = ttk.Scrollbar(png_frame, orient=tk.VERTICAL, command=self.png_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.png_listbox.config(yscrollcommand=scrollbar.set)

        # 4. 保存目录选择
        ttk.Label(main_frame, text="保存目录:").grid(row=3, column=0, sticky=tk.W, pady=5)
        save_frame = ttk.Frame(main_frame)
        save_frame.grid(row=3, column=1, sticky=tk.EW, pady=5)
        ttk.Entry(save_frame, textvariable=self.save_dir, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                                                         padx=(0, 5))
        ttk.Button(save_frame, text="浏览...", command=self.browse_save_dir).pack(side=tk.RIGHT)

        # 5. 资源加载代码示例
        ttk.Label(main_frame, text="资源加载代码:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        code_frame = ttk.LabelFrame(main_frame, text="请在您的游戏代码中使用此函数加载图片")
        code_frame.grid(row=4, column=1, sticky=tk.NSEW, pady=5)

        code_example = """import os
import sys

def get_resource_path(relative_path):
    \"\"\"获取资源文件的正确路径，兼容开发和打包环境\"\"\"
    try:
        # 打包后的环境
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# 使用示例（加载PNG图片）:
# image_path = get_resource_path("images/player.png")  # 替换为实际相对路径
# img = pygame.image.load(image_path).convert_alpha()
"""
        self.code_text = scrolledtext.ScrolledText(code_frame, height=6, wrap=tk.WORD, font=('Consolas', 9))
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.code_text.insert(tk.END, code_example)
        self.code_text.config(state=tk.DISABLED)

        # 6. 进度区域
        ttk.Label(main_frame, text="转换进度:").grid(row=5, column=0, sticky=tk.NW, pady=5)
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=5, column=1, sticky=tk.NSEW, pady=5)

        # 进度条
        self.progress = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)

        # 状态文本
        self.status_text = tk.Text(self.progress_frame, height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # 7. 按钮区域
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=10)
        self.convert_button = ttk.Button(button_frame, text="转换为EXE", command=self.start_conversion)
        self.convert_button.pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="复制资源加载代码", command=self.copy_code).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="打开保存目录", command=self.open_save_dir).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=10)

        # 布局配置
        main_frame.columnconfigure(1, weight=1)
        self.progress_frame.columnconfigure(0, weight=1)
        self.progress_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(5, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def copy_code(self):
        """复制资源加载代码到剪贴板"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.code_text.get("1.0", tk.END))
        messagebox.showinfo("提示", "资源加载代码已复制到剪贴板")

    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="选择Python文件",
            filetypes=[("Python文件", "*.py"), ("所有文件", "*.*")]
        )
        if file_path:
            self.selected_file.set(file_path)
            # 自动填充保存目录
            self.save_dir.set(os.path.join(os.path.dirname(file_path), "dist"))
            # 自动填充资源目录为主程序所在目录
            self.resource_dir.set(os.path.dirname(file_path))
            # 自动扫描PNG文件
            self.scan_png_files()

    def browse_resource_dir(self):
        dir_path = filedialog.askdirectory(title="选择资源目录")
        if dir_path:
            self.resource_dir.set(dir_path)
            # 选择目录后自动扫描PNG
            self.scan_png_files()

    def scan_png_files(self):
        """扫描资源目录中的所有PNG文件"""
        self.png_files = []
        self.png_listbox.delete(0, tk.END)

        resource_dir = self.resource_dir.get()
        if not resource_dir or not os.path.isdir(resource_dir):
            messagebox.showwarning("警告", "请先选择有效的资源目录")
            return

        # 扫描目录及其子目录中的所有PNG文件
        for root, _, files in os.walk(resource_dir):
            for file in files:
                if file.lower().endswith('.png'):
                    full_path = os.path.join(root, file)
                    self.png_files.append(full_path)
                    # 在列表中显示相对路径
                    rel_path = os.path.relpath(full_path, resource_dir)
                    self.png_listbox.insert(tk.END, rel_path)

        count = len(self.png_files)
        self.message_queue.put(f"已扫描到 {count} 个PNG图片文件")
        if count == 0:
            messagebox.showinfo("提示", "未在资源目录中找到PNG图片文件")

    def browse_save_dir(self):
        dir_path = filedialog.askdirectory(title="选择保存目录")
        if dir_path:
            self.save_dir.set(dir_path)

    def check_pyinstaller(self):
        try:
            subprocess.run(["pyinstaller", "--version"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            self.message_queue.put("PyInstaller 已就绪")
        except:
            self.message_queue.put("未检测到PyInstaller，请先手动安装：pip install pyinstaller")

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)

    def process_messages(self):
        try:
            while not self.message_queue.empty():
                message = self.message_queue.get_nowait()
                self.update_status(message)
                self.message_queue.task_done()
        except Empty:
            pass
        self.root.after(100, self.process_messages)

    def start_conversion(self):
        if self.is_converting:
            messagebox.showinfo("提示", "正在转换中，请等待...")
            return

        # 验证Python文件
        if not self.selected_file.get() or not os.path.exists(self.selected_file.get()):
            messagebox.showwarning("警告", "请选择有效的Python文件")
            return

        # 验证是否有PNG文件
        if not self.png_files:
            if messagebox.askyesno("确认", "未检测到PNG图片文件，是否继续转换？"):
                pass
            else:
                return

        # 提示用户检查资源加载代码
        messagebox.showinfo("重要提示",
                            "请确保您的游戏代码中使用了资源加载函数！\n"
                            "1. 已复制的代码中包含get_resource_path()函数\n"
                            "2. 加载图片时使用: image_path = get_resource_path(\"相对路径\")\n"
                            "3. 相对路径需与左侧PNG列表中的路径一致")

        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED)
        self.progress.start()
        threading.Thread(target=self.convert_to_exe, daemon=True).start()

    def convert_to_exe(self):
        try:
            save_dir = self.save_dir.get()
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
                self.message_queue.put(f"创建保存目录: {save_dir}")

            # 构建基础命令
            command = ["pyinstaller",
                       "--distpath", save_dir,
                       "--workpath", os.path.join(save_dir, "build"),
                       "--specpath", os.path.join(save_dir, "spec")]

            # 单文件模式
            command.append("--onefile")  # 游戏推荐使用单文件模式

            # 窗口模式
            command.append("--windowed")  # 游戏推荐使用窗口模式

            # 添加所有PNG图片（关键修复）
            if self.png_files and self.resource_dir.get():
                # 根据系统选择分隔符
                sep = ';' if platform.system() == 'Windows' else ':'
                # 获取主程序目录作为基准
                base_dir = os.path.dirname(self.selected_file.get())
                # 获取资源目录相对路径
                resource_rel_dir = os.path.relpath(self.resource_dir.get(), base_dir)

                # 按目录分组添加，避免重复
                added_dirs = set()
                for png_file in self.png_files:
                    # 获取文件所在目录
                    file_dir = os.path.dirname(png_file)
                    # 计算相对路径
                    rel_dir = os.path.relpath(file_dir, base_dir)

                    if rel_dir not in added_dirs:
                        # 添加目录到打包命令
                        command.extend(["--add-data", f"{file_dir}{sep}{rel_dir}"])
                        added_dirs.add(rel_dir)
                        self.message_queue.put(f"添加图片目录: {file_dir} -> {rel_dir}")

            # 添加目标文件
            command.append(self.selected_file.get())

            self.message_queue.put(f"开始转换: {os.path.basename(self.selected_file.get())}")
            self.message_queue.put(f"执行命令: {' '.join(command)}")

            # 执行转换
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )

            # 输出详细日志
            for line in process.stdout:
                stripped_line = line.strip()
                if stripped_line:  # 只输出非空行
                    self.message_queue.put(stripped_line)

            return_code = process.wait(timeout=1800)
            if return_code == 0:
                self.message_queue.put("转换完成！")
                self.finish_conversion(True)
            else:
                self.message_queue.put(f"转换失败，返回代码: {return_code}")
                self.finish_conversion(False)

        except Exception as e:
            self.message_queue.put(f"转换出错: {str(e)}")
            self.finish_conversion(False)

    def finish_conversion(self, success):
        self.root.after(0, self.progress.stop)
        self.root.after(0, lambda: self.convert_button.config(state=tk.NORMAL))
        self.is_converting = False

        if success:
            self.root.after(0, lambda: messagebox.showinfo(
                "成功",
                f"转换完成！\n文件已保存到: {self.save_dir.get()}\n"
                "请确保游戏代码中使用了正确的资源加载函数\n"
                "加载路径需与PNG列表中的相对路径一致"
            ))

    def open_save_dir(self):
        save_dir = self.save_dir.get()
        if os.path.exists(save_dir):
            try:
                if sys.platform.startswith('win'):
                    os.startfile(save_dir)
                elif sys.platform.startswith('darwin'):
                    subprocess.run(['open', save_dir], check=True)
                else:
                    subprocess.run(['xdg-open', save_dir], check=True)
            except Exception as e:
                messagebox.showerror("错误", f"无法打开目录: {str(e)}")
        else:
            messagebox.showwarning("警告", "保存目录不存在")


if __name__ == "__main__":
    root = tk.Tk()
    app = PyToExeConverter(root)
    root.mainloop()
