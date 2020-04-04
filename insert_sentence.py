import json
import sqlite3
from models import find_word_by_thai

conn = sqlite3.connect('thai.db')
c = conn.cursor()


def retrieve_words_from_sentence(thai):
    words = thai.split('_')
    word_ids = []
    for word in words:
        word = word.replace('-', '')
        word_db_id = find_word_by_thai(word)
        word_ids.append(word_db_id)
    return word_ids


def find_sentence(thai, words):
    answers = list(c.execute(f"SELECT * FROM sentences WHERE words = '{words}'"))
    if answers:
        return answers[0]
    else:
        return None


def insert_sentence(thai, english, words=[], alternatives=[]):
    if not words:
        words = retrieve_words_from_sentence(thai)

    if not find_sentence(thai, words):
        c.execute(f"INSERT INTO sentences (thai, english, words, alternatives) VALUES ('{thai}', '{english}', '{words}', '{alternatives}')")
        conn.commit()


def create_many_to_many_relationships():
    sentences = list(c.execute(f"SELECT * FROM sentences"))
    for sentence in sentences:
        word_ids = json.loads(sentence[3])
        sentence_id = sentence[0]
        for i, word_id in enumerate(word_ids):
            print(word_id)
            c.execute(f"INSERT INTO word_sentence (word_id, sentence_id, i) VALUES ('{word_id}', '{sentence_id}', '{i}')")
    conn.commit()


