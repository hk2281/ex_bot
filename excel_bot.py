import telebot
import json 
import requests 
import xlsxwriter
import os
import time ,sys, datetime
from telebot import types
from flask import Flask, request

token = "1225700210:AAG9JX6b-wk9WQCS_PnCkC1zusuqI3eblQg"
a = "https://io.adafruit.com/api/v2/hk22811/feeds/webtest/data?start_time="
b = "T05:00:00Z&end_time="
c = "T20:00:00Z&x-aio-key=a8f4a8ad8a8040e0ad19ee3928f10431"

bot = telebot.TeleBot(token)
now = datetime.datetime.now()

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('получить документ')
markup.add(itembtn1)


def create_kbord():
  keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
  key_yes = types.InlineKeyboardButton(text='текущий документ', callback_data='curr') 
  keyboard.add(key_yes) 
  return keyboard

def createdoc(name):
    workbook = xlsxwriter.Workbook(str(name) + '.xlsx')
    return workbook

def createWorkSheet(docObj):
    worksheet = docObj.add_worksheet()
    worksheet.write_string('A1','usr_ids')
    worksheet.write_string('B1', 'weights')
    return worksheet

def excelMaker(data1,data2, sell, docObj, workSh):
    workSh.write_number('B'+str(sell), data1)
    workSh.write_number('A'+str(sell), data2)

def formating(dat_from_bd):
    formated = []
    for val in dat_from_bd:
        formated.append(val['value'].replace('�','').rsplit('$',2))
    return formated

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id,text="получить", reply_markup=create_kbord())

@bot.message_handler(content_types=['text'])
def send_file(message):
    print(message.text)
    try:
        time.strptime(message.text,"%Y.%m.%d")
        get_time = message.text
        print(a+get_time+b+get_time+c)
        resp = requests.get(a+get_time+b+get_time+c)

        if not json.loads(resp.text):
            bot.send_message(message.from_user.id, text="на эту дату нет записей")
        else :
            doc = createdoc("dtf")
            scheet = createWorkSheet(doc)
            i = 2
            for x in formating(json.loads(resp.text)):
                excelMaker(float(x[1]),int(x[0]),i,doc,scheet)
                i+=1
            doc.close()
            bot.send_document(message.from_user.id, open('dtf.xlsx', 'rb'), reply_markup=create_kbord())
    except ValueError:
        # print("Unexpected error:", sys.exc_info())
        bot.send_message(message.from_user.id, text="некоректный формат даты, YYYY.MM.DD")

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data == "curr":
            now_t = now.strftime("%Y-%m-%d")
            resp = requests.get(a+now_t+b+now_t+c)
            if not json.loads(resp.text):
                bot.send_message(message.from_user.id, text="на эту дату нет записей")
            else :
                doc = createdoc("dtf")
                scheet = createWorkSheet(doc)
                i = 2
                for x in formating(json.loads(resp.text)):
                    excelMaker(float(x[1]),int(x[0]),i,doc,scheet)
                    i+=1
                doc.close()
                bot.send_document(call.message.chat.id, open('dtf.xlsx', 'rb'), reply_markup=create_kbord())
                print(json.loads(resp.text))
    except TypeError:
        bot.send_message(call.message.chat.id, "опачки ошибка...")
@server.route("/")
  def webhook():
      bot.remove_webhook()
      bot.set_webhook(url='https://intense-badlands-19799.herokuapp.com/' + TOKEN)
      return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

else:
  bot.remove_webhook()
  bot.polling(none_stop=True, interval=0)