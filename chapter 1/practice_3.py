import pygame
import os

file_path = r'C:\Users\Debanjan Das\Downloads\Phir_Mohabbat.mp3'

if os.path.exists(file_path):                         # this is the use an external module "pyagame" to play an audio
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
else:
    print(f"File not found: {file_path}")
