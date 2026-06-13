import telebot
import requests
import urllib.parse
from telebot import types

# التوكن
API_TOKEN = '8732953077:AAE3_IMxo_lTHRE8l63Cc2np22e_UwWp0JQ'
bot = telebot.TeleBot(API_TOKEN)

# الإعدادات
CHANNELS = ["@KU7_4", "@superr_almas"]
DEV_USER = "@II_2P"

# الأوامر كما في الصورة
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت 🚀"),
    types.BotCommand("help", "المساعدة 💡")
])

# القاموس (بنفس التنسيق)
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

# الأعلام (تحت بعضها كما في الصورة)
FLAG_MAP = {
    'EGP': '🇪🇬', 'USD': '🇺🇸', 'SAR': '🇸🇦',
    'KWD': '🇰🇼', 'QAR': '🇶🇦', 'BHD': '🇧🇭',
    'LBP': '🇱🇧', 'IQD': '🇮🇶', 'LYD': '🇱🇾',
    'TND': '🇹🇳', 'YER': '🇾🇪', 'GBP': '🇬🇧',
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'CNY': '🇨🇳'
}

# الدوال
def get_flag(code):
    c = code.upper().strip()
    return FLAG_MAP[c] if c in FLAG_MAP else ('🪙' if code.lower() in CRYPTO_MAP else '🏳️')

def check_subscription(user_id):
    for channel in CHANNELS:
        try:
            if bot.get_chat_member(channel, user_id).status in ['left', 'kicked']: return False
        except: return False
    return True

def get_subscription_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("اشترك في القناة الأولى", url="https://t.me/KU7_4"))
    markup.add(types.InlineKeyboardButton("اشترك في القناة الثانية", url="https://t.me/superr_almas"))
    markup.add(types.InlineKeyboardButton("تحقق ✅", callback_data="check_sub"))
    return markup

def convert_currency(amount, from_c, to_c):
    try:
        c_id = CRYPTO_MAP.get(from_c.lower())
        if c_id:
            res = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={c_id}&vs_currencies={to_c.lower()}").json()
            if c_id in res and to_c.lower() in res[c_id]:
                p = res[c_id][to_c.lower()]
                return p, p * amount
        url = "https://open.er-api.com/v6/latest/USD"
        rates = requests.get(url).json().get('rates', {})
        if from_c.upper() in rates and to_c.upper() in rates:
            p = rates[to_c.upper()] / rates[from_c.upper()]
            return p, p * amount
    except: pass
    return None, None

# الأوامر
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_query(call):
    if check_subscription(call.from_user.id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "✅ تم التحقق بنجاح! اضغط /start لبدء استخدام البوت.")
    else:
        bot.answer_callback_query(call.id, "❌ اشترك في القنوات أولاً!", show_alert=True)

@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 للاستمرار، يجب الانضمام للقنوات:", reply_markup=get_subscription_markup())
        return
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"),
        types.InlineKeyboardButton("🤖 شراء / برمجة بوت", url=f"https://t.me/{DEV_USER.replace('@', '')}?start=شراء_برمجة_بوت")
    )
    bot.reply_to(message, "👋 أهلاً بك في بوت ڤلوكس | VLUX\nاكتب العملة ومثال: `1 btc egp`", parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_msg(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 للاستمرار، يجب الانضمام للقنوات:", reply_markup=get_subscription_markup())
        return
    text = "💡 **مساعدة بوت ڤلوكس**\nاكتب العملة ومثال: `1 btc egp`\n\n⚠️ **لو في أي مشكلة في البوت أو مش عارف تستخدم البوت ازاي كلمني:**"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"))
    bot.reply_to(message, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 للاستمرار، يجب الانضمام للقنوات:", reply_markup=get_subscription_markup())
        return
    words = message.text.split()
    if len(words) == 3:
        p, total = convert_currency(float(words[0]), words[1], words[2])
        if p: bot.reply_to(message, f"{get_flag(words[1])} **من:** {words[1].upper()}\n{get_flag(words[2])} **إلى:** {words[2].upper()}\n💰 **السعر:** {'{:,.4f}'.format(p)} {words[2].upper()}\n💵 **الإجمالي:** {'{:,.2f}'.format(total)} {words[2].upper()}", parse_mode='Markdown')

print("VLUX Running...")
bot.infinity_polling()

