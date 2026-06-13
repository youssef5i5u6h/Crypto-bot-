import telebot
import requests
import urllib.parse
from telebot import types

# التوكن
API_TOKEN = '8732953077:AAE3_IMxo_lTHRE8l63Cc2np22e_UwWp0JQ'
bot = telebot.TeleBot(API_TOKEN)

# --- نظام الاشتراك الإجباري ---
CHANNELS = ["@KU7_4", "@superr_almas"]
DEV_USER = "@II_2P"

def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            status = bot.get_chat_member(channel, user_id).status
            if status in ['left', 'kicked']: return False
        except: return False
    return True

def get_subscription_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("اشترك في القناة الأولى", url="https://t.me/KU7_4"))
    markup.add(types.InlineKeyboardButton("اشترك في القناة الثانية", url="https://t.me/superr_almas"))
    markup.add(types.InlineKeyboardButton("تحقق ✅", callback_data="check_sub"))
    return markup

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_query(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "تم التحقق بنجاح! ✅")
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "✅ تم التحقق بنجاح! اضغط /start لبدء استخدام البوت.")
    else:
        bot.answer_callback_query(call.id, "❌ لم تشترك بعد! اشترك أولاً ثم اضغط تحقق.", show_alert=True)

# 1. تعيين الأوامر
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت 🚀"),
    types.BotCommand("help", "المساعدة 💡")
])

# القاموس الكامل للعملات (بدون عملة إسرائيل)
CRYPTO_MAP = {
    'btc': 'bitcoin', 'eth': 'ethereum', 'bnb': 'binancecoin', 'sol': 'solana',
    'usdt': 'tether', 'xrp': 'ripple', 'ada': 'cardano', 'doge': 'dogecoin',
    'trx': 'tron', 'dot': 'polkadot', 'ltc': 'litecoin', 'shib': 'shiba-inu',
    'avax': 'avalanche-2', 'link': 'chainlink', 'uni': 'uniswap', 'atom': 'cosmos',
    'xlm': 'stellar', 'fil': 'filecoin', 'etc': 'ethereum-classic', 'hbar': 'hedera-hashgraph',
    'apt': 'aptos', 'sui': 'sui', 'near': 'near', 'op': 'optimism', 'arb': 'arbitrum',
    'ldo': 'lido-dao', 'fet': 'fetch-ai', 'inj': 'injective-protocol', 'render': 'render-token',
    'pepe': 'pepe', 'floki': 'floki', 'bonk': 'bonk', 'wif': 'dogwifhat', 'ton': 'the-open-network'
}

FLAG_MAP = {
    'EGP': '🇪🇬', 'USD': '🇺🇸', 'SAR': '🇸🇦', 'AED': '🇦🇪', 'EUR': '🇪🇺', 
    'KWD': '🇰🇼', 'QAR': '🇶🇦', 'BHD': '🇧🇭', 'OMR': '🇴🇲', 'JOD': '🇯🇴', 
    'LBP': '🇱🇧', 'IQD': '🇮🇶', 'LYD': '🇱🇾', 'MAD': '🇲🇦', 'DZD': '🇩🇿', 
    'TND': '🇹🇳', 'YER': '🇾🇪', 'GBP': '🇬🇧', 'JPY': '🇯🇵', 'CAD': '🇨🇦', 
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'CNY': '🇨🇳', 'RUB': '🇷🇺', 'TRY': '🇹🇷'
}

def get_flag(currency_code):
    code = currency_code.upper().strip()
    if code in FLAG_MAP: return FLAG_MAP[code]
    elif code.lower() in CRYPTO_MAP: return '🪙'
    return '🏳️'

def get_crypto_id(symbol):
    symbol = symbol.lower().strip()
    if symbol in CRYPTO_MAP: return CRYPTO_MAP[symbol]
    try:
        search_url = f"https://api.coingecko.com/api/v3/search?query={symbol}"
        response = requests.get(search_url).json()
        coins = response.get('coins', [])
        for coin in coins:
            if coin.get('symbol', '').lower() == symbol: return coin.get('id')
        return None
    except: return None

def convert_any_currency(amount, from_currency, to_currency):
    from_curr = from_currency.lower().strip()
    to_curr = to_currency.upper().strip()
    try:
        crypto_id = get_crypto_id(from_curr)
        if crypto_id:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={to_curr.lower()}"
            response = requests.get(url).json()
            if crypto_id in response and to_curr.lower() in response[crypto_id]:
                price = response[crypto_id][to_curr.lower()]
                return price, price * amount
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url).json()
        rates = response.get('rates', {})
        if from_curr.upper() in rates and to_curr in rates:
            price = rates[to_curr] / rates[from_curr.upper()]
            return price, price * amount
        return None, None
    except: return None, None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 للاستمرار في استخدام البوت، يجب الانضمام للقنوات:", reply_markup=get_subscription_markup())
        return

    welcome_text = (
        "👋 **أهلاً بك في بوت ڤلوكس | VLUX**\n"
        "اكتب أي عملة أنت عايزها وأنا هجيبلك سعرها بالبلد بتاعتها.\n\n"
        "💡 **مثال:** `1 btc egp`"
    )
    preset_msg = "شراء / برمجة بوت"
    buy_url = f"https://t.me/{DEV_USER.replace('@', '')}?start={urllib.parse.quote(preset_msg)}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"),
        types.InlineKeyboardButton("🤖 شراء / برمجة بوت", url=buy_url)
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_msg(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 للاستمرار في استخدام البوت، يجب الانضمام للقنوات:", reply_markup=get_subscription_markup())
        return
    
    text = (
        "💡 **مساعدة بوت ڤلوكس**\n"
        "اكتب العملة ومثال: `1 btc egp`\n\n"
        "⚠️ **لو في أي مشكلة في البوت أو مش عارف تستخدم البوت ازاي كلمني:**"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"))
    bot.reply_to(message, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 للاستمرار في استخدام البوت، يجب الانضمام للقنوات:", reply_markup=get_subscription_markup())
        return

    text = message.text.strip().lower()
    # تم حذف الرد على الكيان
    
    words = text.split()
    if len(words) == 3:
        try:
            amount = float(words[0])
            from_c, to_c = words[1], words[2]
            f_flag, t_flag = get_flag(from_c), get_flag(to_c)
            p_unit, t_price = convert_any_currency(amount, from_c, to_c)
            
            if p_unit is not None:
                resp = (
                    f"{f_flag} **من:** {from_c.upper()}\n"
                    f"{t_flag} **إلى:** {to_c.upper()}\n"
                    f"🔢 **الكمية:** {amount}\n"
                    f"💵 **سعر الوحدة:** {'{:,.4f}'.format(p_unit)} {to_c.upper()}\n"
                    f"💰 **الإجمالي:** {'{:,.2f}'.format(t_price)} {to_c.upper()}"
                )
                bot.reply_to(message, resp, parse_mode='Markdown')
        except: pass

print("VLUX Full Version Running...")
bot.infinity_polling()

