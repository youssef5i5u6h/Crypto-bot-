import telebot
import requests
import urllib.parse
import time
from telebot import types

# التوكن
API_TOKEN = '8732953077:AAE3_IMxo_lTHRE8l63Cc2np22e_UwWp0JQ'
bot = telebot.TeleBot(API_TOKEN)

# الإعدادات
CHANNELS = ["@KU7_4", "@superr_almas"]
DEV_USER = "@II_2P"

# الأوامر في البداية كما في الصورة
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت 🚀"),
    types.BotCommand("help", "المساعدة 💡")
])

# القواميس (العملات ثم الأعلام عمودياً تحت بعضها)
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
    'EGP': '🇪🇬', 'USD': '🇺🇸', 'SAR': '🇸🇦',
    'KWD': '🇰🇼', 'QAR': '🇶🇦', 'BHD': '🇧🇭',
    'LBP': '🇱🇧', 'IQD': '🇮🇶', 'LYD': '🇱🇾',
    'TND': '🇹🇳', 'YER': '🇾🇪', 'GBP': '🇬🇧',
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'CNY': '🇨🇳'
}

# الدوال المساعدة
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
        from_c = from_c.upper().strip()
        to_c = to_c.upper().strip()
        
        # رابط سريع ومفتوح ومجاني لكل العملات والكريبتو
        url = f"https://min-api.cryptocompare.com/data/price?fsym={from_c}&tsyms={to_c}"
        res = requests.get(url).json()
        
        if to_c in res:
            p = float(res[to_c])
            return p, p * amount
    except Exception as e:
        print(f"Error in API: {e}")
    return None, None


# معالجات الأوامر والرسائل
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
    # الرد التلقائي لأمر الشراء والبرمجة (Deep Linking)
    if message.text.startswith('/start buy_'):
        bot.reply_to(message, "تم استلام طلبك لشراء / برمجة بوت! المطور سيتواصل معك قريباً.")
        return

    # التحقق الإجباري من الاشتراك
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 لازم تكون مشترك ف القنوات:", reply_markup=get_subscription_markup())
        return
    
    # نص الترحيب الكامل (عربي + إنجليزي بالتنسيق المطلوب)
    text = (
        "👋 أهلاً بك في بوت ڤلوكس | VLUX\n"
        "اكتب أي عملة أنت عايزها وأنا هجيبلك سعرها بالبلد بتاعتها.\n\n"
        "💡 مثال: 1 btc egp\n"
        "--- --- --- --- --- --- ---\n"
        "👋 Welcome to VLUX Bot\n"
        "Type any currency you want and I will get its price for you.\n\n"
        "💡 Example: 1 btc egp"
    )
    
    # رابط الزر مضاف إليه الطابع الزمني لضمان التحديث وظهور الرد التلقائي في كل مرة
    buy_url = f"https://t.me/{DEV_USER.replace('@', '')}?start=buy_{int(time.time())}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"),
        types.InlineKeyboardButton("🤖 شراء / برمجة بوت", url=buy_url)
    )
    bot.reply_to(message, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['help'])
def help_msg(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 لازم تكون مشترك ف القنوات:", reply_markup=get_subscription_markup())
        return
    text = "💡 **مساعدة بوت ڤلوكس**\nاكتب العملة ومثال: `1 btc egp`\n\n⚠️ **لو في أي مشكلة في البوت أو مش عارف تستخدم البوت ازاي كلمني:**"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"))
    bot.reply_to(message, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_msg(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 لازم تكون مشترك ف القنوات:", reply_markup=get_subscription_markup())
        return
    words = message.text.split()
    if len(words) == 3:
        p, total = convert_currency(float(words[0]), words[1], words[2])
        if p:
            txt = f"{get_flag(words[1])} **من:** {words[1].upper()}\n{get_flag(words[2])} **إلى:** {words[2].upper()}\n💰 **السعر:** {'{:,.4f}'.format(p)} {words[2].upper()}\n💵 **الإجمالي:** {'{:,.2f}'.format(total)} {words[2].upper()}"
            bot.reply_to(message, txt, parse_mode='Markdown')

print("VLUX Running...")
bot.infinity_polling()

