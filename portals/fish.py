import random
from dataclasses import dataclass

MAX_SPEED = 4
MAX_ACCELERATION = 0.3
MAX_JERK = 0.03
LETTERS = [
    "น",
    "า",
    "ร",
    "ก",
    "ฑ",
    "ม",
    "เ",
    "อ",
    "ล",
    "ง",
    "ท",
    "ว",
    "ย",
    "ส",
    "ต",
    "ด",
    "บ",
    "ป",
    "ะ",
    "ค",
    "จ",
    "พ",
    "แ",
    "ห",
    "ใ",
    "ไ",
    "โ",
    "ช",
    "ข",
    "ฟ",
]
WORDS = [
    "คน",
    "ดี",
    "ดู",
    "ใจ",
    "ยิน",
    "ที่",
    "ได้",
    "เห็น",
    "โชค",
    "มาก",
    "ก็",
    "ตาม",
    "เข้า",
    "จำ",
    "ความ",
    "เป็น",
    "คิด",
    "ว่า",
    "การ",
    "ต้อง",
    "จัด",
    "พิมพ์",
    "กลุ่ม",
    "ดาว",
    "เทียม",
    "ตก",
    "น้ำ",
    "ฝน",
    "ปลา",
    "ไป",
    "เสาร์",
    "ถึง",
    "กับ",
    "หา",
    "นอก",
    "ทุ่ง",
    "เกี่ยว",
    "อยู่",
    "เดียว",
    "เหมือน",
    "อาศัย",
    "ขึ้น",
    "รอด",
    "เอง",
    "ทำ",
    "ให้",
    "งาน",
    "บุญ",
    "ร้าย",
    "นา",
    "อาหาร",
    "ผิด",
    "ลอง",
    "เสี่ยง",
    "รู้",
    "รอบ",
    "สึก",
    "ลา",
    "จัก",
    "ผู้",
    "ชีวิต",
    "หญิง",
    "ชาย",
    "นำ",
    "ป่วย",
    "ใหญ่",
    "ใช้",
    "ครู",
    "ส่วน",
    "ไม้",
    "โลก",
    "ใบ",
    "ตัว",
    "ของ",
    "ทั่ว",
    "ร้อน",
    "สงคราม",
    "ชาว",
    "ขั้ว",
    "พื้น",
    "บ้าน",
    "ฤดู",
    "พัก",
    "ไว้",
    "เมือง",
    "เร่า",
    "ไทย",
    "หลวง",
    "พ่อ",
    "วัน",
    "เกิด",
    "ศุกร์",
    "พระ",
    "แม่",
    "เหล็ก",
    "ชี",
    "มด",
    "แดง",
    "รัง",
    "ไก่",
    "หม้าย",
    "ธุดงค์",
    "เลี้ยง",
    "ผี",
    "เสื้อ",
    "พุทธ",
    "ผ้า",
    "ตี",
    "ธาตุ",
    "กล้า",
    "แก่",
    "สร้าง",
    "เจ้า",
    "เก่า",
    "ชาติ",
    "ศิษย์",
    "รุ่น",
    "กรุง",
    "เพื่อน",
    "ยุค",
    "ลูก",
    "สาว",
    "มี",
    "ค่า",
    "ชื่อ",
    "เรื่อง",
    "อายุ",
    "หน้า",
    "เสียง",
    "เสือ",
    "ปี",
    "ดำ",
    "ข้าง",
    "ภาย",
    "ฟอง",
    "อ่อน",
    "ช้าง",
    "แอ",
    "จุด",
    "เผือก",
    "งา",
    "ผล",
    "รัก",
    "เหตุ",
    "ก่อน",
    "น่า",
    "คำ",
    "คู่",
    "แท้",
    "อ๊อด",
    "หิน",
    "ใหม่",
    "ย้อย",
    "ทอง",
    "หนืด",
    "ตู้",
    "ไฟ",
    "หมาย",
    "รวม",
    "จบ",
    "แข็ง",
    "ขาย",
    "ตัด",
    "กฎ",
    "ฟ้า",
    "ปิด",
    "รถ",
    "ป่า",
    "ดับ",
    "ถูก",
    "หมู่",
    "นี้",
    "หอ",
    "สิน",
    "ศิลป์",
    "ผ่า",
    "ผม",
    "ทรง",
    "สี",
    "จุกข้อ",
    "กลดเราะยา",
    "ขาวปวดเมฆ",
    "ส้มกองพ้อง",
    "ทาขับพวก",
    "รากบัสมวล",
    "ปากท้องภาษา",
    "ฟันหลังมนุษย์",
    "ออกปล่อง",
    "กล้วยกบ",
    "ถามคุย",
    "พูดห้อง",
    "ขอราคา",
    "ส่งขี้",
    "เงินลดต่อ",
    "คัดตลาดคราว",
    "ดอกอังกฤษเวลา",
    "กลีบจีนหนาว",
    "จะญี่ปุ่นลม",
    "แปลเขียนชา",
    "เห็ดทะเล",
    "หอมสนาม",
    "หัวบิน",
    "กลิ่นรบ",
    "บาลีนัก",
    "สันสกฤตลง",
    "มลายูจาน",
    "พม่าล้าง",
    "กลางตอบ",
    "ศาสตร์กลับ",
    "กลทาง",
    "ไกด่า",
    "สับเดิน",
    "หมูเส้น",
    "แฮมปลาย",
    "ย่างใน",
    "ปืนเยอรมัน",
    "มือฝรั่งเศส",
    "ดินถิ่น",
    "วิทยาขณะ",
    "เครื่องเรียน",
    "ถือนอน",
    "สองสมุด",
    "จับครัว",
    "ขวาเกาหลี",
    "ฝ่าสเปน",
    "นิ้วเมื่อ",
    "ซ้ายแขก",
    "ดีดพี่",
    "ลายน้อง",
    "สือสะใภ้",
    "ถุงงำ",
    "เท้ามุ้ง",
    "พลาสติกน้า",
    "ยางครอบ",
    "สวนเด็ก",
    "รัด",
    "สุด",
    "เกล้า",
    "ร่ม",
    "ยอด",
    "เย็น",
    "เพศ",
    "สัตว์",
    "เปลี่ยน",
    "ศึกษา",
    "บุตร",
    "สถาน",
    "ประถม",
    "กรณี",
    "อุดม",
    "ภาพ",
    "เตรียม",
    "การณ์",
    "แปลง",
    "คุณ",
    "ฉกรรจ์",
    "โสด",
    "ชู้",
    "เดิม",
    "แบบ",
    "นาง",
    "ง่าย",
    "ใด",
    "นั้น",
    "รูป",
    "ตา",
    "หลาน",
    "กัน",
    "ร่วม",
    "ต่าง",
    "หาด",
    "ทราย",
    "กระดาษ",
    "เม็ด",
    "เนิน",
    "กระบะ",
    "ละเอียด",
    "ปราสาท",
    "ทาน",
    "พายุ",
    "หมุน",
    "หิมะ",
    "เค็ม",
    "เปิด",
    "ปลุก",
    "นาฬิกา",
    "กรวด",
    "ตุ๊กตา",
    "รส",
    "สม",
    "ชู",
    "ไข่",
    "จืด",
    "ทุก",
    "อื่น",
    "บาง",
    "จน",
    "สัก",
    "ขยิบ",
    "ตาย",
    "เล่น",
    "เสีย",
    "นั่ง",
    "ดุ",
    "วาย",
    "พิษ",
    "แว่น",
    "ขยาย",
    "กล้อง",
    "ข่าว",
    "ฝัน",
    "เที่ยว",
    "หยุด",
    "เขต",
    "มืด",
    "เช้า",
    "รอ",
    "ค่ำ",
    "แล้ว",
    "มา",
    "นี่",
    "กลาย",
    "พันธุ์",
]
ACCENTS = " ัุ ู์ ้ ็ ๊ ี ่ำ ื ิ๋"
DISAPPEARS = 0
APPEARS = 1


