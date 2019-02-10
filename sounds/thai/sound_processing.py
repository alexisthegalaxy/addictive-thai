from lexicon.init import init_vocab
from os import walk


def transform_english_into_track_name(english: str):
    return english.replace("/", ":")


def print_thai_words_with_no_audio():
    all_files = []
    sound_files = []
    for (dirpath, dirnames, filenames) in walk("./"):
        all_files.extend(filenames)
    for file_name in all_files:
        if file_name[-4:] == ".mp3":
            sound_files.append(file_name[:-4])

    number_of_files_to_convert = 0
    syllables, words, sentences = init_vocab()
    for word in words.words:
        if word.english not in sound_files:
            print(f"{word.thai}           {word.english}")
            number_of_files_to_convert += 1

    if number_of_files_to_convert == 0:
        print("😁 No files to convert! 😁")
    else:
        print(f"{number_of_files_to_convert} files to convert! 😅")


if __name__ == '__main__':
    print_thai_words_with_no_audio()
