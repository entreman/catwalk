#!/usr/bin/env python3

import argparse
import io
import queue
import threading
import time
import requests
import tkinter as tk

from PIL import Image, ImageTk

        
URL = "https://cataas.com/cat"


def downloader(stop_event, image_queue, delay):
    while not stop_event.is_set():
        try:
            response = requests.get(URL, timeout=10)
            response.raise_for_status()

            image = Image.open(io.BytesIO(response.content))

            # wait until there is room
            image_queue.put(image, timeout=1)

        except queue.Full:
            pass

        except Exception as e:
            print("Download error:", e)

        stop_event.wait(delay)


def update_image():
    try:
        image = image_queue.get_nowait()

        image.thumbnail((screen_width, screen_height))

        photo = ImageTk.PhotoImage(image)

        label.configure(image=photo)
        label.image = photo

    except queue.Empty:
        pass

    root.after(100, update_image)


def shutdown(event=None):
    stop_event.set()
    root.destroy()


parser = argparse.ArgumentParser()
parser.add_argument(
    "delay",
    nargs="?",
    type=int,
    default=3,
    help="seconds between downloads"
)

args = parser.parse_args()


image_queue = queue.Queue(maxsize=10)
stop_event = threading.Event()


root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")
root.config(cursor="none")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label = tk.Label(root, bg="black")
label.pack(expand=True)


threading.Thread(
    target=downloader,
    args=(stop_event, image_queue, args.delay),
    daemon=True
).start()


root.bind("<Escape>", shutdown)

update_image()

root.mainloop()