# """ผม_ชอบ_คุณ | I (male) like you.
# ฉัน_ชอบ_คุณ | I (female) like you.
# ผม_ไม่_ชอบ_คุณ | I (male) dont like you.
# ฉัน_ไม่_ชอบ_คุณ | I (female) dont like you.
# ผม_ชอบ_เมือง-ไทย | I (male) like Thailand.
# คุณ_ชอบ_เมือง-ไทย_ไหม | Do you like Thailand?
# ฉัน_อยาก_อยู่_เมือง-ไทย | I (female) want to be in Thailand.
# ผม_อยาก_อยู่_บ้าน | I (male) want to be home.
# ฉัน_ชอบ_อยู่_บ้าน | I (female) like to be at home.
# ผม_ไม่_ชอบ_อยู่_บ้าน | I (male) dont like to be at home.
# ผม_ชอบ_อยู่_เมือง-ไทย | I (male) like to be in Thailand.
# ฉัน_ไม่_ชอบ_อยู่_เมือง-ไทย | I (female) dont like to be in Thailand.
# ผม_อา-ยุ_สิบ_ปี | I (male) am ten years old.
# ผม_วิ่ง_เร็ว | I (male) run fast.
# ส-วัส-ดี_ค่ะ | Hello (said by female)!
# ส-วัส-ดี_ครับ | Hello (said by male)!
# ฉัน_รัก_เขา | I (female) love him.
# ฉัน_ชอบ_เขา | I (female) like him.
# ผม_ชอบ_เขา | I (male) like him.
# ผม_ไม่_ชอบ_เขา | I (male) dont like him.
# คุณ_ชื่อ_อะ-ไร | Whats your name?
# ฉัน_ชอบ_ชื่อ_คุณ_นะ | I (female) like your name.
# ผม_อา-ศัย_อยู่_ใน_ลอน-ดอน | I (male) live in London.
# ชื่อ-เล่น_ของ_ผม_คือ_ย่อ-มาน | My (male) nickname is Yoman.
# คุณ_มา_จาก-ไหน | Where are you from?
# เธอ_ทำ-ให้_ผม_มี-ความ-สุข | She makes me (male) happy.
# ฉัน_ชอบ_ทำ_ข-นม | I (female) like to make cakes.
# การ_กิน_พิซ-ซ่า_ทำ-ให้_ฉัน_อ้วน | Eating pizza makes me (female) fat.
# เรา_อยาก-ให้_คุณ_พูด_ภา-ษา-ไทย_ทุก_วัน | We want you to speak thai every day.
# ฉัน_มี_อะ-ไร_จะ_บอก_คุณ | I (female) have something to tell you.
# ฉัน_อยาก_คุย_กับ_คุณ | I (female) want to talk to you.
# อย่า_นอน_ดึก | Dont sleep (go to bed) late.
# อย่า_กิน_เหล้า_เยอะ | Dont drink too much alcohol.
# คุณ_ได้-ยิน_ฉัน_ไหม | Can you hear me (female)?
# ผม_ทำ_อา-หาร_เอง | I (male) cook myself.
# ผม_ไม่_ชอบ_กิน_คน-เดียว | I (male) dont like to eat alone.
# อา-หาร_โปรด_ของ_ฉัน_คือ_พิซ-ซ่า | My (female) favorite food is pizza.
# การ_กิน_อา-หาร_มาก-เกิน-ไป_ไม่_ดี | Eating too much food is not good.
# ฉัน_กิน_ข้าว | I (female) eat rice.
# คุณ_กิน_ข้าว | You eat rice.
# ผม_กิน_น้ำ | I (male) drink (colloquial) water.
# ผม_ไม่_ดื่ม_น้ำ | I (male) dont drink (colloquial) water.
# ฉัน_ไม่_เคย_เห็น_หิ-มะ | I (female) have never seen snow.
# เขา_ไม่_เคย_ไป_กรุง-เทพ | He has never been to Bangkok.
# หมา_ตัว_ใหญ่ | The dog is big.
# คุณ_พูด_ภา-ษา_ญี่-ปุ่น_ได้_ไหม | Can you speak Japanese?
# คุณ_พูด_ภา-ษา-ไทย_ได้_ไหม | Can you speak Thai?
# คุณ_พูด_ภา-ษา-อัง-กฤษ_ได้_ไหม | Can you speak English?
# พรุ่ง-นี้_ฉัน_จะ_ไป_กรุง-เทพ | I will go to Bangkok tomorrow.
# ฉัน_เคย_ไป_กรุง-เทพ | I have been to Bangkok.
# เรา_มา_จาก_อัง-กฤษ | We come from England.
# เขา_หล่อ | Hes handsome.
# พวก-เรา_ยัง_เด็ก | We (long form) are (still) young.
# ผม_เป็น_ด็ก-ผู้-ชาย | I am a boy.
# ผม_บิน_ไม่_ได้ | I (male) cant fly.
# เขา_อยาก_กลับ-บ้าน_เพราะ_เขา_เหนื่อย | He wants to go home because hes tired.
# ฉัน_ชอบ_อ่าน_หนัง-สือ | I (female) like to read books.
# ผม_ชอบ_อ่าน_หนัง-สือ_เกี่ยว-กับ_การ_ทำ_อา-หาร | I (male) like to read books about cooking.
# มะ-ม่วง_รา-คา_เท่า-ไหร่ | How much does a mango cost?
# ฉัน_อยาก_เป็น_ครู | I (female) want to become teacher.
# ฉัน_นั่ง_รถ-ไฟ-ฟ้า_เพราะ_มัน_เร็ว_กว่า | I (female) take the sky train because it is faster.
# ผม_กำ-ลัง_เรียน | I (male) am studying.
# คุณ_เป็น_ช้าง | You are an elephant.
# คุณ_ดูเ-หมือน_ลิง | You look like a monkey.
# ฉัน_จำ_ไม่_ได้ | I (female) dont remember.
# มัน_เป็น_รถ-ไฟ_วิ-เศษ | Its a magic train.
# รถ_ไฟ_มา_แล้ว | The train has arrived.
# วัน-นี้_เป็น_วัน_สุด-ท้าย_เหรอ_คะ | Is today the last day?
# คุณ_กำ-ลัง_พูด_อะ-ไร | What are you saying?
# คุณ_กำ-ลัง_คุย_เรื่อง_อะ-ไร_อยู่ | What are you talking about?
# มัน_ไม่_เหมือน_ใน_หนัง-สือ | Its not like in books.
# ทุก-คน_เปิด_หนัง-สือ_ของ_ตัว-เอง_ซะ | Everybody, open your book!
# ลง-น-รก_ไป_ซะ | Go to hell!
# คุณ_กำ-ลัง_อ่าน_หนัง-สือ_ไหม | Are you reading a book?
# เขา_ซื้อ_ให้_คุณ_เหรอ | He bought it for you, right?
# เค้ก_ที่_ฉัน_ให้_คุณ_เป็น_ยัง-ไง_บ้าง | How was the cake I sent you?
# คุณ_ซื้อ_เอง_เหรอ | You bought it yourself, right?
# คุณ_จะ_ซื้อ_มัน_เหรอ | You will buy it, right?
# ก-รุ-ณา_มา_กับ_ผม_เถอะ | Please come with me.
# คุณ_ไม่_ได้-ยิน_ที่_ฉัน_พูด_หรือ-ไง | Didnt you hear what I (female) said?
# ผม_ต้อง-การ_หุ่น-ยนต์_ที่_ฝัน_ได้ | I (male) want a robot that can dream.
# ฉัน_ถาม_ว่า_เขา_อยู่_ที่-ไหน | I (female) ask where he is.
# มัน_มา_จาก_ที่-ไหน | Where did it come from?
# ทำ-ไม_คุณ_ออก-มา_ไม่_ได้_ล่ะ | Why cant you come out?
# คุณ_อยู่_ที่-นี่_ดี_ไหม | Are you here for good?
# ทำ-ไม_คุณ_ยัง_อยู่_ที่-นี่ | Why are you still here?
# เรา_มี_สอบ_อา-ทิตย์ห-น้า | We have an exam next week.
# ฉัน_มี_ที-วี_สอง_เครื่อง | I (female) have two TVs.
# ฉัน_เห็น_พระ_สอง_รูป | I (female) see two monks.
# ฉัน_เชื่อ_ว่า_ฉัน_บิน_ได้ | I (female) believe I can fly.
# พวก-เขา_จะ_ทำ_อะ-ไร_ก่อน | What will they do first?
# คุณ_อยู่_บ้าน_ได้_ไหม | Can you be at home?
# คุณ_ชอบ_ฉัน_ใช่_ไหม | You like me (female), right?
# ผม_ไม่_ควร_อยู่_ที่-นี่ | I (male) should not be here.
# มัน_ควร_อยู่_ใน_รถ | It should be in the car.
# เขา_กิน_เยอะ | He eats a lot.
# เธอ_ไป_ที่-นั่น | She goes there.
# ผม_เกลียด_มัน | I (male) hate it.
# ฉัน_เกลียด_นั่น | I (female) hate that.
# ฉัน_รู้-จัก_เขา | I (female) know him.
# ฉัน_ไม่_รู้-จัก_เขา | I (female) dont know him.
# ผม_ต้อง_กลับ_ประ-เทศ_อังก-ฤษ_อา-ทิตย์_หน้า | I have to return to the United Kingdom next week.
# เธอ_ต้อง_ไป_รับ_แฟน_ของ_เธอ_ที่_ส-นาม-บิน | She has to pick up her boyfriend at the airport.
# คุณ_ไม่_ต้อง_ซื้อ_กา-แฟ_สอง_แก้ว | You dont have to buy two cups of coffee.
# วัน-นี้_ผม_ไม่_ต้อง_ทำ-อา-หาร | Today I (male) dont have to cook.
# เขา_ไม่_ควร_อยู่_หลัง_บ้าน | He shouldnt be behind the house.
# ฉัน_สาย_แล้ว | Im (female) late.
# เขา_คง-จะ_ไป_ตอน-นี้ | He will probably go now.
# คุณ_มี_เว-ลา_ว่าง_พอ_ไหม | Do you have enough free time?
# ฉัน_มี_เว-ลา_ไม่_พอ | I (female) dont have enough free time.
# พอ_แล้ว | enough already!
# คุณ_ใช้_เว-ลา_ว่าง_ที่-ไหน | Where do you spend your free time?
# คน-ไทย_ชอบ_พูด_ภา-ษา_อัง-กฤษ | Thai people like to speak English.
# ฉัน_ชอบ_เรียน_ภา-ษา-ไทย | I (female) like to study Thai.
# ฉัน_ไม่_ชอบ_เรียน_ภา-ษา-อัง-กฤษ | I (male) dont like to study English.
# ฉัน_มี_แมว | I (female) have a cat.
# คุณ_ชอบ_แมว_ไหม | Do you like cats?
# แมว_ของ_ผม_อยู่_บ้าน_ของ_ผม | My cat is in my house.
# แมว_พูด_ไม่_ได้ | Cats cant talk.
# ผม_คิด_ว่า_แมว_ชอบ_หมา_ได้ | I (male) think that cats can like dogs.
# คน-ไทย_ชอบ_แมว | Thai people like cats.
# ฉัน_อยาก_เรียน_ภา-ษา_แมว | I (female) want to learn cat language.
# ฉัน_ชอบ_เห็น_ยิ้ม_ของ_คุณ | I like to see your smile.
# คุณ_คือ_ใคร | Who are you?
# คุณ_ชอบ_คน-ไทย | You like Thai people.
# คน-ไทย_ชอบ_ผม | Thai people like me (male).
# คน-ไทย_ชอบ_ฉัน | Thai people like me (female).
# ผม_ชอบ_คน-ไทย | I (male) like Thai people.
# ฉัน_ชอบ_คน-ไทย | I (female) like Thai people.
# ผม_เป็น_คน-ไทย | I (male) am Thai.
# ฉัน_เป็น_คน-ไทย | I (female) am Thai.
# คน-ไทย_ชอบ_อยู่_บ้าน | Thai people like to be at home.
# คุณ_ชอบ_โรง-เรียน_ไหม | Do you like school?
# คุณ_ชอบ_อยู่_ที่_โรง-เรียน_ไหม | Do you like to be at school?
# เขา_ชอบ_โรง-เรียน_ไทย | He likes Thai school.
# คน-ไทย_ชอบ_โรง-เรียน_ไหม | Do Thai people like school?
# ผม_ชอบ_ไป_โรง-เรียน | I (male) like to go to school.
# ฉัน_อยาก_อยู่_บ้าน_กิน_ข้าว | I (female) want to be at home and eat.
# ฉัน_อยาก_กลับ-บ้าน_เรียน_ภา-ษา-ไทย | I (male) want to return home and study Thai language.
# เขา_อยาก_คุย_กับ_ฉัน | He wants to speak with me (female).
# เขา_ไม่_ชอบ_อยู่_บ้าน | He doesnt like to be at home.
# เขา_ไม่_ชอบ_โรง-เรียน_ไทย | He doesnt like Thai school.
# เขา_ไม่_อยาก_อยู่_โรง-เรียน | He doesnt want to be at school.
# ผม_ไม่_อยาก_ไป_โรง-เรียน | I (male) dont want to go to school.
# เขา_ไม่_ชอบ_พูด | He doesnt like to speak.
# เธอ_ไม่_อยาก_พูด | She doesnt want to speak.
# ฉัน_ดี-ใจ_ที่_คุณ_ชอบ_มัน | Im glad you like it.
# ฉัน_ไม่_ชอบ_ตะ-เกียบ_ไม้ | I (female) don''t like wooden chopsticks.
# ตุ๊ก-แก_เป็น_ส-กุล_ของ_สัตว์-เลื้อย-คลาน | Geckos are a family of reptiles.
# งู_เป็น_ส-กุล_ของ_สัตว์-เลื้อย-คลาน | Snakes are a family of reptiles.
# ตุ๊ก-แก_มี_ขา_มาก_กว่า_งู | Geckos have more legs than snakes.
# เพื่อน_ของ_เขา_กลาย-เป็น_วิศวกร_เมื่อ_ปี_ที่_แล้ว | His friend became an engineer last year.
# ขอบ-คุณ_มาก_ครับ | Thank you very much (said by a male)!
# ผม_กลัว_งู | I''m afraid of snakes.
# คุณ_ดู_สวย_มาก | You''re looking beautiful!
# คุณ_รู้_ไหม_ว่า_พระ-เจ้า_คือ_อะ-ไร | Do you know what a god is?
# ขอ-โทษ_ที่_ทำ-ให้_คุณ_ต้อง_รอ | Sorry to have made you have to wait.
# พวก-เขา_อา-ศัย_อยู่_ใน_ป่า | They live in the jungle.
# เรา_จะ_ไม่-เป็น-ไร | We''re going to be fine!
# คุณ_รู้-จัก_เขา_ไหม | Do you know him?
# คุณ_รู้_ไหม_ว่า_ทำ-ไม | Do you know why?
# ฉัน_คิด_ว่า_รอง-เท้า_คุณ_สกปรก_เกิน-ไป | I (female) think your shoes are too dirty!
# ฉัน_รู้_ว่า_คุณ_ไม่_ชอบ_ฉัน_แต่_ไม่-เป็น-ไร | I (female) know you dont like me, but its fine.
# ฉัน_กำ-ลัง_จะ_ตาย_เร็ว-ๆ-นี้_แต่_ไม่-เป็น-ไร | Im (female) going to die soon, but its fine.
# ฉัน_เห็น_หิ-มะ_เป็น_ครั้ง-แรก_ใน_แค-นา-ดา | I (female) saw snow for the first time in Canada.
# คุณ_เคย_ไป_มาเลเซีย_ไหม | Have you ever been to Malaysia?
# อา-หาร_ไทย_อ-ร่อย_มาก | Thai food is really delicious.
# ฉัน_ไป_เที่ยว_เวียด-นาม_และ_กัม-พู-ชา_ใน_ช่วง_ฤดู-หนาว | I (female) visited Vietnam and Cambodia during winter.
# คุณ_ชอบ_อา-หาร_ไทย_ไหม | Do you like Thai food?
# ฉัน_ไม่-ใช่_คน_ลาว | I''m (female) not Lao.
# เขา_ซื้อ_น้ำ_สับ-ปะ-รด_ให้_เธอ_แต่_เธอ_ป-ฏิ-เสธ_ที่_จะ_รับ_มัน | He bought her a pineapple juice but she refused to take it.
# ฉัน_คิด_ว่า_มะ-ม่วง_มี_ความ-หวาน_มาก_กว่า_สับ-ปะ-รด | I think mangoes are sweeter than pineapples.
# เด็ก-ๆ_ไม่_ชอบ_กิน_ผัก | The children don''t like eating vegetables.
# ผม_จะ_ขึ้น_รถ-ไฟ-ใต้-ดิน_ทุก-วัน_เมื่อ_ผม_อา-ศัย_อยู่_ใน_กรุง-เทพ | I will take the subway everyday when I live in Bangkok.
# ผม_ดี-ใจ_ที่_คุณ_ชอบ | I''m glad you like it (said by a male).
# ฉัน_ดี-ใจ_ที่_ได้_พบ_คุณ | I''m glad I met you (said by a female).
# ลา-ก่อน_ทุก-คน | Goodbye everybody!
# ฉัน_เริ่ม_หิว | I'm (female) getting hungry.
# ผม_หิว_น้ำ | I'm (male) hungry for water.
# บ้าน_ของ_ผม_อยู่_ใกล้_บ้าน_ของ_คุณ | My house (male) is close to your house.
# คุณ_ง่วง_รึ-ป่าว | Are you sleepy (or not?)
# ประ-เทศ_ฝ-รั่ง-เศส_อยู่_ใกล้_ประ-เทศ_อัง-กฤษ | France is close to Britain.
# ประ-เทศ_ไทย_ไกล_จาก_ประ-เทศ_อัง-กฤษ | Thailand is far from Britain.
# หนัง-สือ_เล่ม_นี้_ทำ-ให้_ฉัน_ง่วง-นอน | This book makes me (female) sleepy.
# ทุก-วัน_ผม_ขึ้น_รถ-ไฟ_ไป_ทํา-งาน | Every day, I take the train to work.
# อา-หาร_โปรด_ของ_ผม_คือ_พิซ-ซ่า | My favourite food is pizza.
# """
sentences = """"""
# sentences = """คุณ_ง่วง-นอน_รึ-ป่าว | Are you sleepy or not?"""
for sentence in sentences.split('\n'):
    # print(sentence)
    # try:
    split_values = sentence.split(' | ')
    thai, english = split_values[0], split_values[1]

    insert_sentence(thai, english)
    # except:
    #     pass
        # print('error with the following:')
        # print(sentence)
