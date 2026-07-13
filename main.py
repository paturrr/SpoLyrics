import tkinter as tk
import requests
import time
import threading
import asyncio
import os
import ctypes
from datetime import datetime, timezone
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager as MediaManager

class MiniLyrics:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True) 
        self.root.attributes('-topmost', True) 
        self.root.attributes('-alpha', 0.85) 
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
            
        self.root.geometry("350x120+100+100")
        self.root.configure(bg='#191414') 
        
        self.root.update_idletasks()
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 33, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int))
        except: pass
        
        self.font_cur = 11
        self.font_nxt = 9
        self.is_pinned = False
        
        self.lbl_current = tk.Label(self.root, text="Menunggu lagu...", fg='#1DB954', bg='#191414', font=('Arial', self.font_cur, 'bold'), wraplength=330, justify="center")
        self.lbl_current.pack(expand=True, fill='both', padx=10, pady=(15, 2))
        
        self.lbl_next = tk.Label(self.root, text="", fg='#b3b3b3', bg='#191414', font=('Arial', self.font_nxt), wraplength=330, justify="center")
        self.lbl_next.pack(expand=True, fill='both', padx=10, pady=(0, 15))

        self.grip = tk.Label(self.root, text="⇲", fg='#333333', bg='#191414', cursor="size_nw_se")
        self.grip.place(relx=1.0, rely=1.0, anchor="se")
        
        self.grip.bind("<B1-Motion>", self.on_resize)
        self.root.bind("<B1-Motion>", self.drag)
        self.root.bind("<Button-1>", self.click)
        self.root.bind("<Double-1>", lambda e: not self.is_pinned and self.root.destroy()) 
        self.root.bind("<Button-3>", lambda e: self.media_control('play_pause'))
        self.root.bind("<MouseWheel>", self.on_scroll)
        self.root.bind("<Control-MouseWheel>", self.on_font_scroll)
        self.root.bind("<Button-2>", self.toggle_pin)
        
        for lbl in (self.lbl_current, self.lbl_next, self.grip):
            lbl.bind("<B1-Motion>", self.drag)
            lbl.bind("<Button-1>", self.click)
            lbl.bind("<Double-1>", lambda e: not self.is_pinned and self.root.destroy())
            lbl.bind("<Button-3>", lambda e: self.media_control('play_pause'))
            lbl.bind("<MouseWheel>", self.on_scroll)
            lbl.bind("<Control-MouseWheel>", self.on_font_scroll)
            lbl.bind("<Button-2>", self.toggle_pin)

        self.current_song = ""
        threading.Thread(target=self.poll_song, daemon=True).start()

    def click(self, event):
        self.x, self.y = event.x, event.y
        return "break"

    def toggle_pin(self, event):
        self.is_pinned = not self.is_pinned
        if self.is_pinned:
            self.grip.config(text="🔒", fg='#1DB954', cursor="arrow")
        else:
            self.grip.config(text="⇲", fg='#333333', cursor="size_nw_se")
        return "break"

    def drag(self, event):
        if self.is_pinned or event.widget == self.grip: return "break"
        self.root.geometry(f"+{self.root.winfo_pointerx() - self.x}+{self.root.winfo_pointery() - self.y}")
        return "break"

    def on_resize(self, event):
        if self.is_pinned: return "break"
        new_w = max(200, self.root.winfo_pointerx() - self.root.winfo_rootx())
        new_h = max(80, self.root.winfo_pointery() - self.root.winfo_rooty())
        self.root.geometry(f"{new_w}x{new_h}")
        self.lbl_current.config(wraplength=new_w - 20)
        self.lbl_next.config(wraplength=new_w - 20)
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
        if event.delta > 0: self.media_control('prev')
        else: self.media_control('next')
        return "break"
        
    def update_ui(self, cur, nxt):
        self.lbl_current.config(text=cur)
        self.lbl_next.config(text=nxt)

    def media_control(self, action):
        if self.is_pinned: return "break"
        async def do_action():
            sessions = await MediaManager.request_async()
            current = sessions.get_current_session()
            if current:
                if action == 'play_pause':
                    info = current.get_playback_info()
                    if info and getattr(info.playback_status, 'value', info.playback_status) == 4:
                        await current.try_pause_async()
                    else:
                        await current.try_play_async()
                elif action == 'next':
                    await current.try_skip_next_async()
                elif action == 'prev':
                    await current.try_skip_previous_async()
        threading.Thread(target=lambda: asyncio.run(do_action())).start()
        return "break"

    def fetch_smart_lyrics(self, title, artist, actual_duration):
        try:
            res = requests.get('https://lrclib.net/api/search', params={'track_name': title, 'artist_name': artist}).json()
            if res and isinstance(res, list) and len(res) > 0:
                best_match = None
                
                for track in res:
                    if track.get('syncedLyrics') and track.get('duration'):
                        if abs(track['duration'] - actual_duration) <= 3:
                            best_match = track
                            break
                
                if not best_match:
                    for track in res:
                        if track.get('syncedLyrics'):
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
                            except: pass
                    return parsed
        except: pass
        return []

    def poll_song(self):
        async def main_loop():
            sessions = await MediaManager.request_async()
            synced_lyrics = []
            
            while True:
                try:
                    current = sessions.get_current_session()
                    if current:
                        info = await current.try_get_media_properties_async()
                        timeline = current.get_timeline_properties()
                        playback = current.get_playback_info()
                        
                        pos = 0
                        duration = 0
                        if timeline:
                            duration = timeline.end_time.total_seconds() if hasattr(timeline.end_time, 'total_seconds') else (int(timeline.end_time) / 10000000.0)
                            pos = timeline.position.total_seconds() if hasattr(timeline.position, 'total_seconds') else (int(timeline.position) / 10000000.0)
                            
                            if playback and getattr(playback.playback_status, 'value', playback.playback_status) == 4:
                                if hasattr(timeline, 'last_updated_time'):
                                    diff = (datetime.now(timezone.utc) - timeline.last_updated_time).total_seconds()
                                    pos += diff
                                    
                        title, artist = info.title, info.artist
                        
                        if title and artist:
                            song_id = f"{title} - {artist}"
                            
                            if song_id != self.current_song:
                                self.current_song = song_id
                                self.root.after(0, self.update_ui, f"Mencocokkan lirik pintar...\n{song_id}", "")
                                synced_lyrics = self.fetch_smart_lyrics(title, artist, duration)
                                
                            if not synced_lyrics:
                                self.root.after(0, self.update_ui, f"🎵 {title}", "")
                            else:
                                cur_text, next_text = "...", ""
                                for i, (lyric_time, txt) in enumerate(synced_lyrics):
                                    if pos >= lyric_time:
                                        cur_text = txt
                                        if i + 1 < len(synced_lyrics):
                                            next_text = synced_lyrics[i+1][1]
                                    else:
                                        break
                                self.root.after(0, self.update_ui, cur_text, next_text)
                    else:
                        self.current_song = ""
                        self.root.after(0, self.update_ui, "Tidak ada lagu diputar.", "")
                        
                except Exception:
                    pass
                
                await asyncio.sleep(0.05)
                
        asyncio.run(main_loop())

def start_app():
    app = MiniLyrics()
    app.root.mainloop()

if __name__ == '__main__':
    start_app()
