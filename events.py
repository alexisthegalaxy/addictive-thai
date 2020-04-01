from bag.item import Item
from direction import Direction
from follower import Follower
from lexicon.items import Word, Letter
from models import set_event, get_event_status, get_xp_for_word

# These are called by the function execute_event
# The event is increased to n+1 just before calling the function _function_n
from npc.npc import Position, _process_dialog, Npc
from sounds.play_sound import play_thai_word


def _talk_to_lover_0(al: "All"):
    """
    After talking to player, Lover leaves the garden by the door.
    """
    lover = None
    for npc in al.mas.current_map.npcs:
        if npc.name == "Lover":
            lover = npc
            break
    father_of_lover = None
    for npc in al.mas.lover_house.npcs:
        if npc.name == "father_of_lover":
            father_of_lover = npc
            break
    lover.direction = Direction.DOWN
    father_of_lover.standard_dialog = [
        "You're looking for มะลิ? She went north, to Chumphae."
    ]
    lover.must_walk_to = [
        Position(x=18, y=85),
        Position(x=20, y=85),
        Position(x=20, y=86),
        Position(x=0, y=0),
    ]
    # set_event('talk_to_lover', 0)


def _talk_to_painter_0(al: "All"):
    """
    First time we speak, it's always asking for paint,
    and also teaching the word for blue if we don't know it
    """
    learner_knows_word = get_xp_for_word(split_form="สี-ฟ้า")
    al.active_npc.standard_dialog = al.active_npc.extra_dialog_3
    al.active_npc.active_dialog = al.active_npc.standard_dialog
    if not learner_knows_word:
        al.active_npc.taught = Word.get_by_split_form("สี-ฟ้า")


def _talk_to_painter_1(al: "All"):
    """
    If player has blue_paint:
        - we remove one blue_paint
        - we give them 100 bahts
    Else:
        - reset the event to 1
    """
    has_blue_paint = al.bag.get_item_quantity('blue_paint')
    if has_blue_paint > 0:
        al.learner.money += 20
        al.bag.reduce_item_quantity('blue_paint')
        play_thai_word("ขอบคุณนะครับ")
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_1
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        _process_dialog(al.active_npc.active_dialog, al)
    else:
        al.active_npc.standard_dialog = al.active_npc.defeat_dialog
        al.active_npc.active_dialog = al.active_npc.defeat_dialog
        set_event('talk_to_painter', 1)


def _talk_to_painter_2(al: "All"):
    al.active_npc.standard_dialog = al.active_npc.extra_dialog_2
    al.active_npc.active_dialog = al.active_npc.standard_dialog
    set_event('talk_to_painter', 1)


def _find_gecko_1_0(al: "All"):
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "gecko_to_collect_1"]
    al.bag.add_item(Item('gecko'))


def _find_gecko_2_0(al: "All"):
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "gecko_to_collect_2"]
    al.bag.add_item(Item('gecko'))


def _find_gecko_3_0(al: "All"):
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "gecko_to_collect_3"]
    al.bag.add_item(Item('gecko'))


def _talk_to_gecko_kid_0(al: "All"):
    found_gecko_1 = int(bool(get_event_status('find_gecko_1')))
    found_gecko_2 = int(bool(get_event_status('find_gecko_2')))
    found_gecko_3 = int(bool(get_event_status('find_gecko_3')))
    number_of_collected_geckos = found_gecko_1 + found_gecko_2 + found_gecko_3
    if number_of_collected_geckos == 0:
        play_thai_word("ขอบคุณนะครับ")
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_5
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        _process_dialog(al.active_npc.active_dialog, al)
        set_event('talk_to_gecko_kid', 0)
    elif number_of_collected_geckos == 1:
        set_event('talk_to_gecko_kid', 0)
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_1
        al.active_npc.active_dialog = al.active_npc.standard_dialog
    elif number_of_collected_geckos == 2:
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_2
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        set_event('talk_to_gecko_kid', 0)
    else:
        set_event('talk_to_gecko_kid', 1)
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_3
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        al.active_npc.taught = Word.get_by_split_form("ตุ๊ก-แก")
        al.active_npc.wanna_meet = False
        al.bag.reduce_item_quantity('gecko', 3)


def _talk_to_gecko_kid_1(al: "All"):
    play_thai_word("ขอบคุณนะครับ")
    al.active_npc.standard_dialog = al.active_npc.extra_dialog_4
    al.active_npc.active_dialog = al.active_npc.standard_dialog
    _process_dialog(al.active_npc.active_dialog, al)
    set_event('talk_to_gecko_kid', 1)


def _talk_to_kid_looking_for_dog_0(al: "All"):
    al.bag.add_item(Item('disgusting_bone'))


def _talk_to_kid_looking_for_dog_1(al: "All"):
    if get_event_status("talk_to_sushi") == 1:
        # Has the dog following
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_2
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        al.active_npc.taught = Word.get_by_split_form("หมา")
        # Remove follower dog
        al.learner.followers = [follower for follower in al.learner.followers if follower.name != "ซูชิ"]

        dog = Npc(
            al=al,
            name="Sushi",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=42,
            y=48,
            sprite="dog",
            direction=Direction.UP,
            standard_dialog=["โฮ่ง โฮ่ง"],
        )
        al.mas.current_map.add_npc(dog)
        set_event('sushi_is_following', 2)

    else:
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_1
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        set_event('talk_to_kid_looking_for_dog', 1)


