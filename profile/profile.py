import glob, os
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

        play_thai_word("to save")
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

    def load(self, al: 'All'):
        f = open(self.file_path, "r")

        for i, line in enumerate(f):
            line = line[:-1]
            if i == 0:  # name
                pass
            elif i == 1:  # position
                _, m, x, y = tuple(line.split(" "))
                ma = getattr(al.mas, m)
                al.mas.current_map = ma
                al.learner.ma = ma
                al.learner.x = int(x)
                al.learner.y = int(y)
            elif i == 2:  # hp
                _, hp = tuple(line.split(" "))
                al.learner.hp = int(hp)
            elif i == 3:  # money
                _, money = tuple(line.split(" "))
                al.learner.money = int(money)
            elif i == 4:  # last_heal
                _, m, x, y = tuple(line.split(" "))
                ma = getattr(al.mas, m)
                al.learner.last_healing_place = (int(x), int(y), ma)
            elif i == 5:  # last_saved
                al.learner.last_saved = mktime(strptime(line, TIME_FORMAT))
            else:
                split = line.split(" | ")
                value = split[0]
                xp = max(int(split[1]), 0)
                word = al.words.get_word(value)
                if not word:
                    print(f'ERROR: could not get word for {value}', split)
                word.increase_xp(al, xp)
        f.close()

        # proceed to remove 1 xp for each word if necessary
        seconds_since_last_time = mktime(datetime.now().timetuple()) - al.learner.last_saved
        if seconds_since_last_time > 72000:
            xp_loss = al.words.time_to_xp_loss(seconds_since_last_time)
            for word in al.words.words:
                word.decrease_xp(al, xp_loss)
            print('it has been 20 hours!')
        else:
            print('it has NOT been 20 hours!')


class Profiles(object):
    def __init__(self):
        self.profiles = {}
        self.current_profile = None
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(dir_path)
        print('dir_path', dir_path)
        if len(glob.glob("*.pro")) == 0:
            f = open(f"{dir_path}/Alexis.pro", "w")
            f.write("Alexis\n")
            f.write(f"position chaiyaphum 28 92\n")
            f.write(f"hp 5\n")
            f.write(f"money 5\n")
            f.write(f"last_heal chaiyaphum 28 92\n")
            f.write(f"22:00:53 28 Jan 2019\n")

        for file_name in glob.glob("*.pro"):
            file_path = dir_path + '/' + file_name
            print('file_path', file_path)
            learner_name = file_name[:-4]
            profile = Profile(name=learner_name, file_path=file_path)
            self.profiles[learner_name] = profile

    def set_as_profile(self, name: str):
        self.current_profile = self.profiles[name]
