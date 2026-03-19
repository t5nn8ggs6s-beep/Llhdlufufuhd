from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton


GlavMenu = ReplyKeyboardMarkup(resize_keyboard=True)
GlavMenu.add("💝 Модели")
GlavMenu.add("👤 Профиль","ℹ️ Информация")

adm = InlineKeyboardMarkup()
adm.add(InlineKeyboardButton(text='🥝 Изменить киви', callback_data="qiwi"))
adm.add(InlineKeyboardButton(text='📊 Статистика', callback_data="stat"))
adm.add(InlineKeyboardButton(text='📨 Рассылка', callback_data="send"))
adm.add(InlineKeyboardButton(text='📝 Список анкет', callback_data="spisoka"))
adm.add(InlineKeyboardButton(text='➕ Добавить анкету', callback_data="addancete"))
adm.add(InlineKeyboardButton(text='📸 Добавить фото', callback_data="addphoto"))
adm.add(InlineKeyboardButton(text='➖ Удалить анкету', callback_data="deleteancete"))
adm.add(InlineKeyboardButton(text='❌ Закрыть ❌', callback_data="esc"))

wrk = InlineKeyboardMarkup()
wrk.add(InlineKeyboardButton(text='📩 Сообщение мамонту', callback_data="smsmamont"))
wrk.add(InlineKeyboardButton(text='🔑 Создать Промокод', callback_data="prom"))
wrk.add(InlineKeyboardButton(text='📊 Статистика', callback_data="statwstatw"))
wrk.add(InlineKeyboardButton(text='❌ Закрыть ❌', callback_data="menu"))


mzakr = ReplyKeyboardMarkup(resize_keyboard=True)
mzakr.add('Отмена❌')

bal = ReplyKeyboardMarkup(resize_keyboard=True)
bal.add('Пополнить Баланс')
bal.add('Отмена❌')
