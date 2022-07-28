import json

from datetime import datetime

from utils.db_api.models import Region, District
from .constants import *
from .request import send_get_request, post_request, post_, post_data
import textwrap


async def get_application(app_id):
    """
    Получение данных о приложении
    :param app_id: ID приложения
    :return: ответ сервера
    """
    return await send_get_request(url=f'{baseUrl}/card-delivery/courier/info/{app_id}', lang='ru')


async def get_application_list():
    # return await send_get_request(url=f'{baseUrl}/card-delivery/courier/list', lang='ru')
    resp = {'data':
                [{'applicationId': 'DU002282',
                  'cardType': 'UzCard',
                  'phoneNumber': '998946263101',
                  'fullName': 'OTABEKOVA DILDORA SHUXRATJON QIZI',
                  'passport': 'AD0813017',
                  'dateOfBirth': '1993-09-01',
                  'region': 'Тошкент шахри',
                  'city': 'Учтепа', 'district': 'Учтепа тумани',
                  'street': 'Фазылтепа ',
                  'house': '1',
                  'flat': '1', 'comment': '1', 'status': 'REJECTED'},
                 {'applicationId': 'DU002283',
                  'cardType': 'Humo',
                  'phoneNumber': '998946263101',
                  'fullName': 'OTABEKOVA DILDORA SHUXRATJON QIZI',
                  'passport': 'AD0813017',
                  'dateOfBirth': '1993-09-01',
                  'region': 'Тошкент шахри',
                  'city': 'Бектемир', 'district': 'Бектемир тумани',
                  'street': 'Фазылтепа ',
                  'house': '1',
                  'flat': '1', 'comment': '1', 'status': 'REJECTED'},
                 {'applicationId': 'DU002284',
                  'cardType': 'Visa',
                  'phoneNumber': '998946263101',
                  'fullName': 'OTABEKOVA DILDORA SHUXRATJON QIZI',
                  'passport': 'AD0813017',
                  'dateOfBirth': '1993-09-01',
                  'region': 'Тошкент шахри',
                  'city': 'Учтепа', 'district': 'Учтепа тумани',
                  'street': 'Фазылтепа ',
                  'house': '1',
                  'flat': '1', 'comment': '1', 'status': 'REJECTED'}
                 ],
            'status': 0, 'time': 1658382222671}

    return resp


async def update_application(app_id, **kwargs):
    """
    Обновление данных о приложении
    :param app_id: ID приложения
    :param data: данные для обновления
    :return: ответ сервера
    """
    # hea
    headers = image_headers
    # token = "eyJraWQiOiIvcHJpdmF0ZWtleS5wZW0iLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9
    # .eyJpc3MiOiJpbmZpbmJhbmsiLCJqdGkiOiJpbmZpbjdiNTM1OGYwLTBkNjMtNGVhMS1hOTM2LThmYjZiNTZkYzlkZiIsInN1YiI6IjE5OTgyMiIsImN1c3RvbWVySUQiOiIxOTk4MjIiLCJncm91cHMiOlsiTk9OX0NMSUVOVCJdLCJhdWQiOiJ1c2luZy1qd3QiLCJleHAiOjE2NTQxMDY3MzQsImlhdCI6MTY0ODEwNjczNCwiYXV0aF90aW1lIjoxNjQ4MTA2NzM0fQ.pfiqQy2BfOnzFdWbEveSC9W49khMk8jRRrgUjiv8ddwrfHtOBDXuCavo-ulvlM2iRBYBO-AchFRx8LbmEsFJSu3stq7ERgyKP13y3RIwJ1Q1rr-BYYuz2295M547bpq2_EAnMRQM0XNNPc_EmNJKJG6kOhPLBuNVdUO69ElB0OhU9UhjyinMrWFzrv7j3lqF3D0KtE8jTg4-ViT0ytDs4_vaz2vJ2KwMULO4_LJXDgQP7dVfZJ2su8sjqifQE6pV4wYsKhEPdEMA25mjWpw8wtGDYDIWC8YwIrrPDd6wAJmol-4ciResluVh0UxesKOPZrQ4ttGMv6Fb3X8zYkKLAg" headers['Authorization'] = f'Bearer {token}'
    return await post_data(url=f'{baseUrl}/card-delivery/application/save/photos/{app_id}', headers=headers, **kwargs)


