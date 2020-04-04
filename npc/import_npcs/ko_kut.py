from direction import Direction
from lexicon.items import Letter
from mechanics.naming import Naming
from npc.import_npcs.service import add_wild_letter, add_npc
from npc.npc import Npc


def people_on_the_beach(al):
    add_npc(Npc(
        al=al,
        name="crashed_plane",
        ma=al.mas.get_map_from_name("ko_kut"),
        x=57,
        y=54,
        sprite="_crashed_plane",
        direction=Direction.UP,
        standard_dialog=[
            "The plane is on fire!",
            "Better get some help quick.",
        ]
    ))
    add_npc(Npc(
        al=al,
        ma=al.mas.get_map_from_name("ko_kut"),
        x=57,
        y=55,
        sprite="",
        standard_dialog=[
            "The plane is on fire!",
            "Better get some help quick.",
        ],
    ))
    add_npc(Npc(
        al=al,
        ma=al.mas.get_map_from_name("ko_kut"),
        x=58,
        y=54,
        sprite="",
        standard_dialog=[
            "The plane is on fire!",
            "Better get some help quick.",
        ],
    ))
    add_npc(Npc(
        al=al,
        name="random plane passenger",
        ma=al.mas.get_map_from_name("ko_kut"),
        x=53,
        y=54,
        sprite="mom",
        direction=Direction.RIGHT,
        standard_dialog=[
            "Thank goodness everyone is still alive!",
        ],
    ))
    add_npc(Npc(
        al=al,
        name="random plane passenger",
        ma=al.mas.get_map_from_name("ko_kut"),
        x=57,
        y=56,
        sprite="dad",
        direction=Direction.UP,
        standard_dialog=[
            "While I'm taking out everybody that is still inside, can you get us some help?",
        ],
    ))
    add_npc(Npc(
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
    ))
    add_npc(Npc(
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
    ))
    add_npc(Npc(
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
    ))
    add_npc(Npc(
        al=al,
        name="random plane passenger",
        ma=al.mas.get_map_from_name("ko_kut"),
        x=57,
        y=51,
        sprite="woman",
        direction=Direction.LEFT,
        standard_dialog=[
            "What are we going to do?",
        ],
    ))


