from direction import Direction
from lexicon.items import Letter
from mechanics.naming import Naming
from models import set_event
from npc.import_npcs.service import add_wild_letter, add_npc
from npc.npc import Npc
from weather.weather import Weather


def garbage(al):
    add_npc(
        Npc(
            al=al,
            name="garbage_0",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=34,
            y=16,
            sprite="garbage_0",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_1",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=30,
            y=10,
            sprite="garbage_1",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_2",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=37,
            y=12,
            sprite="garbage_2",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )

    add_npc(
        Npc(
            al=al,
            name="garbage_3",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=22,
            y=12,
            sprite="garbage_3",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_4",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=26,
            y=12,
            sprite="garbage_0",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_5",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=25,
            y=12,
            sprite="garbage_1",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_6",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=19,
            y=15,
            sprite="garbage_2",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_7",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=18,
            y=21,
            sprite="garbage_3",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_8",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=26,
            y=22,
            sprite="garbage_0",
            standard_dialog=["[Name] picks up the garbage."],
        )
    )


def wild_letters(al):
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("บ"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=35,
            y=13,
            standard_dialog=["Nim: oh, you see these letters?",
                             "It's บ the b, and it's big brother ป the bp!", "Let's get them!"],
            defeat_dialog=[
                "Nim: Nice!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ป"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=36,
            y=13,
            standard_dialog=[
                "Nim: Let's get this one too!",
            ],
            defeat_dialog=[
                "Nim: What is that garbage doing here? How dirty!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ะ"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=31,
            y=15,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ค"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=28,
            y=17,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("จ"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=19,
            y=20,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ื"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=24,
            y=22,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("พ"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=20,
            y=14,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("แ-"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=25,
            y=15,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ห"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=26,
            y=19,
            standard_dialog=[
                "Nim: This one will be easy to learn, you know it already!",
                "This is the same as -ั (the short a),",
                "but this is the shape it takes when it's at the end of a syllable.",
                "So, dtap is ตับ, but dta is ตะ.",
                "You get it?",
            ],
            defeat_dialog=[
                "Nim: Great, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ไ-"),
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            x=12,
            y=12,
            standard_dialog=[
                "Nim: These two vowels are very similar: ไ and ใ.",
                "Both are pronounced ai, like in \"I\" or \"eye\",",
                "and both are to be placed before the consonant, like แ- and เ-.",
                "In the past, in Sukhotai period, they used to be different,",
                "but now they're exactly the same.",
                "When we talk about them, to distinguish, we call them maimalai and maimuan.",
            ],
            defeat_dialog=[
                "Nim: Well done!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ใ-"),
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            x=13,
            y=12,
            standard_dialog=[
                "Nim: ใ is interesting because it appears in only twenty words!",
                "But because these words are all quite common,",
                "ใ is actually more frequent than ไ!",
            ],
            defeat_dialog=[
                "Nim: There's a poem that contains all the twenty ใ- words.",
                "If you're interested, we can learn it later!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("โ-"),
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            x=18,
            y=12,
            standard_dialog=[
                "Nim: Here's โ, the cousin of ใ- and ไ-.",
                "Like them, it is placed before the consonant,",
                "and like them, it is taller than the rest of the letters.",
                "However, it's pronounced ōh.",
                "Your mouth when you pronounce โ (ōh) is more closed than with the อ (ō).",
                "Also, notice how โ- looks like a tall ร.",
            ],
            defeat_dialog=[
                "Nim: To remember it, I think of the sound roh: โร,",
                "and I picture โ next to ร.",
            ],
        )
    )


def spirit_gecko(al):
    naming = Naming(
        al,
        # name="ลมสวย",
        name="ล",
        image="spirit_gecko",
        distractors=["น", "า", "ร", "-ั", "ก", "เ-", "อ", "-ี", "ง", "ท", "-ิ", "ต"],
        prompt="Spell the spirit's True Name!",
        # victory_callback=spirit_bird_victory_callback,
    )
    add_npc(
        Npc(
            sprite="spirit_gecko",
            x=23,
            y=8,
            al=al,
            name="spirit_gecko",
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            standard_dialog=["Wahaaan!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons a quake and hurts [Name]!",
            ],
            naming=naming,
        )
    )
    add_npc(
        Npc(
            sprite="",
            x=24,
            y=8,
            al=al,
            name="spirit_gecko",
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            standard_dialog=["Wahaaan!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons a quake and hurts [Name]!",
            ],
            naming=naming,
        )
    )
    add_npc(
        Npc(
            sprite="",
            x=23,
            y=9,
            al=al,
            name="spirit_gecko",
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            standard_dialog=["Wahaaan!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons a quake and hurts [Name]!",
            ],
            naming=naming,
        )
    )
    add_npc(
        Npc(
            sprite="",
            x=24,
            y=9,
            al=al,
            name="spirit_gecko",
            ma=al.mas.get_map_from_name("ko_mak_cave"),
            standard_dialog=["Wahaaan!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons a quake and hurts [Name]!",
            ],
            naming=naming,
        )
    )


def old_people_and_fisherman(al):
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=52,
            y=34,
            sprite="old_man",
            direction=Direction.DOWN,
            standard_dialog=[
                "Old man: Hello there. What are you doing outside in such a wicked storm?",
                "Nim: Our plane crashed south of the island. People need some help over there.",
                "Old man: What? This must be the island spirit again..."
                "Come inside the house, while I'll be calling in for rescue!",
                "My wife will tell you what to do.",
                "Also, if you want to take a rest and restore your health, talk to her!"
            ],
            standard_dialog_2=[
                "Alright, a rescue team should be coming soon!",
                "Now, we should ease the spirit to make it easier for them.",
                "Also, if you want to take a rest and restore your health, talk to my wife!"
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut_house_1"),
            x=3,
            y=8,
            name="nurse",
            sprite="old_woman",
            standard_dialog=[
                "Old woman: Hello?",
                "[Nim explains]",
                "Old woman: What? Then we can help!",
                "It's all the doing of the spirit of the island -",
                "a big bird made of light, you might have seen it already.",
                "It's been furious lately, and this storm is also his doing.",
                "We can make it stop, though.",
                "You'd need to do a Naming ceremony - that is, bind it using it's true name.",
                "It's called ลมสวย.",
                'ลมสวย is pronounced "lom suay".',
                "ลม is pronounced lom because if there is no vowel in between consonants,",
                'we use an inherent short "o" sound.',
                "Alright, good luck now! That mountain is too high for me to accompany you.",
            ],
            standard_dialog_2=[
                "The spirit is called ลมสวย.",
                'ลมสวย is pronounced "lom suay".',
                "ลม is pronounced lom because if there is no vowel in between consonants,",
                'we use an inherent short "o" sound.',
                "Alright, good luck now! That mountain is too high for me to accompany you.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=51,
            y=28,
            name="fisherman",
            sprite="fisherman",
            direction=Direction.RIGHT,
            standard_dialog=[
                "Hello there.",
                "Oh you want to go to Ko Chang?",
                "Well, I can certainly help you.",
                "I was just about to go back home, you can hop in if you want!",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=48,
            y=26,
            name="small_fishing_boat",
            sprite="small_fishing_boat",
            direction=Direction.DOWN,
            standard_dialog=[
                "[Name] and Nim enter the boat.",
            ],
            end_dialog_trigger_event=["enter_boat_in_ko_kut"],
        )
    )


def ko_mak(al):
    garbage(al)
    wild_letters(al)
    spirit_gecko(al)
    # old_people_and_fisherman(al)
