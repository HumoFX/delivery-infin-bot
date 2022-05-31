from aiogram.utils.callback_data import CallbackData


class ApplicationCB:
    __name = 'application'
    action = CallbackData(__name, 'action', 'value')