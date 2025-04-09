from aiogram import  Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

import os, random



BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


users = {}



@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_num': None,
                                       'tries': 5,
                                       'wins':0,
                                       'loses':0,
                                       'total_games': 0,
                                       }


    await message.reply("Привет! Я бот для игры - 'Угадай число!'\n"
                        "Чтобы узнать правила игры напиши: '/help'\n"
                        "Хочешь начать игру ?")


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.reply("Правила игры:\n"
                        "Я загадываю число от 1 до 100, а ты должен отгадать его!\n"
                        "Когда игра начнется, у тебя будет 5 попыток угадать число.\n"
                        "Если ты не угадаешь число - ты проиграл.\n\n"
                        "Команды бота:\n"
                        "Если ты в игре и хочешь выйти, то напиши: /cancel\n"
                        "Чтобы посмотртеь свою статистику напишите: /stats\n\n"
                        "Начало игры:\n"
                        "Чтобы начать игру напиши что-то из:\n"
                        "[yes, game]\n"
                        )

@dp.message(Command(commands=['stats']))
async def process_stats_command(message: Message):
    await message.reply(f"Статистика для игрока: {message.from_user.first_name}\n"
                        f"Победы: {users[message.from_user.id]['wins']}\n"
                        f"Проигрыши: {users[message.from_user.id]['loses']}\n"
                        f"Всего игр: {users[message.from_user.id]['total_games']}\n"
                        "Чтобы начать игру напиши что-то из: [yes,game]\n")


@dp.message(Command(commands=['cancel']))
async def process_cancel_command(message: Message):

    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.reply("Вы вышли из игры!\n"
                            "Если хотите играть напишите что-то из:"
                            "[yes, game]")
    else:
        await message.reply("Вы не в игре!\n"
                            "Напишите '/help', чтобы посмотреть список комманд.\n"
                            "Напишите что-то из:"
                            "[yes, game] чтобы начать игру.")





@dp.message()
async def process_user_command(message: Message):

    if not users[message.from_user.id]['in_game']:
        if message.text.lower() in ['yes', 'game']:
            users[message.from_user.id]['in_game'] = True
            users[message.from_user.id]['tries'] = 5
            users[message.from_user.id]['secret_num'] = random.randint(1, 100)
            print(users[message.from_user.id]['secret_num'])
            await message.reply("Игра началась!\n"
                                "Я загадал число между 1-100\n"
                                f"У вас осталось попыток: {users[message.from_user.id]['tries']}\n")
        else:
            await message.reply("Я не понимаю вас.\n"
                                "Чтобы начать игру напишите что-то из:\n"
                                "[yes, game]")

        return

    #game started

    try:
        user_guess = int(message.text)
    except ValueError:
        await message.reply("Вы уже в игре!\n"
                            "Вам нужно ввести число между 1-100\n"
                            "Если хотите выйти из игры напишите '/cancel'")
        return

    if user_guess > 100 or user_guess < 0:
        await message.reply("Число должно быть меньше 100 и больше 0!")
        return

    if user_guess == users[message.from_user.id]['secret_num']:
        users[message.from_user.id]['wins'] += 1
        users[message.from_user.id]['total_games'] += 1
        users[message.from_user.id]['in_game'] = False
        await message.reply("Вы победели !\n"
                            "Хотите сыграть еще раз?")
    else:
        users[message.from_user.id]['tries'] -= 1
        hint = "🔻 Мое число больше!" if user_guess < users[message.from_user.id]['secret_num'] else "🔺 Мое число меньше!"

        if users[message.from_user.id]['tries'] > 0:
            await message.reply(f"{hint}\nПопыток осталось: {users[message.from_user.id]['tries']}")
        else:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['loses'] += 1
            users[message.from_user.id]['total_games'] += 1
            await message.reply("Вы проиграли!\n"
                                f"Мое число было: {users[message.from_user.id]['secret_num']}\n"
                                f"Хотите сыграть еще раз?")





if __name__ == '__main__':
    dp.run_polling(bot)









