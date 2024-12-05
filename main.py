import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import csv
from dotenv import load_dotenv
import os
import database
from random import choice

load_dotenv()

TOKEN = os.getenv("TOKEN")
database.Base.metadata.create_all(bind=database.engine)


dp = Dispatcher()
bot = Bot(TOKEN)

builder = InlineKeyboardBuilder()
builder.button(text=f"Yes✅", callback_data="1")
builder.button(text=f"No❌", callback_data="0")


@dp.message(Command("start"))
async def start(message: Message):
    id = message.from_user.id
    username = message.from_user.username
    name = message.from_user.full_name
    database.add_user(id, username, name)

    await message.answer(
        text="Do u want something?",
        reply_markup=builder.as_markup(),
    )


@dp.message(Command("shufle"))
async def shufle(message: Message):
    id = message.from_user.id

    all_users = [i[0] for i in database.get_all_users()]

    if not all_users:
        await message.answer("No active users!")
        return

    for i in range(len(all_users)):
        message_to = choice(all_users)
        receiver = choice(database.get_users_except(message_to))

        try:
            await bot.send_message(
                message_to,
                f"Username: {receiver.username}\nName: {receiver.name}\nWant: {receiver.data}\n\nLet's gooo!!",
            )
        except Exception as e:
            print(f"ERROR: {message_to=}")
        else:
            all_users.remove(message_to)
            database.update_sent(receiver.user_id)


@dp.message(Command("notify"))
async def shufle(message: Message):
    id = message.from_user.id
    if id != 1893217856:
        return

    all_users = [i[0] for i in database.get_all_users()]

    for i, v in enumerate(all_users):
        try:
            await bot.send_message(v, f"Get ready!!\nI'll show you results in a minute")
        except Exception as e:
            database.update_sent(v)
            print(f"ERROR: {v=}")


@dp.callback_query(lambda callback: callback.data in ["1", "0"])
async def handle_callback(callback_query: CallbackQuery):
    if callback_query.data == "1":
        database.update_want(callback_query.from_user.id)
        await callback_query.message.answer("What do you want?")
    elif callback_query.data == "0":
        await callback_query.message.answer("Ok, wait for the result.")


@dp.message()
async def handle_messages(message: Message):
    id = message.from_user.id
    text = message.text
    if database.get_want(id):
        result = database.update_data(id, text)
        if result:
            answer = "Ok, thanks.\nWait for results!"
        else:
            answer = "Error!!"
    else:
        answer = "Waiiiit!!"

    await message.answer(answer)


async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
