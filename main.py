from aiogram import *
from aiogram.types import *
from aiogram.utils import executor
from pymongo import MongoClient
import time

TOKEN = "5852292493:AAFU7dwYnCBfP7MCiLdgObP1zZ8V4S7gpkU"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

myclient = MongoClient("mongodb+srv://feruzbek:user12345@cluster0.ljiyuky.mongodb.net/?retryWrites=true&w=majority")
mydb = myclient["sources"]
peoples = mydb["users"]
contests = mydb["contests"]

# ----------- variables --------------
s1 = InlineKeyboardButton(text='Boshlash', callback_data='start')
s2 = InlineKeyboardButton(text='Tugatish', callback_data='stop')
s3 = InlineKeyboardButton(text="O'chirish", callback_data='delete')
s4 = InlineKeyboardButton(text="Qatnashish", callback_data='qatnashish')
s5 = InlineKeyboardButton(text="Ro'xatdan o'tish", callback_data='ariza')
startt = InlineKeyboardMarkup().row(s1)
stop = InlineKeyboardMarkup().row(s2)
delete = InlineKeyboardMarkup().row(s3)
qatnashish = InlineKeyboardMarkup().row(s4)
ariza = InlineKeyboardMarkup().row(s5)

classes = ReplyKeyboardMarkup(resize_keyboard=True).row('5-sinf', '6-sinf').row('7-sinf', '8-sinf').row('9-sinf', '10-sinf').row('11-sinf')
ssssss = ReplyKeyboardMarkup(resize_keyboard=True).row("Ro'yxatdan o'tish")
yana = ReplyKeyboardMarkup(resize_keyboard=True).row("Qidirish 🔍", "Keyingi ➡️").row("Asosiy menyu")

pppp = ReplyKeyboardMarkup(resize_keyboard=True).row("Javoblarni yuborish").row("Tugatish")
menu_btn = ReplyKeyboardMarkup(resize_keyboard=True).row("🏆 Olimpiada", "📜 Olimpiada natijalari").row("👤 Foydalanuvchilar", "🔒 Profile")
schools = ReplyKeyboardMarkup(resize_keyboard=True)
menu_admin = ReplyKeyboardMarkup(resize_keyboard=True).row("➕ Olimpiada qo'shish").row("🏆 Olimpiada", "📜 Olimpiada natijalari").row("👤 Foydalanuvchilar", "🔒 Profile")
cancel = ReplyKeyboardMarkup(resize_keyboard=True).row("Bekor qilish")
add_about = False
add_contest =0
olimp = ''
search = False
names = []
read_ans = False
signup = 0
klasses = ['5-sinf', '6-sinf','7-sinf', '8-sinf', '9-sinf', '10-sinf', '11-sinf']


def check_user():
    global users
    users = []
    x = peoples.find()
    for i in x:
        users.append(i["id"])



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    
    if message.from_user.username == "Feruzbek_Sapayev":
            await message.answer(f"👋Assalomu aleykum *F E R U Z B E K*.", reply_markup=menu_admin, parse_mode='Markdown')
    else:
        check_user()
        if message.from_user.id in users:
            await message.answer(f"👋Assalomu aleykum *{message.from_user.first_name}*.", reply_markup=menu_btn, parse_mode='Markdown')
        else:
            await message.answer(f"👋Assalomu aleykum hurmatli *{message.from_user.first_name}*. Ushbu botda har xil fanlardan online olimpiadalar o'tkaziladi. Botdan foydalanish uchun avval ro'yxatdan o'ting!", reply_markup=ssssss, parse_mode='Markdown')
    
