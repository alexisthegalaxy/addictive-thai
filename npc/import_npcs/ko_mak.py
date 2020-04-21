from direction import Direction
from lexicon.items import Letter
from mechanics.naming import Naming
from models import set_event, get_event_status
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
            beginning_dialog_trigger_event=['picks_up_garbage_0'],
        ),
        condition=get_event_status("picks_up_garbage_0") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_1'],
        ),
        condition=get_event_status("picks_up_garbage_0") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_2'],
        ),
        condition=get_event_status("picks_up_garbage_0") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_3'],
        ),
        condition=get_event_status("picks_up_garbage_3") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_4'],
        ),
        condition=get_event_status("picks_up_garbage_4") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_5'],
        ),
        condition=get_event_status("picks_up_garbage_5") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_6'],
        ),
        condition=get_event_status("picks_up_garbage_6") == 0,
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
            beginning_dialog_trigger_event=['picks_up_garbage_7'],
        ),
        condition=get_event_status("picks_up_garbage_7") == 0,
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_8",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=26,
            y=21,
            sprite="garbage_0",
            standard_dialog=["[Name] picks up the garbage."],
            beginning_dialog_trigger_event=['picks_up_garbage_8'],
        ),
        condition=get_event_status("picks_up_garbage_8") == 0,
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_9",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=12,
            y=14,
            sprite="garbage_1",
            standard_dialog=["[Name] picks up the garbage."],
            beginning_dialog_trigger_event=['picks_up_garbage_9'],
        ),
        condition=get_event_status("picks_up_garbage_9") == 0,
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_10",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=10,
            y=22,
            sprite="garbage_2",
            standard_dialog=["[Name] picks up the garbage."],
            beginning_dialog_trigger_event=['picks_up_garbage_10'],
        ),
        condition=get_event_status("picks_up_garbage_10") == 0,
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_11",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=11,
            y=21,
            sprite="garbage_3",
            standard_dialog=["[Name] picks up the garbage."],
            beginning_dialog_trigger_event=['picks_up_garbage_11'],
        ),
        condition=get_event_status("picks_up_garbage_11") == 0,
    )
    add_npc(
        Npc(
            al=al,
            name="garbage_12",
            ma=al.mas.get_map_from_name("ko_mak"),
            x=8,
            y=14,
            sprite="garbage_0",
            standard_dialog=["[Name] picks up the garbage."],
            beginning_dialog_trigger_event=['picks_up_garbage_12'],
        ),
        condition=get_event_status("picks_up_garbage_12") == 0,
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
                "To remember บ, think of it as a bowl containing some beverage!",
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
                "Nim: Wow, what is that garbage doing here? How dirty!",
                "Let's pick it up!",
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
                "Nim: This symbol is also used to shorten a vowel.",
                "For example, โ− is long on it's own, while โ−ะ is short!",
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
                "Nim: That's ค, and it's pronounced k'h - just like a k, but aspirated.",
                "At the end of a syllable, it's more like a k.",
                "Careful not to get ค and ด (d) confused!",
                "ค looks like a cow (kow) looking at you,",
                "while ด spirals in like a digital finger print.",
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
                "Nim: Now this is จ, the j sound.",
                "Guess how it's pronounced at the end of a syllable.",
                "It would be pronounced t.",
            ],
            defeat_dialog=[
                "Nim: Here's my mnemonic for it:",
                "จ looks like the trajectory of a >j<umping circle.",
                "Although I must say I've heard other mnemonics concerning >g<enitals.",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ื"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=24,
            y=21,
            standard_dialog=[
                "Nim: This vowel is the long \"eu\" sound.",
                "It's in the same family as -ิ and -ี, but it has two streaks on top: -ื.",
                "(And we also have -ึ in that family).",
                "This sound is a bit hard to make:",
                "You have to make the sound \"oo\" with your teeth and tongue,",
                "But you smile with your lips as if you say the sound \"ee\".",
                "I call this the smiling letter because it forces people to smile.",
                "Sometimes, it's on its own, like in มืด (that means \"dark\" by the way),",
                "but sometimes it comes with อ: for example, \"hand\" is มือ.",
                "It's pronounced the same way with or without the extra placeholder.",
            ],
            defeat_dialog=[
                "Nim: Well done!",
                "To remember it, imagine it's a smile with two teeth out.",
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
                "Nim: This letter is the p'h: the aspirated p sound.",
                "พ is low class, and it has a high-class brother ผ also pronounced p'h.",
                "The low-class one looks outside, while the high-class looks inside.",
                "To remember it, imagine that people in the upper class are full of themselves.",
                "While people in the lower class look outside.",
            ],
            defeat_dialog=[
                "Nim: To remember it, I imagine that พ is a wiggly >p<asta.",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ฟ"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=20,
            y=13,
            standard_dialog=[
                "Nim: And this is p'h brother: the f.",
                "Just like พ, ฟ has a high-class brother ฝ also pronounced f.",
                "Here too, the low-class one looks outside, while the high-class looks inside.",
            ],
            defeat_dialog=[
                "Nim: To remember it,",
                "I imagine that ฟ is a พ that is >f<ull-grown and >f<lamboyant.",
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
                "Nim: This is แ-, it looks like twice the เ-, that you learnt already!",
                "It's pronounced ae, like the sound in cat.",
                "Just like the เ-, it is before the consonant.",
            ],
            defeat_dialog=[
                "Nim: Don't forget that แ- and เ- are long vowels!",
                "Their shorter counterparts are แ−ะ and เ−ะ.",
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
                "Nim: This is ห, the h.",
                "For example, หก is pronounced hok - and that's how you write six!",
                "Notice how it looks like a h: it's quite easy to remember.",
                "The ห is also sometimes silent,",
                "and it's used to turn another consonant into a high-class.",
                "High-class helps with telling which is the tone of a syllable.",
                "For example in the word หลัง, you can just ignore the ห: it's simply read \"lang\".",
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
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ข"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=12,
            y=18,
            standard_dialog=[
                "Nim: Here's the k'h: the aspirated k sound.",
                "We've learnt another letter that is pronounced k'h: ค.",
                "It happens that Thai language has several letters for the same sound.",
                "But most languages do, right?",
                "However, ค and ข are different:",
                "ค is low class, and ข is high class.",
                "Each consonant in Thai is either high-, middle-, or low-class.",
                "This helps us determine the tone of a syllable.",
                "You'll have to learn for each eventually,",
                "It will be necessary to unlock their magical potential and use spells.",
            ],
            defeat_dialog=[
                "Nim: Did you see how ข looks like a บ (b), but flattened?",
                "Don't get them confused!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("ช"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=10,
            y=21,
            standard_dialog=[
                "Nim: This is ข's brother, ช!",
                "It looks the same, but has an extra dent.",
                "It's pronounced \"ch\", and \"t\" at the end of a word.",
            ],
            defeat_dialog=[
                "Nim: Did you see how ข looks like a บ (b), but flattened?",
                "Don't get them confused!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ู"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=10,
            y=14,
            standard_dialog=[
                "Nim: That's the vowel ū, the long \"oo\" sound like in \"noon\".",
                "It goes under the consonant:",
                "หู is pronounced hoo (it means ear).",
            ],
            defeat_dialog=[
                "Nim: It's the only letter that goes under, so it's easy to remember:",
                "ū goes ūnder!",
            ],
        )
    )
    add_wild_letter(
        wild_letter=Npc(
            al=al,
            letter=Letter.get_by_thai("-ุ"),
            ma=al.mas.get_map_from_name("ko_mak"),
            x=11,
            y=14,
            standard_dialog=[
                "Nim: And here's -ุ, -ู short sister: the same sound, but shorter.",
                "It's quite similar, but -ุ lack the little bit on the side of -ู.",
            ],
            defeat_dialog=[
                "Nim: These are the only letters that goes under, so it's easy to remember:",
                "ū goes ūnder!",
            ],
        )
    )


def spirit_gecko(al):
    naming = Naming(
        al,
        name="ใจแขวนเกาะ",
        image="spirit_gecko",
        distractors=["น", "า", "ร", "-ั", "ก", "อ", "-ี", "ง"],
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


def ko_mak(al):
    garbage(al)
    wild_letters(al)
    spirit_gecko(al)
