from aiogram.utils.callback_data import CallbackData


class ApplicationCB:
    __name = 'application'
    __in_group = 'ig'
    __in_group_confirmation = 'ic'
    action = CallbackData(__name, 'action', 'value')
    in_group = CallbackData(__in_group, 'act', 'val', 'app_id', 'msg')
    in_group_confirmation = CallbackData(__in_group_confirmation, 'act', 'val', 'app_id', 'msg')
