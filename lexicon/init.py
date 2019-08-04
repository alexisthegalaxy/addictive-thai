from lexicon.items import Words, Sentences
from lexicon.items_creation import add_word, add_sentence
from lexicon.tone import Tone
import os


def tone_name_to_tone(tone_text: str):
    if tone_text == "MID":
        return Tone.MID
    if tone_text == "RISING":
        return Tone.RISING
    if tone_text == "LOW":
        return Tone.LOW
    if tone_text == "HIGH":
        return Tone.HIGH
    if tone_text == "FALLING":
        return Tone.FALLING


# def init_vocab():
#     words = Words()
#     sentences = Sentences()
#
#     file = open(f"{os.path.dirname(os.path.realpath(__file__))}/files/thai", "r")
#     for line_ in file:
#         line = line_.replace("\n", "")
#         if len(line) > 0:
#             if line[0] == 'M':
#                 location = None
#                 items = line.split(" | ")
#                 thai = items[1]
#                 english = items[2]
#                 try:
#                     tone = tone_name_to_tone(items[3])
#                 except:
#                     print(f'error - can\'t convert to tone: {items}')
#                 if len(items) > 4:
#                     location = (items[4].split(' ')[0], int(items[4].split(' ')[1]), int(items[4].split(' ')[2]))
#                 # print(f'add word syllable {thai} {english} {tone}')
#                 # add_word_syllable(words, syllables, thai=thai, english=english, tone=tone, location=location)
#             if line[0] == 'W':
#                 items = line.split(" | ")
#                 thai = items[1]
#                 english = items[2]
#                 # print(f'add word {thai} {english}')
#                 # add_word(words, syllables, thai=thai, english=english)
#             if line[0] == 'S':
#                 items = line.split(" | ")
#                 thai = items[1]
#                 try:
#                     english = items[2]
#                 except:
#                     print('Error with sentence', items)
#                 # print(f'add sentence {thai} {english}')
#                 add_sentence(sentences, words, thai=thai, english=english)
#
#     return words, sentences
