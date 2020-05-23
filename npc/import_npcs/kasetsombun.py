from direction import Direction
from lexicon.items import Word
from npc.import_npcs.service import add_npc
from npc.npc import Npc
from npc.spell import Spell


def kasetsombun_town(al):
    add_npc(
        Npc(
            al=al,
            name="old woman in woman house teach เธอ",
            ma=al.mas.get_map_from_name("kasetsombun_house2"),
            taught=Word.get_by_split_form("เธอ"),
            x=7,
            y=8,
            sprite="old_woman",
            direction=Direction.DOWN,
            standard_dialog=[
                "I don't have much longer to live, and I'm not much now -",
                "But at least I have raised three strong women.",
                "I believe women have the power to change Thailand.",
                'As a parting gift, let me teach you how to say "she".',
            ],
            defeat_dialog=[
                'You can also use เขา, as it means "he, she, they",',
                "but เธอ is only for women.",
                "To remember it, remember that each woman was once a daughter - a daughเธอ.",
                'Note that it can be used to mean "you" as well.',
            ],
        ))
    add_npc(
        Npc(
            al=al,
            name="woman in woman house",
            ma=al.mas.get_map_from_name("kasetsombun_house2"),
            x=5,
            y=10,
            sprite="woman",
            direction=Direction.UP,
            standard_dialog=[
                "Mom was the healer in Kasetsombun.",
                "She used to communicate with spirits, knew plants, could cure most ailments.",
                "Who's gonna save us now that she's dying?",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="woman in woman house",
            ma=al.mas.get_map_from_name("kasetsombun_house2"),
            x=7,
            y=10,
            sprite="mom",
            direction=Direction.UP,
            standard_dialog=[
                "Mom taught us so much.",
                "She's very ill now, it will be our turn to teach her ancient knowledge.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="farmer",
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=21,
            y=8,
            sprite="dad",
            direction=Direction.RIGHT,
            standard_dialog=[
                "I'm seeding out the grass to make this a vegetable field.",
                "Do you know a Spell to help me out?",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="woman in woman house",
            ma=al.mas.get_map_from_name("kasetsombun_house2"),
            x=9,
            y=10,
            sprite="rich_woman",
            direction=Direction.UP,
            standard_dialog=[
                "I came back from Bangkok as soon as I heard the news.",
                "Yeah, I left Kasetsombun when I was 18 because I couldn't stand the rural life.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="old_woman",
            ma=al.mas.get_map_from_name("kasetsombun_house1"),
            x=7,
            y=7,
            sprite="old_woman",
            direction=Direction.DOWN,
            standard_dialog=["ผักของฉันอร่อย"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="lass",
            ma=al.mas.get_map_from_name("kasetsombun_house1"),
            x=5,
            y=9,
            sprite="lass",
            direction=Direction.RIGHT,
            standard_dialog=["อร่อย!"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="mom",
            taught=Word.get_by_split_form("อ-ร่อย"),
            ma=al.mas.get_map_from_name("kasetsombun_house1"),
            x=7,
            y=10,
            sprite="mom",
            direction=Direction.UP,
            standard_dialog=[
                "My mom's vegetables are delicious - she grows the best in Kasetsombun.",
                "Me? I have a restaurant down in Lomsak where I cook traditional food.",
                "I often come here so that my mom can see her grandchildren a bit.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="kid",
            ma=al.mas.get_map_from_name("kasetsombun_house1"),
            x=9,
            y=8,
            sprite="kid",
            direction=Direction.LEFT,
            standard_dialog=[
                "Mom made us some bittermelon with garlic for breakfast,",
                "with granny's vegetables."
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="kid",
            ma=al.mas.get_map_from_name("kasetsombun_temple"),
            x=16,
            y=22,
            sprite="kid",
            direction=Direction.RIGHT,
            standard_dialog=["We found a gecko!"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="gecko",
            ma=al.mas.get_map_from_name("kasetsombun_temple"),
            x=17,
            y=22,
            sprite="gecko",
            direction=Direction.UP,
            standard_dialog=["..."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="kid",
            ma=al.mas.get_map_from_name("kasetsombun_temple"),
            x=17,
            y=21,
            sprite="lass",
            direction=Direction.DOWN,
            standard_dialog=["มันเป็นตุ๊กแก!!"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=3,
            y=11,
            sprite="kid",
            direction=Direction.RIGHT,
            standard_dialog=["no dialog"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=4,
            y=11,
            sprite="gecko",
            direction=Direction.UP,
            standard_dialog=["no dialog"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=4,
            y=10,
            sprite="lass",
            direction=Direction.DOWN,
            standard_dialog=["no dialog"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="student 1",
            ma=al.mas.get_map_from_name("kasetsombun_school"),
            x=11,
            y=24,
            sprite="lass",
            direction=Direction.UP,
            standard_dialog=[
                "We're learning นี้ and นั่น in their subject form,",
                "but both also have an alternative form.",
                "Pronounced the same with a different tone:",
                "นี้ can become นี่, and นั้น can become นั่น.",
                "In that form, they can be used as objects.",
                'For example, "This eats that." is "นี้ กิน นั่น"',
                "They're pronounced the same but with a different tone.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="student 2",
            ma=al.mas.get_map_from_name("kasetsombun_school"),
            x=15,
            y=24,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "Do you know classifiers yet?",
                "Usually, you use นี้ and นั่น after a classifier.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="student 3",
            ma=al.mas.get_map_from_name("kasetsombun_school"),
            x=11,
            y=22,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "นี้ and นั่น are super useful!",
                "They appear in so many words, and can also be used on their own!",
                "For example: I like this: ผม ชอบ นี่.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="student 4",
            ma=al.mas.get_map_from_name("kasetsombun_school"),
            x=14,
            y=22,
            sprite="lass",
            direction=Direction.UP,
            standard_dialog=[
                "These are my grandparents!",
                "People take turns here to teach us.",
                "And today it's my grandparents!",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="teacher",
            ma=al.mas.get_map_from_name("kasetsombun_school"),
            taught=Word.get_by_split_form("นั่น"),
            x=12,
            y=18,
            sprite="old_woman",
            direction=Direction.DOWN,
            standard_dialog=[
                "This is นี้ (nee), that is นั่น (nan).",
                "นี้ is for what is close, นั่น for what is far away.",
            ],
            defeat_dialog=[
                "It's easy to remember, because นี้ has a 'i' sound like 'this'.",
                "And นั่น has a 'a' sound like 'that'.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="teacher",
            ma=al.mas.get_map_from_name("kasetsombun_school"),
            taught=Word.get_by_split_form("นี้"),
            x=14,
            y=18,
            sprite="old_man",
            direction=Direction.DOWN,
            standard_dialog=[
                "This is นี้ (nee), that is นั่น (nan).",
                "นี้ is for what is close, นั่น for what is far away.",
            ],
            defeat_dialog=[
                "Imagine that you have a knee (นี้), and you see a nun (นั่น) far away.",
                "Naturally, your knee is closer to you than the nun.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="the young hermit",
            fight_words=[
                Word.get_by_split_form(battle_word)
                for battle_word in ["มัน-ฝ-รั่ง", "ผัก", "ฝรั่ง", "อ-ร่อย"]
            ],
            ma=al.mas.get_map_from_name("kasetsombun_cave"),
            x=10,
            y=12,
            sprite="kid",
            direction=Direction.UP,
            money=3,
            standard_dialog=["This is my secret place!"],
            defeat_dialog=["Maybe I should brush up on my vegetables."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="old_man",
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=29,
            y=16,
            sprite="old_man",
            direction=Direction.RIGHT,
            standard_dialog=[
                "You're from Phetchabun?",
                "Then you crossed that cave to come here?",
                "Thank you! Welcome to Kasetsombun!",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="monk1",
            taught=Word.get_by_split_form("พระ"),
            ma=al.mas.get_map_from_name("kasetsombun_temple_temple"),
            x=13,
            y=18,
            sprite="monk",
            direction=Direction.UP,
            standard_dialog=["You want to learn a word?", "How about พระ?"],
            defeat_dialog=[
                'พระ is also a prefix to put before words like "king" or "god", showing respect.',
                '"King" is พระราชา, and "god" is พระเจ้า.',
                "To remember it, think that Buddha, monks, kings and gods are praised, พระised.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="dad",
            ma=al.mas.get_map_from_name("kasetsombun_house3"),
            taught=Word.get_by_split_form("ฝรั่ง"),
            x=4,
            y=10,
            sprite="dad",
            direction=Direction.RIGHT,
            standard_dialog=[
                "What is a farang like you doing in Kasetsombun?",
                "What, you don't know what farang means?",
                "It means foreigner, but also guava!",
            ],
            defeat_dialog=[
                "ฝรั่ง is easy to remember because it has the same origin as French:",
                "ฝรั่งเศส (farangset).",
                "Guavas are called farangs because they were brought to Thailand",
                "by Portuguese people, a long time ago.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="mom",
            ma=al.mas.get_map_from_name("kasetsombun_house3"),
            taught=Word.get_by_split_form("มัน"),
            x=5,
            y=10,
            sprite="mom",
            direction=Direction.LEFT,
            standard_dialog=['You want a useful word? How about the pronoun "it"?'],
            defeat_dialog=[
                "I've got an idea for you to remember it!",
                'Imagine a wife that despises her man and refers to him as "it".',
                "No, I'm not doing that, hahaha. haha.",
                "มัน also means yam or tuber.",
                "Not that I'm calling my husband that either.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="woman talking about the spirit house",
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=9,
            y=17,
            sprite="old_woman",
            direction=Direction.UP,
            standard_dialog=[
                "This, there, is a spirit house.",
                "I'm making an offering right now.",
                "I often give things like bananas, coconuts, rice, and desserts.",
                "Also, we give lots of red strawberry-flavored fanta!",
                "Naturally, sweet spirits are sweet tooths.",
                "They will flock here and repel the evil spirits.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="man teaching potato",
            ma=al.mas.get_map_from_name("kasetsombun"),
            taught=Word.get_by_split_form("มัน-ฝ-รั่ง"),
            x=25,
            y=12,
            sprite="dad",
            direction=Direction.UP,
            standard_dialog=[
                "I'm planting potatoes.",
                'Ah, actually that\'s a funny word to learn if you already know "it" and "foreigner"!',
            ],
            defeat_dialog=[
                'Yes, potatoes mean "western yams", but it sounds like "it foreigner"!'
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="woman teach vegetable",
            ma=al.mas.get_map_from_name("kasetsombun"),
            taught=Word.get_by_split_form("ผัก"),
            x=30,
            y=11,
            sprite="woman",
            direction=Direction.UP,
            standard_dialog=[
                "Yes, it's mostly farmland around Kasetsombun.",
                "Actually, 'เกษตร' (kaset) means farmland, and 'สมบูรณ์' (sombum) means perfect.",
                "I wonder if that refers to how perfect my farmland is?",
                "Those words are a bit advanced, but I can teach you the word for vegetable!",
            ],
            defeat_dialog=["To remember it, you can imagine pacman eating vegetables!"],
        )
    )

    # add_npc(
    # Vendor(
    #     al=al,
    #     name="Vendor of Kasetsombun",
    #     ma=al.mas.get_map_from_name("kasetsombun_shop"),
    #     x=8,
    #     y=10,
    #     sprite="vendor",
    #     direction=Direction.LEFT,
    #     vendor_dialog_beginning=[
    #         "สวัสดีครับ.",
    #     ],
    #     vendor_dialog_end=["See you again!"],
    #     sold_items=[
    #         Item(
    #             name="มันฝรั่ง",
    #             description="one kilogram of potatoes from Kasetsombun",
    #             price=28,
    #         ),
    #         Item(
    #             name="water",
    #             description="a plastic one-liter bottle of water",
    #             price=12,
    #         ),
    #     ],
    # ),


def kasetsombun_spell(al):
    add_npc(
        Spell(
            al=al,
            ma=al.mas.get_map_from_name("kasetsombun_temple"),
            x=33,
            y=15,
            word=Word.get_by_split_form("ผัก"),
        )
    )
    add_npc(
        Spell(
            al=al,
            ma=al.mas.get_map_from_name("kasetsombun"),
            x=20,
            y=4,
            word=Word.get_by_split_form("ผัก"),
        )
    )


def kasetsombun(al):
    kasetsombun_town(al)
    kasetsombun_spell(al)
