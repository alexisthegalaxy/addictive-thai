from nltk import CFG, ChartParser
from nltk.parse.generate import generate

grammar = CFG.fromstring("""S -> AFFIRMATION | AFFIRMATION FINALPART | AFFIRMATION QUESTIONPART FINALPART
AFFIRMATION -> NOUNPHRASE TVG NOUNPHRASE | NOUNPHRASE IVG
IVG -> IV | IV ADVG | NEG IVG
TVG -> TV | TV ADVG | NEG TV
ADVG -> ADV | ADV than NOUNPHRASE
NOUNPHRASE -> PRONOUN | NOUN ADJ | NOUNPHRASE OF NOUNPHRASE | NOUN
PRONOUN -> 'พวก-เขา' | 'เขา' | 'เธอ' | 'ผม' | 'ฉัน' | 'พวก-เรา' | 'นี้' | 'นั่น' | 'โน่น' |  'ตัว-เอง' | 'ทุ' | 'พว' 
NOUN -> 'ฝัน' | 'ข้าว' | 'บ้าน' | NOUN NOUN
OF -> 'ของ'
IV -> 'ฝัน' | 'กิน' | 'วิ่ง'
ADJ -> 'เร็ว'
ADV -> 'เร็ว'
TV -> 'ฝัน' 'เกี่ยว-กับ' | 'กิน'""")
parser = ChartParser(grammar)


def is_grammatical(sentence):
    trees = parser.parse(sentence)
    for tree in trees:
        if tree._label == 'S':
            return True
    return False


for sentence in generate(grammar, n=100, depth=6):
    print(' '.join(sentence))


# a = is_grammatical(['บ้าน', 'บ้าน', 'เร็ว', 'กิน'])
# b = is_grammatical(['วิ่ง', 'ข้าว', 'ข้าว', 'เร็ว'])
# c = is_grammatical(['กิน', 'บ้าน', 'บ้าน', 'เร็ว'])
d = is_grammatical(['พวก-เขา', 'ฝัน', 'เกี่ยว-กับ', 'ฝัน', 'ข้าว', 'เร็ว'])

e = """
'(S
  (AFFIRMATION
    (NOUNPHRASE (PRONOUN พวก-เขา))
    (TVG (TV ฝัน เกี่ยว-กับ))
    (NOUNPHRASE (NOUN (NOUN ฝัน) (NOUN ข้าว)) (ADJ เร็ว))))'
"""
print(d)
#
#
#
# a = grammar.is_lexical('บ้าน บ้าน เร็ว กิน')
#
#
#
#
# class Tree(object):
#     def __init__(self):
#         self.root = 'token'
#         self.children = []
#
#
# grammar_rules = """S -> AFFIRMATION | AFFIRMATION FINALPART | AFFIRMATION QUESTIONPART FINALPART
# AFFIRMATION -> NOUNPHRASE TVG NOUNPHRASE | NOUNPHRASE IVG
# IVG -> IV | IV ADVG | NEG IVG
# TVG -> TV | TV ADVG | NEG TV
# ADVG -> ADV | ADV than NOUNPHRASE
# NOUNPHRASE -> PRONOUN | NOUN ADJ | NOUNPHRASE OF NOUNPHRASE | NOUN
# PRONOUN -> พวก-เขา | เขา | เธอ | ผม | ฉัน
# NOUN -> ฝัน | ข้าว | บ้าน | NOUN NOUN
# OF -> ของ
# IV -> ฝัน | กิน
# ADJ -> เร็ว
# ADV -> เร็ว
# TV -> ฝัน เกี่ยว-กับ | กิน"""
#
# grammar_dict = turn_grammar_rules_to_dict(grammar_rules)
# # print(grammar_dict)
#
#
# s = ["เขา", "กิน", "ฝัน"]
