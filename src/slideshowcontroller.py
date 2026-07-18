

class SlideshowController:
    def __init__(self, delay):
        self.delay = delay
        self.paused = False

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

if __name__ == "__main__":
    delay = 3
    state = SlideshowController(delay)