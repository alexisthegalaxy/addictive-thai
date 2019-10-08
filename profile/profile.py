from datetime import datetime
from time import mktime

from models import save_user_to_db, load_current_x_y_money_hp_ma, save_user_details_to_db, \
    load_user_details, save_bag, load_bag
from sounds.play_sound import play_thai_word


def save(al: "All"):
    print("บันทึก")
    play_thai_word("บันทึก")
    al.learner.last_saved = mktime(datetime.now().timetuple())
    save_user_to_db(al, al.learner.x, al.learner.y, al.learner.money, al.learner.hp, al.mas.current_map.filename)
    save_user_details_to_db(al)
    save_bag(al)


def load(al: "All"):
    load_current_x_y_money_hp_ma(al)
    load_user_details(al)
    load_bag(al)

    # TODO XP
    # # proceed to remove 1 xp for each word if necessary
    # seconds_since_last_time = (
    #     mktime(datetime.now().timetuple()) - al.learner.last_saved
    # )
    # if seconds_since_last_time > 72000:
    #     xp_loss = al.words.time_to_xp_loss(seconds_since_last_time)
    #     for word in al.words.words:
    #         word.decrease_xp(al, xp_loss)
    #     print("it has been more than 20 hours!")
    # else:
    #     print("it has NOT been 20 hours!")
