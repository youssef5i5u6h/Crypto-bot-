import telebot
import requests
import urllib.parse  # مكتبة لتشفير النص التلقائي جوه الرابط
from telebot import types  # استدعاء مكتبة الأزرار

# التوكن الخاص ببوتك
API_TOKEN = '8732953077:AAGOENe3KART6vQGAUxCv3uRCobxVdOahHM'
bot = telebot.TeleBot(API_TOKEN)

# 1. تعيين الأوامر تلقائياً في زرار الـ Menu الأزرق
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت وعرض الأزرار 🚀"),
    types.BotCommand("help", "طريقة استخدام البوت الفورية 💡")
])

# قاموس سريع لأشهر العملات الرقمية
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

# قاموس أعلام الدول للعملات المحلية (مع حذف وتجنب الكيان تماماً)
FLAG_MAP = {
    'EGP': '🇪🇬', 'USD': '🇺🇸', 'SAR': '🇸🇦', 'AED': '🇦🇪', 'EUR': '🇪🇺', 
    'KWD': '🇰🇼', 'QAR': '🇶🇦', 'BHD': '🇧🇭', 'OMR': '🇴🇲', 'JOD': '🇯🇴', 
    'LBP': '🇱🇧', 'IQD': '🇮🇶', 'LYD': '🇱🇾', 'MAD': '🇲🇦', 'DZD': '🇩🇿', 
    'TND': '🇹🇳', 'YER': '🇾🇪', 'GBP': '🇬🇧', 'JPY': '🇯🇵', 'CAD': '🇨🇦', 
    'AUD': '🇦🇺', 'CHF': '🇨🇭', 'CNY': '🇨🇳', 'RUB': '🇷🇺', 'TRY': '🇹🇷'
}

def get_flag(currency_code):
    """دالة لجلب علم العملة لو محلي، أو إرجاع إيموجي مميز لو رقمي"""
    code = currency_code.upper().strip()
    if code in FLAG_MAP:
        return FLAG_MAP[code]
    elif code.lower() in CRYPTO_MAP:
        return '🪙'
    return '🏳️'

def get_crypto_id(symbol):
    symbol = symbol.lower().strip()
    if symbol in CRYPTO_MAP:
        return CRYPTO_MAP[symbol]
        
    try:
        search_url = f"https://api.coingecko.com/api/v3/search?query={symbol}"
        response = requests.get(search_url).json()
        coins = response.get('coins', [])
        for coin in coins:
            if coin.get('symbol', '').lower() == symbol:
                return coin.get('id')
        return None
    except Exception:
        return None

def convert_any_currency(amount, from_currency, to_currency):
    from_curr = from_currency.lower().strip()
    to_curr = to_currency.upper().strip()
    
    try:
        # 1. فحص لو العملة الأساسية رقمية
        crypto_id = get_crypto_id(from_curr)
        if crypto_id:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={to_curr.lower()}"
            response = requests.get(url).json()
            if crypto_id in response and to_curr.lower() in response[crypto_id]:
                price_per_unit = response[crypto_id][to_curr.lower()]
                return price_per_unit, price_per_unit * amount

        # 2. فحص لو العملة محلية
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url).json()
        rates = response.get('rates', {})
        
        from_target = from_curr.upper()
        if from_target in rates and to_curr in rates:
            price_per_unit = rates[to_curr] / rates[from_target]
            return price_per_unit, price_per_unit * amount
            
        return None, None
    except Exception as e:
        print(f"Error in conversion: {e}")
        return None, None

# أمر /start و /help بالرابط المباشر الجديد لمنع شاشة التحويل والمشاركة
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **أهلاً بك في بوت ڤلوكس | VLUX**\n"
        "اكتب أي عملة أنت عايزها وأنا هجيبلك سعرها بالبلد بتاعتها.\n\n"
        "💡 **مثال:** `1 btc egp`\n"
        "--- --- --- --- --- --- --- ---\n"
        "👋 **Welcome to VLUX Bot**\n"
        "Type any currency you want and I will get its price for you.\n\n"
        "💡 **Example:** `1 btc egp`"
    )
    
    # الجملة المكتوبة في كيبورد المستخدم تلقائياً
    preset_msg = "عايز بوت زي ده"
    encoded_msg = urllib.parse.quote(preset_msg)
    
    # الرابط الجديد (tg://resolve) بيدخل المستخدم على يوزرك II_2P فوراً ويكتب الجملة تلقائي في الكيبورد
    dev_url = "https://t.me/II_2P"
    create_bot_url = f"tg://resolve?domain=II_2P&text={encoded_msg}"
    
    # صناعة الأزرار الشفافة
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_developer = types.InlineKeyboardButton("👨‍💻 مطور البوت | Developer", url=dev_url)
    btn_create_bot = types.InlineKeyboardButton("🤖 شراء أو برمجة بوت", url=create_bot_url)
    
    markup.add(btn_developer, btn_create_bot)
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    text = message.text.strip().lower()
    
    # الفحص الفوري للكيان بالرد المظبوط والترتيب اللي طلبته
    if 'ils' in text:
        bot.reply_to(message, "كسم إسرائيل : فلسطين حرة 🇵🇸✊", parse_mode='Markdown')
        return

    # فحص الرسالة والتقسيم الذكي للكلمات لمنع التهنيج في الجروبات
    words = text.split()
    if len(words) == 3:
        try:
            amount = float(words[0])
            from_currency = words[1]
            to_currency = words[2]
            
            # جلب أعلام العملات
            from_flag = get_flag(from_currency)
            to_flag = get_flag(to_currency)
            
            price_unit, total_price = convert_any_currency(amount, from_currency, to_currency)
            
            if price_unit is not None:
                formatted_unit = "{:,.4f}".format(price_unit)
                formatted_total = "{:,.2f}".format(total_price)
                
                response_text = (
                    f"{from_flag} **من عملة:** {from_currency.upper()}\n"
                    f"{to_flag} **إلى عملة:** {to_currency.upper()}\n"
                    f"🔢 **الكمية:** {amount}\n"
                    f"💵 **سعر الوحدة:** {formatted_unit} {to_currency.upper()}\n"
                    f"💰 **الإجمالي:** {formatted_total} {to_currency.upper()}"
                )
                bot.reply_to(message, response_text, parse_mode='Markdown')
            else:
                if message.chat.type == 'private':
                    bot.reply_to(message, f"❌ عذراً، لم يتم العثور على العملة `{from_currency.upper()}`.", parse_mode='Markdown')
        except ValueError:
            if message.chat.type == 'private':
                bot.reply_to(message, "❌ خطأ في الصيغة! اكتبها كدا مثلاً:\n`1 btc egp` أو `100 usd sar`", parse_mode='Markdown')
    else:
        if message.chat.type == 'private':
            bot.reply_to(message, "❌ خطأ في الصيغة! اكتبها كدا مثلاً:\n`1 btc egp` أو `100 usd sar`", parse_mode='Markdown')

# تشغيل البوت
print("VLUX Full Bot with direct chat link is running flawlessly...")
bot.infinity_polling()

