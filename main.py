import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from credenciais import telegram_bot, weather

token_bot = telegram_bot.get("token")
token_weather = weather.get("token")
city = weather.get("id_city")
id_chat = 1302198624


class WeatherForecastBot:

    def __init__(self, id_city, token_weather, token_telegram):
        self.id_city = id_city
        self.token_wt = token_weather
        self.token_tlgm = token_telegram
        self.bot = ApplicationBuilder().token(token_bot).build()

    def register_id(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = f"localeId[]={self.id_city}"
        link = f"http://apiadvisor.climatempo.com.br/api-manager/user-token/{self.token_wt}/locales"
        response = requests.request("PUT", link, headers=headers, data=payload)
        return print(response.text)

    def current_weather(self):
        link = f"http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{self.id_city}/current?token={self.token_wt}"
        response = requests.get(link).json()
        information = f"Previsão do tempo atualmente em {response.get('name')}, {response.get('state')}\n" \
                      f"Temperatura: {response['data'].get('temperature')}°C\n" \
                      f"Sensação térmica: {response['data'].get('sensation')}°C\n" \
                      f"Condições: {response['data'].get('condition')}"
        return information

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=self.current_weather())

    def command(self):
        start_handler = CommandHandler('start', self.start)
        self.bot.add_handler(start_handler)

        self.bot.run_polling()


bot = WeatherForecastBot(city, token_weather, token_bot)
bot.command()
