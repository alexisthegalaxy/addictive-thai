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