@dp.message_handler()
async def events(message: types.Message):
    global add_about, signup, full_name, school, sinf, add_contest, link, description, answers, tt, test_img, olimp, mt, read_ans, true_ans, rounds, names, search
    if message.text == "Ro'yxatdan o'tish":
        signup = 1
        await message.answer("Ismingiz va familiyangizni yuboring:")
    elif message.content_type == 'text' and signup == 1 and message.text != "Ismingiz va familiyangizni yuboring:":
        full_name = message.text
        await message.answer("Yaxshi! Endi qaysi maktabda o'qishingizni kiriting!")
        signup = 2
    elif message.content_type == 'text' and signup == 2 and message.text != "Yaxshi! Endi qaysi maktabda o'qishingizni kiriting!":
        school = message.text
        await message.answer("Yaxshi! Endi nechinchi sinfda o'qishingizni tanlang!", reply_markup=classes)
        signup = 3
    elif message.content_type == 'text' and signup == 3 and message.text in klasses:
        sinf = message.text
        signup = 0
        data = {'id': message.from_user.id,'name': full_name, 'school': school, 'clas': sinf, 'rating': 0, 'contests': 0}
        peoples.insert_one(data)
        await message.answer(f"*Siz ro'yxatdan o'tdingiz✅\n*🔹 Ism-Familiya - {full_name}\n🔹 Maktab - {school}\n🔹 Sinf - {sinf}",reply_markup=menu_btn, parse_mode='Markdown')


    elif message.text == "➕ Olimpiada qo'shish" and message.from_user.username == "Feruzbek_Sapayev":
        add_contest = 1
        await message.answer("Contest rasmi linkini yuboring!", reply_markup=cancel)

    elif message.content_type == 'text' and add_contest == 1 and message.text != 'Bekor qilish':
        if 'https://t.me' in message.text:
            link = message.text
            add_contest = 2
            await message.answer("Yaxshi, endi olimpiada haqida yuboring!", reply_markup=cancel)
        else:
            await message.answer("Link xato kiritildi! Tekshirib qayta yuboring!", reply_markup=cancel)

    elif message.content_type == 'text' and add_contest == 2 and message.text != 'Bekor qilish':
        description = message.text
        await message.answer("Yaxshi, endi testni linkini yuboring!", reply_markup=cancel)
        add_contest = 3

    elif message.content_type == 'text' and add_contest == 3 and message.text != 'Bekor qilish':
        test_img = list(map(str, message.text.split()))
        await message.answer("Yaxshi, endi to'g'ri javoblarni yuboring 'ABCD...'", reply_markup=cancel)
        add_contest = 4
    
    elif message.content_type == 'text' and add_contest == 4 and message.text != 'Bekor qilish':
        answers = message.text
        await message.answer("Yaxshi, endi olimpiada qaysi sinfga tegishliligini yuboring! (masalan: 11- sinfga tegishli bo'lsa, 11", reply_markup=cancel)
        add_contest = 5

    elif message.content_type == 'text' and add_contest == 5 and message.text != 'Bekor qilish':
        tt = message.text
        if '0'<=tt<='9':
            t = contests.find()
            r = 0
            for i in t:
                r+=1
            name = "Round " + str(r+1)
            data = {'name': name,'link': link, 'images': test_img,  'about': description, 'answers': answers, 'clas': tt, 'holati': 'boshlanmagan', 'azolar': [],'ballar': []}
            contests.insert_one(data)
            await message.answer("Olimpiada muvaffaqiyatli qo'shildi!", reply_markup=menu_admin)
            add_contest = 0

        else:
            await message.answer("Xatolik, son kiriting!", reply_markup= cancel)
        
    if (message.text == 'Bekor qilish' and add_contest>0):
        add_contest = 0
        await message.answer("Bekor qilindi!", reply_markup=menu_admin)
    if (message.text == 'Bekor qilish' and search):
        search = False
        await message.answer("Bekor qilindi!", reply_markup=yana)
    
    if message.text == "🏆 Olimpiada":
        if message.from_user.username == "Feruzbek_Sapayev":
            x = contests.find()
            t = False
            for  i in x:
                if i['holati'] == 'boshlanmagan':
                    t = True
                    olimp = i['name']
                    ds = '*'+i['about']+'\n\nHolati - ' + i['holati'] + "\nQatnashuvchilar - "+ str(len(i['azolar']))+'*'
                    await bot.send_photo(chat_id=message.chat.id, photo=i['link'], caption=ds, reply_markup=startt, parse_mode="Markdown")
                
                elif i['holati'] == "o'tkazilmoqda":
                    t = True
                    olimp = i['name']
                    ds = '*'+i['about']+'\n\nHolati - ' + i['holati'] + "\nQatnashuvchilar - "+ str(len(i['azolar']))+'*'
                    await bot.send_photo(chat_id=message.chat.id, photo=i['link'], caption=ds, reply_markup=stop, parse_mode="Markdown")
            if not(t):
                await message.answer("Hozircha o'tkaziloyatgan yoki boshlanmagan olimpiada yo'q!")
                
                
        else:
            x = contests.find()
            
            t = False
            for  i in x:
                if i['holati'] == "o'tkazilmoqda":
                    olimp = i['name']
                    t = True
                    ds = '*'+i['about']+'\n\nHolati - ' + i['holati'] + "\nQatnashuvchilar - "+ str(len(i['azolar']))+'*'
                    await bot.send_photo(chat_id=message.chat.id, photo=i['link'], caption=ds, reply_markup=qatnashish, parse_mode="Markdown")
                elif i['holati'] == 'boshlanmagan':
                    olimp = i['name']
                    t = True
                    ds = '*'+i['about']+'\n\nHolati - ' + i['holati'] + "\nQatnashuvchilar - "+ str(len(i['azolar']))+'*' 
                    await bot.send_photo(chat_id=message.chat.id, photo=i['link'], caption=ds, reply_markup=ariza, parse_mode="Markdown")
            if not(t):
                await message.answer("Hozircha o'tkaziloyatgan yoki boshlanmagan olimpiada yo'q!")

    
    if message.text == "Javoblarni yuborish":
        
        x = contests.find()
        for i in x:
            if i['name'] == olimp:
                holati = i["holati"]
                true_ans = i['answers']
                break
        if holati == "o'tkazilmoqda":
            read_ans = True
            await message.answer("Javoblaringni shu tartibda yuboring: ABSD...")
    elif read_ans and message.text != "Javoblaringni shu tartibda yuboring: ABSD...":
        ans = message.text
        if not(' ' in ans) and not('0' in ans or '1' in ans or '2' in ans or '3' in ans or '4' in ans or '5' in ans or '6' in ans or '7' in ans or '8' in ans or '9' in ans ) and len(ans) == len(true_ans):
            ball = 0
            for i in range(len(ans)):
                if ans[i].upper() == true_ans[i]:
                    ball += 1
            x = contests.find()
            for i in x:
                if i['name'] == olimp:
                    azolar = i['azolar']
                    balls = i['ballar']
            balll = (ball*100)//(len(true_ans))
            t = peoples.find()
            for i in t:
                if i['id'] == message.from_user.id:
                    bali = i['rating']
            bali+=balll
            index = azolar.index(message.chat.id)
            balls[index] = balll
            peoples.update_one(
                {"id": message.from_user.id},
                {"$set":{"rating": bali}}
            )
            contests.update_one(
                {"name": olimp},
                {"$set":{"ballar": balls}}
            )
            await message.answer(f"Javoblaringiz qabul qilindi! To'g'ri javoblar soni - {ball}", reply_markup= menu_btn)
            read_ans = False
        else:
            await message.answer("Javoblar xato kiritildi! Hamma savolga javob yozilganini yoki raqam qatnashmaganini tekshiring! ")
    if message.text == 'Tugatish':
        await message.answer('Siz olimpiadani yakunladingiz! Natijangiz - 0', reply_markup=menu_btn)
    
    if message.text == "📜 Olimpiada natijalari":
        names = []
        rounds = ReplyKeyboardMarkup(resize_keyboard=True)
        x = contests.find()
        p = []
    
        for  i in x:
            names.append(i['name'])
            if i['holati'] == "tugagan":
                olimpp = i['name']
                p.append(olimpp)
        p.reverse()
        for i in p:
            rounds.add(i)
        rounds.add('Asosiy menyu')
        await message.answer("Marhamat, olimpiadalardan birini tanlang!", reply_markup=rounds)
    
    if message.text == 'Asosiy menyu':
        if message.from_user.username == "Feruzbek_Sapayev":
            await message.answer("Siz asosiy menyudasiz!", reply_markup=menu_admin)
        else:
            await message.answer("Siz asosiy menyudasiz!", reply_markup=menu_btn)


    if message.text in names:
        t = contests.find()
        for i in t:
            if i['name'] == message.text:
                linkk = i['link']
                ballar = i['ballar']
                disc = i['about']
                status = i['holati']
                azo = i['azolar']
                
                if len(azo)>0:
                    id1 = azo[0]
                    p = peoples.find()
                    for k in p:
                        if k['id'] == id1:
                            id1 = k['name']
                else:
                    id1 = ''
                if len(azo)>1:
                    id2 = azo[1]
                    p = peoples.find()
                    for k in p:
                        if k['id'] == id2:
                            id2 = k['name']
                else:
                    id2=''
                if len(azo)>2:
                    id3 = azo[2]
                    p = peoples.find()
                    for k in p:
                        if k['id'] == id3:
                            id3 = k['name']
                else:
                    id3 = ''
                
                myid = message.from_user.id
                if myid in azo:
                    myplace = "\n\n   Siz ushbu olimpiadada "+str(azo.index(myid)+1) + "-o'rinni egalladingiz!"
                else:
                    myplace = "\n\n   Siz ushbu olimpiadada ishtirok etmagansiz!"
                disc='*'+disc
                if len(azo)>2:
                    disc+="\n\n   🥇  " + str(id1) +"\n\n   🥈  " + str(id2)+ "\n\n   🥉  " + str(id3) + myplace +  '\n\nHolati - ' + status + "\nQatnashuvchilar - "+ str(len(azo))
                if len(azo)==2:
                    disc+="\n\n   🥇  " + str(id1) +"\n\n   🥈  " + str(id2) + myplace +  '\n\nHolati - ' + status + "\nQatnashuvchilar - "+ str(len(azo))
                elif len(azo)==1:
                    disc+="\n\n   🥇  " + str(id1) + myplace +  '\n\nHolati - ' + status + "\nQatnashuvchilar - "+ str(len(azo))
                elif len(azo) == 0:
                    disc+="\n\n   Ushbu olimpiadada hech kim qatnashmagan!" +  '\n\nHolati - ' + status + "\nQatnashuvchilar - "+ str(len(azo))
                await bot.send_photo(chat_id = message.chat.id, photo= linkk, caption=disc+'*', reply_markup=rounds, parse_mode="Markdown")
                
                break
    global namess, schoolss, classesss, ratings, contestss, no
    if message.text == "👤 Foydalanuvchilar":
        t = peoples.find().sort("rating", -1)
        namess = []
        schoolss = []
        classesss = []
        ratings = [] 
        contestss = []
        l = ''
        no = 0
        for i in t:
            namess.append(i['name'])
            schoolss.append(i['school'])
            classesss.append(i['clas'])
            ratings.append(i['rating'])
            contestss.append(i['contests'])
        for i in range(len(namess)):
            no = i
            if i == 0:
                l += f"🥇. {namess[i]}  {ratings[i]}\n"
            elif i == 1:
                l += f"🥈. {namess[i]}  {ratings[i]}\n"
            elif i == 2:
                l += f"🥉. {namess[i]}  {ratings[i]}\n"
            else:
                l += f"{i+1}. {namess[i]}  {ratings[i]}\n"
            if i == 19:
                break
        await message.answer('*'+l+'*', reply_markup=yana, parse_mode="Markdown")
        await message.answer("Kimningdir profilini ko'rmoqchi bo'lsangiz, *'Qidirish 🔍'* tugmasini bosing!", parse_mode="Markdown")
    
    if message.text == "Keyingi ➡️":
        l = '*'
        if len(namess)-no>no:
            for i in range(no+1, len(namess)):
                no = i
                if no == 0:
                    l += f"🥇. {namess[no]}  {ratings[no]}\n"
                elif no == 1:
                    l += f"🥈. {namess[no]}  {ratings[no]}\n"
                elif no == 2:
                    l += f"🥉. {namess[no]}  {ratings[no]}\n"
                else:
                    l += f"{no+1}. {namess[no]}  {ratings[no]}\n"
            await message.answer('*'+l+'*', reply_markup=yana, parse_mode="Markdown")
            
        else:
            await message.answer("Foydalanuvchilar tugadi!", reply_markup=yana)
    
    if message.text == "Qidirish 🔍":
        search = True
        await message.answer("Foydalanuvchi ismini yoki familiyasini kiriting!", reply_markup=cancel)
    if search and message.text != "Qidirish 🔍":
        hh = False
        ss = str(message.text).upper()
        for i in range(len(namess)):
            p = '*'
            if ss in namess[i].upper():
                hh = True
                p += f"Ism-familiya - {namess[i]}\nMaktab - {schoolss[i]}\nSinfi - {classesss[i]}\nReytingi - {ratings[i]}\nQatnashgan olimpiadalar soni - {contestss[i]}"
                await message.answer(p+'*', reply_markup=yana, parse_mode="Markdown")
        if not(hh):
            await message.answer("Foydalanuvchi topilmadi", reply_markup=yana)
        search = False

    if message.text == "🔒 Profile":
        t = peoples.find()
        ll = ''
        for i in t:
            if i['id'] == message.from_user.id:
                ll+=f"*Ism* - _{i['name']}_\n\n*Maktab* - _{i['school']}_\n\n*Sinf* - _{i['clas']}_\n\n*Reyting* - _{i['rating']}_\n\n*Qatnashgan olimpiadalar* - _{i['contests']}_"
                await message.answer(ll, parse_mode="Markdown")
                break






