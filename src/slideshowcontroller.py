from collections import deque
import queue
import threading


class SlideshowController:
    def __init__(self, delay):
        self.delay = delay
        self.paused = False
        self.maxlength = 20
        self.current_index = 0
        self.image_queue = queue.Queue(maxsize=self.maxlength)
        self.history = deque(maxlen=self.maxlength)


    def increase_delay(self):
        self.delay += 1
        print(f"Increase delay to: {self.delay}")

    def decrease_delay(self):
        if self.delay > 1:
            self.delay = self.delay - 1
        else:
            self.delay = max(0.1, self.delay - 0.1)
        print(f"Decrease delay to: {self.delay}")

    def toggle_pause(self):
        self.paused = not self.paused
        print(f"Toggle pause: Currently paused: {self.paused}")

        if not self.paused:
            pass
            #self.next_image()
        
    def next_image(self):
        self.current_index +=1
        print(f"current_index: {self.current_index}")

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1

    def get_current_image(self):
        print("get_current_image")
        if len(self.history) < self.current_index + 1:
            self.fetch_next_image_from_queue()           
        image = self.history[self.current_index]
        self.next_image()
        return image
    
    def fetch_next_image_from_queue(self):
        image = self.image_queue.get()
        self.history.append(image)
        print(f"History Size: {len(self.history)}")



if __name__ == "__main__":
    delay = 3
    state = SlideshowController(delay)