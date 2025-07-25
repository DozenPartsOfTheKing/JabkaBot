
import random
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ChatType
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import dotenv

dotenv.load_dotenv()

from stickers import STICKER_POOL  # ваш пул file_id стикеров

TOKEN = os.getenv("TOKEN")

# ——— Пул звуков жабок ———
SOUND_POOL = [
    "sounds/zvuk.mp3",
    "sounds/zvuk-lyagushki-korotkiy-28632.mp3",
    "sounds/zvonkoe-strekotanie-drevesnoy-lyagushki.mp3",
    "sounds/zvonkaya-lyagushka-chem-to-nedovolna.mp3",
    "sounds/xiaomi_frog-1.mp3",
    "sounds/odinokaya-lyagushka-sidit-v-trave-i-kvakaet.mp3",
    "sounds/obyichnoe-kvakanie-jabyi.mp3",
    "sounds/nestandartnoe-kvakanie-kakoy-to-neponyatnoy-lyagushki.mp3",
    "sounds/lyagushka-na-liste-lotosa-nazyivaetsya-zvukovyim-effektom-41440.mp3",
    "sounds/lyagushka-izdaet-zvuki-37046.mp3",
    "sounds/lyagushache-bolotnoe-logovo.mp3",
    "sounds/kvakanie-ogromnoy-lyagushki.mp3",
    "sounds/jutkiy-zvuk-kvakaniya-lyagushki-byika.mp3",
    "sounds/drevesnaya-lyagushka-pisklyavo-kvakaet.mp3",
    "sounds/chastoe-kvakanie-malenkoy-lyagushki.mp3",
    "sounds/byistryie-zvuki-kvakaniya.mp3"
]

# ——— Подписи под стикерами ———
CAPTION_POOL = [
    "Ква-ква!", "Квааааа!", "Ква-кря-ква!", "Ква? Ква!",
    "КВААА!!! 🐸", "Мягкое ква…", "Бум‑ква‑бум!", "Ква‑фест! 🎉",
    "Сочное ква 🐸", "Двойное ква-ква", "Тройное КВА!!", "Ква в квадрате",
    "Гипер-ква", "Ква-дратное уравнение", "Безумное КВА!", "Гига-ква 🐸",
]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатуры
private_kb = ReplyKeyboardBuilder()
private_kb.row(types.KeyboardButton(text="Ква 🐸"))
private_kb.adjust(1)
inline_kb = InlineKeyboardBuilder()
inline_kb.row(types.InlineKeyboardButton(text="Ква 🐸", callback_data="kva"))
inline_kb.adjust(1)

async def send_sticker_with_caption(chat_id: int, caption: str = None):
    sticker = random.choice(STICKER_POOL)
    sound = random.choice(SOUND_POOL)
    
    await bot.send_sticker(chat_id, sticker)
    
    # Отправляем звук жабки
    with open(sound, 'rb') as audio_file:
        await bot.send_voice(chat_id, audio_file)
    
    text = caption or random.choice(CAPTION_POOL)
    await bot.send_message(chat_id, text)

async def bot_is_admin(chat_id: int) -> bool:
    """Проверяем, является ли бот админом в чате"""
    me = await bot.get_me()
    member = await bot.get_chat_member(chat_id, me.id)
    from aiogram.enums import ChatMemberStatus
    return member.status in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR)

# — Приватные handlers —
@dp.message(Command("start"), F.chat.type == ChatType.PRIVATE)
async def cmd_start(message: types.Message):
    await message.answer("А какая ты жабка сегодня? 🐸", reply_markup=inline_kb.as_markup())
    await message.answer("Или жми Ква снизу 👇", reply_markup=private_kb.as_markup(resize_keyboard=True))

@dp.callback_query(F.data == "kva")
async def on_inline_kva(callback: types.CallbackQuery):
    await callback.answer()
    await send_sticker_with_caption(callback.message.chat.id)

@dp.message(F.text == "Ква 🐸", F.chat.type == ChatType.PRIVATE)
async def on_reply_kva(message: types.Message):
    await send_sticker_with_caption(message.chat.id)

@dp.message(F.chat.type == ChatType.PRIVATE)
async def on_user_message_private(message: types.Message):
    await send_sticker_with_caption(message.chat.id)

# — Групповые handlers —
@dp.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def on_group_message(message: types.Message):
    if not message.text:
        return
    
    text_lower = message.text.lower()
    if "ква" in text_lower or "жабка" in text_lower:
        logging.info(f"Handler triggered for message: '{message.text}'")
        try:
            is_admin = await bot_is_admin(message.chat.id)
            logging.info(f"Bot is admin: {is_admin}")
            if not is_admin:
                return
            await send_sticker_with_caption(message.chat.id)
        except Exception as e:
            logging.error(f"Error in handler: {e}")
            # Отправляем стикер без проверки админских прав для отладки
            await send_sticker_with_caption(message.chat.id)

if __name__ == "__main__":
    logging.info("Бот запущен — пусть квакает!")
    dp.run_polling(bot)
