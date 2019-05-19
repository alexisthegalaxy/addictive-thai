import glob, os
import pickle
from datetime import datetime
from time import mktime

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
        self.save_pickle(al)

    def save_pickle(self, al: "All"):
        pickle.dump(al, open("Alexis.pro", "wb"))

    def load_pickle(self, al: "All"):
        file_name = "Alexis.pro"
        if os.path.getsize(file_name) > 0:
            retrieved_all = pickle.load(open(file_name, "rb"))
            ma = getattr(al.mas, retrieved_all.current_map)
            al.mas.current_map = ma
            al.learner.ma = ma
            al.learner.x = retrieved_all.learner["x"]
            al.learner.y = retrieved_all.learner["y"]
            al.learner.hp = retrieved_all.learner["hp"]
            al.learner.money = retrieved_all.learner["money"]
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

            for word in retrieved_all.words:
                xp = max(word["total_xp"], 0)
                word = al.words.get_word(word["separated_form"])
                if not word:
                    print(f'ERROR: could not get word for {word["separated_form"]}')
                word.increase_xp(al, xp)

    def load(self, al: "All"):
        """
        TODO: this should use the DB only
        """
        self.load_pickle(al)
        # proceed to remove 1 xp for each word if necessary
        seconds_since_last_time = (
            mktime(datetime.now().timetuple()) - al.learner.last_saved
        )
        if seconds_since_last_time > 72000:
            xp_loss = al.words.time_to_xp_loss(seconds_since_last_time)
            for word in al.words.words:
                word.decrease_xp(al, xp_loss)
            print("it has been more than 20 hours!")
        else:
            print("it has NOT been 20 hours!")


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
