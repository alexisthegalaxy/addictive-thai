from lexicon.dex import Dex
from lexicon.items import Words, Sentences, Syllables
from ui.ui import Ui


class All:
    def __init__(
        self,
        mas: 'Mas',
        words: 'Words',
        sentences: 'Sentences',
        syllables: 'Syllables',
        ui: 'Ui',
        cell_types: 'CellType',
        profiles: 'Profile',
    ):
        from lexicon.tests import Test

        self.mas = mas
        self.mas.al = self
        self.words = words
        self.sentences = sentences
        self.syllables = syllables
        self.ui: Ui = ui
        self.learner = None
        self.cell_types = cell_types
        self.profiles = profiles
        self.active_test: Test = None
        self.active_npc: 'Npc' = None
        self.active_learning = None
        self.active_battle = None
        self.dex: Dex = None

    def add_sentences_to_words(self):
        for sentence in self.sentences.sentences:
            for word in sentence.words:
                word.sentences.append(sentence)

    def tick_activity(self):
        if self.active_battle:
            self.active_battle.tick()
