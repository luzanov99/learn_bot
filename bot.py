import logging
import settings
import ephem 
import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

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
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()   
