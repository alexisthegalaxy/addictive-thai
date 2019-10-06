import glob, os
from datetime import datetime
from time import mktime

from models import save_user_to_db, load_current_x_y_money_hp_ma, save_user_details_to_db, \
    load_user_details, save_bag, load_bag
from sounds.play_sound import play_thai_word


class Profile(object):
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

    def save(self, al: "All"):
        play_thai_word("บันทึก")
        f = open(self.file_path, "w+")
        al.learner.last_saved = mktime(datetime.now().timetuple())

        print("save!")
        f.close()
        save_user_to_db(al, al.learner.x, al.learner.y, al.learner.money, al.learner.hp, al.mas.current_map.filename)
        save_user_details_to_db(al)
        save_bag(al)

    def load(self, al: "All"):
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


class Profiles(object):
    def __init__(self):
        self.profiles = {}
        self.current_profile = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)

        for file_name in glob.glob("*.pro"):
            file_path = dir_path + "/" + file_name
            learner_name = file_name[:-4]
            profile = Profile(name=learner_name, file_path=file_path)
            self.profiles[learner_name] = profile

            # def insert_word(thai, english, tones):
            #     if not find_word(thai):
            #         c.execute(f"INSERT INTO words (thai, english, tones) VALUES ('{thai}', '{english}', '{tones}')")
            #         conn.commit()

    def set_as_profile(self, name: str):
        self.current_profile = self.profiles[name]
