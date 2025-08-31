# toolbot1.py
import asyncio
import random
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardButton, InlineKeyboardMarkup
)
from aiogram.filters import CommandStart

# ========== CONFIG ==========
TOKEN = "8447406983:AAFu5zAxqUP1Nvi4TQD--OsnZ1944VaP90s"   # <-- Replace with your BotFather token
REGISTER_LINK = "http://www.tashanwin.limo/#/register?invitationCode=878813000901"
CHANNEL_LINK = "https://t.me/+cFukcEwJvH41MzE1"
# ============================

bot = Bot(token=TOKEN)          # do NOT pass parse_mode here (aiogram v3)
dp = Dispatcher()

# store per-user current period (int)
user_state = {}  # user_state[user_id] = {"period": int}

# Keyboards
def welcome_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Register & Deposit (Server)", url=REGISTER_LINK)]
    ])
    return kb

def prediction_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Register & Deposit (Server)", url=REGISTER_LINK)],
        [
            InlineKeyboardButton(text="📢 Join Our Channel", url=CHANNEL_LINK),
            InlineKeyboardButton(text="🔮 Predict", callback_data="predict")
        ]
    ])
    return kb

# Formatter
def make_prediction_text(period: int, color_text: str, size_text: str) -> str:
    return (
        "🚀 <b>IQ VIP SURESHOT'S TOOL</b> 🚀\n\n"
        f"⏳ <b>Period Number:</b> {period:03d}\n"
        f"🔍 <b>Prediction:</b> {color_text}\n"
        f"⚪ <b>Size Prediction:</b> {size_text} (optional)"
    )

# /start -> welcome + ask period (only register button under welcome)
@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "🌟 <b>Welcome to IQ VIP SURESHOT'S TOOL</b> 🌟\n\n"
        "🚀 The most trusted prediction assistant.\n\n"
        "📌 Please send your <b>Current Period Number</b> (last 3 digits only).\n"
        "💡 Example: if full period = 202308745 → send only <code>745</code>.\n\n"
        "Send the 3 digits now to get the NEXT prediction."
    )
    await message.answer(welcome_text, parse_mode=ParseMode.HTML, reply_markup=welcome_keyboard())

# Handle incoming text: accept exactly 3-digit period
@dp.message()
async def handle_message(message: Message):
    text = (message.text or "").strip()
    user_id = message.from_user.id

    # If user pressed Predict (callback) it will be handled separately.
    # Here we accept exactly 3-digit numeric period input.
    if text.isdigit() and len(text) == 3:
        next_period = (int(text) + 1) % 1000  # predict for next period
        user_state[user_id] = {"period": next_period}
        # Random prediction (color and size)
        color = random.choice(["GREEN 🟢", "RED 🔴"])
        size = random.choice(["SMALL", "BIG"])
        reply = make_prediction_text(next_period, color, size)
        await message.answer(reply, parse_mode=ParseMode.HTML, reply_markup=prediction_keyboard())
        return

    # If user has already set period and is texting something else, remind them
    if user_id in user_state:
        await message.answer("🔔 Use the <b>🔮 Predict</b> button below to get the next prediction.", parse_mode=ParseMode.HTML, reply_markup=prediction_keyboard())
        return

    # Default help
    await message.answer("❗ Please send a 3-digit period number (e.g. 123). Type /start to see instructions.", parse_mode=ParseMode.HTML)

# Callback: Predict button pressed
@dp.callback_query(lambda c: c.data == "predict")
async def cb_predict(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_state or "period" not in user_state[user_id]:
        await callback.message.answer("⚠️ Please send the 3-digit period first (use /start).")
        await callback.answer()
        return

    # increment period each time user requests a new prediction
    user_state[user_id]["period"] = (user_state[user_id]["period"] + 1) % 1000
    period = user_state[user_id]["period"]

    # Random predictions as requested
    color = random.choice(["GREEN 🟢", "RED 🔴"])
    size = random.choice(["SMALL", "BIG"])

    reply = make_prediction_text(period, color, size)
    await callback.message.answer(reply, parse_mode=ParseMode.HTML, reply_markup=prediction_keyboard())
    await callback.answer()  # remove loading spinner

# Entry point
async def main():
    print("🤖 Bot is starting... (aiogram v3)")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
