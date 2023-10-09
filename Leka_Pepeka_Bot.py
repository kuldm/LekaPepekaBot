import os
import asyncio
from datetime import datetime
import random

from aiogram import Bot, Dispatcher, executor, types


import pytz

from config import TOKEN, CHANNEL_ID, MY_TG_ID
from src import load_data, save_data, sending_message_id, sending_media_data

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


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
    # Переменная в которую временно добавляются данные о присланных файлах
    media = {}

    if message.content_type == 'photo':
        # Добавление в media в котором ключ это id сообщения всю необходимую информацию
        media[message.message_id] = {
            'media_group_id': message.media_group_id,
            'file_id': message.photo[-1].file_id,
            'content_type': message.content_type,
            'message_id': message.message_id
        }

    elif message.content_type == 'video':
        media[message.message_id] = {
            'media_group_id': message.media_group_id,
            'file_id': message.video.file_id,
            'content_type': message.content_type,
            'message_id': message.message_id
        }

    data = load_data()  # Чтение содержимого JSON-файла
    data.update(media)  # Добавление к текущей информации в json новую
    save_data(data)  # Запись в json обновлённой информации
    media.clear()  # Очистка словаря media
    # await bot.send_message(MY_TG_ID, 'Мем сохранён 😎')


# Функция для отправки сообщений с медиа
async def send_media_messages(sending_media_data):
    # Переменная в которую добавляются id файлов для отправки в чат
    media_group = []
    # Проходимся по всем Файлам и добавляем id в media_group исходя из типа контента
    for media_item in sending_media_data:
        if media_item['content_type'] == 'photo':
            media_group.append(types.InputMediaPhoto(media=media_item['file_id']))
        elif media_item['content_type'] == 'video':
            media_group.append(types.InputMediaVideo(media=media_item['file_id']))

    await bot.send_media_group(CHANNEL_ID, media=media_group)

    # После успешной отправки удаляем информацию об отправленных файлах из JSON
    data = load_data()
    for i in sending_message_id():
        if i in data:
            del data[i]
            save_data(data)


# Функция для отправки сообщений
async def send_periodic_messages():
    while True:
        try:
            now = datetime.now(pytz.timezone('Europe/Moscow'))
            day_of_week = now.weekday()

            # Определите интервалы времени для каждого дня недели (в формате (час, минута))
            # В этом примере отправка происходит с понедельника по воскресенье
            schedules = {
                0: [(8, 45), (23, 50)],  # Понедельник
                1: [(8, 45), (23, 50)],  # Вторник
                2: [(8, 45), (23, 50)],  # Среда
                3: [(8, 45), (23, 50)],  # Четверг
                4: [(8, 45), (23, 50)],  # Пятница
                5: [(8, 45), (23, 50)],  # Суббота
                6: [(8, 45), (23, 50)]  # Воскресенье
            }

            current_time = (now.hour, now.minute)  # Текущее время
            random_time_sleep = random.randrange(3500, 3601)  # Случайное время отправки сообщения

            # Проверяем, находится ли текущее время в интервале для текущего дня недели
            if current_time >= schedules[day_of_week][0] and current_time <= schedules[day_of_week][1]:
                # Если в текущий интервал времени, то отправляем сообщения
                await send_media_messages(sending_media_data())
                await asyncio.sleep(random_time_sleep)  # Интервал отправки сообщений 60 минут
            else:
                # Если не в интервале, ждем до ближайшего интервала
                next_schedule = schedules[day_of_week][0]
                next_schedule_datetime = now.replace(hour=next_schedule[0], minute=next_schedule[1], second=0,
                                                     microsecond=0)
                time_until_next_schedule = (next_schedule_datetime - now).total_seconds()
                await asyncio.sleep(time_until_next_schedule)

        except IndexError:
            await bot.send_message(MY_TG_ID, 'ALARM! Закончились мемы, кидай ещё срочно!')
            await asyncio.sleep(60)  # Интервал предупреждений о том, что закончились мемы


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_periodic_messages())
    executor.start_polling(dp, skip_updates=True)
