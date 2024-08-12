import os, asyncio, logging, sys
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, FSInputFile,ReplyKeyboardRemove
from aiogram.filters import Command
from music_search import Track
from config import TG_TOKEN


bot = Bot(token=TG_TOKEN, parse_mode="HTML")
dp = Dispatcher()
router = Router()

@router.message(Command("start")) 
async def startmessage(message: Message):
    await bot.send_message(message.chat.id, 'Привет, что бы скачать песню отправь мне ее название 🎼🎼🎼')
    

@router.message(F.text)
async def hundle_text(message: Message):
    print(f"{message.from_user.username} - {message.text}")
    try: 
        track = Track(query=message.text)
        track_path = track.download_track()
        track.set_tags()
        track_file = FSInputFile(track_path)
        await message.answer_audio(track_file, caption=f"Найдено в @BrightSearch_Bot",reply_markup=ReplyKeyboardRemove())
        os.remove(track_path)
    except Exception as e:
        print(e)
        await message.answer('Не нашел такой трек(')

async def main() -> None:
    dp.include_routers(router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
