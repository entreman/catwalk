import requests
from PIL import Image, ImageTk
from io import BytesIO
import tkinter as tk
# shared state
image_queue = []

response = requests.get(URL, timeout=10)
image = Image.open(BytesIO(response.content))

image_queue.append(image)

def show_image():
    if image_queue:
        image = image_queue.pop(0)

        image.thumbnail((screen_width, screen_height))

        photo = ImageTk.PhotoImage(image)

        label.configure(image=photo)
        label.image = photo

    root.after(100, show_image)


# GUI
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(background="black")
root.config(cursor="none")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

label = tk.Label(root, background="black")
label.pack(expand=True)

show_image()

root.mainloop()