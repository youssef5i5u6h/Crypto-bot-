import logging
import re
import requests
import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_fiat():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_fiat)
    t.start()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = "8732953077:AAGOENe3KART6vQGAUxCv3uRCobxVdOahHM"

def get_crypto_price(coin_symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/markets"
        params = {'vs_currency': 'egp', 'symbols': coin_symbol.lower()}
        response = requests.get(url, params=params).json()
        if response and len(response) > 0:
            return response[0]['current_price']
        return None
    except: return None

def get_fiat_price(currency_symbol):
    try:
        url = f"https://open.er-api.com/v6/latest/USD"
        response = requests.get(url).json()
        rates = response.get("rates", {})
        if "EGP" in rates and currency_symbol.upper() in rates:
            return rates["EGP"] / rates[currency_symbol.upper()]
        return None
    except: return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً بك! اكتب لي القيمة والعملة مثل: 50 bnb أو 100 usd وسأحسبها بالجنيه المصري.")

async def handle_conversion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.strip()
    match = re.match(r"^([0-9.]+)\s*([a-zA-Z]+)$", user_text)
    if not match:
        await update.message.reply_text("❌ خطأ! اكتب مثلاً: 50 bnb")
        return
    amount = float(match.group(1))
    symbol = match.group(2).upper()
    
    price = get_crypto_price(symbol) or get_fiat_price(symbol)
    
    if price:
        total = amount * price
        await update.message.reply_text(f"💰 {amount} {symbol} =\n**{total:,.2f} جنيه مصري**", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ عذراً، لم أجد سعر هذه العملة.")

def main():
    keep_alive()
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_conversion))
    print("البوت يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()

