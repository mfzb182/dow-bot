import telebot
import os
import mysql.connector
from telebot import types

bot = telebot.TeleBot('1791633980:AAGnBVNq8dAASULY1m5p_e9YwMWzHsioqZ0')
keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard2 = types.InlineKeyboardMarkup()
keyboard1.row('Получить билд', 'Посмотреть тир')
btn_t1 = types.InlineKeyboardButton('Tier 1')
btn_t2 = types.InlineKeyboardButton('Tier 2')
btn_t3 = types.InlineKeyboardButton('Tier 3')

db_name = os.environ.get('DB_NAME', None)
db_user = os.environ.get('DB_USER', None)
db_pass = os.environ.get('DB_PASS', None)
db_host = os.environ.get('DB_HOST', None)
db_port = os.environ.get('DB_PORT', None)


@bot.message_handler(commands=['start'])
def start_photo(message):
    with open('img/main_image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
        bot.send_message(message.chat.id, '‼️ Добро пожаловать в ассистент DawnOfWar Bot ‼️ \n\nНажми на кнопку 🔽 Получить билд 🔽 чтобы начать работу ✌️',reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'получить билд':
       sch = bot.send_message(message.chat.id, 'Напиши для какого героя нужен билд 🤔')
       bot.register_next_step_handler(sch, search_build)
    elif message.text.lower() == 'посмотреть тир':
        keyboard2.add(btn_t1)
        keyboard2.add(btn_t2)
        keyboard2.add(btn_t3)
        sch_t = bot.send_message(message.chat.id, 'Выбери нужный тир',reply_markup=keyboard2)
        bot.register_next_step_handler(sch_t, search_tier)
    elif message.text.lower() != 'получить билд' or 'посмотреть тир':
        bot.send_message(message.chat.id, 'Нажми на кнопку 🌚',reply_markup=keyboard1)


def search_tier(message):
    cnx = mysql.connector.connect(user=db_user, password=db_pass, host=db_host, port=db_port, database=db_name)
    cursor = cnx.cursor()
    tier_sql = ("SELECT TierList FROM tiers WHERE TierName = %s")
    msg_query = message.text
    cursor.execute(tier_sql, (msg_query,))
    row_tier = cursor.fetchall()

    if not row_tier:
        bot.send_message(message.chat.id, '❌ Этого тир не существует ❌\nНажми снова на кнопку\n ⬇️ Посмотреть тир ⬇️',reply_markup=keyboard1)
    else:
        tier_result = []
        for row in row_tier:
            tier_result = row

        tier = tier_result[0]
        tier_msg = "Рекомендованный тир героев: {}".format(tier)
        bot.send_message(message.chat.id, tier_msg)
        bot.send_message(message.chat.id, 'Нужен тир или билд❓\nНажми на кнопку ⬇️ Получить билд ⬇️или'
                                          '  ⬇️ Посмотреть тир ⬇️',reply_markup=keyboard1)

    cnx.close()


def search_build(message):
    cnx = mysql.connector.connect(user=db_user, password=db_pass, host=db_host, port=db_port, database=db_name)
    cursor = cnx.cursor()
    build_sql = ("SELECT Slot1, Slot2, Slot3, Slot4, Slot5, Slot6 FROM builds WHERE HeroName = %s")
    msg_query = message.text
    cursor.execute(build_sql, (msg_query,))
    rows_build = cursor.fetchall()

    hero_sql = ("SELECT HeroNAME FROM builds WHERE HeroName = %s")
    cursor.execute(hero_sql, (msg_query,))
    row_hero = cursor.fetchone()

    if not row_hero:
        bot.send_message(message.chat.id, '❌ Такого героя не существует ❌\nНажми снова на кнопку\n'
                                          ' ⬇️ Получить билд ⬇️',reply_markup=keyboard1)
    else:
        build_result = []
        for row in rows_build:
            for x in row:
                build_result.append(x)

        slot_1 = build_result[0]
        slot_2 = build_result[1]
        slot_3 = build_result[2]
        slot_4 = build_result[3]
        slot_5 = build_result[4]
        slot_6 = build_result[5]
        full_build = "✅🔝 Рекомендованный билд для {}"\
                     "\n\n1. {}\n2. {}\n3. {}\n4. {}\n5. {}\n6. {}".format(msg_query,slot_1,slot_2,slot_3,slot_4,slot_5,slot_6)
        bot.send_message(message.chat.id, full_build)
        bot.send_message(message.chat.id, 'Нужен еще билд❓\nНажми на кнопку ⬇️ Получить билд ⬇️',reply_markup=keyboard1)

    cnx.close()


bot.polling(timeout=10)

while True:
    pass

