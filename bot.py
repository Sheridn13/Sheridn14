import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.types import *
from datetime import timedelta

API_TOKEN = '6111913380:AAG2Otiy7i_O6hJBg0B1AuqVy05tI-60TlA'


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
warnings = 0

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.chat.type in ["supergroup","group"]:
        await message.reply("ЭЭ здарова чо как Я бот который даст лещя спамерам")



@dp.message_handler(commands=["help"])
async def echo(message: types.Message):
    if message.chat.type in ["supergroup","group"]:
        await message.reply("Я Глава этой парти и вот что я умею\n"
                        "/start- Запустить меня\n"
                        "/mute- Выдать шапалах со скоростью 30минут\n"
                        "/nomute-Не выдать шапалах со скоростью 30минут\n"
                        "/ban- Выдать шапалаж со скоростью света\n"
                        "/noban- не выдает шапалах со скоростью света"
                        "/warn- Выдать предупреждения и угрожать пальцем\n"
                        )


@dp.message_handler(commands=['mute'])
async def send_welcome(message: types.Message):
    if message.chat.type in ["supergroup","group"]:
        if not message.reply_to_message or not message.reply_to_message.from_user:
            await message.reply("Пожалуста покажите этого плохого человека")
            return
        user_to_mute=message.reply_to_message.from_user

        perm= ChatPermissions(
            can_pin_messages=False,
        )
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_to_mute.id,
            permissions=perm,
            until_date=message.date + timedelta(minutes=60)
        ) 

        await message.reply(f"Ты Познал всю боль {user_to_mute.mention} надеюсь ты не забудешь об этом")


@dp.message_handler(commands=['nomute'])
async def send_welcome(message: types.Message):
    if message.chat.type in ["supergroup","group"]:
        if not message.reply_to_message or not message.reply_to_message.from_user:
            await message.reply("Пожалуста покажите этого плохого человека")
            return
        user_to_nomute=message.reply_to_message.from_user

        perm= ChatPermissions(
            can_send_voice_notes=True,
            can_send_videos=True,
            can_pin_messages=True,
            can_add_web_page_previews=True,
            can_send_polls=True,
            can_send_media_messages=True,
        )
        await bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=user_to_nomute.id,
            permissions=perm,
            until_date=message.date 
        ) 

        await message.reply(f"я тебе поздровляю {user_to_nomute.mention} ты можешь говорить")


@dp.message_handler(commands=['ban'])
async def send_welcome(message: types.Message):
    if message.chat.type in ["supergroup","group"]:
        if not message.reply_to_message or not message.reply_to_message.from_user:
            await message.reply("Пожалуста покажите этого плохого человека")
            return
        user_to_ban=message.reply_to_message.from_user

        await bot.kick_chat_member(message.chat.id, user_to_ban.id)
        await message.reply(f"Ты забанен блин и я не буду тебя разбанивать потому-что ты тупой супчик ")


@dp.message_handler(commands="noban")
async def unban(message: types.Message):
    if message.chat.type in ["supergroup" , "group"]:
        if not message.reply_to_message or not message.reply_to_message:
            await message.reply("Пожалуста покажите этого плохого человека")
            return
    
        user_to_ban = message.reply_to_message.from_user

        await bot.unban_chat_member(message.chat.id , user_to_ban.id , only_if_banned=True)

        await message.reply(f"Ты раззабанен блин и мне придется тебя разбанивать потому-что ты нетупой супчик ")


@dp.message_handler(commands=['warn'], is_chat_admin=True)
async def cmd_warn(message: types.Message):
    global warnings

    if not message.reply_to_message or not message.reply_to_message.from_user:
        await message.reply("Пожалуйста, ответьте на сообщение пользователя, чтобы выдать предупреждение.")
        return

    user_to_warn = message.reply_to_message.from_user

    if warnings >= 3:
        perm = ChatPermissions(
            can_send_messages=False
        )
        await bot.restrict_chat_member(
            message.chat.id,
            user_to_warn.id,
            permissions=perm,
            until_date=message.date + timedelta(minutes=30)
        )
        await message.reply(f"Пользователь {user_to_warn.mention} получил мут на 5 минут за нарушение правил.")
        warnings = 0
        return

    warnings += 1

    await message.reply(f"Пользователь {user_to_warn.mention} получил предупреждение ({warnings}/3).")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)