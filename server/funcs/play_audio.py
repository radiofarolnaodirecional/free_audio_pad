from pygame import mixer
import threading
import time

class AudioPlayer:
    def __init__(self) -> None:
        self.is_initialized = False
        self.current_thread = None
        self.is_playing = False

    def initialize_mixer(self, device_name: str) -> None:
        if mixer.get_init():
            mixer.quit
        mixer.init(devicename = device_name)
        self.is_initialized = True

    def load_audio(self, file_path: str) -> None:
        if not self.is_initialized:
            raise Exception("Mixer not initialized")
        mixer.music.load(file_path)

    def play(self) -> None:
        mixer.music.play()

    def play_in_thread(self) -> None:
        
        
        if self.is_playing == True:
            print('playing')
            return

        self.is_playing = True

        # audio already playing
        if self.current_thread and self.current_thread.is_alive():
            raise Exception("Audio already playing")

        def run():
            self.play()
            while mixer.music.get_busy():
                time.sleep(0.1)
            self.is_playing = False
            mixer.quit()

        self.current_thread = threading.Thread(target=run)
        self.current_thread.start()

    def set_volume(self, volume: float) -> None:
        """ Volume 0.0 to 1.0 """
        if 0.0 <= volume <= 1.0:
            mixer.music.set_volume(volume)

    def quit(self):
        mixer.quit()
        self.is_initialized = False

