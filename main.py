import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
import pyrebase

firebaseConfig = {"apiKey": "AIzaSyB3wPtzFhFr0mGn5acHeZvQN6TqSXAdPlo",

                  "authDomain": "firrst--project-with-firebase.firebaseapp.com",

                  "databaseURL": "https://firrst--project-with-firebase-default-rtdb.firebaseio.com",

                  "projectId": "firrst--project-with-firebase",

                  "storageBucket": "firrst--project-with-firebase.appspot.com",

                  "messagingSenderId": "1063364478119",

                  "appId": "1:1063364478119:web:d7fdcb005de23a48e98782",

                  "measurementId": "G-99DXRSNJJP"
                  }

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

load_dotenv()


API_TOKEN = os.getenv("token")
channel_id = os.getenv("channel_key")
group_id = os.getenv("group_key")


# Configure logging

logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# inline keyboard buttons
book1 = InlineKeyboardButton('References', callback_data="reference")  # buttons for reference
book2 = InlineKeyboardButton('TextBook', callback_data="textbook")  # buttons for textbook
key2 = InlineKeyboardMarkup().add(book1, book2)

audio = InlineKeyboardButton('Audio book', callback_data="audio")  # buttons for audio
video = InlineKeyboardButton('video', callback_data="video")  # buttons for video
key3 = InlineKeyboardMarkup().add(audio, video)

IELTS = InlineKeyboardButton('IELTS', callback_data='IELTS')
key4 = InlineKeyboardMarkup().add(IELTS)

btn1 = KeyboardButton('Books📚')
btn2 = KeyboardButton('Tutorial📹')
btn3 = KeyboardButton('IELTS')
btn4 = KeyboardButton('About us👥')

#Bot initialiser with Database
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    print(message)
    if message.chat.type == "private":
        data = {
            message.chat.id: {
                "first_name": message.chat.first_name,
                "last_name": message.chat.last_name,
                "username": message.chat.username,
            }
        }
        db.child('Users').update(data)
        await bot.send_message(group_id, f"User {message.chat.mention} clicked /start")

        btn = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1, btn2) .add(btn3, btn4).add(KeyboardButton("School fee"))

        await message.answer(f"Hi! {message.from_user.first_name}\nI'm Victory Wisdom bot!\ni'm here to provide our service", reply_markup=btn)


@dp.message_handler()  # handling input messages form the reply keyboard buttons
async def first_answer(message: types.Message):
    print(message)
    if message.text == 'Books📚':
        data = {
            message.chat.id: {
                "first_name": message.chat.first_name,
                "last_name": message.chat.last_name,
                "username": message.chat.username,
            }
        }
        db.child('Users').update(data)
        await bot.send_message(group_id, f"User {message.chat.mention} \n clicked #Books button")
        await message.answer('Textbook written source of information, designed specifically for the use of students, on a particular subject or field of study that is usually developed based on a syllabus and geared towards meeting specific quality and learning requirements.\n \nReferences is an option where you can get books that will boost your grades including precious guides and some important books.', reply_markup=key2)
    elif message.text == "Tutorial📹":
        data = {
            message.chat.id: {
                "first_name": message.chat.first_name,
                "last_name": message.chat.last_name,
                "username": message.chat.username,
            }
        }
        db.child('Users').update(data)
        await bot.send_message(group_id, f"User {message.chat.mention} \n clicked #tutorial button")
        await message.answer('TUTORIALS with live tutors are useful for both advanced students and struggling ones.', reply_markup=key3)
    elif message.text == "IELTS":
        data = {
            message.chat.id: {
                "first_name": message.chat.first_name,
                "last_name": message.chat.last_name,
                "username": message.chat.username,
            }
        }
        db.child('Users').update(data)
        await bot.send_message(group_id, f"User {message.chat.mention} \n clicked #IELTS button")
        await message.answer('IELTS is an English language test for study, migration or work. Over three million people take our test every year. IELTS is accepted by more than 11,000 employers, universities, schools and immigration bodies around the world.', reply_markup=key4)
    elif message.text == "About us👥":
        data = {
            message.chat.id: {
                "first_name": message.chat.first_name,
                "last_name": message.chat.last_name,
                "username": message.chat.username,
            }
        }
        db.child('Users').update(data)
        await bot.send_message(group_id, f"User {message.chat.mention} \n clicked #About button")
        await message.answer('VICTORY WISDOM SCHOOL \n \n We are working for more than 10 years teaching English with American & British Accent \n    💼ceo & Founder \n   👨‍🏫[SEYFEDIN TAHIR](https://t.me/victorywisdombot)\n    💼Director\n   👨‍🏫[JEMAL KEDIR](https://t.me/Kedir_ka_jemummela)\n    💼Bot Developer\n   👨‍💻[MIKIGODE](https://t.me/mikigode)\n\nThis bot available in cloud 2023', parse_mode="MARKDOWN")
    elif message.text.startswith('/get_book'):
        ids = message.text.split("_")[2]
        print(ids)
        await bot.copy_message(message.chat.id, channel_id, int(ids))
        

# handling callback data for reference and textbook
@dp.callback_query_handler(text=['reference', 'textbook'])
async def call(call: types.CallbackQuery):
    await call.message.delete()
    if call.data == 'reference':
        await call.message.answer('choose the book for reference\nEnglish like American \n👉 /get_book_7\nVocabulary \n👉 /get_book_9\n Writing skills \n👉 /get_book_10\n \nshare the bot for every one who want to learn english @victorywisdombot')
    if call.data == 'textbook':
        await call.message.answer('choose the book for textbook\nBusiness communication \n👉 /get_book_11\nLearn speed reading \n👉 /get_book_16\n \nshare the bot for every one who want to learn english https://t.me/victorywisdombot')
    else:
        await call.answer()


# handling callback data for audio and video
@dp.callback_query_handler(text=['audio', 'video'])
async def call(call: types.CallbackQuery):
    await call.message.delete()
    if call.data == 'audio':
        await call.message.answer('Audio book\n \nchoose the link for Audio book\n \n audio book 01 \n👉 /get_book_13\naudio book 02 \n👉 /get_book_14\naudio book 03 \n👉 /get_book_15')
    if call.data == 'video':
        await call.message.answer('coming soon 😊\n just join the channel and Groups until we post video tutorials')
    else:
        await call.answer()

#handling callback data for IELTS
@dp.callback_query_handler(text=['IELTS'])
async def call(call: types.CallbackQuery):
    await call.message.delete()
    if call.data == 'IELTS':
        await call.message.answer('IELTS \n \nHere are links for preparation for IELTS examination.\nIELTS reading-QUICK STUDY\n👉 /get_book_17\nIELTS reading- target\n👉 /get_book_18\nIELTS speaking question\n👉 /get_book_19\nIELTS speaking Topics\n👉 /get_book_20\nIELTS speaking Module\n👉 /get_book_21')
    else:
        await call.answer()

# @dp.message_handler(commands=['get_book'])
# async def get_book(message: types.Message):
#     ids = message.text.split(" ")[1]
#     print(ids)
#     await bot.copy_message(message.chat.id, channel_id, int(ids))



# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text)
#     print(message)



if __name__ == '__main__':

    executor.start_polling(dp, skip_updates=True)