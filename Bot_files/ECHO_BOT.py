from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message


BOT_TOKEN = "use your bot TOKEN"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def answer_to_start(message: Message):
    await message.answer("Hello, this is Repeater BOT!\nEverything you will write\nI will repeat and send it")


@dp.message(Command(commands=['help']))
async def answer_to_help(message: Message):
    await message.answer("There is nothing complex BRUH...")


@dp.message()
async def echo_message(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)

    except TypeError:
        await message.answer("Something went wrong")



if __name__ == '__main__':
    dp.run_polling(bot)