def ko_kut(al):
    people_on_the_beach(al)
    npcs = [


        # Npc(
        #     al=al,
        #     name="Nim",
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=49,
        #     y=53,
        #     sprite="nim",
        #     direction=Direction.DOWN,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "[Name], you just made your first step on Ko Kut!",
        #         "Ko Kut is the island where we send young people to learn their first letters.",
        #         "Our parents sent me here too, when I was your age!",
        #         "As you know, Thai is a magical language,",
        #         "and each word is a spell that can change the world around you.",
        #         "But of course, before you turn into a powerful Lingtwister,",
        #         "the first step is to learn the letters.",
        #         "Alright [Name], one last advice before you start your adventure:",
        #         "speak with everybody (using the space bar), and have fun!",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="Nim",
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=49,
        #     y=28,
        #     sprite="nim",
        #     direction=Direction.RIGHT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "Amazing, you learnt quite quickly, [Name]!",
        #         "Let's take the boat to the next island.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="Nim",
        #     ma=al.mas.get_map_from_name("ko_mak"),
        #     x=35,
        #     y=10,
        #     sprite="nim",
        #     direction=Direction.UP,
        #     eyesight=1,
        #     standard_dialog=[
        #         "This is Ko Mak.",
        #         "You can check where we are on the map by pressing m.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="",
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=51,
        #     y=46,
        #     sprite="rich_woman",
        #     direction=Direction.UP,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "You see that tall grass?",
        #         "This is where the letters live.",
        #         "In other areas of Thailand, words also live in tall grass,",
        #         "But this island is special because there are no words here, only letters.",
        #         "So, be prepared to have letters jumping at you!",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="First letter",
        #     taught=Letter.get_by_thai("น"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=57,
        #     y=53,
        #     sprite="old_woman",
        #     direction=Direction.LEFT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "Hello, young one.",
        #         "Let me teach you the most common consonant first: N.",
        #         "I will first show it to you, and then test you on it.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="Second letter",
        #     taught=Letter.get_by_thai("า"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=52,
        #     y=51,
        #     sprite="old_man",
        #     direction=Direction.RIGHT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "I will teach the most common letter in the Thai alphabet, so you'd better focus!",
        #         "า is the vowel 'a:', and note the semicolon, meaning it's a long vowel.",
        #         "Thai has a short 'a' (◌ั) and a long 'a:' (า)",
        #         "It's easy to use it: นา = 'na:'.",
        #     ],
        #     defeat_dialog=[
        #         "It's easy to remember:",
        #         "า looks like the letter A but without the left part and the bar.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="Third letter",
        #     taught=Letter.get_by_thai("ร"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=50,
        #     y=49,
        #     sprite="old_man",
        #     direction=Direction.RIGHT,
        #     wanna_meet=True,
        #     eyesight=5,
        #     standard_dialog=[
        #         "I will teach you the consonant r: ร",
        #         "You have to roll it, like in Spanish or Russian,",
        #         "but actually in informal speach we Thai people just say 'l', not 'r'.",
        #         "Oh! Also, if it's at the end of a word, it turns into a 'n' sound.",
        #         "ราร would be pronounced 'ra:n' (or 'la:n'), not 'ra:r'.",
        #     ],
        #     defeat_dialog=[
        #         "ร is easy to remember: it looks like the letter r, but reversed!",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="Fourth letter",
        #     taught=Letter.get_by_thai("-ั"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=55,
        #     y=48,
        #     sprite="old_woman",
        #     direction=Direction.LEFT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "I will teach you the vowel a:  ั ",
        #         "It's an accent floating like a cloud over another letter.",
        #         "If you put it over a consonant like so: นั ,",
        #         "Then you get the sound na.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="Fifth letter",
        #     taught=Letter.get_by_thai("ก"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=49,
        #     y=49,
        #     sprite="lass",
        #     direction=Direction.LEFT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "I will teach you the consonant g: ก",
        #         "It's the first letter of the Thai alphabet, and it's a very common letter.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="6th letter",
        #     taught=Letter.get_by_thai("ม"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=45,
        #     y=47,
        #     sprite="kid",
        #     direction=Direction.LEFT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "I will teach you the consonant m: ม",
        #         "It looks a lot like the n: น - but in the m, the loops are on the sa>M<e side.",
        #         "And for the น (n) the loops are >N<ot on the same side.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="7th letter",
        #     taught=Letter.get_by_thai("เ-"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=57,
        #     y=42,
        #     sprite="old_man",
        #     direction=Direction.RIGHT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "I will teach you the very common vowel เ!",
        #         "It's pronounced e, like in 'neck'.",
        #         "It's quite similar to the french é, like in café or Pokémon.",
        #         "It's an interesting vowel, because it comes before the consonant:",
        #         "For example, to write 'nay', you write เน!",
        #         "เ can also be combined with า and sandwich a consonant to form the ao sound!",
        #         "For example, เนา is read nao!",
        #     ],
        #     defeat_dialog=[
        #         "The vowel เ has a very similar friend, the vowel แ!",
        #         "You'll learn it later, but แ is pronounced ae, pronounced like in ham.",
        #     ]
        # ),
        # Npc(
        #     al=al,
        #     name="8th letter",
        #     taught=Letter.get_by_thai("อ"),
        #     ma=al.mas.get_map_from_name("ko_kut"),
        #     x=57,
        #     y=40,
        #     sprite="old_woman",
        #     direction=Direction.RIGHT,
        #     wanna_meet=True,
        #     eyesight=1,
        #     standard_dialog=[
        #         "I will teach you the letter o: อ. It is both used as a vowel and a consonant.",
        #         "As a vowel, it's a long o:, like in 'saw'.",
        #         "For example, รอ is pronounced 'ro:'.",
        #         "But it can also be used as a consonant placeholder - and it's silent.",
        #         "For example, to say \"uncle\" in Thai, we say a:.",
        #         "But you cannot just write า, because each vowel in Thai needs a consonant.",
        #         "So you use instead the silent consonant placeholder อ.",
        #         "So, \"uncle\" is อา.",
        #     ],
        #     defeat_dialog=[
        #         "อ is quite easy to remember, because it looks like an o.",
        #         "Because it's both a consonnant and a vowel,",
        #         "\"ออ\" is a syllable read \"o:\", meaning \"to congregate\"!",
        #         "There's also this crazy word \"เออออ\", read \"er o\", meaning \"to agree\"!"
        #     ]
        # ),
        Npc(
            al=al,
            name="Teacher of inherent vowel",
            ma=al.mas.get_map_from_name("ko_kut_house_1"),
            x=6,
            y=10,
            sprite="dad",
            direction=Direction.RIGHT,
            wanna_meet=True,
            eyesight=1,
            standard_dialog=[
                "Did you know? Thai is the opposite of English.",
                "English can write words without consonants,",
                "while Thai can write words without vowels.",
                "For example, รก.",
                "However!",
                'Even though there\'s no vowel written, we still pronounce it with a short "o" sound.',
                "For example, รก is pronounced \"rok\", and not \"rk!\"",
            ],
        ),
        Npc(
            al=al,
            name="Explainer of why the letters are different in the final form",
            ma=al.mas.get_map_from_name("ko_kut_house_1"),
            x=7,
            y=10,
            sprite="woman",
            direction=Direction.LEFT,
            standard_dialog=[
                "Hey,",
                "Do you know why some letters change when they're at the end of a syllable?",
                "Because Thai people tend to close their mouth just before the end of the syllable.",
                "For example, try to pronounce 'nag', but close your mouth just before you finish:",
                "You'll see for yourself, you're saying 'nak'!",
                "It's also true for the 'l' or the 'r' becoming 'n'.",
            ]
        ),
        Npc(
            al=al,
            name="",
            ma=al.mas.get_map_from_name("inn_ko_kut"),
            x=3,
            y=6,
            sprite="woman",
            direction=Direction.RIGHT,
            standard_dialog=[
                "Did you know?",
                "All the places in this game are based off real Thailand!",
                "We're now in Ko Kut, which is often called the most beautiful island in Thailand.",
                "It's all empty beaches, primordial mangroves, white sand, and clear water!",
                "And we have more monkeys than people!",
            ]
        ),
        Npc(
            al=al,
            name="",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=52,
            y=36,
            sprite="spirit_bird",
            standard_dialog=["Kyaaaaa!"],
            wobble=True,
            end_dialog_trigger_event=["talk_to_spirit_bird"],
            naming=Naming(al, name="ลมสวย", image="spirit_bird", distractors=["น", "า", "ร", "-ั", "ก", "เ", "อ", "-ี", "ง", "ท", "-ิ", "ต"], prompt="Spell the spirit's True Name!"),
        ),
        Npc(
            al=al,
            name="",
            ma=al.mas.get_map_from_name("ko_kut"),
            x=48,
            y=29,
            sprite="spirit_gecko",
            standard_dialog=["Tuck gae!"]
        ),
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=52,
            y=37,
            sprite="",
            standard_dialog=["Kyaaaaa!"],
            end_dialog_trigger_event=["talk_to_spirit_bird"],
        ),
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=53,
            y=37,
            sprite="",
            standard_dialog=["Kyaaaaa!"],
            end_dialog_trigger_event=["talk_to_spirit_bird"],
        ),
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("ko_kut"),
            x=53,
            y=36,
            sprite="",
            standard_dialog=["Kyaaaaa!"],
            end_dialog_trigger_event=["talk_to_spirit_bird"],
        ),
        Npc(
            al=al,
            name="",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=37,
            y=8,
            sprite="boat",
            standard_dialog=["Enter the boat?"]
        ),
    ]

    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ม"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=51,
        y=55,
        standard_dialog=[
            "Nim: oh, you see that letter? It's ม, the m!",
        ],
        defeat_dialog=[
            "Nim: Well done [Name], that's one more letter!",
            "It looks a lot like the n: น - but in the m, the loops are on the sa>M<e side.",
            "And for the น (n) the loops are >N<ot on the same side.",
        ]
    ))

    add_wild_letter(wild_letter=Npc(
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
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ก"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=50,
        y=49,
        standard_dialog=[
            "Nim: Another one?",
            "This one is ก, the consonnant g - and it's the first letter of the Thai alphabet.",
        ],
        defeat_dialog=[
            "Nim: Well done [Name]!",
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("เ-"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=52,
        y=45,
        standard_dialog=[
            "Nim: This is the very common vowel เ!",
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
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("อ"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=54,
        y=41,
        standard_dialog=[
            "Nim: This is the very common vowel เ!",
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
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ว"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=51,
        y=41,
        standard_dialog=[
            "Nim: This is the very common vowel เ!",
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
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ย"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=44,
        y=48,
        standard_dialog=[
            "Nim: This is the very common vowel เ!",
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
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ล"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=49,
        y=42,
        standard_dialog=[
            "Nim: That's the consonnant l!",
            "Don't get ล confused with the s: ส!",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("-ี"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=57,
        y=38,
        standard_dialog=[
            "Nim: Here's the vowel -ี!",
            "This is the long sound \"ee\", written ī.",
            "The long ī looks like the short i, don't get them confused.",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ง"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=49,
        y=35,
        standard_dialog=[
            "Nim: Here's the vowel -ี!",
            "This is the long sound \"ee\", written ī.",
            "The long ī looks like the short i, don't get them confused.",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ท"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=47,
        y=39,
        standard_dialog=[
            "Nim: Here's the vowel -ี!",
            "This is the long sound \"ee\", written ī.",
            "The long ī looks like the short i, don't get them confused.",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("-ิ"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=44,
        y=39,
        standard_dialog=[
            "Nim: Here's the vowel -ี!",
            "This is the long sound \"ee\", written ī.",
            "The long ī looks like the short i, don't get them confused.",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ส"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=47,
        y=42,
        standard_dialog=[
            "Nim: Here's the vowel -ี!",
            "This is the long sound \"ee\", written ī.",
            "The long ī looks like the short i, don't get them confused.",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))
    add_wild_letter(wild_letter=Npc(
        al=al,
        letter=Letter.get_by_thai("ต"),
        ma=al.mas.get_map_from_name("ko_kut"),
        x=47,
        y=32,
        standard_dialog=[
            "Nim: Here's the vowel -ี!",
            "This is the long sound \"ee\", written ī.",
            "The long ī looks like the short i, don't get them confused.",
        ],
        defeat_dialog=[
            "Nim: At the end of a word, l in pronounced \"n\".",
            "For example, มล is pronounced \"mon\", not \"mol\"!",
            "You can't end a word in l in Thai."
        ]
    ))

    for npc in npcs:
        npc.ma.add_npc(npc)

