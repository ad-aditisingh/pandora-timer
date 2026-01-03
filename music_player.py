import pygame
import os
from resource import resource_path   # ✅ ADD
# ---------------- LAZY AUDIO INIT ----------------

_mixer_ready = False

def init_audio():
    global _mixer_ready
    if not _mixer_ready:
        print("Initializing pygame mixer")
        pygame.mixer.init()
        _mixer_ready = True


# ---------------- MUSIC FUNCTIONS ----------------

def play_random_music(file_path):
    init_audio()

    file_path = resource_path(file_path)   # ✅ FIX

    if not os.path.exists(file_path):
        print("Music file not found:", file_path)
        return

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)
    print("Playing:", file_path)


def stop_music():
    if _mixer_ready:
        pygame.mixer.music.pause()


def resume_music():
    if _mixer_ready:
        pygame.mixer.music.unpause()


def play_alarm(alarm_path):
    init_audio()
    alarm_path = resource_path(alarm_path)   # ✅ FIX
    pygame.mixer.music.load(alarm_path)
    pygame.mixer.music.play()
