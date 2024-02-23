# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import sqlite3
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd

# Создание БД
conn = sqlite3.connect('tgBot.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS notifies (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_Id TEXT,
                    data_perevoda_na_3LTP TEXT,
                    data_vzyatiya_v_rabotu TEXT,
                    data_pereotkrytiya TEXT,
                    krayniy_srok TEXT,
                    ssylka_na_obrashcheniye TEXT,
                    sostoyaniye_ASUOP TEXT,
                    sostoyaniye_BITRIKS TEXT,
                    otvetstvenny TEXT,
                    kontakt_polzovatelya TEXT,
                    soderzhaniye_obrashcheniya TEXT,
                    kommentariy_ASUOP TEXT,
                    servis TEXT,
                    prioritet TEXT
                )''')

# Бот


# Настройка бота и добавление обработчиков
updater = Updater('7160129906:AAHBQbCiCtuqeTeCHjzWFnaI7OKbsqkwo8k', use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('upload_list', upload_list))
dispatcher.add_handler(CommandHandler('download_list', download_list))
dispatcher.add_handler(CommandHandler('check_deadlines', check_deadlines_command))

bot = telebot.TeleBot('7160129906:AAHBQbCiCtuqeTeCHjzWFnaI7OKbsqkwo8k')


@bot.message_handler(func=lambda message: message.text.lower() == 'напомни')
def handle_remind(message):
    bot.send_message(message.chat.id, 'Хорошо, напомню через 30 секунд...')
    time.sleep(30)  # Делаем паузу в 30 секунд
    bot.send_message(message.chat.id, 'Время напомнить тебе что-то!')


# не забыть включить, чтобы он заработал без остановки (если он вообще заработает, после 6 часов труда)
# bot.polling(none_stop=True)


# Запуск Telegram бота
updater.start_polling()
updater.idle()

#Вызвать битру

# Достать из excel
# продумать структуру данных на выходе
def get():
    return

def logic():
    return

def send():
    return





# Подключение к базе данных SQLite
conn = sqlite3.connect('obrashcheniya.db')
cursor = conn.cursor()

# Создание таблицы с полями



# Функция для автоматического вычисления дат
def calculate_date(data, days):
    return (datetime.strptime(data, '%Y-%m-%d %H:%M:%S') + timedelta(days)).strftime('%Y-%m-%d %H:%M:%S')


# Добавление тестовых данных (можно закомментировать после тестирования)
cursor.execute('''INSERT INTO obrazheniya (nomer_obrashcheniya, data_perevoda_na_3LTP, data_vzyatiya_v_rabotu, 
                data_pereotkrytiya, ssylka_na_obrashcheniye, otvetstvenny, soderzhaniye_obrashcheniya, 
                servis, prioritet)
                VALUES ('123456', '2024-02-23 12:00:00', 
                '2024-02-23 13:00:00', '2024-02-24 10:00:00', 'example.com', 
                'Иванов Иван', 'Содержание обращения', 'Сервис A', 'Высокий')''')

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

# Функция для обновления базы данных из Excel файла
# Подключение к базе данных SQLite
conn = sqlite3.connect('obrashcheniya.db')
cursor = conn.cursor()


def update_database_from_excel(file_path):
    # Загружаем данные из Excel файла
    data = pd.read_excel(file_path)

    # Для каждой записи из Excel файла
    for index, row in data.iterrows():
        nomer_obrashcheniya = row[
            'nomer_obrashcheniya']  # Предположим, что столбец с номером обращения называется 'nomer_obrashcheniya'

        # Проверяем наличие записи в базе данных по номеру обращения
        cursor.execute("SELECT * FROM obrazheniya WHERE nomer_obrashcheniya = ?", (nomer_obrashcheniya,))
        existing_entry = cursor.fetchone()

        if existing_entry:
            # Если запись уже существует, то актуализируем данные
            cursor.execute(
                "UPDATE obrazheniya SET data_perevoda_na_3LTP = ?, data_vzyatiya_v_rabotu = ? WHERE nomer_obrashcheniya = ?",
                (row['data_perevoda_na_3LTP'], row['data_vzyatiya_v_rabotu'], nomer_obrashcheniya))
        else:
            # Если запись не существует, то добавляем новую запись
            cursor.execute(
                "INSERT INTO obrazheniya (nomer_obrashcheniya, data_perevoda_na_3LTP, data_vzyatiya_v_rabotu) VALUES (?, ?, ?)",
                (nomer_obrashcheniya, row['data_perevoda_na_3LTP'], row['data_vzyatiya_v_rabotu']))

    # Сохраняем изменения и закрываем соединение
    conn.commit()


# вызов функции для обновления базы данных из Excel файла
update_database_from_excel('sample_data.xlsx')

# Закрытие соединения с базой данных
conn.close()

import sqlite3

# Подключение к базе данных SQLite
conn = sqlite3.connect('obrashcheniya.db')
cursor = conn.cursor()


def get_list_of_cases():
    # Извлекаем список обращений из базы данных
    cursor.execute("SELECT * FROM obrazheniya")
    cases = cursor.fetchall()

    # Формируем список обращений для пользователя
    list_of_cases = []
    for case in cases:
        list_of_cases.append({
            'nomer_obrashcheniya': case[0],  # Предположим, что номер обращения - первое поле в записи
            'data_perevoda_na_3LTP': case[1],  # Предположим, что дата перевода на 3LTP - второе поле
            'data_vzyatiya_v_rabotu': case[2]  # Предположим, что дата взятия в работу - третье поле
        })

    # Закрываем соединение
    conn.close()

    # Отправляем пользователю список обращений
    return list_of_cases


#  использование функции для получения списка обращений
cases_list = get_list_of_cases()
for case in cases_list:
    print(case)


# Функция для проверки крайнего срока обращений и отправки уведомлений
def check_deadlines():


# Проверяем обращения с крайним сроком на сегодня и обращения, срок которых уже прошел
# Отправляем уведомления о подходящих обращениях

def upload_list(update, context):
    # Получаем файл от пользователя
    file = context.bot.get_file(update.message.document.file_id)
    file_bytes = file.download_as_bytearray()

    # Получаем расширение файла
    file_extension = file.file_path.split('.')[-1]

    if file_extension == 'xlsx':
        # Создаем временный файл и записываем в него содержимое загруженного файла
        with open(f'temp_file.xlsx', 'wb') as temp_file:
            temp_file.write(file_bytes)

        # Обновляем базу данных из Excel файла
        update_database_from_excel('temp_file.xlsx')

        # Удаляем временный файл
        os.remove('temp_file.xlsx')

        context.bot.send_message(chat_id=update.effective_chat.id, text="Список успешно загружен из Excel файла 📂📊")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, загрузите файл в формате xlsx 📑❌")


# Обработчик команды "/download_list" для вывода списка обращений
def download_list(update, context):
    # Получаем список обращений
    list_of_cases = get_list_of_cases()

    # Отправляем список обращений пользователю


# Обработчик команды "/check_deadlines" для проверки крайних сроков
def check_deadlines_command(update, context):
    # Проверяем крайние сроки обращений
    check_deadlines()

def get_notification():
    pass

def task_distribution(task_list, data_base_project_manager):
    notification = get_notification()
    for task in task_list:
        for user in data_base_project_manager:
            if task['RESPONSIBLE_ID'] == user['ID']:
                if task['Notification'] == True:
                    message = "Пользователь с ID {user['ID']} должен выполнить задачу и уже оповещен"
                else:
                    message = "Пользователь с ID {user['ID']} должен выполнить задачу и ему необходимо отправить уведомление"
                break
    return

def bot_send_message(message):
    pass
