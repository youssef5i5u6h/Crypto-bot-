import telebot
import requests
import urllib.parse
from telebot import types

# التوكن الخاص ببوتك
API_TOKEN = '8732953077:AAGOENe3KART6vQGAUxCv3uRCobxVdOahHM'
bot = telebot.TeleBot(API_TOKEN)

# 1. تعيين الأوامر تلقائياً في زرار الـ Menu الأزرق
bot.set_my_commands([
    types.BotCommand("start", "تشغيل البوت وعرض الأزرار 🚀"),
    types.BotCommand("help", "طريقة استخدام البوت الفورية 💡")
])

# قاموس لأشهر العملات (تم حذف وتجنب الكيان)
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
        from_target = from_curr.upper()
        if from_target in rates and to_curr in rates:
            price = rates[to_curr] / rates[from_target]
            return price, price * amount
        return None, None
    except: return None, None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 **أهلاً بك في بوت ڤلوكس | VLUX**\n"
        "اكتب أي عملة أنت عايزها وأنا هجيبلك سعرها بالبلد بتاعتها.\n\n"
        "💡 **مثال:** `1 btc egp`"
    )
    
    # الجملة المطلوبة كجملة تلقائية في الرابط
    preset_msg = "شراء / برمجة بوت"
    encoded_msg = urllib.parse.quote(preset_msg)
    
    # الرابط المباشر ليوزرك II_2P
    direct_chat_url = f"tg://resolve?domain=II_2P&text={encoded_msg}"
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_developer = types.InlineKeyboardButton("👨‍💻 مطور البوت | Developer", url=direct_chat_url)
    btn_create_bot = types.InlineKeyboardButton("🤖 شراء / برمجة بوت", url=direct_chat_url)
    
    markup.add(btn_developer, btn_create_bot)
    bot.reply_to(message, welcome_text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    text = message.text.strip().lower()
    if 'ils' in text:
        bot.reply_to(message, "كسم إسرائيل : فلسطين حرة 🇵🇸✊", parse_mode='Markdown')
        return

    words = text.split()
    if len(words) == 3:
        try:
            amount = float(words[0])
            from_c, to_c = words[1], words[2]
            f_flag, t_flag = get_flag(from_c), get_flag(to_c)
            p_unit, t_price = convert_any_currency(amount, from_c, to_c)
            
            if p_unit is not None:
                response_text = (
                    f"{f_flag} **من:** {from_c.upper()}\n"
                    f"{t_flag} **إلى:** {to_c.upper()}\n"
                    f"🔢 **الكمية:** {amount}\n"
                    f"💵 **سعر الوحدة:** {'{:,.4f}'.format(p_unit)} {to_c.upper()}\n"
                    f"💰 **الإجمالي:** {'{:,.2f}'.format(t_price)} {to_c.upper()}"
                )
                bot.reply_to(message, response_text, parse_mode='Markdown')
        except: pass

print("VLUX with updated text is running...")
bot.infinity_polling()

