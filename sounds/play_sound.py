import pygame
import os

from sounds.thai.sound_processing import transform_english_into_track_name


def play_thai_word(thai_word: str):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = f"{dir_path}/thai/{thai_word}.mp3"
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(0)
    except pygame.error:
        print(f"Error: This sound could not be played:\n{path}")


def play_transformed_thai_word(thai_word: str):
    track_name = transform_english_into_track_name(thai_word)
    try:
        play_thai_word(track_name)
    except pygame.error:
        print(f'no audio file for {thai_word}')
