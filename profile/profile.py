import glob, os
import pickle
from datetime import datetime
from time import mktime

from models import get_current_map, save_user_to_db, get_current_x_y_money_hp
from sounds.play_sound import play_thai_word

TIME_FORMAT = "%H:%M:%S %d %b %Y"

import sqlite3

# open connection and get a cursor
conn = sqlite3.connect("thai.db")
c = conn.cursor()


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
        self.save_pickle(al)

    def save_pickle(self, al: "All"):
        pickle.dump(al, open("Alexis.pro", "wb"))
        pass

    def load_all(self, al: "All"):
        # pass
        file_name = "Alexis.pro"
        if os.path.getsize(file_name) > 0:
            retrieved_all = pickle.load(open(file_name, "rb")) # let's get rid of that!
            ma = get_current_map(al)
            x, y, money, hp = get_current_x_y_money_hp(al)  # from the DB
            al.mas.current_map = ma
            al.learner.ma = ma
            al.learner.x = x
            al.learner.y = y
            al.learner.hp = hp
            al.learner.money = money
            last_healing_place_map = getattr(
                al.mas, retrieved_all.learner["last_healing_place"]["map_name"]
            )
            last_healing_place_x = retrieved_all.learner["last_healing_place"]["x"]
            last_healing_place_y = retrieved_all.learner["last_healing_place"]["y"]
            al.learner.last_healing_place = (
                last_healing_place_x,
                last_healing_place_y,
                last_healing_place_map,
            )
            al.learner.last_saved = retrieved_all.learner["last_saved"]
            al.learner.direction = retrieved_all.learner["direction"]
            al.learner.max_hp = retrieved_all.learner["max_hp"]

            al.bag = retrieved_all.bag

    def load(self, al: "All"):
        """
        TODO: this should use the DB only
        """
        # pass
        self.load_all(al)
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

            user_id = 1

            # def insert_word(thai, english, tones):
            #     if not find_word(thai):
            #         c.execute(f"INSERT INTO words (thai, english, tones) VALUES ('{thai}', '{english}', '{tones}')")
            #         conn.commit()

    def set_as_profile(self, name: str):
        self.current_profile = self.profiles[name]
