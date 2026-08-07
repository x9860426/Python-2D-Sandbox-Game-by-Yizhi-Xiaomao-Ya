import os
import shutil
import threading
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片批量压缩工具")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # 初始化变量
        self.source_folder = os.getcwd()
        self.target_size = (250, 250)
        self.is_processing = False
        
        # 创建GUI组件
        self.create_widgets()
    
    def create_widgets(self):
        """创建GUI组件"""
        # 标题
        title_label = tk.Label(self.root, text="图片批量压缩工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # 源文件夹选择
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(folder_frame, text="源文件夹:", font=("Arial", 10)).pack(anchor=tk.W)
        
        folder_row = tk.Frame(folder_frame)
        folder_row.pack(fill=tk.X, pady=5)
        
        self.folder_var = tk.StringVar(value=self.source_folder)
        folder_entry = tk.Entry(folder_row, textvariable=self.folder_var, state="readonly", font=("Arial", 10), relief=tk.SUNKEN)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(folder_row, text="浏览", command=self.browse_folder, font=("Arial", 10), width=10)
        browse_btn.pack(side=tk.RIGHT)
        
        # 目标尺寸设置
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=15, padx=20, fill=tk.X)
        
        tk.Label(size_frame, text="目标尺寸:", font=("Arial", 10)).pack(anchor=tk.W)
        
        size_row = tk.Frame(size_frame)
        size_row.pack(fill=tk.X, pady=5)
        
        tk.Label(size_row, text="宽度:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.width_var = tk.StringVar(value="250")
        width_entry = tk.Entry(size_row, textvariable=self.width_var, font=("Arial", 10), width=10)
        width_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(size_row, text="高度:", font=("Arial", 10)).pack(side=tk.LEFT, padx=(0, 5))
        self.height_var = tk.StringVar(value="250")
        height_entry = tk.Entry(size_row, textvariable=self.height_var, font=("Arial", 10), width=10)
        height_entry.pack(side=tk.LEFT)
        
        # 开始按钮
        self.start_btn = tk.Button(self.root, text="开始压缩", command=self.start_compression, 
                                  font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
                                  activebackground="#45a049", height=2, width=20)
        self.start_btn.pack(pady=20)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10, padx=20, fill=tk.X)
        
        # 状态信息
        self.status_var = tk.StringVar(value="就绪")
        status_label = tk.Label(self.root, textvariable=self.status_var, font=("Arial", 10), fg="#666666")
        status_label.pack(pady=10)
        
        # 日志信息
        log_frame = tk.Frame(self.root)
        log_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(log_frame, text="处理日志:", font=("Arial", 10)).pack(anchor=tk.W)
        
        self.log_text = tk.Text(log_frame, height=8, font=("Arial", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 添加滚动条
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        # 禁止编辑日志
        self.log_text.config(state=tk.DISABLED)
    
    def browse_folder(self):
        """浏览选择源文件夹"""
        folder = filedialog.askdirectory(initialdir=self.source_folder)
        if folder:
            self.source_folder = folder
            self.folder_var.set(folder)
    
    def log(self, message):
        """添加日志信息"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def resize_image(self, input_path, output_path, target_size):
        """调整图片尺寸"""
        try:
            with Image.open(input_path) as img:
                img_size = img.size
                
                # 如果原图尺寸小于等于目标尺寸，则直接复制
                if img_size[0] <= target_size[0] and img_size[1] <= target_size[1]:
                    self.log(f"跳过: {os.path.basename(input_path)} ({img_size[0]}x{img_size[1]}) 小于等于目标尺寸")
                    img.save(output_path)
                    return True
                
                # 计算缩放比例，保持原始比例
                ratio = min(target_size[0] / img_size[0], target_size[1] / img_size[1])
                new_size = (int(img_size[0] * ratio), int(img_size[1] * ratio))
                
                # 调整图片尺寸
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # 检测图片是否有透明通道
                has_alpha = img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info)
                
                # 根据是否有透明通道选择模式
                if has_alpha:
                    # 创建透明背景的RGBA图片
                    result_img = Image.new('RGBA', target_size, (255, 255, 255, 0))
                else:
                    # 创建白色背景的RGB图片
                    result_img = Image.new('RGB', target_size, (255, 255, 255))
                
                # 将调整后的图片居中粘贴
                paste_x = (target_size[0] - new_size[0]) // 2
                paste_y = (target_size[1] - new_size[1]) // 2
                
                if has_alpha:
                    # 如果有透明通道，使用alpha通道粘贴
                    result_img.paste(resized_img, (paste_x, paste_y), resized_img)
                else:
                    # 否则直接粘贴
                    result_img.paste(resized_img, (paste_x, paste_y))
                
                # 保存图片，保持原图格式
                result_img.save(output_path)
                self.log(f"压缩: {os.path.basename(input_path)} 从 {img_size[0]}x{img_size[1]} 到 {target_size[0]}x{target_size[1]}")
                return True
        except Exception as e:
            self.log(f"错误: {os.path.basename(input_path)} - {e}")
            return False
    
    def get_all_files(self, folder):
        """获取文件夹内所有文件的路径，包括子文件夹"""
        all_files = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                all_files.append(os.path.join(root, file))
        return all_files
    
    def copy_and_compress_folder(self):
        """复制文件夹并压缩图片"""
        try:
            # 解析目标尺寸
            try:
                width = int(self.width_var.get())
                height = int(self.height_var.get())
                target_size = (width, height)
            except ValueError:
                messagebox.showerror("错误", "请输入有效的尺寸数值！")
                self.is_processing = False
                self.start_btn.config(state=tk.NORMAL)
                self.status_var.set("就绪")
                return
            
            source_folder = self.source_folder
            target_folder = f"{source_folder}-压缩"
            
            # 检查目标文件夹是否存在
            if os.path.exists(target_folder):
                messagebox.showerror("错误", f"目标文件夹 {target_folder} 已存在！")
                self.is_processing = False
                self.start_btn.config(state=tk.NORMAL)
                self.status_var.set("就绪")
                return
            
            self.log(f"开始处理...")
            self.log(f"源文件夹: {source_folder}")
            self.log(f"目标文件夹: {target_folder}")
            self.log(f"目标尺寸: {target_size[0]}x{target_size[1]}")
            
            # 获取所有文件列表（包括子文件夹）
            all_files = self.get_all_files(source_folder)
            total_files = len(all_files)
            
            if total_files == 0:
                self.log("源文件夹中没有文件")
                messagebox.showinfo("提示", "处理完成！源文件夹中没有文件。")
                self.is_processing = False
                self.start_btn.config(state=tk.NORMAL)
                self.status_var.set("就绪")
                self.progress_var.set(0)
                return
            
            # 处理文件
            processed = 0
            for source_path in all_files:
                if not self.is_processing:
                    break
                    
                # 计算相对路径
                relative_path = os.path.relpath(source_path, source_folder)
                target_path = os.path.join(target_folder, relative_path)
                
                # 创建目标文件夹（如果不存在）
                target_dir = os.path.dirname(target_path)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                
                # 检查文件是否为图片
                try:
                    with Image.open(source_path) as img:
                        # 是图片文件，进行压缩处理
                        self.resize_image(source_path, target_path, target_size)
                except Exception as e:
                    # 非图片文件，直接复制
                    shutil.copy2(source_path, target_path)
                    self.log(f"复制: {relative_path} (非图片文件)")
                
                # 更新进度
                processed += 1
                progress = (processed / total_files) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"处理中: {processed}/{total_files} 文件")
                self.root.update_idletasks()
            
            if self.is_processing:
                self.log(f"\n处理完成！")
                self.log(f"总计处理: {processed} 个文件")
                messagebox.showinfo("成功", f"处理完成！\n源文件夹: {source_folder}\n目标文件夹: {target_folder}")
            else:
                self.log(f"\n处理已取消！")
                messagebox.showinfo("提示", "处理已取消。")
        
        except Exception as e:
            self.log(f"\n发生错误: {e}")
            messagebox.showerror("错误", f"处理过程中发生错误: {e}")
        finally:
            self.is_processing = False
            self.start_btn.config(state=tk.NORMAL)
            self.start_btn.config(text="开始压缩")
            self.status_var.set("就绪")
            self.progress_var.set(0)
    
    def start_compression(self):
        """开始压缩处理"""
        if self.is_processing:
            # 取消处理
            self.is_processing = False
            self.start_btn.config(text="取消中...")
            return
        
        # 开始处理
        self.is_processing = True
        self.start_btn.config(text="取消", state=tk.NORMAL)
        self.status_var.set("准备中...")
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # 在后台线程中执行处理
        threading.Thread(target=self.copy_and_compress_folder, daemon=True).start()


def main():
    """主函数"""
    root = tk.Tk()
    app = ImageCompressorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()