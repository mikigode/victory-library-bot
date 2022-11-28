import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

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

btn1 = KeyboardButton('Menu🏠')
btn2 = KeyboardButton('Books📚')
btn3 = KeyboardButton('Tutorial📹')
btn4 = KeyboardButton('About us👥')

#Bot initialiser
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    btn = ReplyKeyboardMarkup(resize_keyboard=True).add(btn1, btn2) .add(btn3, btn4).add(KeyboardButton("Channel🔙"))
    print(message)

    await message.answer(f"Hi! {message.from_user.first_name}\nI'm Victory Wisdom bot!\nPowered by @mikigode", reply_markup=btn)


@dp.message_handler()  # handling input messages form the reply keyboard buttons
async def first_answer(message: types.Message):
    if message.text == 'Menu🏠':
        await message.answer('select your desire ', reply_markup=key2)
    elif message.text == "Books📚":
        await message.answer('select your Book', reply_markup=key2)
    elif message.text == "Tutorial📹":
        await message.answer('coming soon 😊', reply_markup=key3)
    elif message.text == "About us👥":
        await message.answer('coming soon 😊', reply_markup=key2)
    elif message.text.startswith('/get_book'):
        ids = message.text.split("_")[2]
        print(ids)
        await bot.copy_message(message.chat.id, channel_id, int(ids))
        

# handling callback data for reference and textbook
@dp.callback_query_handler(text=['reference', 'textbook'])
async def call(call: types.CallbackQuery):
    await call.message.delete()
    if call.data == 'reference':
        await call.message.answer('choose the book for reference\n/get_book_7\n/get_book_8')
    if call.data == 'textbook':
        await call.message.answer('choose the book for textbook\nExample1\nExample2')
    else:
        await call.answer()


# handling callback data for audio and video
@dp.callback_query_handler(text=['audio', 'video'])
async def call(call: types.CallbackQuery):
    await call.message.delete()
    if call.data == 'audio':
        await call.message.answer('choose the button for Audio book\nExample1\nExample2')
    if call.data == 'video':
        await call.message.answer('choose the button for Video\nExample1\nExample2')
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