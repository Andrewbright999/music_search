import os, asyncio, logging, sys
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile,ReplyKeyboardRemove
from aiogram.filters import Command
from music_search import search
from database import get_allusers, add_user
from config import TG_TOKEN


bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher()
router = Router()

@router.message(Command("start")) 
async def startmessage(message: Message):
    add_user(message.from_user.username, message.chat.id)
    await bot.send_message(message.chat.id, 'Привет, что бы скачать песню отправь мне ее название 🎼🎼🎼')
    
@router.message(Command("users"))     
async def allusers(message: Message):
    users = get_allusers()
    await message.answer(f"{users}",parse_mode='Markdown')


@router.message(F.text)
async def hundle_text(message: Message):
    add_user(message.from_user.username, message.chat.id)
    print(f"{message.from_user.username} - {message.text}")
    result = search(message.text, message.from_user.username)
    print(result)
    if result != 'Не нашли такой трек(':
        track_file = FSInputFile(f"{result}")
        await bot.send_audio(message.chat.id, track_file ,caption=f"Найдено в @BrightSearch_Bot",reply_markup=ReplyKeyboardRemove())
        os.remove(result)
        os.rmdir(message.from_user.username)
    else: 
        await bot.answer(result)

async def main() -> None:
    dp.include_routers(router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
