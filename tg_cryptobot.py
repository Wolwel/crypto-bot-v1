import os
from dotenv import load_dotenv
import asyncio
import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart  # Тільки фільтри
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton # Тільки типи
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    print("❌ Помилка: Токен не знайдено!")
    exit()

bot = Bot(
    token=TOKEN, 
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# --- ФУНКЦІЯ ОТРИМАННЯ ЦІНИ ---
async def get_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            price = float(data["price"])
            return price
        except Exception as e:
            print(f"Помилка: {e}")
            return None

# --- СТВОРЕННЯ КЛАВІАТУРИ ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💰 Bitcoin"), KeyboardButton(text="📉 Ethereum"), KeyboardButton(text="💵 SOLUSDT")], 
        [KeyboardButton(text="🆘 Допомога")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Вибери дію..."
)

# --- ОБРОБНИКИ (HANDLERS) ---

# 1. Головна команда /start (показує клавіатуру)
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт! Я крипто-бот. Тисни кнопки нижче 👇", 
        reply_markup=main_keyboard
    )

# 2. Обробка кнопки Bitcoin
@dp.message(F.text == "💰 Bitcoin")
async def btc_handler(message: types.Message):
    await message.answer("🔍 Отримую ціну...")
    price = await get_price("BTCUSDT")
    
    if price:
        await message.answer(f"🔥 <b>Bitcoin:</b> <code>${price:,.2f}</code>")
    else:
        await message.answer("Помилка з'єднання з біржею.")

# 3. Обробка кнопки Ethereum
@dp.message(F.text == "📉 Ethereum")
async def eth_handler(message: types.Message):
    await message.answer("🔍 Отримую ціну...")
    price = await get_price("ETHUSDT")
    if price:
        await message.answer(f"🔥 <b>Ethereum:</b> <code>${price:,.2f}</code>")
    else:
        await message.answer("Помилка з'єднання з біржею.")

@dp.message(F.text == "💵 SOLUSDT")
async def sol_handler(message: types.Message):
    await message.answer("🔍 Отримую ціну...")
    price = await get_price("SOLUSDT")
    if price:
        await message.answer(f"🔥 <b>SOLUSDT:</b> <code>${price:,.2f}</code>")
    else:
        await message.answer("Помилка з'єднання з біржею.")

# 4. Обробка кнопки Допомога
@dp.message(F.text == "🆘 Допомога")
async def help_handler(message: types.Message):
    await message.answer("Дані беруться з біржі <a href='https://www.binance.com'>Binance</a>.")

# --- ЗАПУСК ---
async def main():
    print("Бот з кнопками запущено! 🚀")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот зупинено")