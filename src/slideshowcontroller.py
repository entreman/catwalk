from collections import deque
import queue
import threading


class SlideshowController:
    def __init__(self, delay):
        self.delay = delay
        self.paused = False
        self.maxlength = 20
        self.current_index = -1
        self.downloaded_queue = queue.Queue(maxsize=self.maxlength)
        self.history = deque(maxlen=100)
        self.presentation_queue = queue.Queue(maxsize=self.maxlength)


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
        print("next_image")
        self.current_index +=1
        if len(self.history) < self.current_index + 1:
            if not self.fetch_next_image_from_downloaded_queue():
                self.current_index -= 1      
        image = self.history[self.current_index]
        print(f"Current Image: {self.current_index+1}/{len(self.history)} [Downloaded: {self.downloaded_queue.qsize()}]")
        self.present_image(image)

    def previous_image(self):
        print("previous_image")
        if self.current_index > 0:
            self.current_index -= 1
        print(f"Current Image: {self.current_index+1}/{len(self.history)} [Downloaded: {self.downloaded_queue.qsize()}]")
        image = self.history[self.current_index]
        self.present_image(image)


    def fetch_next_image_from_downloaded_queue(self):
        try:
            image = self.downloaded_queue.get_nowait()
            self.history.append(image)
            return True

        except queue.Empty:
            return False

        print(f"History Size: {len(self.history)}")


    def get_current_image(self):
        image = self.presentation_queue.get_nowait()
        print(f"presentation_queue: {self.presentation_queue.qsize()}")
        return image        
    
    def present_image(self, image):
        # wait until there is room
        self.presentation_queue.put_nowait(image)
        print(f"presentation_queue: {self.presentation_queue.qsize()}")



if __name__ == "__main__":
    delay = 3
    state = SlideshowController(delay)