import requests
import json

from config import \
    TELEBOT_TOKEN, \
    CURRENCY_VALUES, \
    API_KEY, \
    API_URL

class APIException(Exception):
    pass

class CurrencyConverter:

    @staticmethod
    def convert(from_: str, to_: str, amount_: str):
        headers = {
            "apikey": API_KEY
        }

        if from_ == to_:
            raise APIException("Невозможно перевести одинаковые валюты")
        try:
            from_ticker = CURRENCY_VALUES[from_]
        except KeyError:
            raise APIException(f"*{from_}* - данная валюта не найдена в списке возможных для конвертации")

        try:
            to_ticker = CURRENCY_VALUES[to_]
        except KeyError:
            raise APIException(f"*{to_}* - данная валюта не найдена в списке возможных для конвертации")
        try:
            amount_ = float(amount_)
        except ValueError:
            raise APIException(f'Не удалось обработать количество *{amount_}*')

        r = requests.get(API_URL.format(from_ticker, to_ticker, amount_), headers=headers)

        answer_to_user = json.loads(r.content)['result']
        print(answer_to_user)

        return answer_to_user