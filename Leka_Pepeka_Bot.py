import os
import asyncio
from datetime import datetime

import random

import pytz
import aiogram
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

import json

# Загрузка токена и ID канала из файла .env
load_dotenv()

# Константы с путём
channel_id = os.getenv('CHANNEL_ID')
media_path = os.getenv('MEDIA_PATH')
token = os.getenv('TOKEN')
time_sleep = int(os.getenv('TIME_SLEEP'))

# Создание бота и диспетчера
bot = Bot(token=token)
dp = Dispatcher(bot=bot)

media = {}


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAMpZBAAAfU09xqQuhom1s8wBMW98ausAAI4CwACTuSZSzKxR9LZT4zQLwQ')
    await message.answer(f'{message.from_user.first_name}, добро пожаловать в мемный рай!')
    await asyncio.sleep(1)
    await message.answer(f'Отправь мне или перешли от другого пользователя или канала фото или видео,'
                         f' и они автоматически будут отправляться в твой канал каждый час c 8 утра '
                         f'и до 24 часов вечера, каждый день, пока не закончаться.')


@dp.message_handler(content_types=['photo', 'video'])
async def handle_media(message: types.Message):
    if message.content_type == 'photo':
        # Добавление в media в котором ключ это id сообщения всю необходимую информацию
        media[message.message_id] = {
            'media_group_id': message.media_group_id,
            'file_id': message.photo[-1].file_id,
            'content_type': message.content_type
        }

    elif message.content_type == 'video':
        media[message.message_id] = {
            'media_group_id': message.media_group_id,
            'file_id': message.video.file_id,
            'content_type': message.content_type
        }

    # Чтение содержимого JSON-файла
    with open('media.json', 'r') as f:
        data = json.load(f)

    # Добавление к текущей информации в json новую
    data.update(media)

    # Запись в json обновлённой информации
    with open('media.json', 'w') as f:
        json.dump(data, f, indent=4)
        # Очистка содержимого переменной media
        media.clear()


    #
    #
    # # # Очищаем информацию о фото и видео из переменной media
    # # media.clear()
    #
    # # пауза перед отправкой
    # await asyncio.sleep(15)
    #
    # with open('media.json') as f:
    #     data = json.load(f)
    #     # Распаковываем список списков
    #     for i in data:
    #         # Проверяем, это 1 сообщение или это несколько файлов в сообщении(Если None то в сообщении один файл)
    #         if i[0] is None:
    #             # Если тип файла фото, то отправляем фото
    #             if i[-1] == 'photo':
    #                 await bot.send_photo(channel_id, i[-2])
    #             elif i[-1] == 'video':
    #                 await bot.send_video(channel_id, i[-2])
    #
    #             # удаляем из списка информацию об отправленном фото
    #             del data[data.index(i)]
    #             # Удаляем из списка медиа наш элемент потому что там он тоже хранится, а иначе он повторно перезапишется когда боту будет отправлен новый файл
    #             media.remove(i)
    #
    #             # Записываем обновлённую информацию в наш список.
    #             with open('media.json', 'w') as f:
    #                 json.dump(data, f)
    #
    #
    #         elif i[0] is not None:
    #             # Сюда записываются id файлов для отправки медиа группой
    #             group_files_id =[]
    #             # Это id группы сообщений для сравнения с ним в цикле
    #             media_group_id = data[0][0]
    #             if i[-1] == 'photo':
    #                 for i in data:
    #                     if i[0] == media_group_id:
    #                         # Добавление id файла в список
    #                         group_files_id.append(i[-2])
    #                     else:
    #                         pass
    #
    #                 await bot.send_media_group(channel_id, [types.InputMediaPhoto(files) for files in group_files_id])
    #
    #
    #                 # Удаляю из медиа файлы которые были отправлены. Удаляются первые элементы к оличестве штук отправленных фото
    #
    #
    #             elif i[-1] == 'video':
    #                 await bot.send_video(channel_id, i[-2])
    #
    #             # print(media)
    #             print(data)
    #
    #
    #             for i in range(0, len(group_files_id)):
    #                 del media[0]
    #                 with open('media.json', 'w') as f:
    #                     json.dump(data, f)
    #
    #                 for i in range(0, len(group_files_id)):
    #                     del data[0]
    #                     with open('media.json', 'w') as f:
    #                         json.dump(data, f)
    #
    #
    #             # # Записываем обновлённую информацию в наш список.
    #             # with open('media.json', 'w') as f:
    #             #     json.dump(data, f)


if __name__ == '__main__':
    executor.start_polling(dp)
