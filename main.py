import tkinter as tk
import requests
import time
import threading
import asyncio
import os
import ctypes
import json
import shutil
import subprocess
import logging
import sqlite3
from datetime import datetime, timezone
from assets import ICON_B64
from tkinter import messagebox
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

CURRENT_VERSION = "1.2.5"
CONFIG_PATH = os.path.join(os.environ.get("APPDATA", ""), "SpoLyrics", "config.json")
APP_DIR = os.path.join(os.environ.get("APPDATA", ""), "SpoLyrics")
os.makedirs(APP_DIR, exist_ok=True)
LOG_PATH = os.path.join(APP_DIR, "error.log")
STARTUP_SHORTCUT = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "SpoLyrics.lnk")
ICON_PATH = os.path.join(APP_DIR, "icon.ico")

logging.basicConfig(filename=LOG_PATH, level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

CACHE_DB_PATH = os.path.join(APP_DIR, "lyrics_cache.db")
db_lock = threading.Lock()
def init_db():
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS lyrics
                     (artist TEXT, title TEXT, duration REAL, parsed_lyrics TEXT)''')
        c.execute('''CREATE INDEX IF NOT EXISTS idx_song ON lyrics (artist, title)''')
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error("DB init error", exc_info=e)

init_db()

def get_cached_lyrics(title, artist, duration):
    try:
        conn = sqlite3.connect(CACHE_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT parsed_lyrics FROM lyrics WHERE artist=? AND title=? AND abs(duration - ?) <= 3", (artist.lower(), title.lower(), duration))
        row = c.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
    except Exception as e:
        logging.error("Cache read error", exc_info=e)
    return None

def save_cached_lyrics(title, artist, duration, parsed_lyrics):
    try:
        with db_lock:
            conn = sqlite3.connect(CACHE_DB_PATH, timeout=5)
            c = conn.cursor()
            c.execute("INSERT INTO lyrics (artist, title, duration, parsed_lyrics) VALUES (?, ?, ?, ?)", 
                      (artist.lower(), title.lower(), duration, json.dumps(parsed_lyrics)))
            conn.commit()
            conn.close()
    except Exception as e:
        logging.error("Cache write error", exc_info=e)

def load_config():
    default_config = {
        'color': '#1DB954',
        'auto_start': False,
        'font_size': 11,
        'opacity': 0.85
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r') as f:
                loaded = json.load(f)
                default_config.update(loaded)
        except Exception as e:
            logging.error("Failed to load config", exc_info=e)
    return default_config

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f)

def get_exe_path():
    import sys
    if getattr(sys, 'frozen', False):
        return sys.executable
    script_exe = os.path.join(sys.prefix, 'Scripts', 'spolyrics.exe')
    if os.path.exists(script_exe):
        return script_exe
    
    pythonw = os.path.join(sys.prefix, 'pythonw.exe')
    if os.path.exists(pythonw):
        return (pythonw, os.path.abspath(__file__))
    return sys.executable

def set_auto_start(enable, force_update=False):
    try:
        if enable:
            app_dir = os.path.join(os.environ.get("APPDATA", ""), "SpoLyrics")
            icon_path = os.path.join(app_dir, 'icon.ico')
            exe_path = get_exe_path()
            if exe_path and os.path.exists(icon_path):
                if force_update or not os.path.exists(STARTUP_SHORTCUT):
                    if isinstance(exe_path, tuple):
                        target, args = exe_path
                        ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{STARTUP_SHORTCUT}');$s.TargetPath='{target}';$s.Arguments='\"{args}\"';$s.IconLocation='{icon_path}';$s.Save()"
                    else:
                        ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{STARTUP_SHORTCUT}');$s.TargetPath='{exe_path}';$s.IconLocation='{icon_path}';$s.Save()"
                    subprocess.run(["powershell", "-Command", ps_script], creationflags=0x08000000)
        else:
            if os.path.exists(STARTUP_SHORTCUT):
                os.remove(STARTUP_SHORTCUT)
    except Exception as e:
        logging.error("Failed to set auto start", exc_info=e)

class MiniLyrics:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.root.overrideredirect(True) 
        self.root.attributes('-topmost', True) 
        self.root.attributes('-alpha', self.config.get('opacity', 0.85)) 
        
        if os.path.exists(ICON_PATH):
            self.root.iconbitmap(ICON_PATH)
            
        self.root.geometry("350x120+100+100")
        self.root.configure(bg='#191414') 
        
        self.root.update_idletasks()
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int))
        except Exception as e:
            logging.error("Failed to set DWM rounded corners", exc_info=e)
        
        self.font_cur = 11
        self.font_nxt = max(4, self.font_cur - 2)
        self.is_pinned = False
        self.show_title = True
        
        self.lbl_title = tk.Label(self.root, text="", fg='#a0a0a0', bg='#191414', font=('Segoe UI', 8, 'bold'), justify='center', wraplength=320)
        self.lbl_title.place(relx=0.5, y=8, anchor='n')
        
        self.lbl_current = tk.Label(self.root, text="Waiting for song...", fg=self.config['color'], bg='#191414', font=('Arial', self.font_cur, 'bold'), wraplength=330, justify="center")
        self.lbl_current.pack(expand=True, fill='both', padx=10, pady=(25, 2))
        
        self.lbl_next = tk.Label(self.root, text="", fg='#b3b3b3', bg='#191414', font=('Arial', self.font_nxt), wraplength=330, justify="center")
        self.lbl_next.pack(expand=True, fill='both', padx=10, pady=(0, 15))
        
        self.update_available = False
        self.root.after(2000, self.check_updates)

        self.grip = tk.Label(self.root, text="⇲", fg='#333333', bg='#191414', cursor="size_nw_se")
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        
        self.grip.bind("<B1-Motion>", self.on_resize)
        self.grip.bind("<Enter>", lambda e: not self.is_pinned and self.grip.config(fg='#888888'))
        self.grip.bind("<Leave>", lambda e: not self.is_pinned and self.grip.config(fg='#333333'))
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<Button-1>", self.click)
        self.root.bind("<Double-1>", lambda e: not self.is_pinned and self.root.destroy()) 
        self.root.bind("<Button-3>", lambda e: self.media_control('play_pause'))
        self.root.bind("<MouseWheel>", self.on_scroll)
        self.root.bind("<Control-MouseWheel>", self.on_font_scroll)
        self.root.bind("<Button-2>", self.toggle_pin)
        self.root.bind("<Control-Button-1>", self.toggle_title)
        
        for lbl in (self.lbl_current, self.lbl_next, self.lbl_title):
            lbl.bind("<B1-Motion>", self.drag)
            
        for w in (self.lbl_current, self.lbl_next, self.grip, self.lbl_title):
            w.bind("<Button-1>", self.click)
            w.bind("<Control-Button-1>", self.toggle_title)
            w.bind("<Double-1>", lambda e: not self.is_pinned and self.root.destroy())
            w.bind("<Button-3>", lambda e: self.media_control('play_pause'))
            w.bind("<MouseWheel>", self.on_scroll)
            w.bind("<Control-MouseWheel>", self.on_font_scroll)
            w.bind("<Button-2>", self.toggle_pin)

        self.current_song = ""
        self.synced_lyrics = []
        self.base_pos = 0.0
        self.base_time = time.time()
        self.is_playing = False
        
        self.render_lyrics()
        threading.Thread(target=self.poll_song, daemon=True).start()

    def get_tray_menu(self):
        import pystray
        items = [
            pystray.MenuItem("Shortcuts & Info", self.tray_callbacks['on_info']),
            pystray.MenuItem("Settings", self.tray_callbacks['on_settings']),
            pystray.MenuItem("Toggle Visibility", self.tray_callbacks['on_toggle_lyrics']),
            pystray.MenuItem("Quit", self.tray_callbacks['on_quit']),
            pystray.MenuItem(f"v{CURRENT_VERSION}", lambda: None, enabled=False)
        ]
        if getattr(self, 'update_available', False):
            items.insert(0, pystray.MenuItem("🔥 Update Available!", lambda: self.root.after(0, self.prompt_update)))
        return pystray.Menu(*items)


    def render_lyrics(self):
        if self.synced_lyrics:
            pos = self.base_pos
            if self.is_playing:
                pos += time.time() - self.base_time
                
            cur_text, next_text = "...", ""
            for i, (lyric_time, txt) in enumerate(self.synced_lyrics):
                if pos >= lyric_time:
                    cur_text = txt
                    if i + 1 < len(self.synced_lyrics):
                        next_text = self.synced_lyrics[i+1][1]
                else:
                    break
                    
            if getattr(self, '_last_cur', None) != cur_text:
                self.lbl_current.config(text=cur_text)
                self._last_cur = cur_text
            if getattr(self, '_last_nxt', None) != next_text:
                self.lbl_next.config(text=next_text)
                self._last_nxt = next_text
                
        self.root.after(50, self.render_lyrics)

    def click(self, event):
        self._offset_x = self.root.winfo_pointerx() - self.root.winfo_rootx()
        self._offset_y = self.root.winfo_pointery() - self.root.winfo_rooty()
        return "break"

    def toggle_title(self, event):
        if self.is_pinned: return "break"
        self.show_title = not self.show_title
        self.lbl_title.config(text=self.current_song if self.show_title else "")
        return "break"

    def toggle_pin(self, event):
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.grip.config(text="🔒", fg=self.config['color'], cursor="arrow")
        else:
            self.grip.config(text="⇲", fg='#333333', cursor="size_nw_se")
        return "break"

    def drag(self, event):
        if self.is_pinned or event.widget == self.grip: return "break"
        x = self.root.winfo_pointerx() - self._offset_x
        y = self.root.winfo_pointery() - self._offset_y
        self.root.geometry(f"+{x}+{y}")
        return "break"

    def on_resize(self, event):
        if self.is_pinned: return "break"
        new_w = max(200, self.root.winfo_pointerx() - self.root.winfo_rootx())
        new_h = max(80, self.root.winfo_pointery() - self.root.winfo_rooty())
        self.root.geometry(f"{new_w}x{new_h}")
        self.lbl_current.config(wraplength=new_w - 20)
        self.lbl_next.config(wraplength=new_w - 20)
        self.lbl_title.config(wraplength=new_w - 30)
        return "break"

    def on_font_scroll(self, event):
        if self.is_pinned: return "break"
        if event.delta > 0:
            self.font_cur += 1
            self.font_nxt += 1
        else:
            self.font_cur = max(6, self.font_cur - 1)
            self.font_nxt = max(4, self.font_nxt - 1)
            
        self.lbl_current.config(font=('Arial', self.font_cur, 'bold'))
        self.lbl_next.config(font=('Arial', self.font_nxt))
        return "break"

    def on_scroll(self, event):
        if self.is_pinned: return "break"
        
        now = time.time()
        if not hasattr(self, 'last_scroll_time'):
            self.last_scroll_time = 0
            
        if now - self.last_scroll_time < 0.8:
            return "break"
            
        self.last_scroll_time = now
        
        if event.delta > 0: self.media_control('prev')
        else: self.media_control('next')
        return "break"
        
    def update_ui(self, cur, nxt):
        self.lbl_current.config(text=cur)
        self.lbl_next.config(text=nxt)
        self.lbl_title.config(text=self.current_song if self.show_title else "")

    def toggle_visibility(self):
        if self.root.winfo_viewable():
            self.root.withdraw()
        else:
            self.root.deiconify()

    def open_info(self):
        if hasattr(self, 'info_win') and self.info_win.winfo_exists():
            self.info_win.focus()
            return
            
        self.info_win = tk.Toplevel(self.root)
        self.info_win.title("SpoLyrics Info")
        self.info_win.geometry("420x400")
        self.info_win.configure(bg='#191414')
        self.info_win.attributes('-topmost', True)
        self.info_win.overrideredirect(True)
        self.info_win.attributes('-alpha', 1.0)
        
        def start_drag(e):
            self.info_win._offset_x = self.info_win.winfo_pointerx() - self.info_win.winfo_rootx()
            self.info_win._offset_y = self.info_win.winfo_pointery() - self.info_win.winfo_rooty()

        def do_drag(e):
            x = self.info_win.winfo_pointerx() - self.info_win._offset_x
            y = self.info_win.winfo_pointery() - self.info_win._offset_y
            self.info_win.geometry(f"+{x}+{y}")
            
        self.info_win.bind("<Button-1>", start_drag)
        self.info_win.bind("<B1-Motion>", do_drag)
        
        lbl_title = tk.Label(self.info_win, text="📚 SpoLyrics Shortcuts", fg='#1DB954', bg='#191414', font=('Segoe UI', 14, 'bold'))
        lbl_title.pack(pady=(20, 15))
        lbl_title.bind("<Button-1>", start_drag)
        lbl_title.bind("<B1-Motion>", do_drag)
        
        shortcuts = [
            ("🖱️ Left Click (Hold)", "Move Window"),
            ("🖱️ Right Click", "Play / Pause"),
            ("🖱️ Middle Mouse Click", "Pin / Unpin Window (🔒)"),
            ("🖱️ Middle Mouse Scroll", "Next / Previous Track"),
            ("🖱️ Double Left Click", "Quit Application"),
            ("⌨️ Ctrl + Left Click", "Show / Hide Title"),
            ("⌨️ Ctrl + Scroll", "Resize Text")
        ]
        
        for k, v in shortcuts:
            frame = tk.Frame(self.info_win, bg='#191414')
            frame.pack(fill='x', padx=30, pady=5)
            frame.bind("<Button-1>", start_drag)
            frame.bind("<B1-Motion>", do_drag)
            
            lbl_k = tk.Label(frame, text=k, fg='white', bg='#191414', font=('Segoe UI', 9, 'bold'))
            lbl_k.pack(side='left')
            lbl_k.bind("<Button-1>", start_drag)
            lbl_k.bind("<B1-Motion>", do_drag)
            
            lbl_v = tk.Label(frame, text=v, fg='#a0a0a0', bg='#191414', font=('Segoe UI', 9))
            lbl_v.pack(side='right')
            lbl_v.bind("<Button-1>", start_drag)
            lbl_v.bind("<B1-Motion>", do_drag)
            
        close_btn = tk.Label(self.info_win, text="Close", bg='#333333', fg='white', font=('Segoe UI', 10, 'bold'), pady=6, cursor='hand2')
        close_btn.pack(fill='x', padx=40, pady=(20, 10))
        close_btn.bind("<Button-1>", lambda e: self.info_win.destroy())
        
        close_btn.bind("<Enter>", lambda e: close_btn.config(bg='#444444'))
        close_btn.bind("<Leave>", lambda e: close_btn.config(bg='#333333'))
        
        x = self.root.winfo_rootx()
        y = self.root.winfo_rooty() + 80
        self.info_win.geometry(f"+{x}+{y}")

    def open_settings(self):
        if hasattr(self, 'settings_win') and self.settings_win.winfo_exists():
            self.settings_win.focus()
            return
            
        self.settings_win = tk.Toplevel(self.root)
        self.settings_win.title("SpoLyrics Settings")
        self.settings_win.geometry("380x520")
        self.settings_win.configure(bg='#191414')
        self.settings_win.attributes('-topmost', True)
        self.settings_win.resizable(False, False)
        
        if os.path.exists(ICON_PATH):
            self.settings_win.iconbitmap(ICON_PATH)
            
        def on_settings_close():
            self.root.attributes('-alpha', self.config.get('opacity', 0.85))
            self.settings_win.destroy()
        self.settings_win.protocol("WM_DELETE_WINDOW", on_settings_close)
        
        header_frame = tk.Frame(self.settings_win, bg='#191414')
        header_frame.pack(fill='x', padx=25, pady=(20, 15))
        tk.Label(header_frame, text="Settings", fg='white', bg='#191414', font=('Segoe UI', 18, 'bold')).pack(side='left')
        
        info_lbl = tk.Label(header_frame, text="❔", fg='#888888', bg='#191414', font=('Segoe UI', 12), cursor='hand2')
        info_lbl.pack(side='right', pady=(5,0))
        info_lbl.bind("<Button-1>", lambda e: self.open_info())
        info_lbl.bind("<Enter>", lambda e: info_lbl.config(fg='white'))
        info_lbl.bind("<Leave>", lambda e: info_lbl.config(fg='#888888'))
        
        tk.Label(self.settings_win, text="APPEARANCE", fg='#888888', bg='#191414', font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=25, pady=(0, 5))
        app_card = tk.Frame(self.settings_win, bg='#242424')
        app_card.pack(fill='x', padx=25, pady=(0, 15))
        
        color_frame = tk.Frame(app_card, bg='#242424')
        color_frame.pack(fill='x', padx=15, pady=12)
        tk.Label(color_frame, text="Lyrics Color", fg='#e0e0e0', bg='#242424', font=('Segoe UI', 10)).pack(side='left')
        
        self.current_hex = self.config['color']
        color_btn = tk.Frame(color_frame, bg=self.current_hex, width=24, height=24, cursor='hand2', highlightbackground='#555', highlightthickness=1)
        color_btn.pack(side='right')
        
        palette_frame = tk.Frame(app_card, bg='#1e1e1e')
        self.palette_visible = False
        
        import colorsys
        def hls_to_hex(h, l, s=1.0):
            rgb = colorsys.hls_to_rgb(h, l, s)
            return "#{:02x}{:02x}{:02x}".format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
            
        tk.Label(palette_frame, text="Hue:", fg='#888', bg='#1e1e1e', font=('Segoe UI', 8)).pack(anchor='w', padx=15, pady=(10,2))
        hue_canvas = tk.Canvas(palette_frame, width=240, height=12, bg='#1e1e1e', highlightthickness=0, cursor='hand2')
        hue_canvas.pack(pady=(0, 5))
        
        for i in range(120):
            c = hls_to_hex(i/120.0, 0.5)
            hue_canvas.create_rectangle(i*2, 0, (i+1)*2, 12, fill=c, outline=c)
        hue_thumb = hue_canvas.create_rectangle(0, 0, 4, 12, fill='white', outline='black')
        
        tk.Label(palette_frame, text="Lightness:", fg='#888', bg='#1e1e1e', font=('Segoe UI', 8)).pack(anchor='w', padx=15, pady=(5,2))
        lit_canvas = tk.Canvas(palette_frame, width=240, height=12, bg='#1e1e1e', highlightthickness=0, cursor='hand2')
        lit_canvas.pack(pady=(0, 10))
        
        lit_rects = []
        for i in range(120):
            r = lit_canvas.create_rectangle(i*2, 0, (i+1)*2, 12, fill='#fff', outline='#fff')
            lit_rects.append(r)
        lit_thumb = lit_canvas.create_rectangle(120, 0, 124, 12, fill='black', outline='white')
        
        custom_frame = tk.Frame(palette_frame, bg='#1e1e1e')
        custom_frame.pack(pady=(0, 15))
        tk.Label(custom_frame, text="Hex:", fg='#888', bg='#1e1e1e', font=('Segoe UI', 9)).pack(side='left')
        hex_entry = tk.Entry(custom_frame, width=9, bg='#333', fg='white', insertbackground='white', relief='flat', justify='center')
        hex_entry.insert(0, self.current_hex)
        hex_entry.pack(side='left', padx=5)
        
        self.cur_h = 0.33
        self.cur_l = 0.5
        
        def update_lit_canvas():
            for i in range(120):
                c = hls_to_hex(self.cur_h, i/120.0)
                lit_canvas.itemconfig(lit_rects[i], fill=c, outline=c)
                
        def set_color_from_picker():
            c = hls_to_hex(self.cur_h, self.cur_l)
            self.current_hex = c
            color_btn.config(bg=c)
            hex_entry.delete(0, 'end')
            hex_entry.insert(0, c)
            
        def on_hue_drag(e):
            x = max(0, min(e.x, 240))
            self.cur_h = x / 240.0
            hue_canvas.coords(hue_thumb, x-2, 0, x+2, 12)
            update_lit_canvas()
            set_color_from_picker()
            
        def on_lit_drag(e):
            x = max(0, min(e.x, 240))
            self.cur_l = x / 240.0
            lit_canvas.coords(lit_thumb, x-2, 0, x+2, 12)
            set_color_from_picker()
            
        hue_canvas.bind("<B1-Motion>", on_hue_drag)
        hue_canvas.bind("<Button-1>", on_hue_drag)
        lit_canvas.bind("<B1-Motion>", on_lit_drag)
        lit_canvas.bind("<Button-1>", on_lit_drag)
        
        def apply_hex(e):
            v = hex_entry.get().strip()
            if v.startswith('#') and len(v) in [4, 7]:
                self.current_hex = v
                color_btn.config(bg=v)
        hex_entry.bind("<Return>", apply_hex)
        
        def toggle_palette(e=None):
            if not self.palette_visible:
                self.settings_win.geometry("380x680")
                update_lit_canvas()
                palette_frame.pack(fill='x', after=color_frame)
                hex_entry.delete(0, 'end')
                hex_entry.insert(0, self.current_hex)
            else:
                self.settings_win.geometry("380x520")
                palette_frame.pack_forget()
            self.palette_visible = not self.palette_visible
            
        color_btn.bind("<Button-1>", toggle_palette)
        
        tk.Frame(app_card, height=1, bg='#333').pack(fill='x', padx=15)
        
        op_frame = tk.Frame(app_card, bg='#242424')
        op_frame.pack(fill='x', padx=15, pady=12)
        tk.Label(op_frame, text="Window Opacity", fg='#e0e0e0', bg='#242424', font=('Segoe UI', 10)).pack(side='left')
        
        self.cur_op = self.config.get('opacity', 0.85)
        op_val_lbl = tk.Label(op_frame, text=f"{int(self.cur_op*100)}%", fg='#888', bg='#242424', font=('Segoe UI', 9, 'bold'))
        op_val_lbl.pack(side='right')
        
        op_canvas = tk.Canvas(app_card, width=330, height=14, bg='#242424', highlightthickness=0, cursor='hand2')
        op_canvas.pack(pady=(0, 15))
        op_canvas.create_rectangle(20, 5, 310, 9, fill='#333', outline='#333', width=0)
        op_fill = op_canvas.create_rectangle(20, 5, int(self.cur_op*290)+20, 9, fill='#1DB954', outline='#1DB954', width=0)
        th_x = int(self.cur_op*290)+20
        op_thumb = op_canvas.create_oval(th_x-6, 1, th_x+6, 13, fill='white', outline='white')
        
        def on_op_drag(e):
            x = max(20+29, min(e.x, 310))
            self.cur_op = (x-20) / 290.0
            op_canvas.coords(op_fill, 20, 5, x, 9)
            op_canvas.coords(op_thumb, x-6, 1, x+6, 13)
            op_val_lbl.config(text=f"{int(self.cur_op*100)}%")
            self.root.attributes('-alpha', self.cur_op)
            
        op_canvas.bind("<B1-Motion>", on_op_drag)
        op_canvas.bind("<Button-1>", on_op_drag)
        
        tk.Label(self.settings_win, text="SYSTEM", fg='#888888', bg='#191414', font=('Segoe UI', 8, 'bold')).pack(anchor='w', padx=25, pady=(5, 5))
        sys_card = tk.Frame(self.settings_win, bg='#242424')
        sys_card.pack(fill='x', padx=25, pady=(0, 15))
        
        toggle_frame = tk.Frame(sys_card, bg='#242424')
        toggle_frame.pack(fill='x', padx=15, pady=12)
        tk.Label(toggle_frame, text="Auto-start Windows", fg='#e0e0e0', bg='#242424', font=('Segoe UI', 10)).pack(side='left')
        
        class ToggleSwitch(tk.Canvas):
            def __init__(self, parent, initial_state=False, *args, **kwargs):
                tk.Canvas.__init__(self, parent, width=40, height=20, bg='#242424', highlightthickness=0, cursor='hand2', *args, **kwargs)
                self.is_on = initial_state
                self.track = self.create_oval(2, 2, 18, 18, fill="#555", outline="#555")
                self.track2 = self.create_oval(22, 2, 38, 18, fill="#555", outline="#555")
                self.rect = self.create_rectangle(10, 2, 30, 18, fill="#555", outline="#555")
                self.thumb = self.create_oval(4, 4, 16, 16, fill="white", outline="white")
                self.bind("<Button-1>", self.toggle)
                self._update_ui()
                
            def toggle(self, event):
                self.is_on = not self.is_on
                self._update_ui()
                
            def _update_ui(self):
                if self.is_on:
                    self.itemconfig(self.track, fill="#1DB954", outline="#1DB954")
                    self.itemconfig(self.track2, fill="#1DB954", outline="#1DB954")
                    self.itemconfig(self.rect, fill="#1DB954", outline="#1DB954")
                    self.coords(self.thumb, 24, 4, 36, 16)
                else:
                    self.itemconfig(self.track, fill="#555", outline="#555")
                    self.itemconfig(self.track2, fill="#555", outline="#555")
                    self.itemconfig(self.rect, fill="#555", outline="#555")
                    self.coords(self.thumb, 4, 4, 16, 16)

        toggle = ToggleSwitch(toggle_frame, initial_state=self.config['auto_start'])
        toggle.pack(side='right')
        
        tk.Frame(sys_card, height=1, bg='#333').pack(fill='x', padx=15)
        
        cache_frame = tk.Frame(sys_card, bg='#242424')
        cache_frame.pack(fill='x', padx=15, pady=12)
        tk.Label(cache_frame, text="Lyrics Cache", fg='#e0e0e0', bg='#242424', font=('Segoe UI', 10)).pack(side='left')
        
        def get_db_size():
            try:
                if os.path.exists(CACHE_DB_PATH):
                    size_bytes = os.path.getsize(CACHE_DB_PATH)
                    if size_bytes >= 1024 * 1024: return f"{size_bytes / (1024 * 1024):.2f} MB"
                    else: return f"{size_bytes / 1024:.2f} KB"
            except Exception: pass
            return "0.00 KB"
            
        del_btn = tk.Label(cache_frame, text="Clear", bg='#333', fg='#ff4444', font=('Segoe UI', 8, 'bold'), padx=8, pady=2, cursor='hand2')
        del_btn.pack(side='right')
        
        cache_size_lbl = tk.Label(cache_frame, text=get_db_size(), fg='#888', bg='#242424', font=('Segoe UI', 9))
        cache_size_lbl.pack(side='right', padx=(0, 10))
        
        def delete_cache(e=None):
            try:
                conn = sqlite3.connect(CACHE_DB_PATH)
                c = conn.cursor()
                c.execute("DELETE FROM lyrics")
                conn.commit()
                c.execute("VACUUM")
                conn.close()
                cache_size_lbl.config(text=get_db_size())
                self.synced_lyrics = []
            except Exception as ex:
                logging.error("Failed to delete cache", exc_info=ex)
                
        del_btn.bind("<Button-1>", delete_cache)
        del_btn.bind("<Enter>", lambda e: del_btn.config(bg='#ff4444', fg='white'))
        del_btn.bind("<Leave>", lambda e: del_btn.config(bg='#333', fg='#ff4444'))
        
        def save_and_apply(e=None):
            self.config['color'] = self.current_hex
            self.config['auto_start'] = toggle.is_on
            self.config['opacity'] = self.cur_op
            save_config(self.config)
            self.lbl_current.config(fg=self.config['color'])
            set_auto_start(self.config['auto_start'])
            if self.is_pinned:
                self.grip.config(fg=self.config['color'])
            
            save_btn.config(bg='#15893e')
            self.settings_win.protocol("WM_DELETE_WINDOW", lambda: None)
            self.root.after(100, lambda: self.settings_win.destroy() if self.settings_win.winfo_exists() else None)
            
        save_btn = tk.Label(self.settings_win, text="Save & Apply", bg='#1DB954', fg='white', font=('Segoe UI', 10, 'bold'), pady=8, cursor='hand2')
        save_btn.pack(fill='x', padx=25, pady=(5, 20))
        
        save_btn.bind("<Button-1>", save_and_apply)
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg='#1ed760'))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg='#1DB954'))

    def media_control(self, action):
        if self.is_pinned: return "break"
        async def do_action():
            sessions = await MediaManager.request_async()
            current = sessions.get_current_session()
            if current:
                if action == 'play_pause':
                    info = current.get_playback_info()
                    if info and getattr(info.playback_status, 'value', info.playback_status) == 4:
                        self.is_playing = False
                        await current.try_pause_async()
                    else:
                        self.is_playing = True
                        self.base_time = time.time()
                        await current.try_play_async()
                elif action == 'next':
                    await current.try_skip_next_async()
                elif action == 'prev':
                    await current.try_skip_previous_async()
        threading.Thread(target=lambda: asyncio.run(do_action())).start()
        return "break"

    def fetch_smart_lyrics(self, title, artist, actual_duration):
        cached = get_cached_lyrics(title, artist, actual_duration)
        if cached:
            return cached

        try:
            # Menggunakan User-Agent agar tidak diblokir API
            res = requests.get('https://lrclib.net/api/search', params={'track_name': title, 'artist_name': artist}, headers={'User-Agent': 'SpoLyrics/2.0'}, timeout=8).json()
            if res and isinstance(res, list) and len(res) > 0:
                best_match = None
                t_low = title.lower()
                a_low = artist.lower()
                
                # --- TAHAP 1: Kumpulkan semua kandidat yang durasinya valid (Toleransi 3 detik) ---
                duration_matches = []
                for track in res:
                    if track.get('syncedLyrics') and track.get('duration'):
                        if abs(track['duration'] - actual_duration) <= 3:
                            duration_matches.append(track)
                
                if duration_matches:
                    # --- TAHAP 2: Prioritas Judul Spesifik (Slayer of False Positives) ---
                    # Cari yang judulnya sangat identik (untuk mendeteksi "English Version", "Twin Ver", dll)
                    for track in duration_matches:
                        tr_name = track.get('trackName', '').lower()
                        if tr_name == t_low or t_low in tr_name or tr_name in t_low:
                            best_match = track
                            break
                    
                    # Fallback Tahap 2: Jika judul tidak ada yang cocok persis, ambil kandidat durasi pertama
                    if not best_match:
                        best_match = duration_matches[0]
                
                # --- TAHAP 3: Fallback Ultimate (Jika durasi dari API atau Spotify ngaco/berbeda jauh) ---
                if not best_match:
                    for track in res:
                        if track.get('syncedLyrics'):
                            tr_name = track.get('trackName', '').lower()
                            ar_name = track.get('artistName', '').lower()
                            if tr_name and ar_name and (t_low in tr_name or tr_name in t_low) and (a_low in ar_name or ar_name in a_low):
                                best_match = track
                                break
                            
                if best_match:
                    parsed = []
                    for line in best_match['syncedLyrics'].split('\n'):
                        if line.startswith('[') and ']' in line:
                            t_str = line[1:line.find(']')]
                            txt = line[line.find(']')+1:].strip()
                            if not txt: continue
                            try:
                                m, s = t_str.split(':')
                                parsed.append((int(m) * 60 + float(s), txt))
                            except Exception as e:
                                pass # abaikan format timestamp yg rusak
                    if parsed:
                        save_cached_lyrics(title, artist, actual_duration, parsed)
                    return parsed
        except Exception as e:
            logging.error("Failed to fetch smart lyrics", exc_info=e)
        return []

    def poll_song(self):
        async def main_loop():
            sessions = await MediaManager.request_async()
            
            while True:
                try:
                    current = sessions.get_current_session()
                    if current:
                        info = await current.try_get_media_properties_async()
                        timeline = current.get_timeline_properties()
                        playback = current.get_playback_info()
                        
                        title, artist = info.title, info.artist
                        if title and artist:
                            song_id = f"🎵 {title} • {artist}"
                            
                            if timeline:
                                duration = timeline.end_time.total_seconds() if hasattr(timeline.end_time, 'total_seconds') else (int(timeline.end_time) / 10000000.0)
                                pos = timeline.position.total_seconds() if hasattr(timeline.position, 'total_seconds') else (int(timeline.position) / 10000000.0)
                                self.is_playing = (playback and getattr(playback.playback_status, 'value', playback.playback_status) == 4)
                                
                                if hasattr(timeline, 'last_updated_time'):
                                    diff = (datetime.now(timezone.utc) - timeline.last_updated_time).total_seconds()
                                    if self.is_playing:
                                        pos += diff
                                    
                                self.base_pos = pos
                                self.base_time = time.time()
                            
                            if song_id != self.current_song:
                                self.current_song = song_id
                                self.root.after(0, lambda sid=song_id: self.lbl_title.config(text=sid if self.show_title else ""))
                                self.root.after(0, self.update_ui, "Loading lyrics... ⏳", "")
                                
                                async def fetch_and_apply(sid, t, a, d):
                                    await asyncio.sleep(0.5)
                                    if self.current_song != sid:
                                        return
                                    loop = asyncio.get_event_loop()
                                    lyrics = await loop.run_in_executor(None, self.fetch_smart_lyrics, t, a, d)
                                    if self.current_song == sid:
                                        self.synced_lyrics = lyrics
                                        if not lyrics:
                                            self.root.after(0, self.update_ui, f"🎵 {t}", "")
                                            
                                asyncio.create_task(fetch_and_apply(song_id, title, artist, duration))
                    else:
                        if self.current_song:
                            self.current_song = ""
                            self.synced_lyrics = []
                            self.root.after(0, self.update_ui, "No song playing.", "")
                        
                except Exception as e:
                    logging.error("Error in poll_song loop", exc_info=e)
                
                await asyncio.sleep(0.2)
                
        asyncio.run(main_loop())

    def check_updates(self):
        def _check():
            try:
                resp = requests.get('https://pypi.org/pypi/spolyrics/json', timeout=5).json()
                latest = resp['info']['version']
                if latest != CURRENT_VERSION:
                    self.root.after(0, self.show_update_prompt, latest)
            except Exception as e:
                logging.error("Failed to check for updates", exc_info=e)
        threading.Thread(target=_check, daemon=True).start()
        
    def prompt_update(self):
        if self.update_available:
            self.show_update_prompt(self.update_available)
            
    def show_update_prompt(self, latest):
        self.update_available = latest
        if getattr(self, 'tray_icon', None):
            self.tray_icon.menu = self.get_tray_menu()
            
        res = messagebox.askyesno("Update Available", f"A new version of SpoLyrics (v{latest}) is available!\n\nYou are currently on v{CURRENT_VERSION}.\nWould you like to update now?")
        if res:
            import tempfile
            bat_path = os.path.join(tempfile.gettempdir(), "update_spolyrics.bat")
            exe_path = get_exe_path()
            
            # Extract arguments if get_exe_path returns pythonw.exe + main.py
            exe_cmd = f'"{exe_path}"'
            if isinstance(exe_path, tuple):
                exe_cmd = f'"{exe_path[0]}" "{exe_path[1]}"'
                
            with open(bat_path, 'w') as f:
                f.write('@echo off\n')
                f.write('echo Updating SpoLyrics...\n')
                f.write('ping 127.0.0.1 -n 3 > nul\n')
                f.write('taskkill /f /im spolyrics.exe > nul 2>&1\n')
                import sys
                f.write(f'"{sys.executable}" -m pip install --upgrade --no-cache-dir spolyrics\n')
                f.write(f'start "" {exe_cmd}\n')
                f.write('del "%~f0"\n')
            
            # Run bat silently without creating a window
            import subprocess
            subprocess.Popen(['cmd.exe', '/c', bat_path], creationflags=0x08000000)
            if getattr(self, 'tray_icon', None):
                self.tray_icon.stop()
            self.root.quit()
            import sys
            sys.exit(0)

def create_shortcut():
    path_changed = False
    try:
        shortcut_path = os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs", "SpoLyrics.lnk")
        app_dir = os.path.join(os.environ.get("APPDATA", ""), "SpoLyrics")
        icon_path = os.path.join(app_dir, 'icon.ico')
        
        needs_update = False
        if not os.path.exists(icon_path):
            os.makedirs(app_dir, exist_ok=True)
            import base64
            with open(icon_path, "wb") as f:
                f.write(base64.b64decode(ICON_B64))
            needs_update = True
            
        if not os.path.exists(shortcut_path):
            needs_update = True
            
        exe_path = get_exe_path()
        path_file = os.path.join(app_dir, 'current_exe_path.txt')
        saved_path = ""
        if os.path.exists(path_file):
            with open(path_file, 'r') as f:
                saved_path = f.read().strip()
                
        if saved_path != str(exe_path):
            needs_update = True
            path_changed = True
            with open(path_file, 'w') as f:
                f.write(str(exe_path))
            
        if needs_update:
            if exe_path:
                if isinstance(exe_path, tuple):
                    target, args = exe_path
                    ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{target}';$s.Arguments='\"{args}\"';$s.IconLocation='{icon_path}';$s.Save()"
                else:
                    ps_script = f"$s=(New-Object -COM WScript.Shell).CreateShortcut('{shortcut_path}');$s.TargetPath='{exe_path}';$s.IconLocation='{icon_path}';$s.Save()"
                subprocess.run(["powershell", "-Command", ps_script], creationflags=0x08000000)
    except Exception as e:
        logging.error("Failed to create shortcut", exc_info=e)
    return path_changed

def setup_tray(app):
    try:
        import pystray
        from PIL import Image
        
        def on_quit(icon, item):
            app.root.after(0, app.root.quit)
            
        def on_settings(icon, item):
            app.root.after(0, app.open_settings)
            
        def on_toggle_lyrics(icon, item):
            app.root.after(0, app.toggle_visibility)
            
        def on_info(icon, item):
            app.root.after(0, app.open_info)
    
        app_dir = os.path.join(os.environ.get("APPDATA", ""), "SpoLyrics")
        icon_path = os.path.join(app_dir, 'icon.ico')
        
        try:
            image = Image.open(icon_path)
        except Exception as e:
            logging.error("Failed to open tray icon image, using fallback", exc_info=e)
            image = Image.new('RGB', (64, 64), color = (29, 185, 84))
            
        app.tray_callbacks = {
            'on_quit': on_quit,
            'on_settings': on_settings,
            'on_toggle_lyrics': on_toggle_lyrics,
            'on_info': on_info
        }
        
        app_dir = os.path.join(os.environ.get("APPDATA", ""), "SpoLyrics")
        icon_path = os.path.join(app_dir, 'icon.ico')
        
        try:
            image = Image.open(icon_path)
        except Exception as e:
            logging.error("Failed to open tray icon image, using fallback", exc_info=e)
            image = Image.new('RGB', (64, 64), color = (29, 185, 84))
            
        icon = pystray.Icon("SpoLyrics", image, "SpoLyrics", menu=app.get_tray_menu())
        app.tray_icon = icon
        threading.Thread(target=icon.run, daemon=True).start()
    except Exception as e:
        logging.error("Tray icon failed to load", exc_info=e)

def check_single_instance():
    mutex_name = "Global\\SpoLyrics_Mutex"
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)
    last_error = ctypes.windll.kernel32.GetLastError()
    
    if last_error == 183:
        from tkinter import messagebox
        import sys
        temp_root = tk.Tk()
        temp_root.withdraw()
        temp_root.attributes('-topmost', True)
        res = messagebox.askyesno("Already Running", "SpoLyrics is already running in the background.\n\nAre you sure you want to open another instance?", parent=temp_root)
        temp_root.destroy()
        if not res:
            sys.exit(0)
    return mutex

def start_app():
    global _app_mutex
    _app_mutex = check_single_instance()
    
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception as e:
        logging.error("Failed to set DPI awareness", exc_info=e)
        logging.error("Failed to set DPI awareness", exc_info=e)
        
    path_changed = create_shortcut()
    config = load_config()
    set_auto_start(config['auto_start'], force_update=path_changed)
    
    app = MiniLyrics(config)
    setup_tray(app)
    app.root.mainloop()

if __name__ == '__main__':
    start_app()
