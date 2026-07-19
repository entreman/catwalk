import tkinter as tk
import requests
import io
import queue
import threading

from PIL import Image, ImageTk

from slideshowcontroller import SlideshowController
from helper import resource_path

class CatwalkApp:
    def __init__(self, delay=3):
        self.URL = "https://cataas.com/cat"
        self.delay = delay
        self.paused = False
        self.controller = SlideshowController(self.delay)
        
        #image_queue = queue.Queue(maxsize=10)
        self.stop_event = threading.Event()
        self.start_downloader()

        self._init_gui()
        self._init_keybinds()

        self.start_timer() # Call it only after self._init_gui()

        
    def _init_gui(self):
        self.root = tk.Tk()
        self.root.title("Catwalk")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.config(cursor="none")

        icon_path = "assets/catwalk.png"
        icon = tk.PhotoImage(file=resource_path(icon_path))
        self.root.iconphoto(True, icon)

        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        self.label = tk.Label(self.root, bg="black")
        self.label.pack(expand=True)

    def _init_keybinds(self):
        self.root.bind("<Escape>", self.shutdown)
        self.root.bind("<space>", self.on_space)
        self.root.bind("<Up>", lambda e: self.controller.decrease_delay())
        self.root.bind("<Down>", lambda e: self.controller.increase_delay())
        self.root.bind("<Left>", self.on_left)
        self.root.bind("<Right>", self.on_right)

    def on_left(self, event=None):
        self.show_previous()

    def on_right(self, event=None):
        self.show_next()

    def on_space(self, event=None):
        self.toggle_pause()
        


    def downloader(self, stop_event, image_queue, url):
        while not stop_event.is_set():
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                image = Image.open(io.BytesIO(response.content))

                # wait until there is room
                image_queue.put(image, timeout=1)
                print(f"Queue Size: {image_queue.qsize()}")

            except queue.Full:
                pass

            except Exception as e:
                print("Download error:", e)

    def start_downloader(self):
        threading.Thread(
            target=self.downloader,
            args=(self.stop_event, self.controller.downloaded_queue, self.URL),
            daemon=True
        ).start()


    def start_timer(self):
        self.timer_id = self.root.after(int(self.controller.delay * 1000), self.timer_tick)

    def timer_tick(self):
        self.show_next()

    def reset_timer(self):
        if not self.paused:
            self.stop_timer()
            self.start_timer()
    
    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def toggle_pause(self):
        self.paused = not self.paused
        print(f"Toggle pause: Currently paused: {self.paused}")

        if self.paused:
            self.stop_timer()
        else:
            self.reset_timer()  # Start timer again, after being paused. 

    def update_image(self):
        try:
            image = self.controller.get_current_image()

            image.thumbnail((self.screen_width, self.screen_height))

            photo = ImageTk.PhotoImage(image)

            self.label.configure(image=photo)
            self.label.image = photo

        except queue.Empty:
            pass
        
        self.root.after(10, self.update_image)
        #self.root.after(int(self.controller.delay * 1000), self.update_image)


    def show_previous(self):
        self.controller.previous_image()
        self.reset_timer()

    def show_next(self):
        self.controller.next_image()
        self.reset_timer()
    

    def shutdown(self, event=None):
        self.stop_event.set()
        self.root.destroy()

    def run(self):
        self.update_image()
        self.root.mainloop()


if __name__ == "__main__":
    app = CatwalkApp()
    app.run()