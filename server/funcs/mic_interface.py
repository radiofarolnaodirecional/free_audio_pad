import pyaudio
import threading

class MicInterface:
    def __init__(self) -> None:
        self.CHUNK = 1024  # Tamanho do buffer
        self.FORMAT = pyaudio.paInt16  # Formato de áudio (16 bits por amostra)
        self.CHANNELS = 1  # Mono
        self.RATE = 44100  # Taxa de amostragem (44.1 kHz)
        
        self.output_device_index = None
        self.is_playing = False
        self.audio_thread = None

        self.pa = pyaudio.PyAudio()

    def set_device(self, device: str) -> str:
        if device == 'CABLE Input (VB-Audio Virtual Cable)':
            device = 'CABLE Input (VB-Audio Virtual C'
        try:
            for i in range(self.pa.get_device_count()):
                device_info = self.pa.get_device_info_by_index(i)
                if device_info['name'] == device:
                    #print(f"ID {i}: {device_info['name']}")
                    self.output_device_index = i
        except Exception as e:
            return f'{e}'

        return 'ok'

    def start_audio_stream(self) -> str:

        if self.is_playing:
            print('already streaming')
            return 'already playing'

        if self.output_device_index == None:
            return 'device not configured'

        self.is_playing = True

        def play_thread() -> None:
            stream = self.pa.open(format=self.FORMAT,
                    channels=self.CHANNELS,
                    rate=self.RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=self.CHUNK,
                    output_device_index=self.output_device_index)
            
            try:
                while self.is_playing:
                    # Lê dados do microfone
                    data = stream.read(self.CHUNK)
                    # Reproduz os dados lidos
                    stream.write(data)

            except Exception as e:
                return f'{e}'
            finally:
                self.is_playing = False
            
            stream.stop_stream()
            stream.close()

        self.audio_thread = threading.Thread(target=play_thread)
        self.audio_thread.start()

        return 'playing'

    def stop_audio_streaming(self) -> None:
        self.is_playing = False
        if self.audio_thread:
            self.audio_thread.join()

    def __del__(self) -> None:
        if self.pa:
            self.pa.terminate()

'''
mi = MicInterface()
mi.set_device('CABLE Input (VB-Audio Virtual Cable)')
mi.start_audio_stream()
time.sleep(5)
mi.stop_audio_streaming()
'''
