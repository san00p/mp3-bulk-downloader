# youtube_to_mp3.pyw
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import yt_dlp
import threading
import os
from pathlib import Path
import queue

# Set FFmpeg path
FFMPEG_PATH = r'C:\Users\san00\Desktop\ffmpeg-2025-04-14-git-3b2a9410ef-full_build\ffmpeg-2025-04-14-git-3b2a9410ef-full_build\bin\ffmpeg.exe'

class YouTubeToMP3:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube MP3 Downloader with Progress")
        self.root.geometry("700x600")
        self.download_queue = queue.Queue()
        self.currently_downloading = False
        self.total_files = 0
        self.completed_files = 0
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Arial', 11), padding=5)
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('Progress.TLabel', font=('Arial', 10, 'bold'))
        
        # Main container
        self.main_frame = ttk.Frame(root, padding="15")
        self.main_frame.pack(expand=True, fill=tk.BOTH)
        
        # URL input
        ttk.Label(self.main_frame, text="YouTube URLs (one per line):").pack(anchor=tk.W)
        self.url_text = scrolledtext.ScrolledText(self.main_frame, height=8, width=80, font=('Arial', 9))
        self.url_text.pack(fill=tk.X, pady=(0,10))
        
        # Options frame
        options_frame = ttk.Frame(self.main_frame)
        options_frame.pack(fill=tk.X, pady=5)
        
        # Audio quality
        ttk.Label(options_frame, text="Quality:").pack(side=tk.LEFT, padx=(0,5))
        self.quality_var = tk.StringVar(value="192")
        self.quality_combo = ttk.Combobox(
            options_frame,
            textvariable=self.quality_var,
            values=["320", "192", "128"],
            state="readonly",
            width=5
        )
        self.quality_combo.pack(side=tk.LEFT, padx=(0,15))
        
        # Save location
        ttk.Label(options_frame, text="Save To:").pack(side=tk.LEFT, padx=(0,5))
        self.location_entry = ttk.Entry(options_frame, width=40)
        self.location_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Button(
            options_frame,
            text="Browse",
            command=self.browse_location,
            width=8
        ).pack(side=tk.LEFT, padx=(5,0))
        self.location_entry.insert(0, str(Path.home() / "Downloads"))
        
        # Progress frame
        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.pack(fill=tk.X, pady=(10,5))
        
        # Current download info
        ttk.Label(progress_frame, text="Now Downloading:").pack(side=tk.LEFT)
        self.current_file_var = tk.StringVar(value="None")
        ttk.Label(
            progress_frame,
            textvariable=self.current_file_var,
            width=50,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(5,0)
        ).pack(side=tk.LEFT, padx=(5,0), expand=True, fill=tk.X)
        
        # File progress percentage
        self.file_progress_var = tk.StringVar(value="0%")
        ttk.Label(
            progress_frame,
            textvariable=self.file_progress_var,
            style='Progress.TLabel',
            width=5
        ).pack(side=tk.LEFT, padx=(5,0))
        
        # File progress bar
        self.file_progress = ttk.Progressbar(
            self.main_frame,
            orient=tk.HORIZONTAL,
            length=650,
            mode='determinate'
        )
        self.file_progress.pack(fill=tk.X, pady=(0,10))
        
        # Overall progress frame
        overall_frame = ttk.Frame(self.main_frame)
        overall_frame.pack(fill=tk.X, pady=(0,10))
        
        ttk.Label(overall_frame, text="Total Progress:").pack(side=tk.LEFT)
        self.overall_progress_var = tk.StringVar(value="0/0 (0%)")
        ttk.Label(
            overall_frame,
            textvariable=self.overall_progress_var,
            style='Progress.TLabel',
            width=15
        ).pack(side=tk.LEFT, padx=(5,0))
        
        self.overall_progress = ttk.Progressbar(
            overall_frame,
            orient=tk.HORIZONTAL,
            length=400,
            mode='determinate'
        )
        self.overall_progress.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5,0))
        
        # Button frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=(10,5))
        
        # Download button
        self.download_btn = ttk.Button(
            button_frame,
            text="Download All",
            command=self.start_download,
            style='TButton'
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0,10))
        
        # Cancel button
        self.cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel_download,
            state=tk.DISABLED
        )
        self.cancel_btn.pack(side=tk.LEFT, padx=(0,10))
        
        # Clear button
        ttk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            style='TButton'
        ).pack(side=tk.LEFT)
        
        # Status log
        ttk.Label(self.main_frame, text="Download Log:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(
            self.main_frame,
            height=12,
            width=80,
            font=('Consolas', 9),
            state='disabled'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Start queue checker
        self.check_queue()

    def browse_location(self):
        folder = filedialog.askdirectory()
        if folder:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, folder)
    
    def clear_all(self):
        self.url_text.delete('1.0', tk.END)
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')
        self.reset_progress()
    
    def reset_progress(self):
        self.file_progress['value'] = 0
        self.overall_progress['value'] = 0
        self.file_progress_var.set("0%")
        self.overall_progress_var.set("0/0 (0%)")
        self.current_file_var.set("None")
    
    def log_message(self, message, color="black"):
        self.log_text.config(state='normal')
        self.log_text.tag_config(color, foreground=color)
        self.log_text.insert(tk.END, message + "\n", color)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        self.root.update()
    
    def start_download(self):
        urls = [url.strip() for url in self.url_text.get('1.0', tk.END).split('\n') if url.strip()]
        
        if not urls:
            messagebox.showerror("Error", "Please enter at least one YouTube URL")
            return
            
        if not os.path.isdir(self.location_entry.get().strip()):
            messagebox.showerror("Error", "Invalid save location")
            return
        
        # Clear log and reset progress
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state='disabled')
        self.reset_progress()
        
        # Add to queue
        self.total_files = len(urls)
        self.completed_files = 0
        for url in urls:
            self.download_queue.put((url, self.location_entry.get().strip(), self.quality_var.get()))
        
        self.update_overall_progress()
        self.download_btn.config(state=tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL)
        self.log_message("=== Starting batch download ===", "blue")
    
    def cancel_download(self):
        self.download_queue.queue.clear()
        self.currently_downloading = False
        self.cancel_btn.config(state=tk.DISABLED)
        self.download_btn.config(state=tk.NORMAL)
        self.log_message("=== Download cancelled ===", "red")
        self.reset_progress()
    
    def update_overall_progress(self):
        if self.total_files > 0:
            percent = (self.completed_files / self.total_files) * 100
            self.overall_progress_var.set(f"{self.completed_files}/{self.total_files} ({int(percent)}%)")
            self.overall_progress['value'] = percent
    
    def check_queue(self):
        if not self.currently_downloading and not self.download_queue.empty():
            url, save_path, quality = self.download_queue.get()
            self.currently_downloading = True
            self.current_file_var.set(url[:60] + "..." if len(url) > 60 else url)
            
            threading.Thread(
                target=self.download_mp3,
                args=(url, save_path, quality),
                daemon=True
            ).start()
        
        self.root.after(500, self.check_queue)
    
    def download_mp3(self, url, save_path, quality):
        try:
            self.log_message(f"\nStarting: {url}", "blue")
            
            class ProgressHook:
                def __init__(self, callback):
                    self.callback = callback
                
                def __call__(self, d):
                    self.callback(d)
                    return True
            
            def update_progress(d):
                if d['status'] == 'downloading':
                    if 'total_bytes' in d:
                        percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                        self.file_progress_var.set(f"{int(percent)}%")
                        self.file_progress['value'] = percent
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
                'ffmpeg_location': FFMPEG_PATH,
                'progress_hooks': [ProgressHook(update_progress)],
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                mp3_file = filename.replace('.webm', '.mp3').replace('.m4a', '.mp3')
                
                if os.path.exists(mp3_file):
                    self.log_message(f"✓ Success: {os.path.basename(mp3_file)}", "green")
                else:
                    raise Exception("MP3 file not created")
            
        except Exception as e:
            self.log_message(f"✗ Failed: {str(e)}", "red")
        finally:
            self.currently_downloading = False
            self.completed_files += 1
            self.update_overall_progress()
            self.file_progress_var.set("0%")
            self.file_progress['value'] = 0
            
            if self.download_queue.empty():
                self.log_message("\n=== All downloads completed ===", "blue")
                self.download_btn.config(state=tk.NORMAL)
                self.cancel_btn.config(state=tk.DISABLED)
                if self.completed_files == self.total_files:
                    messagebox.showinfo("Complete", "All downloads finished successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeToMP3(root)
    root.mainloop()