@dp.callback_query_handler(text = ['start', 'stop', 'delete', 'qatnashish', 'ariza'])
async def events(call: types.CallbackQuery):
    chat_id = call.from_user.id
    if call.data == 'start':
        contests.update_one(
            {"name": olimp},
            {"$set":{"holati": "o'tkazilmoqda"}}
        )
        await call.answer("Olimpiada boshlandi!")

    elif call.data == 'stop':
        mtt = []
        ball = []
        sortt = []
        t = contests.find()
        
        for i in t:
            
            if i['name'] == olimp:
                mtt = i['azolar']
                ball = i['ballar']
                
        for i in ball:
            sortt.append(i)
        sortt.sort()
        sortt.reverse()
        
        while not(sortt == ball):
            for i in range(len(ball)-1):
                if ball[i]<ball[i+1]:
                    t = ball[i]
                    ball[i] = ball[i+1]
                    ball[i+1] = t
                    tt = mtt[i]
                    mtt[i] = mtt[i+1] 
                    mtt[i+1] = tt
        
        contests.update_one(
            {"name": olimp},
            {"$set":{"holati": "tugagan"}}
        )
        contests.update_one(
            {"name": olimp},
            {"$set":{"azolar": mtt}}
        )
        contests.update_one(
            {"name": olimp},
            {"$set":{"ballar": ball}}
        )
        await call.answer("Olimpiada tugadi!")
    
    elif call.data == 'delete':
        contests.delete_one(
            {"name": olimp}
        )
        await call.answer("Olimpiada o'chirildi!")
    
    elif call.data == 'qatnashish':
        mt = []
        ball = []
        t = contests.find()
        for i in t:
            if i['name'] == olimp:
                imgs = i['images']
                mt = i['azolar']
                ball = i['ballar']
                klas = i['clas']
                break
        x = peoples.find()
        for i in x:
            if i['id'] == chat_id:
                clas = i['clas']
        if  klas + '-sinf' == clas:
            if (chat_id in mt):
                index = mt.index(chat_id)
                y = ball[index]    
                if y != 0:
                    await call.answer("Siz ushbu olimpiadada ishtirok etib bo'lgansiz!")
                else:
                    for i in imgs:
                        await call.message.answer_photo(photo=i)
                    await call.message.answer("Siz ushbu olimpiadada ishtirok etyapsiz!\nOmad tilaymiz!", reply_markup=pppp)
            else:
                mt.append(chat_id)
                ball.append(0)
                contests.update_one(
                {"name": olimp},
                {"$set":{"azolar": mt}}
                )
                contests.update_one(
                {"name": olimp},
                {"$set":{"ballar": ball}}
                )
                for i in imgs:
                    await call.message.answer_photo(photo=i)
                await call.message.answer("Siz ushbu olimpiadada ishtirok etyapsiz!\nOmad tilaymiz!", reply_markup=pppp)
        else:
            await call.answer(f'Ushbu olimpiada faqat {klas}-sinflar uchun!')



    elif call.data == 'ariza':
        mt = []
        ball = []
        x = contests.find()
        for i in x:
            if i['name'] == olimp:
                mt = i['azolar']
                ball = i['ballar']
                break
        if not(chat_id in mt):
            mt.append(chat_id)
            ball.append(0)
            contests.update_one(
                {"name": olimp},
                {"$set":{"azolar": mt}}
            )
            contests.update_one(
                {"name": olimp},
                {"$set":{"ballar": ball}}
            )
            await call.answer("Siz ro'yxatdan o'tdingiz!")

        else:
            await call.answer("Siz allaqachon ro'yxatdan o'tgansiz!")

    await call.answer()



if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)


# ROUND 1

#  🔹Fani - Matematika
#  🔹Sinf - 11 - sinf
#  🔹Savollar soni - 30 ta
#  🔹Boshlanish vaqti - 12:00 02.02.2023

# Hammaga omad tilaymiz!