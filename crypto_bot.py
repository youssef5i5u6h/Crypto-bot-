import telebot
import requests
import os
from telebot import types

# التوكن
API_TOKEN = '8732953077:AAE3_IMxo_lTHRE8l63Cc2np22e_UwWp0JQ'
bot = telebot.TeleBot(API_TOKEN)

# الإعدادات
CHANNELS = ["@KU7_4", "@superr_almas"]
DEV_USER = "@II_2P"

# الأوامر في قائمة التليجرام
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت 🚀"),
    types.BotCommand("help", "المساعدة 💡")
])

# قاموس التشفير الأساسي للـ CoinGecko
CRYPTO_MAP = {
    'btc': 'bitcoin', 'eth': 'ethereum', 'bnb': 'binancecoin', 'sol': 'solana', 
    'usdt': 'tether', 'xrp': 'ripple', 'ada': 'cardano', 'doge': 'dogecoin', 
    'trx': 'tron', 'ton': 'the-open-network', 'pepe': 'pepe', 'floki': 'floki', 
    'shib': 'shiba-inu'
}

# قاموس الأعلام الكامل
FLAG_MAP = {
    'EGP': '🇪🇬', 'USD': '🇺🇸', 'SAR': '🇸🇦', 'AED': '🇦🇪', 'EUR': '🇪🇺', 
    'KWD': '🇰🇼', 'QAR': '🇶🇦', 'BHD': '🇧🇭', 'OMR': '🇴🇲', 'JOD': '🇯🇴', 
    'LBP': '🇱🇧', 'IQD': '🇮🇶', 'LYD': '🇱🇾', 'MAD': '🇲🇦', 'DZD': '🇩🇿', 
    'TND': '🇹🇳', 'YER': '🇾🇪', 'GBP': '🇬🇧', 'JPY': '🇯🇵', 'CAD': '🇨🇦', 
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'CNY': '🇨🇳', 'RUB': '🇷🇺', 'TRY': '🇹🇷',
    'SDG': '🇸🇩', 'SLL': '🇸🇱', 'SOS': '🇸🇴', 'SSP': '🇸🇸', 'SYP': '🇸🇾',
    'KGS': '🇰🇬', 'KHR': '🇰🇭', 'KMF': '🇰🇲', 'KPW': '🇰🇵', 'KRW': '🇰🇷'
}

def get_flag(code):
    c = code.upper().strip()
    if c in FLAG_MAP:
        return FLAG_MAP[c]
    elif code.lower() in CRYPTO_MAP:
        return '🪙'
    else:
        return '🏳️'

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

# دالة التحويل الاحترافية الشاملة
def convert_currency(amount, from_c, to_c):
    from_c = from_c.lower().strip()
    to_c = to_c.lower().strip()
    
    # 1. لو العملة الأساسية كريبتو (تشفير)
    if from_c in CRYPTO_MAP:
        try:
            coin_id = CRYPTO_MAP[from_c]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={to_c}"
            res = requests.get(url).json()
            if coin_id in res and to_c in res[coin_id]:
                p = float(res[coin_id][to_c])
                return p, p * amount
        except:
            pass

    # 2. لجميع العملات العادية (جنيه، ريال، دولار...) أو لو الكريبتو كـ عملة ثانية
    try:
        url_fiat = f"https://open.er-api.com/v6/latest/{from_c.upper()}"
        res_fiat = requests.get(url_fiat).json()
        if res_fiat.get('result') == 'success':
            rates = res_fiat.get('rates', {})
            if to_c.upper() in rates:
                p = float(rates[to_c.upper()])
                return p, p * amount
    except:
        pass

    # 3. خطة إنقاذ أخيرة (لو التحويل من عملة عادية لكريبتو مثل usd لـ btc)
    if to_c in CRYPTO_MAP:
        try:
            coin_id = CRYPTO_MAP[to_c]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={from_c}"
            res = requests.get(url).json()
            if coin_id in res and from_c in res[coin_id]:
                p = 1 / float(res[coin_id][from_c])
                return p, p * amount
        except:
            pass
            
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
    if message.text.startswith('/start buy_'):
        bot.reply_to(message, "تم استلام طلبك لشراء / برمجة بوت! المطور سيتواصل معك قريباً.")
        return

    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 لازم تكون مشترك ف القنوات:", reply_markup=get_subscription_markup())
        return
    
    text = (
        "👋 أهلاً بك في بوت ڤلوكس | VLUX\n"
        "اكتب أي عملة أنت عايزها وأنا هجيبلك سعرها بالبلد بتاعتها.\n\n"
        "--- --- --- --- --- --- ---\n"
        "👋 Welcome to VLUX Bot\n"
        "Type any currency you want and I will get its price for you."
    )
    
    buy_url = f"https://t.me/{DEV_USER.replace('@', '')}?start=buy_123"
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
    text = "💡 **مساعدة بوت ڤلوكس**\n\n⚠️ **لو في أي مشكلة في البوت أو مش عارف تستخدم البوت ازاي كلمني:**"
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
        try:
            val = float(words[0])
            p, total = convert_currency(val, words[1], words[2])
            
            if p is not None:
                txt = f"{get_flag(words[1])} **من:** {words[1].upper()}\n{get_flag(words[2])} **إلى:** {words[2].upper()}\n💰 **السعر:** {'{:,.4f}'.format(p)} {words[2].upper()}\n💵 **الإجمالي:** {'{:,.2f}'.format(total)} {words[2].upper()}"
                bot.reply_to(message, txt, parse_mode='Markdown')
            else:
                bot.reply_to(message, "⚠️ عذراً، لم أتمكن من جلب السعر. تأكد من صحة رموز العملات.")
        except ValueError:
            pass
    else:
        pass

if __name__ == '__main__':
    print("VLUX Running...")
    bot.polling(none_stop=True)

