import os
import asyncio

from aiogram import Bot, Dispatcher, executor, types

from dotenv import load_dotenv

from config import TOKEN, CHANNEL_ID, MY_TG_ID
from src import load_data, save_data, sending_message_id, sending_media_data

# Создание бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# Переменная в которую временно добавляются данные о присланных файлах
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

    # Чтение содержимого JSON-файла
    data = load_data()

    # Добавление к текущей информации в json новую
    data.update(media)

    # Запись в json обновлённой информации
    save_data(data)
    await bot.send_message(MY_TG_ID, 'Мем сохранён 😎')

    # Очистка словаря media
    media.clear()


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


# Функция для отправки сообщений каждый час
async def send_periodic_messages():
    while True:
        try:
            # Передаём список словарей которые нужно отправить
            await send_media_messages(sending_media_data())

            await asyncio.sleep(10)  # Интервал отправки сообщений 10 секунд

        except IndexError:
            await bot.send_message(MY_TG_ID, 'ALARM! Закончились мемы, кидай ещё срочно!')
            await asyncio.sleep(60)  # Интервал прдупреждений о том что закончились мемы


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_periodic_messages())
    executor.start_polling(dp, skip_updates=True)
