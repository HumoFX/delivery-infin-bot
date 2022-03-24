from sqlalchemy import (Column, Integer, String, Sequence, LargeBinary,
                        Numeric, ForeignKey, Boolean, TIMESTAMP, Text,
                        CheckConstraint, Date, BigInteger, JSON, and_, Enum, DateTime)
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from utils.db_api.database import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(String(50))
    first_name = Column(String(64))
    last_name = Column(String(64))
    contact = Column(String(64))


class Application(db.Model):
    __tablename__ = "application"
    app_id = Column(BigInteger, primary_key=True)
    app_name = Column(String(64))
    app_file_first = Column(LargeBinary, nullable=True)
    app_file_second = Column(LargeBinary, nullable=True)
    app_status = Column(String(64))
    app_owner = Column(BigInteger)
    app_created_date = Column(DateTime)
    app_updated_date = Column(DateTime)
    app_finished = Column(Boolean, default=False)


class Log(db.Model):
    __tablename__ = "http_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=True)
    customer_id = Column(BigInteger, nullable=True)
    url = Column(String(128))
    method = Column(String(16))
    status = Column(Integer)
    headers = Column(JSON)
    request = Column(JSON, nullable=True)
    response = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.now())