import telebot
import requests
import urllib.parse
import time
import os  # ضفنا ده عشان نقرأ البورت بتاع ريلواي
from telebot import types

# التوكن
API_TOKEN = '8732953077:AAE3_IMxo_lTHRE8l63Cc2np22e_UwWp0JQ'
bot = telebot.TeleBot(API_TOKEN)

# الإعدادات
CHANNELS = ["@KU7_4", "@superr_almas"]
DEV_USER = "@II_2P"

# الأوامر
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت 🚀"),
    types.BotCommand("help", "المساعدة 💡")
])

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

# الدوال المساعدة
def get_flag(code):
    c = code.upper().strip()
    crypto_list = ['BTC', 'ETH', 'BNB', 'SOL', 'USDT', 'XRP', 'ADA', 'DOGE', 'TRX', 'TON', 'PEPE', 'FLOKI', 'SHIB']
    if c in FLAG_MAP:
        return FLAG_MAP[c]
    elif c in crypto_list:
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

# دالة تحويل العملات السريعة
def convert_currency(amount, from_c, to_c):
    try:
        from_c = from_c.upper().strip()
        to_c = to_c.upper().strip()
        url = f"https://min-api.cryptocompare.com/data/price?fsym={from_c}&tsyms={to_c}"
        res = requests.get(url).json()
        if to_c in res:
            p = float(res[to_c])
            return p, p * amount
    except Exception as e:
        print(f"API Error: {e}")
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
        "💡 مثال: 1 btc egp\n"
        "--- --- --- --- --- --- ---\n"
        "👋 Welcome to VLUX Bot\n"
        "Type any currency you want and I will get its price for you.\n\n"
        "💡 Example: 1 btc egp"
    )
    
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
        try:
            p, total = convert_currency(float(words[0]), words[1], words[2])
            if p is not None:
                txt = f"{get_flag(words[1])} **من:** {words[1].upper()}\n{get_flag(words[2])} **إلى:** {words[2].upper()}\n💰 **السعر:** {'{:,.4f}'.format(p)} {words[2].upper()}\n💵 **الإجمالي:** {'{:,.2f}'.format(total)} {words[2].upper()}"
                bot.reply_to(message, txt, parse_mode='Markdown')
            else:
                bot.reply_to(message, "⚠️ عذراً، لم أتمكن من جلب السعر. تأكد من صحة رموز العملات (مثال: btc, usd, egp).")
        except ValueError:
            bot.reply_to(message, "❌ خطأ: يرجى إدخال رقم صحيح في البداية. مثال: `1 btc egp`", parse_mode='Markdown')
    else:
        bot.reply_to(message, "❌ صيغة غير صحيحة، يرجى كتابة الأمر هكذا: `1 btc egp`", parse_mode='Markdown')

# خد بالك من الجزء الجديد ده المخصص لريلواي وسيرفرات الهوست
if __name__ == '__main__':
    print("VLUX Running on Server...")
    # فتح بورت وهمي عشان ريلواي ميقفلش البوت
    port = int(os.environ.get('PORT', 5000))
    
    # دالة بولينج قوية ومستقرة ومبتعملش كراش
    bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)

