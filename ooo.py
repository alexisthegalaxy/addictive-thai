# from lexicon.items import Word
#
# import sqlite3
#
# conn = sqlite3.connect('thai.db')
# c = conn.cursor()
# answers = list(c.execute(f"SELECT * FROM words WHERE thai = '{'ข้าว'}'"))
# print(answers)
#
#
#
# a = "aa\nbb"
# for line in a.split('\n'):
#     print(f'_{line}_')
from fontTools.ttLib import TTFont
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
font_path = f"{dir_path}/fonts/Sarabun-Medium.ttf"
font = TTFont(font_path)


def char_in_font(unicode_char, font):
    for cmap in font['cmap'].tables:
        if cmap.isUnicode():
            if ord(unicode_char) in cmap.cmap:
                return True
    return False


print('า', char_in_font('า', font))
print('a', char_in_font('a', font))
print('ā', char_in_font('ā', font))
print('ဘ', char_in_font('ဘ', font))
print('ភ', char_in_font('ភ', font))
