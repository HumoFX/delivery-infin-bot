import json
from io import BytesIO
from loader import dp
import aiohttp
import ujson
from data.config import LOGS_CHANNEL
from aiohttp import FormData, MultipartWriter

from utils.db_api.models import Users, Log as HTTPLog
from .constants import verify_headers as auth_header, image_headers
from utils.misc.logging import logger


async def send_get_request(url, lang, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=auth_header, params=kwargs) as response:
                data = await response.json()
                print(dict(data))
                return data
        except Exception as err:
            logger.exception(err)


async def get_(url, headers):
    async with aiohttp.ClientSession() as session:
        try:
            # Specifying lang in HEADER
            async with session.get(url, headers=headers) as response:
                status = response.status

                if status == 200:
                    data = await response.json()
                    return data
        except Exception as err:
            logger.exception(err)


async def post_request(url, **kwargs):
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        try:
            async with session.post(url, json=kwargs) as response:
                status = response.status
                try:
                    await HTTPLog.create(url=url,
                                         headers=response.headers,
                                         request=kwargs,
                                         status=status,
                                         response=await response.json(encoding='utf-8'),
                                         method='POST')
                except Exception as err:
                    logger.exception(err)
                if status == 200:
                    data = await response.json()
                    if data.get('data'):
                        return data['data']
                    else:
                        return data
        except Exception as err:
            logger.exception(f"Error in ArchiveCurrencies {err}")


async def post_(url, headers, **kwargs):
    async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
        try:
            async with session.post(url, headers=headers, json=kwargs) as response:
                status = response.status
                try:
                    customer_id = headers.get('customerId')
                    if customer_id and customer_id.isdigit():
                        customer_id = int(customer_id)

                    await HTTPLog.create(url=url,
                                         headers=headers,
                                         request=kwargs,
                                         status=status,
                                         response=await response.json(encoding='utf-8'),
                                         method='POST',
                                         customer_id=customer_id)
                except Exception as err:
                    logger.exception(err)
                print(await response.json())
                if status == 200:
                    data = await response.json()
                    if data.get('errorMessage'):
                        await dp.bot.send_message(LOGS_CHANNEL, text=f"Ошибка в запросе:\n\n<code>{url}\n\n{json.dumps(kwargs, indent=4, ensure_ascii=False)}\n\n{data}</code>")
                    return data
        except Exception as err:
            logger.exception(f"Error in post {err}")


async def post_data(url, headers, **kwargs):
    async with aiohttp.ClientSession() as session:
        try:
            data = FormData()
            data.add_field('file',
                           kwargs.get('app_file_first'),
                           filename='app_file_first_name')
            data.add_field('file',
                           kwargs.get('app_file_second'),
                           filename='app_file_second_name')
            async with session.post(url, headers=headers, data=data) as response:
                print(response)
                status = response.status
                try:
                    await HTTPLog.create(url=url,
                                         headers=headers,
                                         request={'app_name': kwargs.get('app_name')},
                                         status=status,
                                         response=await response.json(encoding='utf-8'),
                                         method='POST')
                except Exception as err:
                    logger.exception(err)
                if status == 200:
                    data = await response.json()
                    return data
        except Exception as err:
            logger.exception(f"Error in post {err}")


# async def refresh_tokens(user: Users):
#     url = REFRESH_TOKEN
#     headers = verify_headers
#     headers['Authorization'] = f"Bearer {user.token}"
#     headers['lang'] = user.lang
#     headers['customerId'] = str(user.customer_id)
#     kwargs = {
#         "refreshToken": user.refresh_token
#     }
#     response = await post_(url, headers, **kwargs)
#     if response.get('data'):
#         user_data = user.data
#         user_data['client'] = response['data']
#         await user.update(data=user_data).apply()
#         return user.token
#     else:
#         print("logout")
#         return None


# async def client_post(url, headers, user: Users = None, **kwargs):
#     async with aiohttp.ClientSession(json_serialize=ujson.dumps) as session:
#         try:
#             async with session.post(url, headers=headers, json=kwargs) as response:
#                 status = response.status
#                 try:
#                     customer_id = headers.get('customerId')
#                     if customer_id and customer_id.isdigit():
#                         customer_id = int(customer_id)
#                     await HTTPLog.create(url=url,
#                                          headers=headers,
#                                          request=kwargs,
#                                          status=status,
#                                          response=await response.json(encoding='utf-8'),
#                                          method='POST',
#                                          customer_id=customer_id)
#                 except Exception as err:
#                     logger.exception(err)
#                 print(await response.json())
#                 if status == 200:
#                     data = await response.json()
#                     # if data.get('errorMessage') == 'Клиент не найден':
#                     #     if data.get('errorMessage'):
#                     #         await dp.bot.send_message(LOGS_CHANNEL,
#                     #                                   text=f"Ошибка в запросе:\n\n<code>METHOD: <b>{response.method}</b>\nURL: {response.url}\n\nHEADERS\n{json.dumps(headers, indent=4, ensure_ascii=False)}\n\nREQUEST\n{json.dumps(kwargs, indent=4,ensure_ascii=False)}\n\nRESPONSE\n{json.dumps(data, indent=4,ensure_ascii=False)}</code>")
#                     #     print("refresh token")
#                     #     if user:
#                     #         token = await refresh_tokens(user)
#                     #         if token:
#                     #             headers['Authorization'] = 'Bearer ' + token
#                     #             async with session.post(url, headers=headers, json=kwargs) as response:
#                     #                 status = response.status
#                     #                 if status == 200:
#                     #                     print('refreshed')
#                     #                     data = await response.json()
#                     return data
#         except Exception as err:
#             logger.exception(f"Error in post {err}")


# async def client_get(url, headers, user):
#     async with aiohttp.ClientSession() as session:
#         try:
#             # Specifying lang in HEADER
#             async with session.get(url, headers=headers) as response:
#                 status = response.status
#                 # print(response.body, response.text, response.json())
#
#                 try:
#                     customer_id = headers.get('customerId')
#                     resp = await response.json()
#                     if customer_id and customer_id.isdigit():
#                         customer_id = int(customer_id)
#                     await HTTPLog.create(url=url,
#                                          headers=headers,
#                                          status=status,
#                                          response=resp,
#                                          method='GET',
#                                          customer_id=customer_id)
#                 except Exception as err:
#                     logger.exception(err)
#                 # print(await response.json())
#                 if status == 200:
#                     data = await response.json()
#                     # if data.get('errorMessage') == 'Клиент не найден':
#                     #     if data.get('errorMessage'):
#                     #         await dp.bot.send_message(LOGS_CHANNEL,
#                     #                                   text=f"Ошибка в запросе:\n\n<code>METHOD: <b>{response.method}</b>\nURL: {response.url}\n\nHEADERS\n{json.dumps(headers, indent=4, ensure_ascii=False)}\n\nRESPONSE\n{json.dumps(data, indent=4, ensure_ascii=False)}</code>")
#                     #     token = await refresh_tokens(user)
#                     #     if token:
#                     #         headers['Authorization'] = 'Bearer ' + token
#                     #         async with session.get(url, headers=headers) as response:
#                     #             status = response.status
#                     #             if status == 200:
#                     #                 print('refreshed')
#                     #                 data = await response.json()
#                     return data
#         except Exception as err:
#             logger.exception(err)