# create class Customer with kwargs of name, surname, patronymic, phone_number fields
class Customer:
    def __init__(self, **kwargs):
        self.phone_number = kwargs.get('phoneNumber')

    def __str__(self):
        return f'*Телефон:* {self.phone_number}'


# create class Passport with kwargs of name, lastname, patronymic, series, number, issued_by, date_of_issue,  birth_date, birth_place fields
class Passport:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.lastname = kwargs.get('lastName')
        self.patronymic = kwargs.get('patronymic')
        self.series = kwargs.get('passportSerial')
        self.number = kwargs.get('passportNumber')
        self.birth_place = kwargs.get('birthPlace')
        self.date_of_issue = datetime.fromtimestamp(kwargs.get('dateOfIssue') / 1000).date().strftime('%d.%m.%Y')
        self.date_of_expiry = datetime.fromtimestamp(kwargs.get('dateOfExpiry') / 1000).date().strftime('%d.%m.%Y')
        self.date_of_birth = kwargs.get('dateOfBirth')
        self.issued_by = kwargs.get('issuedBy')
        self.inn = kwargs.get('inn')

    def __str__(self):
        return f"""
        *ФИО:*{self.lastname} {self.name} {self.patronymic}
        *Серия и номер:* {self.series} {self.number}
        *Дата рождения:* {self.date_of_birth}
        *Место рождения:* {self.birth_place}
        *Дата выдачи:* {self.date_of_issue}
        *Дата окончания:* {self.date_of_expiry}
        *Кем выдан:* {self.issued_by}
        *ИНН:* {self.inn}
        """


# create class Address with kwargs of region, city, district, street, house, flat, comment fields
class Address:
    def __init__(self, **kwargs):
        self.region = kwargs.get('region', '')
        self.city = kwargs.get('city', '')
        self.district = kwargs.get('district', '')
        self.street = kwargs.get('street', '')
        self.house = kwargs.get('house', '')
        self.flat = kwargs.get('flat', '')
        self.comment = kwargs.get('comment', '')

    def __str__(self):
        return f"""
        *Регион:* {self.region}
        *Город:* {self.city}
        *Район:* {self.district}
        *Улица:* {self.street}
        *Дом:* {self.house}
        *Квартира:* {self.flat}
        *Комментарий:* {self.comment}
        """


STATUS = {
    "APPROVED": "Заявка подтверждена банком",
    "CANCELLED_BY_CRM": "Заявка отклонена банком",
    "CARD_ISSUED": "Карта выпущена",
    "COMPLETED": "Заявка завершена",
    "COURIER": "Карта передана курьеру",
    "HISTORY": "Заявка архивирована",
    "NON_COMPLETE": "Заявка не завершена",
    "PENDING": "Ожидает подтверждения заявки банком",
    "REJECTED": "Заявка отклонена",
    "UNDERWRITER": "Заявка возвращена банком на доработку",
    "VISIT_BANK": "По заявке необходимо посетить банк"
}


# create class Delivery with kwargs of customer, passport, address fields
class Delivery:
    def __init__(self, **kwargs):
        # self.customer = Customer(**kwargs.get('customerData'))
        # self.passport = Passport(**kwargs.get('passportDataEntity'))
        # self.address = Address(**kwargs.get('address', {}))
        self.application_id = kwargs.get('applicationId', '')
        self.card_type = kwargs.get('cardType', '')
        self.phone_number = kwargs.get('phoneNumber', '')
        self.full_name = kwargs.get('fullName', '')
        self.passport = kwargs.get('passport', '')
        self.date_of_birth = kwargs.get('dateOfBirth', '')
        self.region = kwargs.get('region', '')
        self.city = kwargs.get('city', '')
        self.district = kwargs.get('district', '')
        self.street = kwargs.get('street', '')
        self.house = kwargs.get('house', '')
        self.flat = kwargs.get('flat', '')
        self.comment = kwargs.get('comment', '')
        self.status = kwargs.get('status', '')

    def __str__(self):
        return f"""
        *Номер заявки:* {self.application_id}
        *Тип карты:* {self.card_type}
        *Статус:* {STATUS[self.status]}
        
        *Номер телефона:* {self.phone_number}
        *ФИО:* {self.full_name}
        *Паспорт:* {self.passport}
        *Дата рождения:* {self.date_of_birth}
        *Регион:* {self.region}
        *Город:* {self.city}
        *Район:* {self.district}
        *Улица:* {self.street}
        *Дом:* {self.house}
        *Квартира:* {self.flat}
        
        *Комментарий:* {self.comment}
        """

    async def new_str(self):
        region = await Region.query.where(Region.id == int(self.region)).gino.first()
        district = await District.query.where(District.id == int(self.district)).gino.first()
        region_name = self.region
        district_name = self.district
        if region:
            region_name = region.name_ru
        if district:
            district_name = district.name_ru
        return f"""
        *Номер заявки:* {self.application_id}
        *Тип карты:* {self.card_type}
        *Статус:* {STATUS[self.status]}

        *Номер телефона:* {self.phone_number}
        *ФИО:* {self.full_name}
        *Паспорт:* {self.passport}
        *Дата рождения:* {self.date_of_birth}
        *Регион:* {region_name}
        *Город:* {self.city}
        *Район:* {district_name}
        *Улица:* {self.street}
        *Дом:* {self.house}
        *Квартира:* {self.flat}

        *Комментарий:* {self.comment}
        """


