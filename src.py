# Загрузка данных из JSON-файла
import json


# Выгрузка данных из JSON-файла
def load_data():
    with open('media.json', 'r') as json_file:
        data = json.load(json_file)
    return data


# Сохранение данных в JSON-файл
def save_data(data):
    with open('media.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)


# Функция которая возвращает список словарей с данными о файлах которые нужно будет отправить
def sending_media_data():
    # Загрузка данных из вашего JSON-файл
    data = load_data()

    # Ищем первый ключ и его значение "media_group_id"
    first_key = list(data.keys())[0]
    first_value = data[first_key]["media_group_id"]

    sending_data = []

    # Если first_value определено, фильтруем данные по media_group_id
    if first_value is not None:
        for key, value in data.items():
            if value.get("media_group_id") == first_value:
                sending_data.append(value)

    # Если first_value равно None, добавляем первое значение целиком
    elif first_key is not None:
        sending_data.append(data[first_key])

    return sending_data


# Функция которая возвращает список message_id чтобы потом из JSON-файла удалить эти ключи
def sending_message_id():
    # Загрузка данных из вашего JSON-файл
    data = load_data()

    # Ищем первый ключ и его значение "media_group_id"
    first_key = list(data.keys())[0]
    first_value = data[first_key]["media_group_id"]

    sending_message_id = []

    # Если first_value определено, фильтруем данные по media_group_id
    if first_value is not None:
        for key, value in data.items():
            if value.get("media_group_id") == first_value:
                # добавляем message_id
                sending_message_id.append(key)

    # Если first_value равно None, добавляем первое значение целиком
    elif first_key is not None:
        # Добавляем message_id
        sending_message_id.append(list(data.keys())[0])

    return sending_message_id
