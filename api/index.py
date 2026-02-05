import asyncio
import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update

# Инициализация
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()
app = FastAPI()

# Хендлер на команду /start
@dp.message(lambda message: message.text == "/start")
async def start_handler(message: types.Message):
    await message.answer("Теперь я тебя слышу! Бот на Vercel готов к работе. 🚀")

# Обработка POST-запросов от Telegram (на корень "/")
@app.post("/")
async def feed_update(request: Request):
    try:
        json_str = await request.json()
        update = Update.model_validate(json_str, context={"bot": bot})
        await dp.feed_update(bot, update)
    except Exception as e:
        print(f"Error: {e}")
    return {"ok": True}

# Просто для проверки в браузере
@app.get("/")
async def index():
    return {"status": "Bot is running. Send a POST request from Telegram!"}