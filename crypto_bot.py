import telebot
import requests
import re

# التوكن الجديد الخاص ببوتك تم وضعه هنا مباشرة
API_TOKEN = '8732953077:AAGOENe3KART6vQGAUxCv3uRCobxVdOahHM'
bot = telebot.TeleBot(API_TOKEN)

# قاموس سريع لأشهر العملات الرقمية لزيادة سرعة الرد وعدم حدوث ضغط على الـ API
CRYPTO_MAP = {
    'btc': 'bitcoin', 'eth': 'ethereum', 'bnb': 'binancecoin', 'sol': 'solana',
    'usdt': 'tether', 'xrp': 'ripple', 'ada': 'cardano', 'doge': 'dogecoin',
    'trx': 'tron', 'dot': 'polkadot', 'ltc': 'litecoin', 'shib': 'shiba-inu',
    'avax': 'avalanche-2', 'link': 'chainlink', 'uni': 'uniswap', 'atom': 'cosmos',
    'xlm': 'stellar', 'fil': 'filecoin', 'etc': 'ethereum-classic', 'hbar': 'hbar',
    'apt': 'aptos', 'sui': 'sui', 'near': 'near', 'op': 'optimism', 'arb': 'arbitrum',
    'ldo': 'lido-dao', 'fet': 'fetch-ai', 'inj': 'injective-protocol', 'render': 'render-token',
    'pepe': 'pepe', 'floki': 'floki', 'bonk': 'bonk', 'wif': 'dogwifhat', 'ton': 'the-open-network'
}

# دالة برمجية للبحث الديناميكي عن ID العملة الرقمية لو مش موجودة في القاموس السريع
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

# الدالة الشاملة لتحويل أي عملة في العالم لعملة تانية
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

        # 2. فحص لو العملة محلية لكل دول العالم
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

# أمر /start و /help بالصيغة العربية والإنجليزية مدموجين معاً
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **أهلاً بك في بوت ڤلوكس | VLUX**\n"
        "اكتب أي عملة أنت عايزها وأنا هجيبلك سعرها.\n\n"
        "💡 **مثال:** `1 btc egp`\n"
        "--- --- --- --- --- --- --- ---\n"
        "👋 **Welcome to VLUX Bot**\n"
        "Type any currency you want and I will get its price for you.\n\n"
        "💡 **Example:** `1 btc egp`"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

# قراءة وفك شفرة الرسائل في الخاص والجروبات تلقائياً
@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    text = message.text.strip().lower()
    
    # فك الرسالة بذكاء: (الرقم) ثم (العملة 1) ثم مسافة ثم (العملة 2)
    match = re.match(r"([0-9.]+)\s*([a-z0-9\-]+)\s+([a-z]+)", text)
    
    if match:
        amount = float(match.group(1))
        from_currency = match.group(2)
        to_currency = match.group(3)
        
        # تنفيذ التحويل الشامل
        price_unit, total_price = convert_any_currency(amount, from_currency, to_currency)
        
        if price_unit is not None:
            # تنسيق الأرقام بشكل احترافي للجروبات
            formatted_unit = "{:,.4f}".format(price_unit)
            formatted_total = "{:,.2f}".format(total_price)
            
            response_text = (
                f"🪙 **من عملة:** {from_currency.upper()}\n"
                f"🎯 **إلى عملة:** {to_currency.upper()}\n"
                f"🔢 **الكمية:** {amount}\n"
                f"💵 **سعر الوحدة:** {formatted_unit} {to_currency.upper()}\n"
                f"💰 **الإجمالي:** {formatted_total} {to_currency.upper()}"
            )
            bot.reply_to(message, response_text, parse_mode='Markdown')
        else:
            if message.chat.type == 'private':
                bot.reply_to(message, f"❌ عذراً، لم يتم العثور على العملة `{from_currency.upper()}` أو أن التحويل لـ `{to_currency.upper()}` غير مدعوم حالياً.", parse_mode='Markdown')
    else:
        if message.chat.type == 'private':
            bot.reply_to(message, "❌ خطأ في الصيغة! اكتبها كدا مثلاً:\n`1 btc egp` أو `100 usd sar`", parse_mode='Markdown')

# تشغيل البوت
print("VLUX is running flawlessly...")
bot.infinity_polling()
