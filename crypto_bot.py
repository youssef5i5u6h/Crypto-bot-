import telebot
import requests
import os
import time
from telebot import types

# التوكن الخاص بك
API_TOKEN = '8732953077:AAE3_IMxo_lTHRE8l63Cc2np22e_UwWp0JQ'
bot = telebot.TeleBot(API_TOKEN)

# الإعدادات والقنوات
CHANNELS = ["@KU7_4", "@superr_almas"]
DEV_USER = "@II_2P"

# تعيين الأوامر الرسمية في القائمة الجانبية للتليجرام
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت 🚀"),
    types.BotCommand("help", "المساعدة 💡")
])

# 1. القاموس الكامل والموسع جداً للعملات الرقمية (الـ IDs المعتمدة)
CRYPTO_MAP = {
    'btc': 'bitcoin', 'eth': 'ethereum', 'bnb': 'binancecoin', 'sol': 'solana', 
    'usdt': 'tether', 'xrp': 'ripple', 'ada': 'cardano', 'doge': 'dogecoin', 
    'trx': 'tron', 'dot': 'polkadot', 'ltc': 'litecoin', 'shib': 'shiba-inu', 
    'avax': 'avalanche-2', 'link': 'chainlink', 'uni': 'uniswap', 'atom': 'cosmos', 
    'xlm': 'stellar', 'fil': 'filecoin', 'etc': 'ethereum-classic', 'hbar': 'hedera-hashgraph', 
    'apt': 'aptos', 'sui': 'sui', 'near': 'near', 'op': 'optimism', 
    'arb': 'arbitrum', 'ldo': 'lido-dao', 'fet': 'fetch-ai', 'inj': 'injective-protocol', 
    'render': 'render-token', 'pepe': 'pepe', 'floki': 'floki', 'bonk': 'bonk', 
    'wif': 'dogwifhat', 'ton': 'the-open-network'
}

# 2. القاموس الكامل للأعلام لجميع الدول العربية والأجنبية
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
    elif code.lower().strip() in CRYPTO_MAP:
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

# دالة الحساب المتكاملة والمحدثة بالكامل
def convert_currency(amount, from_c, to_c):
    from_c_clean = from_c.lower().strip()
    to_c_clean = to_c.lower().strip()
    from_upper = from_c.upper().strip()
    to_upper = to_c.upper().strip()
    
    # الخيار أ: التحويل من عملة رقمية (كريبتو)
    if from_c_clean in CRYPTO_MAP:
        try:
            coin_id = CRYPTO_MAP[from_c_clean]
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={to_c_clean}"
            res = requests.get(url, timeout=7).json()
            if coin_id in res and to_c_clean in res[coin_id]:
                p = float(res[coin_id][to_c_clean])
                return p, p * amount
        except: pass

    # الخيار ب: التحويل للعملات العادية وعملات وسيطة (باستخدام السيرفر الأصلي المستقر)
    try:
        url_fiat = "https://open.er-api.com/v6/latest/USD"
        res_fiat = requests.get(url_fiat, timeout=7).json()
        if res_fiat.get('result') == 'success':
            rates = res_fiat.get('rates', {})
            
            # لو العملتين عملات عادية ومعروفة للسيرفر
            if from_upper in rates and to_upper in rates:
                p = float(rates[to_upper]) / float(rates[from_upper])
                return p, p * amount
                
            # لو بيحول من عملة عادية إلى عملة كريبتو (مثال: EGP إلى BTC)
            elif from_upper in rates and to_upper in [c.upper() for c in CRYPTO_MAP]:
                url_rev = f"https://min-api.cryptocompare.com/data/price?fsym={to_upper}&tsyms={from_upper}"
                res_rev = requests.get(url_rev, timeout=7).json()
                if from_upper in res_rev and float(res_rev[from_upper]) > 0:
                    p = 1 / float(res_rev[from_upper])
                    return p, p * amount
    except: pass
    
    # خطة الطوارئ النهائية: في حال تهنيج السيرفرات السابقة بالكامل
    try:
        url_backup = f"https://min-api.cryptocompare.com/data/price?fsym={from_upper}&tsyms={to_upper}"
        res_backup = requests.get(url_backup, timeout=7).json()
        if to_upper in res_backup:
            p = float(res_backup[to_upper])
            return p, p * amount
    except: pass

    return None, None

# [1] معالج أزرار التحقق من الاشتراك بقنوات الإجبار
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_query(call):
    if check_subscription(call.from_user.id):
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "✅ تم التحقق بنجاح! اضغط /start لبدء استخدام البوت.")
    else:
        bot.answer_callback_query(call.id, "❌ اشترك في القنوات أولاً!", show_alert=True)

# [2] معالج أمر التشغيل الترحيبي الأصلي /start
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

# [3] معالج أمر المساعدة والدعم الفني /help
@bot.message_handler(commands=['help'])
def help_msg(message):
    if not check_subscription(message.from_user.id):
        bot.reply_to(message, "🚀 لازم تكون مشترك ف القنوات:", reply_markup=get_subscription_markup())
        return
    text = "💡 **مساعدة بوت ڤلوكس**\n\n⚠️ **لو في أي مشكلة في البوت أو مش عارف تستخدم البوت ازاي كلمني:**"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("👨‍💻 مطور البوت", url=f"https://t.me/{DEV_USER.replace('@', '')}"))
    bot.reply_to(message, text, parse_mode='Markdown', reply_markup=markup)

# [4] المعالج الذكي للرسائل العادية (يتم استدعاؤه فقط إذا لم تكن الرسالة تبدأ بـ / )
@bot.message_handler(func=lambda message: not message.text.startswith('/'))
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

# التشغيل النهائي المستقر
if __name__ == '__main__':
    print("VLUX Active & Complete...")
    while True:
        try:
            bot.polling(none_stop=True, timeout=20)
        except Exception as e:
            time.sleep(3)

