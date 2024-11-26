from pygame import _sdl2 as devicer, mixer

def get_audio_devices() -> dict:
    """ Get input and output audio devices """
    mixer.init()

    inputs = devicer.audio.get_audio_device_names(True)
    outputs = devicer.audio.get_audio_device_names(False)

    mixer.quit()

    return {"inputs": inputs, "outputs": outputs}
