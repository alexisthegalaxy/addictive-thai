from direction import Direction
from npc.npc import Npc


def chumphae_lomsak(al):
    npcs = [
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house1"),
            x=4,
            y=11,
            dialog_0=[
                "Hello, young one.",
                "Want to learn a word?",
                "Well, I am a rice farmer, so how about rice?",
            ],
            direction=Direction.DOWN,
            sprite="old_man",
            taught_word=al.words.get_word("ข้าว"),
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house1"),
            x=6,
            y=11,
            sprite="mom",
            direction=Direction.LEFT,
            dialog_0=[
                "Rice is an important word, it is very common.",
                'To say that you are eating, you literally say "I am eating rice".',
                'And to say that you are hungry, you literally say "I\'m hungry for rice".',
                "Well except if you're eating or are hungry for something else,",
                'then of course you say "I\'m eating something else", haha!',
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("น้ำ"),
            ma=al.mas.get_map_from_name("chumphae_lomsak_house2"),
            x=5,
            y=10,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "What, you came all the way from ชัยภูมิ?",
                "You must be tired!",
                "Do you want something?",
                "Water, maybe?",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house2"),
            x=11,
            y=7,
            sprite="old_man",
            direction=Direction.UP,
            dialog_0=["I'm a rice farmer.", "That's a common job, around here."],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("กิน"),
            ma=al.mas.get_map_from_name("chumphae_lomsak_house3"),
            x=5,
            y=10,
            sprite="mom",
            direction=Direction.LEFT,
            dialog_0=[
                "Do you know what Thai people love most?",
                "Eating",
                "I gotta teach you this word!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house3"),
            x=3,
            y=8,
            sprite="old_man",
            direction=Direction.DOWN,
            dialog_0=[
                "You can use the verb กิน to mean both eating and drinking actually!"
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house3"),
            x=2,
            y=10,
            sprite="kid",
            direction=Direction.RIGHT,
            dialog_0=["ผมกินน้ำ"],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house3"),
            x=3,
            y=11,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "To say 'I am eating',",
                "if you don't want to precise what you are eating,",
                "you must add 'rice': ฉันกินข้าว.",
            ],
        ),
        Npc(
            al=al,
            name="FirstBattleTrainer",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ผม", "ฉัน", "ชอบ"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=110,
            y=55,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "Let's fight!",
            ],
            dialog_1=["What, you won already?",
                      "Here, have two Bahts then."],
        ),
        Npc(
            al=al,
            name="SecondBattleTrainer",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["บ้าน", "โรง-เรียน"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=102,
            y=50,
            sprite="old_man",
            direction=Direction.DOWN,
            dialog_0=[
                "Let's have a short fight!",
            ],
            dialog_1=["Ah, I'm not as fast as I use to be."],
        ),
        Npc(
            al=al,
            name="ThirdBattleTrainer",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ฉัน", "คุณ", "ผม", "เขา"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=97,
            y=45,
            sprite="lass",
            direction=Direction.RIGHT,
            dialog_0=[
                "I love word fights!",
                "My favorite words are pronouns.",
            ],
            dialog_1=[
                "I only know four pronouns so far,",
                "but I know that Thai has many pronouns!",
                "The word 'I' alone has more that ten different pronouns,",
                "to use in different situations.",
            ],
        ),
        Npc(
            al=al,
            name="FourthBattleTrainer",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ฉัน", "คุณ", "ผม", "เขา"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=97,
            y=45,
            sprite="lass",
            direction=Direction.RIGHT,
            dialog_0=[
                "You wanna fight?",
                "Let me warn you, I'm pretty strong!",
            ],
            dialog_1=[
                "That was a good fight!",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def chumphae_school(al):
    npcs = [
        Npc(
            al=al,
            name="TeacherBottomRight",
            taught_word=al.words.get_word("ของ"),
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=20,
            y=15,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "ของ means 'of'",
            ],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=21,
            y=20,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "To say my or your or their and so on, you use ของ too.",
                "บ้าน ของ ผม = house of me = my house.",
            ],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=18,
            y=22,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "ของ is too easy.",
                "I am 4 already, I know this, come on!",
            ],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=22,
            y=22,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "It's funny how ของ sounds like kong.",
                "Does that mean that King Kong means 'king of'?",
            ],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=17,
            y=20,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "To say <'s> in English, you have to invert the order!",
                "Mari's brother = brother ของ Mari",
                "It's easier to think of it as the word 'of'",
            ],
        ),
        Npc(
            al=al,
            name="TeacherBottomLeft",
            taught_word=al.words.get_word("ไหม"),
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=6,
            y=15,
            sprite="old_man",
            direction=Direction.DOWN,
            dialog_0=[
                "ไหม is used at the end of sentence to make it a question.",
                "We only use it for yes/no questions.",
            ],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=4,
            y=20,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "So, if I understood correctly, you have to put the ไหม at the end?",
                "So, 'Do you like Thailand?' is 'You like Thailand ไหม': คุณ ชอบ เมืองไทย ไหม",
            ],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=8,
            y=20,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "In thai, we don't use a question mark.",
                "We don't use punctuation at all, actually, only spaces between chunks of words.",
            ],
        ),
        Npc(
            al=al,
            name="TeacherTopRight",
            taught_word=al.words.get_word("ไม่"),
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=19,
            y=4,
            sprite="old_man",
            direction=Direction.DOWN,
            dialog_0=[
                "ไม่ is used to create negative sentences.",
                "Careful not to get ไม่ (not) confused with ไหม (question mark),",
                "both are pronounced mai!",
            ],
        ),
        Npc(
            al=al,
            name="PupilTopRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=18,
            y=9,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "ไม่ also means no.",
                "Be careful to add the politeness particle afterwards to not sound rude though!",
                "For example, I'm a boy, so to say 'no', I say ไม่ครับ.",
            ],
        ),
        Npc(
            al=al,
            name="PupilTopRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=17,
            y=9,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "ไม่ is the 12th most used word in Thai!",
                "I'd better learn how to say it properly.",
            ],
        ),
        Npc(
            al=al,
            name="TeacherTopLeft",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=7,
            y=4,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "There are five tones in Thai.",
                "Mid, low, high, falling, rising.",
            ],
        ),
        Npc(
            al=al,
            name="PupilTopLeft",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=4,
            y=9,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "My favorite tone is the falling tone.",
                "It sounds like somebody just realising something.",
                "Like 'aaAAaa! I see now!'",
            ],
        ),
        Npc(
            al=al,
            name="PupilTopLeft",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=9,
            y=11,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "The rising tone goes down and then up.",
                "It sounds like in English when you say: Really?",
                "Or: Correct? Down and then up.",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def chumphae(al):
    npcs = [
        Npc(
            al=al,
            name="ชุมแพ",
            ma=al.mas.get_map_from_name("chumphae"),
            x=123,
            y=69,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "ชุมแพ",
            ],
        ),
        Npc(
            al=al,
            name="โรงเรียน",
            ma=al.mas.get_map_from_name("chumphae"),
            x=124,
            y=60,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "โรงเรียน (school)",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae"),
            x=126,
            y=76,
            sprite="mom",
            direction=Direction.UP,
            dialog_0=[
                "This is the inn.",
                "You can rest here for free and restore your health.",
            ],
        ),
        Npc(
            al=al,
            name="sign",
            ma=al.mas.get_map_from_name("chumphae"),
            x=122,
            y=80,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "North: ชุมแพ",
                "South: ชัยภูมิ",
            ],
        ),
        Npc(
            al=al,
            name="MomOfKidWhoWannaGoToSchool",
            taught_word=al.words.get_word("โรง-เรียน"),
            ma=al.mas.get_map_from_name("chumphae_house1"),
            x=3,
            y=11,
            sprite="mom",
            direction=Direction.UP,
            dialog_0=[
                "My son is to young for going to school yet, but he only thinks about that.",
                "This is because we live next to the school I guess.",
                "Do you know how to say school?",
            ],
        ),
        Npc(
            al=al,
            name="KidWhoWannaGoToSchool",
            ma=al.mas.get_map_from_name("chumphae_house1"),
            x=4,
            y=11,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "ผมชอบ โรงเรียนของชุมแพ!",
                "ผมชอบ โรงเรียนของชุมแพ!!!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("เขา"),
            ma=al.mas.get_map_from_name("chumphae_house2"),
            x=3,
            y=10,
            sprite="old_man",
            direction=Direction.UP,
            dialog_0=[
                "Let me teach you เขา. It's an important word, it means they/she/he.",
                "It's very common. It also means them/her/him.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae"),
            x=110,
            y=64,
            sprite="mom",
            direction=Direction.RIGHT,
            dialog_0=[
                "Many young people on this road like language challenge.",
                "I don't like it personally, it's too stressful for me.",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def chumphae_khonkaen(al):
    npcs = [
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_1"),
            x=10,
            y=7,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "The word สวัสดี was invented in the 1930s by Phraya Upakit Silapasan,",
                "of Chulalongkorn University.",
                "It comes from the Sanskrit svasti, meaning well-being.",
                "It was popularised by the government in a modernising effort.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_1"),
            x=11,
            y=10,
            sprite="kid",
            direction=Direction.DOWN,
            dialog_0=[
                "You don't have to say สวัสดี if you're with your friends,",
                "You can just say วัสดี!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ส-วัส-ดี"),
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_1"),
            x=5,
            y=9,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "Hello!",
                "...",
                "What, you don't know how to respond?",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ขอ-โทษ"),
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_2"),
            x=5,
            y=9,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "Sorry, what do you want?",
                "A word? Sorry, I'm not the best at teaching...",
                "Sorry. Oh, Sorry is good enough for you?",
                "Well, let's go for 'sorry' then!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ขอบ-คุณ"),
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_3"),
            x=5,
            y=9,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "The best way to live your life is to always be grateful.",
                "Gratitude makes you happy, makes others happy.",
                "I'll teach you how to say 'thank you'.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ครับ"),
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_4"),
            x=9,
            y=11,
            sprite="monk",
            direction=Direction.DOWN,
            dialog_0=[
                "ครับ is the male polite particle.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_4"),
            x=7,
            y=5,
            sprite="monk",
            direction=Direction.DOWN,
            dialog_0=[
                "Did you learn ค่ะ and ครับ yet?",
                "They are the two most common polite particles.",
                "Add ค่ะ if you are a female, and ครับ if you are a male,",
                "when you want to express politeness, at the end of a sentence.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ค่ะ"),
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_4"),
            x=5,
            y=11,
            sprite="monk",
            direction=Direction.DOWN,
            dialog_0=[
                "ค่ะ is the female polite particle.",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def nurses(al):
    npcs = [
        Npc(
            al=al,
            name="Nurse",
            ma=al.mas.get_map_from_name("inn1"),
            x=4,
            y=1,
            sprite="nurse",
            direction=Direction.DOWN,
            dialog_0=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="Nurse",
            ma=al.mas.get_map_from_name("inn2"),
            x=4,
            y=1,
            sprite="nurse",
            direction=Direction.DOWN,
            dialog_0=[
                "Welcome to the inn of Lomsak!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="Nurse",
            ma=al.mas.get_map_from_name("inn3"),
            x=4,
            y=1,
            sprite="nurse",
            direction=Direction.DOWN,
            dialog_0=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="Nurse",
            ma=al.mas.get_map_from_name("inn4"),
            x=4,
            y=1,
            sprite="nurse",
            direction=Direction.DOWN,
            dialog_0=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="Nurse",
            ma=al.mas.get_map_from_name("inn5"),
            x=4,
            y=1,
            sprite="nurse",
            direction=Direction.DOWN,
            dialog_0=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def chaiyaphum(al):
    npcs = [
        Npc(
            al=al,
            name="Mom",
            taught_word=al.words.get_word("ฉัน"),
            ma=al.mas.get_map_from_name("house1"),
            x=2,
            y=11,
            sprite="mom",
            direction=Direction.UP,
            dialog_0=[
                "Mom> [Name]!",
                "Mom> So, you decided to begin your Thai Adventure?",
                "Mom> Let me teach you the first word:",
            ],
        ),
        Npc(
            al=al,
            name="Dad",
            taught_word=al.words.get_word("ผม"),
            ma=al.mas.get_map_from_name("house1"),
            x=4,
            y=7,
            sprite="dad",
            direction=Direction.UP,
            dialog_0=[
                "Dad> What's up [Name]!",
                "Dad> I'll teach you a useful word before you go:",
            ],
        ),
        Npc(
            al=al,
            name="Teacher",
            taught_word=al.words.get_word("เมือง-ไทย"),
            ma=al.mas.get_map_from_name("lab"),
            x=4,
            y=7,
            sprite="old_man",
            direction=Direction.UP,
            dialog_0=[
                "Oh, hello [Name]. Are you ready to begin your Thai language adventure?",
                "Here's an important word: how to say Thailand in Thai!",
            ],
        ),
        Npc(
            al=al,
            name="มะลิ",
            taught_word=al.words.get_word("ชอบ"),
            ma=al.mas.get_map_from_name("house2"),
            x=9,
            y=12,
            sprite="mali",
            direction=Direction.DOWN,
            dialog_0=[
                "มะลิ> Hey [Name]! I heard you're about to go on an adventure?",
                "มะลิ> Before you go... I wanted to tell you that...",
                "มะลิ> I like you.",
                "มะลิ> Let me teach you the word 'to like' so you can remember me <3",
            ],
        ),
        Npc(
            al=al,
            name="สมชาย",
            taught_word=al.words.get_word("คุณ"),
            ma=al.mas.get_map_from_name("house3"),
            x=5,
            y=11,
            sprite="somchai",
            direction=Direction.DOWN,
            dialog_0=[
                "สมชาย> [Name]! I have decided to go on an adventure to learn all the Thai words!",
                "สมชาย> What??? You too?",
                "สมชาย> Ha! I'll be your rival then!",
                "สมชาย> I learnt one already. Let me teach it to you!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("บ้าน"),
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=54,
            y=47,
            sprite="old_man",
            direction=Direction.DOWN,
            dialog_0=[
                "That's my house!",
                "Pretty nice, eh?",
                "Wanna learn how to say house?",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("อยาก"),
            ma=al.mas.get_map_from_name("house5"),
            x=12,
            y=7,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "What do you want?",
                "You came all the way here, you must want something.",
                "Want to learn how to say want?",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("อยู่"),
            ma=al.mas.get_map_from_name("house4"),
            x=6,
            y=11,
            sprite="mom",
            direction=Direction.DOWN,
            dialog_0=[
                "I'm at home. You're at my place.",
                "Do you know how to say where you are?",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=20,
            y=93,
            sprite="mom",
            direction=Direction.UP,
            dialog_0=[
                "Did you know? You can save the game just by pressing the s key.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=45,
            y=10,
            sprite="mom",
            direction=Direction.UP,
            dialog_0=[
                "This is the inn.",
                "You can rest here for free and restore your health.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=32,
            y=88,
            sprite="mom",
            direction=Direction.UP,
            dialog_0=[
                "Be careful out there, words can attack you when you're in tall grass.",
                "I'll let you go if you know at least 5 words!",
                "You can see the words you know by pressing 'w'.",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=36,
            y=80,
            sprite="mom",
            direction=Direction.RIGHT,
            dialog_0=[
                "If you are hurt, you can rest a bit on your bed,",
                "you'll feel better after waking up!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=35,
            y=60,
            sprite="mom",
            direction=Direction.RIGHT,
            dialog_0=[
                "It's quite frustrating to meet words I never learnt,",
                "but I guess that's how life works.",
                "I heard you can learn these words in the houses along this path though.",
            ],
        ),
        Npc(
            al=al,
            name="sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=31,
            y=84,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "North: ชุมแพ",
                "South: ชัยภูมิ",
            ],
        ),
        Npc(
            al=al,
            name="sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=41,
            y=14,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "North: ชุมแพ",
                "South: ชัยภูมิ",
            ],
        ),
        Npc(
            al=al,
            name="ชัยภูมิ",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=24,
            y=94,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "ชัยภูมิ",
            ],
        ),
        Npc(
            al=al,
            name="House sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=26,
            y=91,
            sprite="sign",
            direction=Direction.RIGHT,
            dialog_0=[
                "House of [Name]",
            ],
        ),
        Npc(
            al=al,
            name="Rob",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=32,
            y=22,
            sprite="old_man",
            direction=Direction.DOWN,
            dialog_0=[
                "Yo, my name is Rob!",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def lomsak(al):
    npcs = [
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ภา-ษา"),
            ma=al.mas.get_map_from_name("lomsak_house_1"),
            x=3,
            y=11,
            sprite="mom",
            direction=Direction.RIGHT,
            dialog_0=[
                "Have you visited our school yet?",
                "I teach languages English and Thai at Lomsak school.",
                "You wanna learn the word for language?",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ภา-ษา-ไทย"),
            ma=al.mas.get_map_from_name("lomsak_house_1"),
            x=4,
            y=6,
            sprite="dad",
            direction=Direction.DOWN,
            dialog_0=[
                "My wife taught me how to speak Thai.",
                "To say Thai, you just say language-Thai!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            taught_word=al.words.get_word("ภา-ษา-อัง-กฤษ"),
            ma=al.mas.get_map_from_name("lomsak_house_1"),
            x=9,
            y=10,
            sprite="kid",
            direction=Direction.UP,
            dialog_0=[
                "I'm learning English at Lomsak's school.",
                "ฉันเรียนภาษาอังกฤษที่โรงเรียนหล่มสัก",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def empty(al):
    npcs = [
        # Npc(
        #     al=al,
        #     name="Nurse",
        #     ma=al.mas.get_map_from_name("inn1"),
        #     x=4,
        #     y=1,
        #     sprite="nurse",
        #     direction=Direction.DOWN,
        #     dialog_0=[
        #         "Welcome to the inn of Chumphae!",
        #         "You can rest here for a while, and you'll feel better!",
        #     ],
        # ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)
"""
    taught_word=al.words.get_word("โรง"),
"""


def import_npcs(al):
    chumphae_lomsak(al)
    chumphae_school(al)
    chumphae(al)
    chumphae_khonkaen(al)
    chaiyaphum(al)
    nurses(al)
    lomsak(al)
