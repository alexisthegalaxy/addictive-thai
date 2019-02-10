from lexicon.items import Syllable, Word, Sentence
from lexicon.tone import Length, Tone


def add_syllable(syllables, thai="no_thai", english="no_english", tone=Tone.UNKNOWN, length=Length.UNKNOWN, audio=""):
    syllable = syllables.get_syllable(thai=thai)
    if not syllable:
        syllables.add_syllable(Syllable(thai=thai, english=english, tone=tone, length=length))
    elif syllable.english == "":
        syllable.english = english


def add_word(words, syllables, thai="no_thai", english="no_english", tone=Tone.UNKNOWN, length=Length.UNKNOWN, audio="", location=None):
    words.add_word(Word(syllables, thai=thai, english=english, location=location))
    # words.add_word(Word(syllables, thai=thai, english=english, location=location))


def add_word_syllable(words, syllables, thai="no_thai", english="no_english", tone=Tone.UNKNOWN, location=None):
    """This function is used to add monosyllabic words to both words and syllables"""
    add_word(words, syllables, thai=thai, english=english, location=location)
    add_syllable(syllables, thai, english, tone)


def add_sentence(sentences, words, thai, english):
    sentences.add_sentence(Sentence(words, thai=thai, english=english))
