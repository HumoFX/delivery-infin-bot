from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    contact = State()


class ProcessApp(StatesGroup):
    application = State()
    first_photo = State()
    second_photo = State()
    confirm = State()
