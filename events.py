from direction import Direction, opposite_direction
from models import set_event
from npc.npc import Npc, Position
# These are called by the function execute_event


def _talk_to_lover_0(al: 'All'):
    """
    Create lover where the user stands.
    """
    x, y = al.learner.x, al.learner.y
    lover = None
    for npc in al.mas.current_map.npcs:
        if npc.name == 'Lover':
            lover = npc
            break
    lover.direction = Direction.DOWN
    lover.must_walk_to = Position(x=18, y=85)
    print('yay')
    set_event('talk_to_lover', 0)


def _lover_goes_right_0(al: 'All'):
    lover = None
    for npc in al.mas.current_map.npcs:
        if npc.name == 'Lover':
            lover = npc
            break
    lover.direction = Direction.RIGHT
    lover.must_walk_to = Position(x=23, y=85)
    print('yay')
    set_event('lover_goes_right', 0)

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

def _talk_to_lover_2(al: 'All'):
    """
    Create lover where the user stands.
    """
    direction = opposite_direction(al.learner.direction)
    lover = Npc(
            al=al,
            name="Test Lover",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=17,
            y=84,
            sprite="mali",
            direction=direction,
            standard_dialog=["[Name]! I'm number four"],
            end_dialog_trigger_event=['talk_to_lover'],
        )

    al.mas.current_map.add_npc(lover)


def _talk_to_lover_3(al: 'All'):
    """
    Create lover where the user stands.
    """
    set_event('talk_to_lover', 0)
    al.mas.current_map.npcs = [npc for npc in al.mas.current_map.npcs if npc.name != "Test Lover"]
    lover = Npc(
            al=al,
            name="Test Lover",
            ma=al.mas.get_map_from_name("chaiyaphum"),
            x=18,
            y=82,
            sprite="mali",
            direction=Direction.DOWN,
            standard_dialog=["[Name]! I'm number four"],
            end_dialog_trigger_event=['talk_to_lover'],
        )
    al.mas.current_map.add_npc(lover)

