from aiogram.dispatcher import Dispatcher
from aiogram import types
from glas_osla.db.base import async_session
from glas_osla.db import db_commands
from glas_osla.db.models.users_md import User
from glas_osla.filters.is_client import ClientFilter
from glas_osla.templates import general_phrases
from glas_osla.keyboards.inline import keyboards
from sqlalchemy import select


async def profile(message: types.Message):
    async with async_session() as db_sess:
        query = select(User.tg_id, User.name, User.person_type, User.created_date).where(
            User.tg_id == message.from_user.id)
        data = map(str, (await db_sess.execute(query)).first())
    await message.answer(f"Информация о вас:\n{' '.join(data)}")


async def show_menu(message: types.Message):
    user_nickname = await db_commands.get_user_nickname(message.from_user.id)
    await message.answer(general_phrases.menu_text.format(user_nickname), reply_markup=keyboards.menu_keyboard)


async def show_quick_info(message: types.Message):
    await message.answer(general_phrases.quick_info_text, reply_markup=keyboards.menu_keyboard)


async def show_expenses_categories(callback: types.CallbackQuery):
    expenses_keyboard = await keyboards.expenses_categories_keyboard(callback.from_user.id)
    await callback.message.answer("Ваши категории у расходов", reply_markup=expenses_keyboard)


def setup_general_handlers(dp: Dispatcher):
    dp.register_message_handler(profile, ClientFilter(True), commands='profile')
    dp.register_message_handler(show_menu, ClientFilter(True), commands='menu')
    dp.register_message_handler(show_quick_info, ClientFilter(True), commands='quick')
    dp.register_callback_query_handler(show_expenses_categories, text='get_expenses')