def _talk_to_kid_looking_for_dog_2(al: "All"):
    al.active_npc.standard_dialog = al.active_npc.extra_dialog_3
    al.active_npc.active_dialog = al.active_npc.standard_dialog
    al.active_npc.taught = Word.get_by_split_form("หมา")
    set_event('talk_to_kid_looking_for_dog', 2)


def _talk_to_sushi_0(al: "All"):
    al.learner.followers.append(
        Follower(
            al,
            direction=Direction.DOWN,
            sprite='dog',
            name='ซูชิ',
            x=51,
            y=10,
        )
    )
    # set_event('talk_to_sushi', 0)
    set_event('sushi_is_following', 1)
    # Remove sushi
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "sushi"]


def _talked_to_nim_in_plane_0(al: "All"):
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "Nim"]

    new_nim_teaching_second_letter = Npc(
        al=al,
        name="Nim",
        taught=Letter.get_by_thai("า"),
        ma=al.mas.get_map_from_name("plane"),
        x=8,
        y=7,
        sprite="nim",
        direction=Direction.RIGHT,
        wanna_meet=True,
        eyesight=1,
        standard_dialog=[
            "Nim: Good, that was your first letter.",
            "After the most common consonnant, here's the most common vowel:",
            "า is the vowel 'ā' (ā), and note the accent on top, meaning it's a long vowel.",
            "Thai has a short 'a' (-ั) and a long 'ā' (า)",
            "It's easy to use it: นา = 'nā'.",
        ],
        defeat_dialog=[
            "It's easy to remember:",
            "า looks like the letter A but without the left part and the bar.",
        ],
        end_dialog_trigger_event=["talked_to_nim_in_plane"],
    )
    al.mas.current_map.add_npc(new_nim_teaching_second_letter)


def _talked_to_nim_in_plane_1(al: "All"):
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "Nim"]
    # TODO: set weather to shaking and red
    new_nim_teaching_second_letter = Npc(
        al=al,
        name="Nim",
        ma=al.mas.get_map_from_name("plane"),
        x=8,
        y=7,
        sprite="nim",
        direction=Direction.RIGHT,
        wanna_meet=True,
        eyesight=1,
        standard_dialog=[
            "Nim: What was that?",
            "PA: The plane is experiencing technical difficulties.",
            "We will attempt a landing.",
            "Brace for impact!",
        ],
        end_dialog_trigger_event=["talked_to_nim_in_plane"],
    )
    al.mas.current_map.add_npc(new_nim_teaching_second_letter)





# for npc in al.mas.current_map.npcs:
#     if npc.name == "gecko_to_collect_1":
#         gecko = npc
#         break
# al.active_npc.standard_dialog = al.active_npc.extra_dialog_2
# al.active_npc.active_dialog = al.active_npc.standard_dialog
# set_event('talk_to_lover', 1)
#
#
# lover = None
# for npc in al.mas.current_map.npcs:
#     if npc.name == "Lover":
#         lover = npc
#         break
# father_of_lover = None
# for npc in al.mas.lover_house.npcs:
#     if npc.name == "father_of_lover":
#         father_of_lover = npc
#         break
# lover.direction = Direction.DOWN
# father_of_lover.standard_dialog = [
#     "You're looking for มะลิ? She went north, to Chumphae."
# ]
# lover.must_walk_to = [
#     Position(x=18, y=85),
#     Position(x=20, y=85),
#     Position(x=20, y=86),
#     Position(x=0, y=0),
# ]
print("yay!!!!")
# set_event('talk_to_lover', 0)


# def _lover_disappears_0(al: 'All'):
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     print('_lover_disappears_0')
#     al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "Lover"]
#     # lover = None
#     # for npc in al.mas.current_map.npcs:
#     #     if npc.name == 'Lover':
#     #         lover = npc
#     #         break
#     # lover.direction = Direction.RIGHT
#     # lover.must_walk_to = Position(x=23, y=85)
#     # print('yay')
#     set_event('lover_disappears', 0)

#
# def _talk_to_lover_1(al: 'All'):
#     """
#     Create lover where the user stands.
#     """
#     lover = Npc(
#             al=al,
#             name="Test Lover",
#             ma=al.mas.get_map_from_name("chaiyaphum"),
#             x=23,
#             y=83,
#             sprite="mali",
#             direction=Direction.DOWN,
#             standard_dialog=["[Name]! I'm number three"],
#             end_dialog_trigger_event=['talk_to_lover'],
#         )
#
#     al.mas.current_map.add_npc(lover)
#
#
# def _talk_to_lover_2(al: 'All'):
#     """
#     Create lover where the user stands.
#     """
#     direction = opposite_direction(al.learner.direction)
#     lover = Npc(
#             al=al,
#             name="Test Lover",
#             ma=al.mas.get_map_from_name("chaiyaphum"),
#             x=17,
#             y=84,
#             sprite="mali",
#             direction=direction,
#             standard_dialog=["[Name]! I'm number four"],
#             end_dialog_trigger_event=['talk_to_lover'],
#         )
#
#     al.mas.current_map.add_npc(lover)
#
#
# def _talk_to_lover_3(al: 'All'):
#     """
#     Create lover where the user stands.
#     """
#     set_event('talk_to_lover', 0)
#     al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "Test Lover"]
#     lover = Npc(
#             al=al,
#             name="Test Lover",
#             ma=al.mas.get_map_from_name("chaiyaphum"),
#             x=18,
#             y=82,
#             sprite="mali",
#             direction=Direction.DOWN,
#             standard_dialog=["[Name]! I'm number four"],
#             end_dialog_trigger_event=['talk_to_lover'],
#         )
#     al.mas.current_map.add_npc(lover)
#
