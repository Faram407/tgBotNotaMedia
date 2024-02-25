import telebot
import sqlite3
import pandas as pd
import os
import random  # Для тестов, Денис


data_base_project_manager = [{"ID": 4805, "ProjectName": "@nastasia_project"},  # Данные по Проджект менеджерам
                             {"ID": 4609, "ProjectName": "@anatoliyavd"},
                             {"ID": 4368, "ProjectName": "@avetiss"},
                             {"ID": 5641, "ProjectName": "@exxxlight"}
                             ]

BotKey = "7160129906:AAHBQbCiCtuqeTeCHjzWFnaI7OKbsqkwo8k"  # Замените на ваш ключ бота

# Инициализация бота
bot = telebot.TeleBot(BotKey)

DB_FILE = 'database.sql'

# Проверка существования базы данных
if not os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Создание таблицы
    cur.execute('CREATE TABLE IF NOT EXISTS Helpdesk_ticket ('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'Number_ticket VARCHAR(11),'
                'Date_of_handover VARCHAR(11),'
                'Date_of_commencement_of_employment VARCHAR(11),'
                'Reopening_date VARCHAR(11),'
                'Deadline VARCHAR(11),'
                'URL VARCHAR(200),'
                'Status_ASUOP VARCHAR(50),'
                'Status_BITRIX VARCHAR(50),'
                'Responsible_for_this_task VARCHAR(50),'
                'User_contact VARCHAR(200),'
                'Subject_of_the_ticket VARCHAR(1000),'
                'Comment VARCHAR(500),'
                'Service VARCHAR(50),'
                'Priority VARCHAR(50)'
                ')')

    conn.commit()
    cur.close()
    conn.close()


# Обработчик команды "start"
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, сейчас загрузим обращения!')
    bot.register_next_step_handler(message, handle_document)


# test
# Обработчик документов
def handle_document(message):
    if message.document is not None and message.document.file_name.endswith('.xlsx'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('data.xlsx', 'wb') as new_file:
            new_file.write(downloaded_file)

        df = pd.read_excel('data.xlsx')

        conn = sqlite3.connect(DB_FILE)

        # Сохранение данных из Excel в базу данных
        df.to_sql('Helpdesk_ticket', conn, if_exists='replace', index=False)

        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, 'Данные успешно загружены и сохранены в базе данных!')
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте файл в формате XLSX.')


# Обработчик команды "query"
@bot.message_handler(commands=['query'])
def handle_query(message):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Helpdesk_ticket")
    rows = cur.fetchall()

    if rows:
        for row in rows:
            row_task = dict_create_from_list(list(row))
            bot.send_message(message.chat.id, row_task)


    else:
        bot.send_message(message.chat.id, 'Нет данных в базе!')

    cur.close()
    conn.close()


# Квартыч

def append_Notification_and_RESPONSIBLE(row):  # ДЛЯ ТЕСТА Добавляем в список 2 поля , Responsible_ID и Notification
    responsible_ID_list = [4805, 4609, 4368, 4368]
    notification_list = [True, False]
    row.append(random.choice(responsible_ID_list))
    row.append(random.choice(notification_list))
    return row


def dict_create_from_list(row):  # Преобразуем список в словарь
    row = append_Notification_and_RESPONSIBLE(row)
    keys = ["task_url", "task_number", "date_start", "date_take", "objective", "status", "applicant_name", "date,end",
            "RESPONSIBLE_ID", "Notification"]
    task_dictionary = dict(zip(keys, row))
    return task_distribution(task_dictionary, data_base_project_manager)


def get_notification(task_dictionary):  # Смотрим Отправляли ли мы уже сообщение.
    if task_dictionary["Notification"] == True:
        return True
    else:
        return False


def task_distribution(task_dictionary,
                      data_base_project_manager):  # Проверяем ответственного по задаче, Формируем сообщение.

    for user in data_base_project_manager:

        if task_dictionary["RESPONSIBLE_ID"] == user["ID"]:
            if get_notification(task_dictionary) == True:
                message_for_project = user['ProjectName'] + " уже оповещен по задаче " + task_dictionary[
                    "task_number"]
                break
            else:

                message_for_project = user[
                                          'ProjectName'] + " прошу взять задачу " + \
                                      task_dictionary["task_number"] + " в работу \n" + task_dictionary["task_url"]
            break
    return message_for_project


# Квартыч


# Запуск обработки сообщений бота
bot.polling(none_stop=True)


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

# Вызвать битру

# Достать из excel
# продумать структуру данных на выходе
# def get():


# def logic():


# def send():


# Подключение к базе данных SQLite
conn = sqlite3.connect('obrashcheniya.db')
cursor = conn.cursor()

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

    # def upload_list(update, context):
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
        context.bot.send_message(chat_id=update.effective_chat.id, text="АЛЕ, загрузите файл в формате xlsx 📑❌")


# Обработчик команды "/download_list" для вывода списка обращений
def download_list(update, context):
    # Получаем список обращений
    list_of_cases = get_list_of_cases()

    # Отправляем список обращений пользователю


# Обработчик команды "/check_deadlines" для проверки крайних сроков
def check_deadlines_command(update, context):
    # Проверяем крайние сроки обращений
    check_deadlines()


# Квартыч








