# -*- coding: utf-8 -*-
"""
CSDN博客爬虫 - 可视化界面
版本: 1.2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import threading
from datetime import datetime
import sys
import os
from pathlib import Path
import json

# 导入核心模块
sys.path.insert(0, str(Path(__file__).parent))

from src import CSDNBlogScraper, Config, setup_logger
import logging


class ImageZoomWindow(tk.Toplevel):
    """图片放大查看窗口"""
    def __init__(self, parent, image_path, title):
        super().__init__(parent)
        self.title(title)
        self.geometry("800x600")
        self.minsize(400, 300)
        
        # 加载原始图片
        self.original_image = Image.open(image_path)
        self.current_scale = 1.0
        self.photo = None
        
        # 创建画布
        self.canvas = tk.Canvas(self, bg='#333')
        self.canvas.pack(fill='both', expand=True)
        
        # 添加关闭按钮
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="关闭", command=self.destroy).pack()
        
        # 绑定事件
        self.canvas.bind('<Configure>', self.on_resize)
        self.bind('<Escape>', lambda e: self.destroy())
        
        # 初始显示
        self.on_resize(None)
    
    def on_resize(self, event):
        """窗口大小改变时重新调整图片"""
        # 获取画布尺寸
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width < 10 or canvas_height < 10:
            self.after(100, lambda: self.on_resize(None))
            return
        
        # 计算缩放比例
        img_width, img_height = self.original_image.size
        scale_x = (canvas_width - 40) / img_width
        scale_y = (canvas_height - 40) / img_height
        scale = min(scale_x, scale_y, 1.0)
        
        # 调整图片大小
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        if new_width > 0 and new_height > 0:
            resized = self.original_image.resize((new_width, new_height), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(resized)
            
            # 清空画布
            self.canvas.delete('all')
            
            # 居中显示图片
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            self.canvas.create_image(x, y, anchor='nw', image=self.photo)


class WelcomeDialog(tk.Toplevel):
    """欢迎弹窗"""
    def __init__(self, parent, config_path):
        super().__init__(parent)
        self.title("欢迎使用")
        self.geometry("500x400")
        self.resizable(False, False)
        
        self.config_path = config_path
        
        # 居中显示
        self.center_window()
        
        # 创建内容
        self.create_content()
        
        # 禁止关闭窗口（除非点击按钮）
        self.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def center_window(self):
        """窗口居中"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_content(self):
        """创建弹窗内容"""
        # 主容器
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill='both', expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="🎉 欢迎使用CSDN博客爬虫",
            font=('Microsoft YaHei', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # 开发者信息
        info_frame = ttk.LabelFrame(main_frame, text="开发者信息", padding="20")
        info_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(info_frame, text="开发者：艺杯羹", font=('Microsoft YaHei', 11)).pack(pady=5)
        ttk.Label(info_frame, text="QQ：3057454077").pack(pady=5)
        ttk.Label(info_frame, text="公众号：艺杯羹").pack(pady=5)
        
        # 赞助引导
        donate_frame = ttk.LabelFrame(main_frame, text="支持开发者", padding="20")
        donate_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        donate_text = (
            "如果您觉得这个工具对您有帮助，\n"
            "欢迎扫码赞赏支持开发者！\n\n"
            "您的支持是我持续更新的动力~ 💪"
        )
        ttk.Label(donate_frame, text=donate_text, justify='center').pack(pady=10)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x')
        
        ttk.Button(btn_frame, text="关闭", command=self.on_close).pack(side='left', padx=5, expand=True)
        ttk.Button(btn_frame, text="今天不弹出", command=self.on_dont_show_today).pack(side='right', padx=5, expand=True)
    
    def on_close(self):
        """关闭按钮"""
        self.destroy()
    
    def on_dont_show_today(self):
        """今天不弹出按钮"""
        # 保存今天的日期
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            config_data = {"last_dismiss_date": today}
            
            # 确保配置目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f)
        except Exception as e:
            print(f"保存配置失败: {e}")
        
        self.destroy()


class CSDNScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSDN博客爬虫 v1.2.0")
        self.root.geometry("900x750")
        self.root.minsize(800, 650)
        
        # 配置路径
        self.config_dir = os.path.join(os.path.expanduser("~"), ".csdn_scraper")
        self.config_path = os.path.join(self.config_dir, "config.json")
        
        # 设置图标和样式
        self.setup_style()
        
        # 创建主框架
        self.create_widgets()
        
        # 日志输出
        self.log_buffer = []
        
        # 检查是否显示欢迎弹窗
        self.check_welcome_dialog()
    
    def setup_style(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('Microsoft YaHei', 18, 'bold'), foreground='#333')
        style.configure('Subtitle.TLabel', font=('Microsoft YaHei', 11), foreground='#666')
        style.configure('Info.TLabel', font=('Microsoft YaHei', 9), foreground='#666')
        style.configure('Action.TButton', font=('Microsoft YaHei', 10))
        style.configure('Progress.Horizontal.TProgressbar', thickness=12)
        style.configure('Dev.TLabel', font=('Microsoft YaHei', 9), foreground='#444')
    
    def check_welcome_dialog(self):
        """检查是否显示欢迎弹窗"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                
                last_date = config_data.get("last_dismiss_date")
                today = datetime.now().strftime("%Y-%m-%d")
                
                if last_date == today:
                    # 今天已经点击过"今天不弹出"
                    return
            
            # 显示弹窗
            self.root.after(500, self.show_welcome_dialog)
        except Exception as e:
            print(f"检查欢迎弹窗失败: {e}")
            self.root.after(500, self.show_welcome_dialog)
    
    def show_welcome_dialog(self):
        """显示欢迎弹窗"""
        dialog = WelcomeDialog(self.root, self.config_path)
        dialog.grab_set()
    
    def get_desktop_path(self):
        """获取桌面路径"""
        if sys.platform == 'win32':
            import ctypes.wintypes
            CSIDL_DESKTOP = 0
            SHGFP_TYPE_CURRENT = 0
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DESKTOP, 0, SHGFP_TYPE_CURRENT, buf)
            return buf.value
        else:
            return os.path.join(os.path.expanduser("~"), "Desktop")
    
    def create_widgets(self):
        """创建界面组件"""
        # 标题区域
        header_frame = ttk.Frame(self.root, padding="20 20 20 10")
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, text="CSDN博客爬虫工具", style='Title.TLabel')
        title_label.pack(anchor='w')
        
        subtitle_label = ttk.Label(header_frame, 
                                   text="一键爬取CSDN博客文章，支持多种输出格式",
                                   style='Subtitle.TLabel')
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # 主内容区域 - 使用Notebook分隔标签页
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # 创建标签页
        main_frame = ttk.Frame(notebook, padding="10")
        notebook.add(main_frame, text="爬取工具")
        
        dev_frame = ttk.Frame(notebook, padding="10")
        notebook.add(dev_frame, text="关于作者")
        
        # ====================== 爬取工具页 ======================
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="配置信息", padding="15")
        input_frame.pack(fill='x', pady=(0, 15))
        
        # 博客URL
        ttk.Label(input_frame, text="博客URL:").grid(row=0, column=0, sticky='e', pady=5)
        
        self.url_var = tk.StringVar(value="")
        url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, sticky='we', padx=10, pady=5)
        
        url_hint = ttk.Label(input_frame, text="在此输入CSDN个人博客链接", 
                            style='Info.TLabel', foreground='#999')
        url_hint.grid(row=0, column=2, sticky='w', pady=5)
        
        # 输出格式
        ttk.Label(input_frame, text="输出格式:").grid(row=1, column=0, sticky='e', pady=5)
        
        self.format_var = tk.StringVar(value="csv")
        format_frame = ttk.Frame(input_frame)
        format_frame.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        ttk.Radiobutton(format_frame, text="CSV", variable=self.format_var, 
                       value="csv").pack(side='left', padx=(0, 20))
        ttk.Radiobutton(format_frame, text="JSON", variable=self.format_var, 
                       value="json").pack(side='left', padx=(0, 20))
        ttk.Radiobutton(format_frame, text="TXT", variable=self.format_var, 
                       value="txt").pack(side='left')
        
        # 高级配置
        advanced_frame = ttk.LabelFrame(main_frame, text="高级配置", padding="15")
        advanced_frame.pack(fill='x', pady=(0, 15))
        
        # 延迟配置
        ttk.Label(advanced_frame, text="请求延迟:").grid(row=0, column=0, sticky='e', pady=3)
        
        delay_frame = ttk.Frame(advanced_frame)
        delay_frame.grid(row=0, column=1, sticky='w', padx=10, pady=3)
        
        self.min_delay_var = tk.DoubleVar(value=1.5)
        ttk.Label(delay_frame, text="最小:").pack(side='left')
        ttk.Spinbox(delay_frame, from_=0.5, to=10.0, increment=0.5,
                   textvariable=self.min_delay_var, width=8).pack(side='left', padx=(5, 15))
        
        self.max_delay_var = tk.DoubleVar(value=3.0)
        ttk.Label(delay_frame, text="最大:").pack(side='left')
        ttk.Spinbox(delay_frame, from_=0.5, to=10.0, increment=0.5,
                   textvariable=self.max_delay_var, width=8).pack(side='left', padx=(5, 0))
        
        # 页数限制
        ttk.Label(advanced_frame, text="页面限制:").grid(row=1, column=0, sticky='e', pady=3)
        
        pages_frame = ttk.Frame(advanced_frame)
        pages_frame.grid(row=1, column=1, sticky='w', padx=10, pady=3)
        
        self.limit_pages_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(pages_frame, text="限制页数:", variable=self.limit_pages_var,
                       command=self.toggle_pages).pack(side='left')
        
        self.max_pages_var = tk.IntVar(value=5)
        self.pages_spinbox = ttk.Spinbox(pages_frame, from_=1, to=100, increment=1,
                                        textvariable=self.max_pages_var, width=8,
                                        state='disabled')
        self.pages_spinbox.pack(side='left', padx=(5, 0))
        
        # 输出目录
        ttk.Label(advanced_frame, text="输出目录:").grid(row=2, column=0, sticky='e', pady=3)
        
        desktop_path = self.get_desktop_path()
        self.output_dir_var = tk.StringVar(value=desktop_path)
        output_frame = ttk.Frame(advanced_frame)
        output_frame.grid(row=2, column=1, sticky='we', padx=10, pady=3)
        
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=30).pack(side='left', fill='x', expand=True)
        ttk.Button(output_frame, text="浏览", command=self.browse_output_dir).pack(side='left', padx=(10, 0))
        
        advanced_frame.columnconfigure(1, weight=1)
        
        # 操作按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=(0, 10))
        
        self.start_button = ttk.Button(button_frame, text="开始爬取", 
                                       command=self.start_scraping, style='Action.TButton')
        self.start_button.pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="清空日志", 
                  command=self.clear_log).pack(side='left', padx=(0, 10))
        
        ttk.Button(button_frame, text="打开输出目录", 
                  command=self.open_output_dir).pack(side='left')
        
        # 进度条
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var,
                                           maximum=100, style='Progress.Horizontal.TProgressbar')
        self.progress_bar.pack(fill='x', pady=(0, 10))
        
        # 状态标签
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, style='Info.TLabel')
        status_label.pack(anchor='w', pady=(0, 5))
        
        # 日志区域
        log_frame = ttk.LabelFrame(main_frame, text="运行日志", padding="10")
        log_frame.pack(fill='both', expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap='word',
                                                  height=10, font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True)
        
        # 配置列权重
        input_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        # ====================== 关于作者页 ======================
        # 标题
        dev_title = ttk.Label(dev_frame, text="关于作者", font=('Microsoft YaHei', 14, 'bold'))
        dev_title.pack(pady=(10, 20))
        
        # 作者信息
        info_frame = ttk.Frame(dev_frame)
        info_frame.pack(pady=10)
        
        author_name = ttk.Label(info_frame, text="开发者：艺杯羹", font=('Microsoft YaHei', 12, 'bold'))
        author_name.grid(row=0, column=0, columnspan=2, pady=5)
        
        qq_label = ttk.Label(info_frame, text="QQ：3057454077", style='Dev.TLabel')
        qq_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        mp_label = ttk.Label(info_frame, text="公众号：艺杯羹", style='Dev.TLabel')
        mp_label.grid(row=2, column=0, columnspan=2, pady=5)
        
        # 二维码展示区域
        qr_frame = ttk.Frame(dev_frame)
        qr_frame.pack(pady=20, fill='both', expand=True)
        
        # 存储图片引用
        self.mp_photo = None
        self.donate_photo = None
        self.mp_path = None
        self.donate_path = None
        
        # 加载图片
        try:
            # 获取基础路径
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            docs_path = os.path.join(base_path, 'docs')
            
            # 公众号二维码
            self.mp_path = os.path.join(docs_path, '公众号.png')
            if os.path.exists(self.mp_path):
                # 加载图片并调整大小
                mp_img = Image.open(self.mp_path)
                mp_img.thumbnail((250, 250), Image.LANCZOS)
                self.mp_photo = ImageTk.PhotoImage(mp_img)
                
                mp_container = ttk.Frame(qr_frame)
                mp_container.grid(row=0, column=0, padx=20, pady=10)
                
                mp_label = tk.Label(mp_container, image=self.mp_photo, cursor='hand2', bg='#f0f0f0')
                mp_label.pack()
                mp_label.bind('<Button-1>', lambda e: self.show_image_zoom(self.mp_path, "公众号二维码"))
                
                mp_desc = ttk.Label(mp_container, text="公众号二维码 (点击放大)")
                mp_desc.pack(pady=5)
            
            # 赞赏码
            self.donate_path = os.path.join(docs_path, '赞赏码.png')
            if os.path.exists(self.donate_path):
                donate_img = Image.open(self.donate_path)
                donate_img.thumbnail((250, 250), Image.LANCZOS)
                self.donate_photo = ImageTk.PhotoImage(donate_img)
                
                donate_container = ttk.Frame(qr_frame)
                donate_container.grid(row=0, column=1, padx=20, pady=10)
                
                donate_label = tk.Label(donate_container, image=self.donate_photo, cursor='hand2', bg='#f0f0f0')
                donate_label.pack()
                donate_label.bind('<Button-1>', lambda e: self.show_image_zoom(self.donate_path, "赞赏码"))
                
                donate_desc = ttk.Label(donate_container, text="赞赏码 (点击放大)")
                donate_desc.pack(pady=5)
        
        except Exception as e:
            print(f"加载图片失败: {e}")
            ttk.Label(qr_frame, text="图片加载失败，请检查文件是否存在", foreground='red').pack(pady=20)
        
        # 感谢语
        thanks_label = ttk.Label(dev_frame, text="感谢使用！如果觉得好用，欢迎赞赏支持~", 
                               style='Info.TLabel', foreground='#666')
        thanks_label.pack(pady=20)
    
    def show_image_zoom(self, image_path, title):
        """显示图片放大窗口"""
        if image_path and os.path.exists(image_path):
            zoom_window = ImageZoomWindow(self.root, image_path, title)
            zoom_window.grab_set()
    
    def toggle_pages(self):
        """切换页数限制状态"""
        if self.limit_pages_var.get():
            self.pages_spinbox.config(state='normal')
        else:
            self.pages_spinbox.config(state='disabled')
    
    def browse_output_dir(self):
        """浏览输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录", initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def log(self, message):
        """添加日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert('end', log_message)
        self.log_text.see('end')
        self.log_buffer.append(log_message)
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, 'end')
        self.log_buffer = []
    
    def open_output_dir(self):
        """打开输出目录"""
        output_dir = self.output_dir_var.get()
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        if sys.platform == 'win32':
            os.startfile(output_dir)
        elif sys.platform == 'darwin':
            subprocess.call(['open', output_dir])
        else:
            subprocess.call(['xdg-open', output_dir])
    
    def start_scraping(self):
        """开始爬取"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入博客URL！")
            return
        
        if 'blog.csdn.net' not in url:
            messagebox.showerror("错误", "请输入有效的CSDN博客URL！")
            return
        
        # 禁用按钮
        self.start_button.config(state='disabled')
        self.status_var.set("正在爬取...")
        
        # 启动线程
        thread = threading.Thread(target=self.scrape_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def scrape_thread(self, url):
        """爬虫线程"""
        try:
            # 创建配置
            config = Config(
                blog_url=url,
                min_delay=self.min_delay_var.get(),
                max_delay=self.max_delay_var.get(),
                max_pages=self.max_pages_var.get() if self.limit_pages_var.get() else None,
                output_dir=self.output_dir_var.get()
            )
            
            # 创建爬虫
            logger = setup_logger(log_file=f"{config.output_dir}/scraper.log", 
                                 log_level=logging.INFO)
            scraper = CSDNBlogScraper(config, logger)
            
            # 开始爬取
            self.log("=" * 60)
            self.log("开始爬取文章...")
            self.log(f"目标: {url}")
            self.log(f"格式: {self.format_var.get()}")
            
            articles = scraper.scrape_all_articles()
            
            self.progress_var.set(70)
            
            if articles:
                self.log(f"爬取完成，共 {len(articles)} 篇文章")
                
                # 保存
                self.log("正在保存文件...")
                output_format = self.format_var.get()
                
                filename = f"csdn_articles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{output_format}"
                
                if output_format == 'csv':
                    filepath = scraper.save_to_csv(articles, filename)
                elif output_format == 'json':
                    filepath = scraper.save_to_json(articles, filename)
                else:
                    filepath = scraper.save_to_txt(articles, filename)
                
                self.progress_var.set(100)
                self.log(f"文件已保存: {filepath}")
                self.log("=" * 60)
                
                self.status_var.set("爬取完成！")
                messagebox.showinfo("成功", f"爬取完成！共 {len(articles)} 篇文章\n文件已保存到: {filepath}")
            else:
                self.log("未找到文章")
                self.status_var.set("爬取完成，但未找到文章")
                messagebox.showwarning("提示", "未找到文章")
            
        except Exception as e:
            error_msg = f"错误: {str(e)}"
            self.log(error_msg)
            self.status_var.set("发生错误")
            messagebox.showerror("错误", error_msg)
            import traceback
            self.log(traceback.format_exc())
        finally:
            # 恢复按钮
            self.start_button.config(state='normal')
            self.progress_var.set(0)


def main():
    """主函数"""
    root = tk.Tk()
    app = CSDNScraperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
