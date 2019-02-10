import os
from lexicon.init import init_vocab
from os import walk


def transform_english_into_track_name(english: str):
    return english.replace("/", ":")


def get_all_mp3_files():
    all_files = []
    sound_files = []
    for (dirpath, dirnames, filenames) in walk("./"):
        all_files.extend(filenames)
    for file_name in all_files:
        if file_name[-4:] == ".mp3":
            sound_files.append(file_name[:-4])
    return sound_files


def print_thai_words_with_no_audio():
    sound_files = get_all_mp3_files()
    number_of_files_to_convert = 0
    syllables, words, sentences = init_vocab()
    for word in words.words:
        if word.thai not in sound_files:
            print(f"{word.thai}           {word.english}")
            number_of_files_to_convert += 1

    if number_of_files_to_convert == 0:
        print("😁 No files to convert! 😁")
    else:
        print(f"{number_of_files_to_convert} files to convert! 😅")


def rename_files_in_english_to_thai():
    sound_files = get_all_mp3_files()
    syllables, words, sentences = init_vocab()
    for word in words.words:
        if word.english in sound_files:
            old_filename = f"{word.english}.mp3"
            new_filename = f"{word.thai}.mp3"
            path = os.path.dirname(os.path.realpath(__file__))
            os.rename(os.path.join(path, old_filename), os.path.join(path, new_filename))


if __name__ == '__main__':
    print_thai_words_with_no_audio()
    # rename_files_in_english_to_thai()
