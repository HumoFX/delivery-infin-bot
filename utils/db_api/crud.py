from datetime import datetime, timedelta

from aiogram import types
from utils.db_api.models import Users, Application
from sqlalchemy import and_, or_, func, String
from sqlalchemy.sql.expression import cast

from utils.db_api.database import db


async def get_user(user_id=None):
    """Returns user object"""
    user_id = types.User.get_current().id if not user_id else user_id
    user = await Users.query.where(Users.user_id == user_id).gino.first()
    return user