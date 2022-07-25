from enum import Enum

PAGINATION = {
    "prev": "⬅",
    "next": "➡"
}


class ApplicationStatus(Enum):
    CARD_ISSUED = "Карта выпущена"
    COURIER = "К доставке"
    PENDING_APPROVEMENT = "Ожидает подтверждения фото"
    APPROVED = "Одобрено андеррайтером"
    DECLINED_BY_UNDERWRITER = "Отклонено андеррайтером"
    DECLINED_BY_CLIENT = "Отклонено клиентом"
