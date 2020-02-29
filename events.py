from direction import Direction
from models import set_event


# These are called by the function execute_event
from npc.npc import Position, _process_dialog
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
    print("yay")
    # set_event('talk_to_lover', 0)


def _talk_to_painter_0(al: "All"):
    """
    If player has blue_paint:
        - we remove one blue_paint
        - we give them 100 bahts
    Else:
        -
    """
    al.learner.money += 10
    has_blue_paint = al.bag.get_item_quantity('blue_paint')
    print(f'number of blue paints: {has_blue_paint}')
    if has_blue_paint > 0:
        al.learner.money += 10
        al.bag.remove_item('blue_paint')
        play_thai_word("ขอบคุณนะครับ")
        al.active_npc.standard_dialog = al.active_npc.extra_dialog_1
        al.active_npc.active_dialog = al.active_npc.standard_dialog
        _process_dialog(al.active_npc.active_dialog, al)
        set_event('talk_to_lover', 1)  # useless
    else:
        set_event('talk_to_lover', 0)


def _talk_to_painter_1(al: "All"):
    al.active_npc.standard_dialog = al.active_npc.extra_dialog_2
    al.active_npc.active_dialog = al.active_npc.standard_dialog
    set_event('talk_to_lover', 1)


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
