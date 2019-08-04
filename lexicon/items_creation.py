from lexicon.items import Word, Sentence
from lexicon.tone import Length, Tone


def add_word(words, thai="no_thai", english="no_english", tone=Tone.UNKNOWN, length=Length.UNKNOWN, audio=""):
    words.add_word(Word(thai=thai, english=english))


def add_sentence(sentences, words, thai, english):
    sentences.add_sentence(Sentence(words, thai=thai, english=english))
