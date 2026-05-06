# -*- coding: utf-8 -*-
"""
CSDN博客爬虫 - 可视化界面
版本: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
from datetime import datetime
import sys
from pathlib import Path

# 导入核心模块
sys.path.insert(0, str(Path(__file__).parent))

from src import CSDNBlogScraper, Config, setup_logger
import logging


class CSDNScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSDN博客爬虫 v1.0.0")
        self.root.geometry("800x650")
        self.root.minsize(700, 550)
        
        # 设置图标和样式
        self.setup_style()
        
        # 创建主框架
        self.create_widgets()
        
        # 日志输出
        self.log_buffer = []
        
    def setup_style(self):
        """设置界面样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 配置样式
        style.configure('Title.TLabel', font=('Microsoft YaHei', 16, 'bold'), foreground='#333')
        style.configure('Subtitle.TLabel', font=('Microsoft YaHei', 11), foreground='#666')
        style.configure('Info.TLabel', font=('Microsoft YaHei', 9), foreground='#666')
        style.configure('Action.TButton', font=('Microsoft YaHei', 10))
        style.configure('Progress.Horizontal.TProgressbar', thickness=12)
    
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
        
        # 主内容区域
        main_frame = ttk.Frame(self.root, padding="20 0 20 20")
        main_frame.pack(fill='both', expand=True)
        
        # 输入区域
        input_frame = ttk.LabelFrame(main_frame, text="配置信息", padding="15")
        input_frame.pack(fill='x', pady=(0, 15))
        
        # 博客URL
        ttk.Label(input_frame, text="博客URL:").grid(row=0, column=0, sticky='e', pady=5)
        
        self.url_var = tk.StringVar(value="https://blog.csdn.net/qq_46987323")
        url_entry = ttk.Entry(input_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=0, column=1, sticky='we', padx=10, pady=5)
        
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
        
        self.output_dir_var = tk.StringVar(value="outputs")
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
                                                  height=12, font=('Consolas', 9))
        self.log_text.pack(fill='both', expand=True)
        
        # 配置列权重
        input_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def toggle_pages(self):
        """切换页数限制状态"""
        if self.limit_pages_var.get():
            self.pages_spinbox.config(state='normal')
        else:
            self.pages_spinbox.config(state='disabled')
    
    def browse_output_dir(self):
        """浏览输出目录"""
        directory = filedialog.askdirectory(title="选择输出目录")
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
        import os
        import subprocess
        
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
            messagebox.showerror("错误", "请输入博客URL")
            return
        
        # 验证URL
        if 'blog.csdn.net' not in url:
            messagebox.showerror("错误", "请输入有效的CSDN博客URL")
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
            
            # 重定向日志输出
            original_log = getattr(logger, '_log', None)
            
            def custom_log(level, msg, args, **kwargs):
                self.log(msg)
                if original_log:
                    original_log(level, msg, args, **kwargs)
            
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
                messagebox.showinfo("成功", f"爬取完成！共 {len(articles)} 篇文章\n文件已保存")
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