class DeliveryShort:
    def __init__(self, **kwargs):
        self.application_id = kwargs.get('applicationId', '')
        self.card_type = kwargs.get('cardType', '')
        self.phone_number = kwargs.get('phoneNumber', '')
        self.full_name = kwargs.get('fullName', '')
        self.passport = kwargs.get('passport', '')
        self.date_of_birth = kwargs.get('dateOfBirth', '')
        self.region = kwargs.get('region', '')
        self.city = kwargs.get('city', '')
        self.district = kwargs.get('district', '')
        self.street = kwargs.get('street', '')
        self.house = kwargs.get('house', '')
        self.flat = kwargs.get('flat', '')
        self.comment = kwargs.get('comment', '')
        self.status = kwargs.get('status', '')

    def __str__(self):
        return f"""
        🆔 /{self.application_id} - {STATUS[self.status]}
        💳 {self.card_type}
        📦 {self.region}, {self.city}, {self.district}, ул. {self.street}, д.{self.house} кв.{self.flat}
        📲 Тел. {self.phone_number}
        """

    async def new_str(self):
        region_name = self.region
        district_name = self.district
        if self.region.isdigit():
            region = await Region.query.where(Region.id == int(self.region)).gino.first()
            if region:
                region_name = region.name_ru
        if self.district.isdigit():
            district = await District.query.where(District.id == int(self.district)).gino.first()
            if district:
                district_name = district.name_ru
        return f"""
                🆔 /{self.application_id} - {STATUS[self.status]}
                💳 {self.card_type}
                📦 {region_name}, {self.city}, {district_name}, ул. {self.street}, д.{self.house} кв.{self.flat}
                📲 Тел. {self.phone_number}
                """

    def to_dict(self):
        result: dict = {
            "applicationId": self.application_id,
            "cardType": self.card_type,
            "phoneNumber": self.phone_number,
            "fullName": self.full_name,
            "passport": self.passport,
            "dateOfBirth": self.date_of_birth,
            "region": self.region,
            "city": self.city,
            "district": self.district,
            "street": self.street,
            "house": self.house,
            "flat": self.flat,
            "comment": self.comment,
            "status": self.status,
        }
        return result


# create class Application with kwargs of id, data fields
class Application:
    def __init__(self, **kwargs):
        self.data = Delivery(**kwargs.get('data'))

    def __str__(self):
        text = f"""
        {self.data}
        """
        return textwrap.dedent(text)

    def __str_group__(self):
        text = f"""
        {self.data}
        """
        return textwrap.dedent(text)

    async def new_str(self):
        text = f"""
                {await self.data.new_str()}
                """
        return textwrap.dedent(text)


class ApplicationList:
    def __init__(self, **kwargs):
        self.data = [DeliveryShort(**x) for x in kwargs.get('data')]

    def __str__(self):
        text = ""
        for i in self.data:
            text += f"{i}"
        return textwrap.dedent(text)

    def __str_group__(self):
        text = ""
        for i in self.data:
            text += f"{i}"
        return textwrap.dedent(text)

    async def new_str(self):
        text = ""
        for i in self.data:
            text += f"{await i.new_str()}"
        return textwrap.dedent(text)

    def to_dict(self):
        result: dict = {'data': self.data}
        return result
