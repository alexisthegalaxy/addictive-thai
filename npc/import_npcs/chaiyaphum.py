from direction import Direction
from lexicon.items import Letter, Word
from models import get_event_status
from npc.import_npcs.service import add_npc, no_callback
from npc.npc import Npc
from npc.question import Question
from npc.spell import Spell


def chaiyaphum_learner_house(al):
    add_npc(
        Npc(
            al=al,
            name="Mom",
            taught=Word.get_by_split_form("ฉัน"),
            ma=al.mas.get_map_from_name("house_learner_f1"),
            x=5,
            y=10,
            sprite="mom",
            direction=Direction.RIGHT,
            standard_dialog=[
                "Mom: [Name]!",
                "Mom: So, you decided to begin your Thai Adventure?",
                "Mom: Let me teach you the first word:",
            ],
            defeat_dialog=[
                'That\'s how women say "I" in Thai, but actually, there\'s many ways to say "I".',
                "Mom: I thought it woulb be a useful word for your adventure.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Dad",
            taught=Word.get_by_split_form("ผม"),
            ma=al.mas.get_map_from_name("house_learner_f1"),
            x=7,
            y=9,
            sprite="dad",
            direction=Direction.DOWN,
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
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Grandpa",
            taught=Word.get_by_split_form("ไทย"),
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=33,
            y=104,
            wanna_meet=True,
            eyesight=3,
            sprite="old_man",
            direction=Direction.LEFT,
            standard_dialog=[
                "Grandpa: Oh, [Name].",
                "Grandpa: So, you're leaving... How can I help you, I don't know much words...",
                "Grandpa: Oh, I know a word that would be useful for you!",
                "Grandpa: How to say Thai in Thai!",
            ],
            defeat_dialog=[
                'Grandpa: And to say "Thai people", we simply say "People-Thai": คนไทย'
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Granny",
            taught=Word.get_by_split_form("คน"),
            ma=al.mas.get_map_from_name("chaiyaphum_house_1"),
            x=8,
            y=11,
            sprite="old_woman",
            direction=Direction.LEFT,
            standard_dialog=[
                "Granny: Is that you, [Name]? Your mother told me your going on an adventure to learn Thai?",
                "Granny: My advice is: talk to everybody!",
                "Granny: People will teach you new words and help you greatly.",
                "Granny: So you can remember this advice, I will teach you this very word: people.",
            ],
            defeat_dialog=[
                'Granny: And to say "Thai people", we simply say "People-Thai": คนไทย',
                "Granny: If you're looking for grandpa, he's working in the field.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="television",
            ma=al.mas.get_map_from_name("house_learner_f2"),
            x=5,
            y=8,
            sprite="_television_on",
            standard_dialog=["It's a video game involving geckos."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="bed of Nim",
            ma=al.mas.get_map_from_name("house_learner_f2"),
            x=2,
            y=12,
            sprite="bed",
            standard_dialog=["That's the bed of Nim."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nim",
            ma=al.mas.get_map_from_name("house_learner_f2"),
            x=5,
            y=10,
            sprite="nim",
            direction=Direction.UP,
            standard_dialog=["Nim: Yo, [Name]!"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="bed",
            ma=al.mas.get_map_from_name("house_learner_f2"),
            x=8,
            y=12,
            sprite="bed",
            standard_dialog=["Let's take a nap and restore my health!"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="สมชาย",
            ma=al.mas.get_map_from_name("house_rival_f1"),
            x=5,
            y=9,
            sprite="dad",
            direction=Direction.LEFT,
            standard_dialog=[
                "Oh, [Name]. You came to see Somchai?",
                "He's upstairs in his room learning Thai!",
            ],
        )
    )


def chaiyaphum_chumphae_mo_hin_khao(al):
    add_npc(
        Npc(
            al=al,
            name="woman praying at stones",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=27,
            y=72,
            sprite="mom",
            direction=Direction.RIGHT,
            standard_dialog=[
                "I use to pray here every day to the Spell of Wind.",
                "But it has been gone for more than a week already...",
                "I wonder what happened.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="old man looking at stones",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=31,
            y=71,
            sprite="old_man",
            direction=Direction.UP,
            standard_dialog=[
                "These stones are quite famous around here.",
                "They are called มอหินขาว but tourists call those the Thai Stonehenge,",
                "although they are entirely natural.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="old woman looking at stones",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=29,
            y=74,
            sprite="old_woman",
            direction=Direction.LEFT,
            standard_dialog=[
                "I'm quite worried.",
                "I can see that not a single one of these five rock pillars is inhabited by a Spell.",
                "Last time I came, all five were protected by their spirits.",
                "But now, it's only a matter of time before they crumble, if their Spell are gone!",
                "Please, if you find them, help them find their way back into the pillars.",
                "I remember the spirits were Spells of Wind, Rock, Rain, Sun and Time.",
                "I will mark them in your Tablet, so that you know when you see them.",
            ],
        )
    )


def chaiyaphum_rest_of_the_city(al):
    add_npc(
        Npc(
            al=al,
            name="Lover",
            taught=Word.get_by_split_form("ชอบ"),
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=18,
            y=82,
            sprite="mali",
            direction=Direction.LEFT,
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
            end_dialog_trigger_event=["talk_to_lover"],
        ),
        get_event_status("talk_to_lover") == 0
    )
    add_npc(
        Npc(
            al=al,
            name="Policeman guarding road to Bua Yai",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=34,
            y=98,
            sprite="policeman",
            direction=Direction.DOWN,
            standard_dialog=[
                "Sorry, the road to Bua Yai is closed at the moment.",
                "We've had many reports of people who've been under attack",
                "from Thai words gone wild.",
                "Only those knowing more than 50 Thai words are allowed to pass through.",
            ],
        ),
    )
    add_npc(
        Npc(
            al=al,
            name="father_of_lover",
            ma=al.mas.get_map_from_name("lover_house"),
            x=4,
            y=9,
            sprite="old_man",
            direction=Direction.RIGHT,
            standard_dialog=[
                "Hey [Name], มะลิ wanted to talk to you, she's waiting in the garden."
            ]
            if get_event_status("talk_to_lover") == 0
            else ["You're looking for มะลิ? She went north, to Chumphae."],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="สมชาย",
            taught=Word.get_by_split_form("คุณ"),
            ma=al.mas.get_map_from_name("house_rival_f2"),
            x=6,
            y=10,
            sprite="somchai",
            direction=Direction.UP,
            standard_dialog=[
                "สมชาย> [Name]! I have decided to go on an adventure to learn all the Thai words!",
                "สมชาย> What??? You too?",
                "สมชาย> Ha! I'll be your rival then!",
                "สมชาย> I learnt one already. Let me teach it to you!",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=27,
            y=91,
            sprite="mom",
            direction=Direction.LEFT,
            standard_dialog=[
                "Did you know? You can save the game just by pressing the s key."
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=18,
            y=92,
            sprite="lass",
            direction=Direction.LEFT,
            standard_dialog=[
                "The road east is quite dangerous if you don't know Thai.",
                "I wouldn't go there myself,",
                "although I have been learning thai for three months already!",
            ],
        )
    )


def set_consonant_challenge_old_dude(al, npc):
    if al.learner.money >= 1:
        npc.active_dialog = npc.active_dialog[:] + ["Alright, let's do it!"]
        npc.consonants = [Letter.get_by_thai(l) for l in
                          ["น", "ร", "ก", "ม", "อ", "ล", "ง", "ท", "ว", "ย", "ส", "ต", "ด", "บ", "ป", "ค", "จ", "พ",
                           "ห", "ช", "ข", "ฟ"]]
    else:
        npc.active_dialog = npc.active_dialog[:] + ["You need to have at least one Baht..."]
        npc.consonants = None


def set_no_consonant_challenge_old_dude(al, npc):
    npc.consonants = None
    npc.active_dialog = npc.active_dialog[:] + ["Alright, but you should try eventually!", "Check your letters with L."]


def kid_sell_advice_to_beat_old_dude(al, npc):
    if al.learner.money >= 5:
        al.learner.money -= 5
        npc.active_dialog[4] = "You can press L during the fight to check the consonant class!"
    else:
        npc.active_dialog[4] = "You don't have enough money..."


def kid_sell_no_advice_to_beat_old_dude(al, npc):
    npc.active_dialog[4] = "As you prefer."


def chaiyaphum_chumphae_path(al):
    add_npc(
        Npc(
            name="old man consonant challenge",
            al=al,
            ma=al.mas.get_map_from_name("chaiyaphum_hidden_cave"),
            x=8,
            y=6,
            sprite="old_man",
            standard_dialog=[
                # "Yeh",
                # "I challenge you to a consonant race.",
                # "I give you 22 consonants, and you tell me their class.",
                # "You have 40 seconds. If you win I give you 3 Bahts, if you lose you give me 1 Baht.",
                Question(
                    precursor_text="Wanna try?",
                    choice_1="Yes",
                    choice_2="No",
                    choice_1_callback=set_consonant_challenge_old_dude,
                    choice_2_callback=set_no_consonant_challenge_old_dude,
                ),
            ],
            defeat_dialog=[
                "Well played!",
                "I gave you 3 Bahts, as promised",
            ],
            victory_dialog=[
                "Haha, I got you, youngster!",
                "Come on, show me a shiny Baht!",
                "You should check your letters with L more often.",
            ],
            direction=Direction.DOWN,
            hp=40,
            money=3,
            lost_money_on_defeat=1,
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=28,
            y=36,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "Have you been in the cave over there?",
                "There's an old man in there that will challenge you to a consonant race.",
                "If you give me 5 Bahts I'll give you a trick to beat him.",
                Question(
                    precursor_text="Wanna hear it?",
                    choice_1="Yes, pay 5 Bahts",
                    choice_2="No, I'm strong enough on my own",
                    choice_1_callback=kid_sell_advice_to_beat_old_dude,
                    choice_2_callback=kid_sell_no_advice_to_beat_old_dude,
                ),
                "[PLACEHOLDER]",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=30,
            y=88,
            sprite="mom",
            direction=Direction.UP,
            standard_dialog=[
                "Be careful out there, words can attack you when you're in tall grass.",
                "I'll let you go if you know at least 5 words!",
                "You can see the words you know by pressing 'w'.",
            ],
        )
    )
    add_npc(
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
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=39,
            y=57,
            sprite="mom",
            direction=Direction.RIGHT,
            standard_dialog=[
                "It's quite frustrating to meet words I never learnt,",
                "but I guess that's how it is.",
                "I heard you can learn these words in the houses along this path though.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=42,
            y=63,
            sprite="kid",
            direction=Direction.RIGHT,
            standard_dialog=[
                "You see how the grass is darker and taller over there?",
                "It means that more Spells will jump at you than usual.",
                "It's good if you want to meet a lot!",
                "But I find it a bit scary so I'll try to stay out.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=51,
            y=8,
            sprite="cat",
            direction=Direction.DOWN,
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=56,
            y=38,
            sprite="old_woman",
            direction=Direction.DOWN,
            standard_dialog=[
                "This, here, is a Spell.",
                "Do you know how to catch it?",
                "First, you need to know the word it is linked to.",
                "Then, you need to put it in a receptacle.",
            ],
        )
    )
    add_npc(
        Spell(
            al=al,
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=56,
            y=39,
            color="white",
        )
    )
    add_npc(
        Npc(
            al=al,
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=58,
            y=43,
            sprite="kid",
            direction=Direction.UP,
            standard_dialog=[
                "You see up there?",
                "It looks like it's a Spell!",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="kid informing stone path is also dangerous",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=30,
            y=59,
            sprite="kid",
            direction=Direction.DOWN,
            standard_dialog=[
                "That path leads to มอหินขาว, the Thai Stonehenge.",
                "Be careful, you can also get attacked by words,",
                "on mountain paths like these!",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="kid looking for his dog",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=42,
            y=47,
            sprite="kid",
            direction=Direction.RIGHT,
            standard_dialog=[
                "You!",
                "I'm looking for ซูชิ, my dog!",
                "He went chasing after a Spell, and I lost him.",
                "Can you help me find him?",
                "If you do, I'll teach you the word for dog!",
                "If you find him, give him his favorite bone, and he'll follow you!",
                "[Name] receives a disgusting-looking bone.",
                "I think he went north, up that hill...",
            ],
            extra_dialog_1=[
                "I think he went north, up that hill...",
            ],
            extra_dialog_2=[
                "ซูชิ, oh I'm so happy to see you!",
                "Thank you for bringing ซูชิ back!",
                "As promised, I'll teach you the word for dog!",
            ],
            extra_dialog_3=[
                "Thank you again!",
            ],
            beginning_dialog_trigger_event=['talk_to_kid_looking_for_dog'],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="sushi",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=51,
            y=10,
            sprite="dog",
            direction=Direction.UP,
            standard_dialog=[
                "This is ซูชิ, the lost dog!",
                "[Name] gives the bone to ซูชิ.",
                "ซูชิ seems to recognise the bone, and follows you.",
            ],
            beginning_dialog_trigger_event=['talk_to_sushi'],
        ),
        get_event_status("talk_to_sushi") == 0
    )
    add_npc(
        Npc(
            al=al,
            name="Sushi",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=42,
            y=48,
            sprite="dog",
            direction=Direction.UP,
            standard_dialog=["โฮ่ง โฮ่ง"],
        ),
        get_event_status("sushi_is_following") == 2
    )


def signs(al):
    add_npc(
        Npc(
            al=al,
            name="sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=31,
            y=84,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["North: ชุมแพ", "South: ชัยภูมิ"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=41,
            y=14,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["North: ชุมแพ", "South: ชัยภูมิ"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="ชัยภูมิ",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=24,
            y=94,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["ชัยภูมิ"],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="House sign",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=27,
            y=101,
            sprite="sign",
            direction=Direction.RIGHT,
            standard_dialog=["House of [Name]"],
        )
    )


def chaiyaphum_chumphae_houses(al):
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=45,
            y=10,
            sprite="old_woman",
            direction=Direction.UP,
            standard_dialog=[
                "This is the inn.",
                "You can rest here for free and restore your health.",
            ],
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            taught=Word.get_by_split_form("บ้าน"),
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
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            taught=Word.get_by_split_form("อยาก"),
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
        )
    )
    add_npc(
        Npc(
            al=al,
            name="Nobody",
            taught=Word.get_by_split_form("อยู่"),
            ma=al.mas.get_map_from_name("house4"),
            x=6,
            y=11,
            sprite="mom",
            direction=Direction.DOWN,
            standard_dialog=[
                "I'm at home. You're at my place.",
                "Do you know how to say where you are?",
            ],
        )
    )


def chaiyaphum(al):
    chaiyaphum_chumphae_mo_hin_khao(al)
    chaiyaphum_learner_house(al)
    chaiyaphum_rest_of_the_city(al)
    chaiyaphum_chumphae_path(al)
    chaiyaphum_chumphae_houses(al)
    signs(al)