@dataclass
class Point:
    x: float
    y: float


def get_nice_color():
    r = random.choice([0, 255])
    g = random.choice([0, 255])
    b = 255 - r if r == g else random.choice([0, 255])
    return r, g, b


def get_letters_from_word(word):
    letters = []
    previous_letter = ""
    for char in word:
        # if previous_letter == "":
        #     previous_letter = char
        if char in ACCENTS:
            previous_letter += char
        else:
            if previous_letter:
                letters += [previous_letter]
            previous_letter = char
    letters += [previous_letter]
    return letters


class Fish(object):
    def __init__(self, al):
        self.pos = Point(x=random.randint(-4000, 3000), y=random.randint(-3000, 3000))
        self.spe = Point(x=random.uniform(-1, 1), y=random.uniform(-1, 1))
        self.acc = Point(x=random.uniform(-0.1, 0.1), y=random.uniform(-0.1, 0.1))
        self.jer = Point(x=random.uniform(-0.01, 0.01), y=random.uniform(-0.01, 0.01))
        word = random.choice(WORDS)
        letters = get_letters_from_word(word)
        # self.letter = random.choice(LETTERS)
        self.letter = letters[0]
        f = al.ui.fonts
        self.font = random.choice(
            [f.sarabun22, f.sarabun24, f.sarabun26, f.sarabun28, f.sarabun32]
        )
        self.color = get_nice_color()
        self.light = random.uniform(0, 1.0)
        self.current_color = (
            int(self.color[0] * self.light),
            int(self.color[1] * self.light),
            int(self.color[2] * self.light),
        )
        self.rendered = self.font.render(self.letter, True, self.current_color)
        self.tendency = APPEARS
        # self.number_of_followers = random.choice([3, 5, 6, 7, 10, 15, 25])
        self.followers = letters[1:]
        # self.followers = [random.choice(LETTERS) for _ in range(self.number_of_followers)]
        self.rendered_followers = [
            self.font.render(follower, True, self.current_color)
            for follower in self.followers
        ]
        self.old_pos = [self.pos for _ in range(5 * len(self.followers))]

    def invert_tendency(self):
        self.tendency = 1 - self.tendency

    def is_visible(self, al):
        x = self.pos.x + al.mesh.offset.x
        y = self.pos.y + al.mesh.offset.y
        return -100 < x < al.ui.width + 100 and -100 < x < al.ui.width + 100

    def moves(self, al):
        if self.is_visible(al):
            if random.uniform(0, 1) < 0.1:
                if self.tendency == APPEARS:
                    self.light = min(self.light + 0.1, 1.0)
                if self.tendency == DISAPPEARS:
                    self.light = max(self.light - 0.1, 0)
                new_color = (
                    int(self.color[0] * self.light),
                    int(self.color[1] * self.light),
                    int(self.color[2] * self.light),
                )
                if new_color != self.current_color:
                    self.current_color = new_color
                    self.rendered = self.font.render(
                        self.letter, True, self.current_color
                    )
                    self.rendered_followers = [
                        self.font.render(follower, True, self.current_color)
                        for follower in self.followers
                    ]
                else:
                    self.invert_tendency()

            for i, old_po in enumerate(self.old_pos):
                if i < len(self.old_pos) - 1:
                    self.old_pos[i] = Point(
                        self.old_pos[i + 1].x, self.old_pos[i + 1].y
                    )
                else:
                    self.old_pos[i] = self.pos

            self.pos.x = int(self.pos.x + self.spe.x)
            self.pos.y = int(self.pos.y + self.spe.y)

            self.spe.x = max(min(self.spe.x + self.acc.x, MAX_SPEED), -MAX_SPEED)
            self.spe.y = max(min(self.spe.y + self.acc.y, MAX_SPEED), -MAX_SPEED)

            self.acc.x = max(
                min(self.acc.x + self.jer.x, MAX_ACCELERATION), -MAX_ACCELERATION
            )
            self.acc.y = max(
                min(self.acc.y + self.jer.y, MAX_ACCELERATION), -MAX_ACCELERATION
            )

            self.jer.x = max(
                min(self.jer.x + random.uniform(-0.01, 0.01), MAX_JERK), -MAX_JERK
            )
            self.jer.y = max(
                min(self.jer.y + random.uniform(-0.01, 0.01), MAX_JERK), -MAX_JERK
            )

    def draw(self, al):
        x = self.pos.x + al.mesh.offset.x
        y = self.pos.y + al.mesh.offset.y
        if -100 < x < al.ui.width + 100 and -100 < x < al.ui.width + 100:
            al.ui.screen.blit(self.rendered, (x, y))
            for i, follower in enumerate(self.rendered_followers):
                f_x = self.old_pos[i * 5].x + al.mesh.offset.x
                f_y = self.old_pos[i * 5].y + al.mesh.offset.y
                al.ui.screen.blit(follower, (f_x, f_y))
#
#
# for word in WORDS:
#     print(word, get_letters_from_word(word))
