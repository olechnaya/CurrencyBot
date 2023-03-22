import telebot
from utils import  APIException, CurrencyConverter
from config import \
    TELEBOT_TOKEN, \
    CURRENCY_VALUES, \
    API_KEY, \
    API_URL

#API_URL.format("RUB", "USD", 4))
bot = telebot.TeleBot(TELEBOT_TOKEN)



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу с валютой нужно ввести команду в чате:\n<*имя валюты*> \
<*в какую валюту перевести*> \
<*какое количество нужно перевести*>.\n\
Увидеть список всех доступных валют: нажмите /values'
    bot.reply_to(message, text, parse_mode= 'Markdown')

@bot.message_handler(commands=['values'])
def available_currencies(message: telebot.types.Message):
    text = '*Доступные валюты:*'

    for k in CURRENCY_VALUES:
        text = '\n'.join((text, k))
    bot.reply_to(message,text, parse_mode= 'Markdown')

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        # создали отдельную переменную чтобы отлавливать некорректно введенные данные
        user_input = message.text.split(' ')

        if len(user_input) < 3:
            raise APIException('Мало параметров')
        elif len(user_input) > 3:
            raise APIException('Много параметров')

        from_, to_, amount_ = user_input
        answer_to_user = CurrencyConverter.convert(from_, to_, amount_)

    except APIException as e:
        bot.reply_to(message, f"Ошибка ввода пользователем:\n  - {e}", parse_mode= 'Markdown' )
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f'Цена {amount_} {from_} в {to_}: {float(answer_to_user)*float(amount_)}'
        bot.send_message(message.chat.id, text)


bot.infinity_polling()
