from aiogram import types

from loader import dp


@dp.message_handler(commands='help', state='*')
async def bot_help(message: types.Message):
    text = (
        "/start - начать работу\n",
        "/help - помощь\n",
        "/scan - отсканировать qr коды\n",
        "/myapps - показать все приложения\n",
        "/app_list - Показать список 'К принятию'\n",
        "/delivery_list - Показать список 'К доставке'\n",
    )
    await message.answer("\n".join(text))

#
# @dp.message_handler(commands='scan')
# async def bot_scaner(message: types.Message):
#     text = "Отправьте фото с QR-кодами"
#     await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
#     await ProcessScan.photo.set()
#
#
# @dp.message_handler(state=ProcessScan.photo, content_types=types.ContentType.PHOTO)
# async def bot_scaner(message: types.Message, state: FSMContext):
#     image_data = await dp.bot.download_file_by_id(message.photo[-1].file_id, destination_dir='photos/')
#     decoded = read_qr(image_data.name)
#     if decoded:
#         text = "Отсканировано {} QR-кодов".format(len(decoded))
#         for code in decoded:
#             code_id = code.split('=')[-1]
#             text += "\n[{}]({})".format(code_id, code)
#             if await MyApp.query.where(and_(MyApp.app_id == code_id, MyApp.finished == True)).gino.first():
#                 text += " - заявка уже обработана"
#             elif await MyApp.query.where(and_(MyApp.app_id == code_id, MyApp.user_id == message.chat.id,
#                                               MyApp.finished == False)).gino.first():
#                 pass
#             else:
#                 await MyApp.create(user_id=message.from_user.id, app_id=code_id, app_url=code)
#         msg = await message.reply(text=text, parse_mode='Markdown')
#         await msg.pin()
#         await state.finish()
#
#
# @dp.message_handler(commands='myapps', state='*')
# async def bot_myapps(message: types.Message, state: FSMContext):
#     text = "Ваши заявки:\n"
#     apps = await MyApp.query.where(and_(MyApp.user_id == message.from_user.id,
#                                         MyApp.finished == False)).gino.all()
#     print(apps)
#     await message.answer(text=text, reply_markup=myapps(apps), parse_mode='Markdown')
