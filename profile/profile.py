import glob, os
import pickle
from datetime import datetime
from time import strptime
from time import mktime

from sounds.play_sound import play_thai_word
TIME_FORMAT = '%H:%M:%S %d %b %Y'


class Profile(object):
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

    def save(self, al: 'All'):
        now_string = datetime.now().strftime(TIME_FORMAT)

        play_thai_word("บันทึก")
        f = open(self.file_path, "w+")
        map = al.learner.ma.filename
        x = al.learner.x
        y = al.learner.y

        f.write(self.name + "\n")
        f.write(f"position {map} {str(x)} {str(y)}\n")
        f.write(f"hp {al.learner.hp}\n")
        f.write(f"money {al.learner.money}\n")
        f.write(f"last_heal {al.learner.last_healing_place[2].filename} {al.learner.last_healing_place[0]} {al.learner.last_healing_place[1]}\n")
        f.write(f"{now_string}\n")
        for word in al.words.words:
            f.write(f"{word.separated_form} | {word.total_xp}\n")
        print('save!')
        f.close()
        self.save_pickle(al)

    def save_pickle(self, al: 'All'):
        pickle.dump(al, open("Alexis.pro", "wb"))

    def load_pickle(self, al: 'All'):
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
            last_healing_place_map = getattr(al.mas, retrieved_all.learner["last_healing_place"]["map_name"])
            last_healing_place_x = retrieved_all.learner["last_healing_place"]["x"]
            last_healing_place_y = retrieved_all.learner["last_healing_place"]["y"]
            al.learner.last_healing_place = (last_healing_place_x, last_healing_place_y, last_healing_place_map)
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

    def load(self, al: 'All'):
        self.load_pickle(al)
        # proceed to remove 1 xp for each word if necessary
        seconds_since_last_time = mktime(datetime.now().timetuple()) - al.learner.last_saved
        if seconds_since_last_time > 72000:
            xp_loss = al.words.time_to_xp_loss(seconds_since_last_time)
            for word in al.words.words:
                word.decrease_xp(al, xp_loss)
            print('it has been more than 20 hours!')
        else:
            print('it has NOT been 20 hours!')


class Profiles(object):
    def __init__(self):
        self.profiles = {}
        self.current_profile = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        # if len(glob.glob("*.pro")) == 0:
        #     f = open(f"{dir_path}/Alexis.pro", "w")
        #     f.write("Alexis\n")
        #     f.write(f"position chaiyaphum 28 92\n")
        #     f.write(f"hp 5\n")
        #     f.write(f"money 5\n")
        #     f.write(f"last_heal chaiyaphum 28 92\n")
        #     f.write(f"22:00:53 28 Jan 2019\n")

        for file_name in glob.glob("*.pro"):
            file_path = dir_path + '/' + file_name
            learner_name = file_name[:-4]
            profile = Profile(name=learner_name, file_path=file_path)
            self.profiles[learner_name] = profile

    def set_as_profile(self, name: str):
        self.current_profile = self.profiles[name]
