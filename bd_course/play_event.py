import pyttsx3


class PlayEvent:
    engine = None

    def __init__(self):
        self.engine = pyttsx3.init()

    def tts_emote(self, emote):
        self.engine.say(emote)
        self.engine.runAndWait()
