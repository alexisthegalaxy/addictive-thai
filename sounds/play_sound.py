import sqlite3
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


def print_all_words_and_letters_without_audio():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect("../thai.db")
    cursor = conn.cursor()
    thai_words = [t[0] for t in list(cursor.execute(
        f"SELECT w.thai FROM main.words w "
    ))]
    numer_of_words_with_audio = 0
    numer_of_words_without_audio = 0
    for thai_word in thai_words:
        if not os.path.exists(f"{dir_path}/thai/{thai_word}.mp3"):
            print(thai_word)
            numer_of_words_without_audio += 1
        else:
            numer_of_words_with_audio += 1
    print('numer_of_words_with_audio', numer_of_words_with_audio)
    print('numer_of_words_without_audio', numer_of_words_without_audio)


if __name__ == '__main__':
    print_all_words_and_letters_without_audio()