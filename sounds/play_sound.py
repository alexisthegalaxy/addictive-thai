import pygame
import os

from sounds.thai.sound_processing import transform_english_into_track_name


def play_thai_word(english: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = f"{dir_path}/thai/{english}.mp3"
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(0)
    except pygame.error:
        print(f"Error: This sound could not be played:\n{path}")


def play_transformed_thai_word(english: str):
    track_name = transform_english_into_track_name(english)
    try:
        play_thai_word(track_name)
    except pygame.error:
        print(f'no audio file for {english}')
