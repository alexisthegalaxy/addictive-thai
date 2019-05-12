from bag.bag import Compartment
from bag.item import Item
from direction import Direction
from npc.npc import Npc
from npc.vendor import Vendor


def chumphae_lomsak(al):
    npcs = [
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house1"),
            x=4,
            y=11,
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=["I'm a rice farmer.", "That's a common job, around here."],
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=["ผมกินน้ำ"],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_lomsak_house3"),
            x=3,
            y=11,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
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
            x=108,
            y=55,
            sprite="kid",
            direction=Direction.RIGHT,
            money=2,
            standard_dialog=["Let's fight!"],
            defeat_dialog=["What, you won already?", "Here, have two Bahts then."],
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
            standard_dialog=["Let's have a short fight!"],
            defeat_dialog=["Ah, I'm not as fast as I use to be."],
        ),
        Npc(
            al=al,
            name="ThirdBattleTrainer",
            battle_words=[
                al.words.get_word(battle_word)
                for battle_word in ["ฉัน", "คุณ", "ผม", "เขา"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=97,
            y=45,
            sprite="lass",
            direction=Direction.RIGHT,
            standard_dialog=["I love word fights!", "My favorite words are pronouns."],
            defeat_dialog=[
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
                al.words.get_word(battle_word)
                for battle_word in ["ฉัน", "คุณ", "ผม", "เขา"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=85,
            y=42,
            sprite="lass",
            direction=Direction.UP,
            standard_dialog=["You wanna fight?", "Let me warn you, I'm pretty strong!"],
            defeat_dialog=["That was a good fight!"],
        ),
        Npc(
            al=al,
            name="FifthBattleTrainer",
            battle_words=[
                al.words.get_word(battle_word)
                for battle_word in ["น้ำ", "ข้าว", "กิน", "เขา"]
            ],
            ma=al.mas.get_map_from_name("chumphae"),
            x=23,
            y=24,
            sprite="lass",
            direction=Direction.DOWN,
            standard_dialog=["I hope you like to talk about food!"],
            defeat_dialog=[
                "Ah, maybe you're better when it comes to talking about food,",
                "but I'm better when it comes to eating it!",
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
            standard_dialog=["ของ means 'of'"],
        ),
        Npc(
            al=al,
            name="PupilBottomRight",
            ma=al.mas.get_map_from_name("chumphae_school"),
            x=21,
            y=20,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=["ชุมแพ"],
        ),
        Npc(
            al=al,
            name="โรงเรียน",
            ma=al.mas.get_map_from_name("chumphae"),
            x=124,
            y=60,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["โรงเรียน (school)"],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae"),
            x=126,
            y=76,
            sprite="mom",
            direction=Direction.UP,
            standard_dialog=[
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
            standard_dialog=["North: ชุมแพ", "South: ชัยภูมิ"],
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
            standard_dialog=[
                "My son is to young for going to school yet, but he only thinks about that.",
                "This is because we live next to the school I guess.",
                "Do you know how to say school?",
            ],
        ),
        Npc(
            al=al,
            name="Person that teaches baht",
            taught_word=al.words.get_word("บาท"),
            ma=al.mas.get_map_from_name("non_muang_house_1"),
            x=8,
            y=8,
            sprite="mom",
            direction=Direction.DOWN,
            standard_dialog=[
                "I heard that this place is full of bats.",
                "Not to be confused with bahts, the Thai currency!",
                "Bahts are spelled บาท!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("non_muang_house_1"),
            x=1,
            y=7,
            sprite="mom",
            direction=Direction.UP,
            standard_dialog=[
                "Non Muang is famous for the skeletons that have been discovered here.",
                "They are from the iron age!",
            ],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("non_muang_house_1"),
            x=2,
            y=7,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=["These skeletons are so tall!"],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae"),
            x=105,
            y=71,
            sprite="kid",
            direction=Direction.DOWN,
            standard_dialog=[
                "The road to Non Muang is not easy to walk!",
                "But Non Muang is fun.",
                "It has bats and skeletons!",
            ],
        ),
        Npc(
            al=al,
            name="นนเมือง",
            ma=al.mas.get_map_from_name("chumphae"),
            x=114,
            y=75,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["นนเมือง"],
        ),
        Npc(
            al=al,
            name="KidWhoWannaGoToSchool",
            ma=al.mas.get_map_from_name("chumphae_house1"),
            x=4,
            y=11,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=["ผมชอบ โรงเรียนของชุมแพ!", "ผมชอบ โรงเรียนของชุมแพ!!!"],
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
            standard_dialog=[
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
            standard_dialog=[
                "Many young people on this road like language challenge.",
                "I don't like it personally, it's too stressful for me.",
            ],
        ),
        Vendor(
            al=al,
            name="Vendor of Chumphae",
            ma=al.mas.get_map_from_name("chumphae_house3"),
            x=10,
            y=8,
            sprite="§",
            direction=Direction.DOWN,
            vendor_dialog_beginning=[
                "I've never seen you here, it's your first time in Chumphae?",
                "You want to buy something?",
            ],
            vendor_dialog_end=["See you again!"],
            sold_items=[
                Item(
                    name="apple",
                    compartment=Compartment.BATTLE_ITEMS,
                    description="delicious apple from chumphae",
                    price=8,
                ),
                Item(
                    name="water",
                    compartment=Compartment.BATTLE_ITEMS,
                    description="a plastic one-liter bottle of water",
                    price=12,
                ),
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=["Hello!", "...", "What, you don't know how to respond?"],
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=["ครับ is the male polite particle."],
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chumphae_khonkaen_house_4"),
            x=7,
            y=5,
            sprite="monk",
            direction=Direction.DOWN,
            standard_dialog=[
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
            standard_dialog=["ค่ะ is the female polite particle."],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def nurses(al):
    npcs = [
        Npc(
            al=al,
            name="nurse",
            ma=al.mas.get_map_from_name("inn1"),
            x=4,
            y=1,
            sprite="vendor",
            direction=Direction.DOWN,
            standard_dialog=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="nurse",
            ma=al.mas.get_map_from_name("inn2"),
            x=4,
            y=1,
            sprite="vendor",
            direction=Direction.DOWN,
            standard_dialog=[
                "Welcome to the inn of Lomsak!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="nurse",
            ma=al.mas.get_map_from_name("inn3"),
            x=4,
            y=1,
            sprite="vendor",
            direction=Direction.DOWN,
            standard_dialog=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="nurse",
            ma=al.mas.get_map_from_name("inn4"),
            x=4,
            y=1,
            sprite="vendor",
            direction=Direction.DOWN,
            standard_dialog=[
                "Welcome to the inn of Chumphae!",
                "You can rest here for a while, and you'll feel better!",
            ],
        ),
        Npc(
            al=al,
            name="nurse",
            ma=al.mas.get_map_from_name("inn5"),
            x=4,
            y=1,
            sprite="vendor",
            direction=Direction.DOWN,
            standard_dialog=[
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
            standard_dialog=[
                "Mom: [Name]!",
                "Mom: So, you decided to begin your Thai Adventure?",
                "Mom: Let me teach you the first word:",
            ],
        ),
        Npc(
            al=al,
            name="Dad",
            taught_word=al.words.get_word("ผม"),
            ma=al.mas.get_map_from_name("house1"),
            x=4,
            y=6,
            sprite="dad",
            direction=Direction.UP,
            standard_dialog=[
                "Dad: What's up [Name]!",
                "Dad: I'll teach you a useful word before you go:",
            ],
            defeat_dialog=[
                "Dad: Well done, [Name]!",
                "Dad: Now, go on your adventure!",
                "Dad: Come again when you'll have learned more than 100 words,",
                "Dad: and I'll give you something!",
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
            standard_dialog=[
                "Oh, hello [Name]. Are you ready to begin your Thai language adventure?",
                "Here's an important word: how to say Thailand in Thai!",
            ],
        ),
        Npc(
            al=al,
            name="มะลิ",
            taught_word=al.words.get_word("ชอบ"),
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=18,
            y=82,
            sprite="mali",
            direction=Direction.DOWN,
            standard_dialog=[
                "มะลิ> Hey [Name]! I heard you're about to go on an adventure?",
                "มะลิ> Before you go... I wanted to tell you that...",
                "มะลิ> I like you.",
                "มะลิ> Let me teach you the word 'to like' so you can remember me <3",
            ],
            defeat_dialog=[
                "มะลิ> Don't forget the word, [Name]...",
                "มะลิ> We'll meet again!",
            ],
        ),
        Npc(
            al=al,
            name="Father of Mali",
            ma=al.mas.get_map_from_name("house2"),
            x=4,
            y=9,
            sprite="old_man",
            direction=Direction.RIGHT,
            standard_dialog=[
                "มะลิ wanted to talk to you, she's waiting in the garden."
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
                "Did you know? You can save the game just by pressing the s key."
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=["North: ชุมแพ", "South: ชัยภูมิ"],
        ),
        Npc(
            al=al,
            name="sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=41,
            y=14,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["North: ชุมแพ", "South: ชัยภูมิ"],
        ),
        Npc(
            al=al,
            name="ชัยภูมิ",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=24,
            y=94,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["ชัยภูมิ"],
        ),
        Npc(
            al=al,
            name="House sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=26,
            y=91,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["House of [Name]"],
        ),
        Npc(
            al=al,
            name="Rob",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=32,
            y=22,
            sprite="old_man",
            direction=Direction.DOWN,
            standard_dialog=["Yo, my name is Rob!"],
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
            standard_dialog=[
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
            standard_dialog=[
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
            standard_dialog=[
                "I'm learning English at Lomsak's school.",
                "ฉันเรียนภาษาอังกฤษที่โรงเรียนหล่มสัก",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 1",
            taught_word=al.words.get_word("ได้"),
            ma=al.mas.get_map_from_name("lomsak"),
            x=32,
            y=17,
            sprite="mom",
            direction=Direction.RIGHT,
            standard_dialog=[
                "To say that you can do something, you use ได้ (dai).",
                "Put ได้ (dai) at the end of the sentence.",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 1 - kid 1",
            ma=al.mas.get_map_from_name("lomsak"),
            x=32,
            y=19,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "ได้ is so easy to use!",
                "I just put it at the end of my sentence if I want to say it's possible!",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 1 - kid 2",
            ma=al.mas.get_map_from_name("lomsak"),
            x=34,
            y=19,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "To ask a question with ได้,",
                "At the end of your sentence, first say ได้, then ไหม.",
                "For example, guess the meaning of: คุณ อยู่ บ้าน ได้ ไหม",
                "It means 'Can you be at home?'",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 1 - kid 1",
            ma=al.mas.get_map_from_name("lomsak"),
            x=35,
            y=17,
            sprite="kid",
            direction=Direction.LEFT,
            standard_dialog=[
                "If you want to negate ได้, Just put ไม่ (not) in front of it!",
                "So, cannot is mai-dai: ไม่ได้",
                "I can't eat: ฉัน กิน ไม่ ได้",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 2",
            ma=al.mas.get_map_from_name("lomsak_school"),
            x=7,
            y=16,
            sprite="mom",
            direction=Direction.DOWN,
            standard_dialog=[
                "In Thai, we don't really have a word for yes or no.",
                "To answer yes, you have to repeat the verb of the question.",
                "To answer no, you repeat the verb and put ไม่ (no) in front.",
                "For example: 'Do you like me?' 'คุณ ชอบ ฉัน ไหม'",
                "The verb is ชอบ (like), so the answer is ชอบ (yes) or ไม่ ชอบ (no).",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 2 - kid 1",
            ma=al.mas.get_map_from_name("lomsak_school"),
            x=8,
            y=20,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "It works the same with adjectives:",
                "You repeat the adjective to say yes,",
                "And put ไม่ before the adjective to say no!",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 3",
            ma=al.mas.get_map_from_name("lomsak_school"),
            taught_word=al.words.get_word("ใช่"),
            x=25,
            y=21,
            sprite="old_man",
            direction=Direction.LEFT,
            standard_dialog=[
                "When you ask a question that ends with '..., right?',",
                "Or something like '..., isn't it?',",
                "in Thai, we use ใช่ ไหม (chai mai) at the end of the sentence.",
                "For example: 'You like me, right?' 'คุณ ชอบ ผม ใช่ ไหม'",
                "",
            ],
        ),
        Npc(
            al=al,
            name="Lomsak - Prof 3 - kid 1",
            ma=al.mas.get_map_from_name("lomsak_school"),
            x=21,
            y=20,
            sprite="kid",
            direction=Direction.RIGHT,
            standard_dialog=[
                "The answer to a question ending in ใช่ ไหม",
                "would be ใช่ (yes), or ไม่ ใช่ (no).",
            ],
        ),
        Vendor(
            al=al,
            name="Vendor of Chumphae",
            ma=al.mas.get_map_from_name("lomsak_house_2"),
            x=10,
            y=8,
            sprite="fat_vendor",
            direction=Direction.DOWN,
            vendor_dialog_beginning=["Welcome to Lomsak!", "How can I help you?"],
            vendor_dialog_end=["Hope to See you again!"],
            sold_items=[
                Item(
                    name="apple",
                    compartment=Compartment.BATTLE_ITEMS,
                    description="delicious apple from chumphae",
                    price=8,
                ),
                Item(
                    name="water",
                    compartment=Compartment.BATTLE_ITEMS,
                    description="a plastic one-liter bottle of water",
                    price=12,
                ),
            ],
        ),
        Npc(
            al=al,
            name="lomsak_gym_battle_1",
            ma=al.mas.get_map_from_name("lomsak_gym"),
            x=14,
            y=22,
            standard_dialog=[
                "Welcome to the gym of Lomsak!",
                "If you beat us all and also the leader, you'll get something.",
                "I won't let you beat me easily, though!",
            ],
            defeat_dialog=["What, you won already?", "The leader won't be so easy!"],
            direction=Direction.LEFT,
            sprite="kid",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ใช่", "ภา-ษา"]
            ],
            money=4,
        ),
        Npc(
            al=al,
            name="lomsak_gym_battle_2",
            ma=al.mas.get_map_from_name("lomsak_gym"),
            x=11,
            y=20,
            standard_dialog=[
                "Do you know your pronouns? I'll test you!",
            ],
            defeat_dialog=["You're too good!"],
            direction=Direction.RIGHT,
            sprite="kid",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["คุณ", "ผม", "ฉัน", "เขา"]
            ],
            money=4,
        ),
        Npc(
            al=al,
            name="lomsak_gym_battle_3",
            ma=al.mas.get_map_from_name("lomsak_gym"),
            x=15,
            y=18,
            standard_dialog=[
                "I like to be in that gym,", "I train against every body who comes to challenge the leader!",
            ],
            defeat_dialog=["I lost! But I learned a lot from you."],
            direction=Direction.LEFT,
            sprite="kid",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ครับ", "ค่ะ"]
            ],
            money=4,
        ),
        Npc(
            al=al,
            name="lomsak_gym_battle_4",
            ma=al.mas.get_map_from_name("lomsak_gym"),
            x=11,
            y=16,
            standard_dialog=[
                "Let's see how well you know the polite words!",
            ],
            defeat_dialog=["What, you won already?", "The leader won't be so easy!"],
            direction=Direction.RIGHT,
            sprite="kid",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ขอบ-คุณ", "ขอ-โทษ", "ส-วัส-ดี"]
            ],
            money=4,
        ),
        Npc(
            al=al,
            name="lomsak_gym_battle_5",
            ma=al.mas.get_map_from_name("lomsak_gym"),
            x=12,
            y=14,
            standard_dialog=[
                "I am the last one before the leader!",
                "I'll do my best to give you a good fight!",
            ],
            defeat_dialog=["I knew already that you'd win!", "I saw you fighting the others.", "You're good."],
            direction=Direction.RIGHT,
            sprite="kid",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["น้ำ", "ได้", "ภา-ษา"]
            ],
            money=4,
        ),
        Npc(
            al=al,
            name="lomsak_gym_leader",
            ma=al.mas.get_map_from_name("lomsak_gym"),
            x=13,
            y=5,
            standard_dialog=[
                "Welcome, challenger!",
                "I am the leader of Lomsak's gym.",
                "Oh, this is your first time battling a gym's leader?",
                "If you can win this battle, I'll give you a something special!",
            ],
            defeat_dialog=["Congratulations!", "You have great knowledge of the Thai language already!", "Here, as promised, have the Lomsak badge."],
            direction=Direction.DOWN,
            sprite="dad",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ใช่", "ภา-ษา", "ภา-ษา-อัง-กฤษ", "ได้", "เรียน", "พูด", "ของ", "เรียน"]
            ],
            money=15,
        ),
        Npc(
            al=al,
            name="lomsak_monk_1",
            taught_word=al.words.get_word("พูด"),
            ma=al.mas.get_map_from_name("lomsak_temple"),
            x=8,
            y=9,
            sprite="monk",
            direction=Direction.DOWN,
            standard_dialog=[
                "สวัสดีครับ",
            ],
        ),
        Npc(
            al=al,
            name="lomsak_monk_2",
            taught_word=al.words.get_word("เรียน"),
            ma=al.mas.get_map_from_name("lomsak_temple"),
            x=18,
            y=9,
            sprite="monk",
            direction=Direction.DOWN,
            standard_dialog=[
                "สวัสดีครับ",
            ],
        ),
        Npc(
            al=al,
            name="lomsak_monk_3",
            taught_word=al.words.get_word("ไป"),
            ma=al.mas.get_map_from_name("lomsak_temple"),
            x=13,
            y=8,
            sprite="monk",
            direction=Direction.DOWN,
            standard_dialog=[
                "สวัสดีครับ",
            ],
        ),
        Npc(
            al=al,
            name="lomsak_house_3_person_1",
            taught_word=al.words.get_word("ดี"),
            ma=al.mas.get_map_from_name("lomsak_house_3"),
            x=14,
            y=23,
            sprite="mom",
            direction=Direction.LEFT,
            standard_dialog=[
                "I will teach you the most useful adjective ever.",
                "Good!",
            ],
            defeat_dialog=[
                "ดี is everywhere, even in hello: สวัสดี!",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def cat_cove(al):
    npcs = [
        Npc(
            al=al,
            name="cat_girl",
            taught_word=al.words.get_word("แมว"),
            ma=al.mas.get_map_from_name("cat_cove_house"),
            x=5,
            y=10,
            sprite="lass",
            direction=Direction.DOWN,
            standard_dialog=[
                "Oh, you found my secret cat paradise?",
                "Let's have a deal: I teach you the word cat,"
                "and you tell nobody, ok?",
            ],
            defeat_dialog=[
                "Funny how it sounds like a cat meowing, right?"
            ]
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove_house"),
            x=9,
            y=12,
            sprite="cat",
            direction=Direction.DOWN,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=11,
            y=10,
            sprite="cat",
            direction=Direction.LEFT,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=13,
            y=12,
            sprite="cat",
            direction=Direction.UP,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=9,
            y=15,
            sprite="cat",
            direction=Direction.RIGHT,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=18,
            y=22,
            sprite="cat",
            direction=Direction.LEFT,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=18,
            y=7,
            sprite="cat",
            direction=Direction.DOWN,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=22,
            y=26,
            sprite="cat",
            direction=Direction.UP,
            taught_word=al.words.get_word("ปลา"),
            standard_dialog=[
                "I want to eat fish",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=9,
            y=19,
            sprite="cat",
            direction=Direction.RIGHT,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=10,
            y=19,
            sprite="cat",
            direction=Direction.LEFT,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=16,
            y=11,
            sprite="cat",
            direction=Direction.RIGHT,
            standard_dialog=[
                "...",
            ],
        ),
        Npc(
            al=al,
            name="แมว",
            ma=al.mas.get_map_from_name("cat_cove"),
            x=16,
            y=12,
            sprite="cat",
            direction=Direction.RIGHT,
            standard_dialog=[
                "...",
            ],
        ),
    ]
    for npc in npcs:
        npc.ma.add_npc(npc)


def phetchabun(al):
    npcs = [
        Npc(
            al=al,
            name="Lass_who_lost_dog",
            ma=al.mas.get_map_from_name("phetchabun"),
            x=43,
            y=12,
            sprite="kid",
            direction=Direction.RIGHT,
            standard_dialog=[
                "I lost my dog!",
                "He went in the mountains behind me, can you help me to find it back?",
                "Please please!",
            ],
            eyesight=10,
            wanna_meet=True,
        ),
        Npc(
            al=al,
            name="โฮ่งโฮ่ง",
            ma=al.mas.get_map_from_name("phetchabun"),
            x=15,
            y=37,
            sprite="dog",
            direction=Direction.RIGHT,
            standard_dialog=[
                "โฮ่ง โฮ่ง",
            ],
            eyesight=10,
        ),
        Npc(
            al=al,
            name="เหมียว",
            ma=al.mas.get_map_from_name("phetchabun"),
            x=16,
            y=37,
            sprite="cat",
            direction=Direction.LEFT,
            standard_dialog=[
                "เหมียว",
            ],
            eyesight=10,
        ),
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("phetchabun"),
            x=22,
            y=16,
            sprite="dad",
            direction=Direction.UP,
            standard_dialog=[
                "You're looking for a dog?", "I just saw one running past me down there!",
            ],
            eyesight=10,
            wanna_meet=True,
        ),
        Npc(
            al=al,
            name="question_teacher_1",
            taught_word=al.words.get_word("อะ-ไร"),
            ma=al.mas.get_map_from_name("phetchabun_mountain_house_1"),
            x=9,
            y=11,
            sprite="mom",
            direction=Direction.LEFT,
            standard_dialog=[
                "You're going to the mountains?",
                "You'll need to know how to ask questions there!",
                "Here's how to say 'what':",
            ],
            eyesight=10,
            wanna_meet=True,
        ),
        Npc(
            al=al,
            name="question_teacher_1",
            taught_word=al.words.get_word("ที่-ไหน"),
            ma=al.mas.get_map_from_name("phetchabun_mountain_house_1"),
            x=4,
            y=5,
            sprite="mom",
            direction=Direction.DOWN,
            standard_dialog=[
                "Here's how to say 'where':",
            ],
        ),
        Npc(
            al=al,
            name="question_teacher_1",
            taught_word=al.words.get_word("ใคร"),
            ma=al.mas.get_map_from_name("phetchabun_mountain_house_1"),
            x=12,
            y=7,
            sprite="mom",
            direction=Direction.LEFT,
            standard_dialog=[
                "Here's how to say 'who':",
            ],
            defeat_dialog=[
                "To remember, imagine asking:",
                "Who cries? Who krai?",
            ],
        ),
        Npc(
            al=al,
            name="MountainTrainer",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["อะ-ไร", "ที่-ไหน", "ใคร"]
            ],
            ma=al.mas.get_map_from_name("phetchabun"),
            x=21,
            y=20,
            sprite="kid",
            direction=Direction.RIGHT,
            money=2,
            standard_dialog=["The mountain is full of interrogative words!", "Do you think you're ready?"],
            defeat_dialog=["Ha! I think you're ready!"],
            eyesight=10,
        ),
        Npc(
            al=al,
            name="MountainTrainer",
            battle_words=[
                al.words.get_word(battle_word) for battle_word in ["ได้", "ข้าว", "อยาก"]
            ],
            ma=al.mas.get_map_from_name("phetchabun"),
            x=32,
            y=18,
            sprite="kid",
            direction=Direction.RIGHT,
            money=2,
            standard_dialog=["Let's have a word battle!"],
            defeat_dialog=["That was a cool fight!", "Huh? You're looking for a dog?", "Maybe it went to the cave?"],
            eyesight=10,
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
        #     standard_dialog=[
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
    phetchabun(al)
    cat_cove(al)
