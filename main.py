from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import os
import sqlite3

from sqlclass import USER_DATA

Current_User_Data = USER_DATA()

BOT_TOKEN = "BOT_TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

awaiting_video = set()
awaiting_name = set()
awaiting_change = set()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет!")


@dp.message_handler(commands=['add_video_to_database'])
async def add_video_command(message: types.Message):
    await message.reply("Пожалуйста, отправьте кружочек с вашим лицом.")
    awaiting_video.add(message.from_user.id)


@dp.message_handler(content_types=types.ContentType.VIDEO_NOTE)
async def handle_video_note(message: types.Message):
    user_id = message.from_user.id
    if user_id in awaiting_video:
        video_note = message.video_note
        file = await bot.get_file(video_note.file_id)
        video_path = f"videos/{user_id}_{video_note.file_id}.mp4"
        await bot.download_file(file.file_path, video_path)
        # AI Work
        await bot.send_message(user_id, "Теперь отправьте свое ФИО (через пробел) и уровень доступа.")
        awaiting_name.add(user_id)
        awaiting_video.remove(user_id)


@dp.message_handler(lambda message: message.from_user.id in awaiting_name)
async def handle_name_data(message: types.Message):
    user_id = message.from_user.id
    _user_data = message.text.split()
    if len(_user_data) < 4:
        await bot.send_message(user_id, "Введите Фамилию Имя Отчество и уровень доступа через пробел.")
    else:
        Current_User_Data.add_user(user_id, _user_data[0], _user_data[1], _user_data[2], int(_user_data[3]))
        await bot.send_message(user_id, "Данные успешно добавлены.")
        awaiting_name.remove(user_id)


@dp.message_handler(commands=['change_access_level'])
async def change_access_level_command(message: types.Message):
    await message.reply('Введите ФИО и новый уровень доступа.')
    awaiting_change.add(message.from_user.id)


@dp.message_handler(lambda message: message.from_user.id in awaiting_change)
async def handle_access_level_change(message: types.Message):
    user_id = message.from_user.id
    _text = message.text.split()
    if len(_text) < 4:
        await bot.send_message(user_id, "Введите Фамилию Имя Отчество и новый уровень доступа через пробел.")
    else:
        Current_User_Data.update_access_level(_text[0], _text[1], _text[2], int(_text[3]))
        await bot.send_message(user_id, "Данные обновлены!")
        awaiting_change.remove(user_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
