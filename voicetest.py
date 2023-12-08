import os
import pygame

voice2 = 'id-ID-GadisNeural'


def speak(data):
    voice = 'id-ID-GadisNeural'
    data = data.replace("\n", "\t"+",")
    data = data.replace("\"", "\'")
    command = f'edge-tts --voice "{voice}" --text "{data}" --write-media "data.mp3"'
    os.system(command)

    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("data.mp3")

    try:
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()


speak()
