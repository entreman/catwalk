#!/usr/bin/env python3

import argparse
import io
import queue
import threading
import time
import requests
import tkinter as tk
import sys


from PIL import Image, ImageTk
from pathlib import Path


from slideshowcontroller import SlideshowController
        
URL = "https://cataas.com/cat"



parser = argparse.ArgumentParser()
parser.add_argument(
    "delay",
    nargs="?",
    type=int,
    default=3,
    help="seconds between downloads"
)
args = parser.parse_args()
controller = SlideshowController(delay=args.delay)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / relative_path
    return Path(__file__).resolve().parent.parent / relative_path


def downloader(stop_event, image_queue):
    while not stop_event.is_set():
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content))

            # wait until there is room
            image_queue.put(image, timeout=1)
            print(f"Queue Size: {image_queue.qsize()}")

        except queue.Full:
            pass

        except Exception as e:
            print("Download error:", e)



def update_image():
    if not controller.paused:
        try:
            image = controller.get_current_image()

            image.thumbnail((screen_width, screen_height))

            photo = ImageTk.PhotoImage(image)

            label.configure(image=photo)
            label.image = photo

        except queue.Empty:
            pass

    root.after(int(controller.delay * 1000), update_image)


def shutdown(event=None):
    stop_event.set()
    root.destroy()




#image_queue = queue.Queue(maxsize=10)
stop_event = threading.Event()


root = tk.Tk()
root.title("Catwalk")
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.config(cursor="none")

icon_path = "assets/catwalk.png"
icon = tk.PhotoImage(file=resource_path(icon_path))
root.iconphoto(True, icon)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label = tk.Label(root, bg="black")
label.pack(expand=True)


threading.Thread(
    target=downloader,
    args=(stop_event, controller.image_queue),
    daemon=True
).start()


root.bind("<Escape>", shutdown)
root.bind("<space>", lambda e: controller.toggle_pause())
root.bind("<Up>", lambda e: controller.decrease_delay())
root.bind("<Down>", lambda e: controller.increase_delay())
root.bind("<Left>", lambda e: controller.previous_image())
root.bind("<Right>", lambda e: controller.next_image())

update_image()

root.mainloop()