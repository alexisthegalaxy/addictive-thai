from direction import Direction
from lexicon.items import Letter
from mechanics.naming import Naming
from models import set_event
from npc.import_npcs.service import add_wild_letter, add_npc
from npc.npc import Npc
from weather.weather import Weather


def spirit_bird_victory_callback(al):
    for npc in al.mas.current_map.npcs:
        if npc.name == "spirit_bird":
            npc.is_walkable = True
            npc.is_silent = True
            if npc.sprite == "spirit_bird":
                npc.sprite = "spirit_bird_invisible"
    al.weather = Weather(al)
    set_event('spirit_bird_is_beaten', 1)


def people_on_the_beach(al):
    add_npc(
        Npc(
            al=al,
            name="crashed_plane",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=57,
            y=54,
            sprite="_crashed_plane",
            direction=Direction.UP,
            standard_dialog=["The plane is on fire!", "Better get some help quick."],
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=57,
            y=55,
            sprite="",
            standard_dialog=["The plane is on fire!", "Better get some help quick."],
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=58,
            y=54,
            sprite="",
            standard_dialog=["The plane is on fire!", "Better get some help quick."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=53,
            y=54,
            sprite="mom",
            direction=Direction.RIGHT,
            standard_dialog=["Thank goodness everyone is still alive!"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=57,
            y=56,
            sprite="dad",
            direction=Direction.UP,
            standard_dialog=[
                "While I'm taking out everybody that is still inside, can you get us some help?"
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=55,
            y=57,
            sprite="old_man",
            direction=Direction.UP,
            standard_dialog=[
                "My wife thinks the island spirit might be behind that.",
                "She sees spirit, so I believe her.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=56,
            y=57,
            sprite="old_woman",
            direction=Direction.UP,
            standard_dialog=[
                "This crash, and this storm...",
                "I feel dark energies being at work.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=56,
            y=51,
            sprite="kid",
            direction=Direction.LEFT,
            standard_dialog=[
                "Do we need to cross the jungle?",
                "It's scaring me, with the storm...",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=57,
            y=51,
            sprite="woman",
            direction=Direction.LEFT,
            standard_dialog=["What are we going to do?"],
        )
    )


def wild_letters(al):
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ม"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=51,
            y=55,
            standard_dialog=["Nim: oh, you see that letter? It's ม, the m!"],
            defeat_dialog=[
                "Nim: Well done [Name], that's one more letter!",
                "It looks a lot like the n: น - but in the m, the loops are on the sa>M<e side.",
                "And for the น (n) the loops are >N<ot on the same side.",
            ],
        )
    )

    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ั"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=50,
            y=53,
            standard_dialog=[
                "Nim: You see this thing, blocking our way?",
                "That is a wild letter.",
                "To have it go away, we have to learn it!",
                "This one is -ั: shorter version of the letter a า.",
            ],
            defeat_dialog=[
                "Nim: If you put it over a consonant like so: นั ,",
                "Then you get the sound na.",
                "Alright, let's carry on!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ก"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=50,
            y=49,
            standard_dialog=[
                "Nim: Another one?",
                "This one is ก, the consonant g - and it's the first letter of the Thai alphabet.",
            ],
            defeat_dialog=["Nim: Well done [Name]!"],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("เ-"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=52,
            y=45,
            standard_dialog=[
                "Nim: This is the very common vowel เ, the long ē!",
                "It's pronounced e, like in 'neck'.",
                "It's quite similar to the french é, like in café or Pokémon.",
                "It's an interesting vowel, because it comes before the consonant:",
                "For example, to write 'nay', you write เน!",
                "เ can also be combined with า and sandwich a consonant to form the ao sound!",
                "For example, เนา is read nao!",
            ],
            defeat_dialog=[
                "Nim: The vowel เ has a very similar friend, the vowel แ!",
                "You'll learn it later, but แ is pronounced ae, pronounced like in ham.",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("อ"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=54,
            y=41,
            standard_dialog=[
                "Nim: This the letter o: อ. It is both used as a vowel and a consonant.",
                "As a vowel, it's a long ō, like in 'saw'.",
                "For example, รอ is pronounced 'ro:'.",
                "But it can also be used as a consonant placeholder - and it's silent.",
                'For example, to say "uncle" in Thai, we say a:.',
                "But you cannot just write า, because each vowel in Thai needs a consonant.",
                "So you use instead the silent consonant placeholder อ.",
                'So, "uncle" is อา.',
            ],
            defeat_dialog=[
                "Nim: อ is quite easy to remember, because it looks like an o.",
                'Given that it\'s both a consonant and a vowel, "ออ" is a syllable!',
                '"ออ" is read "o:", and means "to congregate"!',
                'There\'s also this crazy word "เออออ", read "er o", meaning "to agree"!',
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ว"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=51,
            y=41,
            standard_dialog=[
                "Nim: Good find, I didn't see this one!",
                "This is the w, ว!",
                "Don't get it confused with the า (ā): ว has an extra loop.",
                "By the way, the loop indicates how to write a letter:.",
                "You have to write starting from the loop.",
            ],
            defeat_dialog=["Nim: Good job!"],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ย"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=44,
            y=48,
            standard_dialog=[
                "Nim: Here's the y!",
                "ยาย is my favorite word, it means grandmother, and it's pronounced yai!",
            ],
            defeat_dialog=[
                "Nim: I find that ย looks like a y, somehow, so it's easy to remember!"
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ล"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=49,
            y=42,
            standard_dialog=[
                "Nim: That's the consonant l!",
                "Don't get ล confused with the s: ส!",
            ],
            defeat_dialog=[
                'Nim: At the end of a word, l is pronounced "n".',
                'For example, มล is pronounced "mon", not "mol"!',
                "You can't end a word in l in Thai.",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ง"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=49,
            y=35,
            standard_dialog=[
                "Nim: That's ง, the ng consonant!",
                "Don't you think ง looks like a muscle flexing?",
                "I like to imagine somebody flexing and making the sound ng.",
                "Nim: 'ng' can come at the end of a syllable like in English,",
                "but it can also come at the beginning.",
                'For example, the word "confused" in Thai is งง: ngong!',
            ],
            defeat_dialog=["Well done [Name]!"],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ท"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=57,
            y=38,
            standard_dialog=[
                "Nim: Here's ท!",
                "It's pronounced like a t, but aspirated, so we can write it t'h.",
            ],
            defeat_dialog=[
                "Nim: the sound t doesn't exist in Thai, it's either ด d, ต dt or ท t'h.",
                'However, all three sounds become a "t" at the end of a syllable.',
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ี"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=46,
            y=39,
            standard_dialog=[
                "Nim: Here's the vowel -ี!",
                'This is the long sound "ee", written ī.',
                "It sits like an accent on the consonant: mī is มี.",
            ],
            defeat_dialog=[
                "Nim: Good!",
                'By the way, มี means "to have", it\'s very commonly used!',
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ิ"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=45,
            y=39,
            standard_dialog=[
                "Nim: And here is her short sister -ิ, pronounced i.",
                "-ิ is like -ี, but -ิ is short while -ี is long.",
                "Can you see the difference?",
            ],
            defeat_dialog=[
                "Nim: I remember that -ิ is shorter than -ี,",
                "because it's shorter to write -ิ than -ี!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ส"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=47,
            y=42,
            standard_dialog=[
                "Nim: Here's ส, don't get it confused with the l ล!",
                "It's the s, well, one of them.",
                "Thai has four letters for s: ส, ษ, ซ, and ศ.",
                "ส is the most common of them.",
                "Notice how most of them are >s<triken though:",
                "It makes it easy to remember that ส, ษ, ซ, and ศ are s.",
            ],
            defeat_dialog=[
                'Nim: At the end of a word, s is pronounced "t".',
                "By the way, do you know why letters are pronounced differently at the end?",
                "Because Thai people don't voice the last part of syllable.",
                "You can think that they don't take the time to properly finish.",
                "So, l becomes n, g becomes k, d becomes t, and s becomes t also!",
                "Try yourself!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ด"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=47,
            y=32,
            standard_dialog=["Nim: Here's the consonant ด!", "This is the d."],
            defeat_dialog=[
                'Nim: At the end of a syllable, it\'s pronounced "t", not d.'
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ต"),
            ma=al.mas.get_map_from_name("ko_kut"),
            x=48,
            y=32,
            standard_dialog=[
                "Nim: And here's ด's sister: ต.",
                "It has a little dent on top, and it's pronounced dt.",
            ],
            defeat_dialog=[
                'Nim: This one too is pronounced "t" at the end of a syllable.'
            ],
        )
    )


def spirit_bird(al):
    naming = Naming(
        al,
        name="ลมสวย",
        image="spirit_bird",
        distractors=["น", "า", "ร", "-ั", "ก", "เ-", "อ", "-ี", "ง", "ท", "-ิ", "ต"],
        prompt="Spell the spirit's True Name!",
        victory_callback=spirit_bird_victory_callback,
    )
    add_npc(
        Npc(
            sprite="",
            x=52,
            y=37,
            al=al,
            name="spirit_bird",
            ma=al.mas.get_map_from_name("ko_kut"),
            standard_dialog=["Kyaaaaa!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons thunder and hurts [Name]!",
            ],
            naming=naming,
        )
    )
    add_npc(
        Npc(
            sprite="spirit_bird",
            x=52,
            y=36,
            wobble=True,
            al=al,
            name="spirit_bird",
            ma=al.mas.get_map_from_name("ko_kut"),
            standard_dialog=["Kyaaaaa!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons thunder and hurts [Name]!",
            ],
            naming=naming,
        )
    )
    add_npc(
        Npc(
            sprite="",
            x=53,
            y=37,
            al=al,
            name="spirit_bird",
            ma=al.mas.get_map_from_name("ko_kut"),
            standard_dialog=["Kyaaaaa!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons thunder and hurts [Name]!",
            ],
            naming=naming,
        )
    )
    add_npc(
        Npc(
            sprite="",
            x=53,
            y=36,
            al=al,
            name="spirit_bird",
            ma=al.mas.get_map_from_name("ko_kut"),
            standard_dialog=["Kyaaaaa!"],
            defeat_dialog=["Nim: Well done [Name]! You got it!"],
            victory_dialog=[
                "The name is not correct!",
                "The spirit summons thunder and hurts [Name]!",
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


def ko_kut(al):
    people_on_the_beach(al)
    wild_letters(al)
    spirit_bird(al)
    old_people_and_fisherman(al)
