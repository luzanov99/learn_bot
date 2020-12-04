import logging
import settings
import ephem 
import copy
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


#Шаблон списка городов для пользователя
spisok=['москва', 'киев','ровм','новосибирск','алжир','ара','винница']
#Словарь городов для пользователей
states={}
#Словарь количества ходов игры для каждого пользователя
games={}
#Словарь последних букв для пользователей
lst={}
def game(update, context):
    chat_id=update.message.chat.id
    #Проверка на существование уже активной игры польщзователя
    #Если нет то инициализация начальных параметров
    if chat_id not in lst:
        lst[chat_id]=''
    if chat_id not in states:
        states[chat_id] = copy.copy(spisok)

    if chat_id not in games:
        games[chat_id]=0
    #Если первый ход
    if games[chat_id]==0:
        games[chat_id]+=1
        stroka=update.message.text.split(' ',1)
        #Проверка на наличие города  в списке 
        if stroka[1] in states[chat_id] : 
            #Количество выводимых ответов ботом должно быть 1
            kol_otvet=0
            #Удаляем использованное  пользователем слово
            states[chat_id].remove(stroka[1])
            #Ищем в списке подходящий город
            for element in states[chat_id]:
                if stroka[1][-1]==element[0]:
                    kol_otvet+=1
                    #Вывод ответа, фиксирование последний буквы бота, удаление города из списка
                    if kol_otvet==1:
                        update.message.reply_text(element)
                        lst[chat_id]=element[-1]
                        states[chat_id].remove(element)
                       
                    else: return
        #Если названия города нет в списке вывод ошибки    
        else:
            update.message.reply_text("Вы ввели неправильную букву или такого слова нет")

    else:
    #Если больше 1 хода
        games[chat_id]+=1
        stroka=update.message.text.split(' ',1)
        #Проверка на наличие слова в списке и совпадение последней буквы слова бота
        if stroka[1] in states[chat_id]  and stroka[1][0]==lst[chat_id]: 
           
            kol_otvet=0
            states[chat_id].remove(stroka[1])
            for element in states[chat_id]:
                if stroka[1][-1]==element[0]:
               
                    kol_otvet+=1
                    if kol_otvet==1:
                    
                        update.message.reply_text(element)
                        lst[chat_id]=element[-1]
                        states[chat_id].remove(element)
                        print(states[chat_id])
                    else: return
        else:
            update.message.reply_text("Вы ввели неправильную букву или такого слова нет")
            
        
        

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

#Функция показа созвездия 
def show_planet(update, context):
    now = datetime.datetime.now()
    print('Вызван /planet')
    active_planet=0
    planet=update.message.text.split(' ')
    date='{}/{}/{}'.format(now.year,now.month,now.day)
    #print(date)
    if planet[1].lower()=='mars':
        
        active_planet=ephem.Mars(date)
        constellation = ephem.constellation(active_planet)
        update.message.reply_text(constellation)
        
    elif planet[1].lower()=='jupiter':
        active_planet=ephem.Jupiter(date)
        constellation = ephem.constellation(active_planet)
        update.message.reply_text(constellation)
    elif planet[1].lower()=='mercury':
        active_planet=ephem.Mercury(date)
        constellation = ephem.constellation(active_planet)
        update.message.reply_text(constellation)
    elif planet[1].lower()=='venus':
        active_planet=ephem.Venus(date)
        constellation = ephem.constellation(active_planet)
        update.message.reply_text(constellation)
    elif planet[1].lower()=='saturn':
        active_planet=ephem.Saturn(date)
        constellation = ephem.constellation(active_planet)
        update.message.reply_text(constellation)
    elif planet[1].lower()=='uranus':
        active_planet=ephem.Uranus(date)
        constellation = ephem.constellation(active_planet)
        update.message.reply_text(constellation)
    else:
        update.message.reply_text("Такой планеты нет в базе данных")

    
 #Калькулятор-функция       
def calculate(update, context):
    stroka=update.message.text.split(' ',1)
    result=0
    for i in range(0,len(stroka[1])):
        if stroka[1][i]==' ':
            update.message.reply_text("Введите выражение без пробелов")
            return
    
    for i in range(0,len(stroka[1])):
        if stroka[1][i]=='+':
            argument1=float(stroka[1][0:i])
            argument2=float(stroka[1][i+1:len(stroka[1])])
            result=argument2+argument1
            update.message.reply_text(result)
        if stroka[1][i]=='-':
            argument1=float(stroka[1][0:i])
            argument2=float(stroka[1][i+1:len(stroka[1])])
            result=argument1-argument2
            update.message.reply_text(result)
        if stroka[1][i]=='/':
            argument1=float(stroka[1][0:i])
            argument2=float(stroka[1][i+1:len(stroka[1])])
            if argument2 ==0.0:
                update.message.reply_text("На 0 делить нельзя")
                return
            else:
                result=argument1/argument2
                update.message.reply_text(result)
        if stroka[1][i]=='*':
            argument1=float(stroka[1][0:i])
            argument2=float(stroka[1][i+1:len(stroka[1])])
            result=argument1*argument2
            update.message.reply_text(result)
    






def talk_to_me(update, context):
    user_text=update.message.text
    #print(update)
    print(user_text)
    update.message.reply_text(user_text)


def main():
    mybot=Updater(settings.API_KEY,use_context=True, request_kwargs=PROXY )
    dp=mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", show_planet))
    dp.add_handler(CommandHandler("calc", calculate))
    dp.add_handler(CommandHandler("cities", game))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()   
