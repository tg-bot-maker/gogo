from sqlalchemy import (
    String,
    BigInteger,
    DateTime,
    Column,
    ForeignKey,
    Boolean
)
from sqlalchemy.sql import func
from database.base import Base
from database.db import engine




class User(Base):
    """Таблица со всеми пользователями"""

    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True, index=True)
    user_fio = Column(String(255), server_default="Аноним", default="Аноним", index=True)
    user_name = Column(String(255), default=None, index=True)
    user_number = Column(String(255), default=None, index=True)
    user_stage = Column(String(255), default=None, index=True)
    register_date = Column(DateTime, nullable=True, default=func.now(), index=True)
    product_choice = Column(String(255), default=None, index=True)
    user_manager_id = Column(BigInteger, server_default="0000000000", default=0000000000, index=True)
    user_notifications_status = Column(Boolean, server_default="true", default=True, index=True)
    notifications_for_partners_status = Column(Boolean, server_default="true", default=True, index=True)
    is_partner = Column(Boolean, server_default="false", default=False, index=True)
    client_step_help_notification_job_id = Column(String(255), nullable=True, server_default="false", default="false", index=True)
    client_step_help_notification_status = Column(Boolean, nullable=True, server_default="false", default=False, index=True)  # True - sent | False - not sent
    mortgage_result = Column(Boolean, nullable=True, default=None, index=True)
    user_group = Column(String, nullable=True)
    user_notes = Column(String(1024), nullable=True)


class UserForm(Base):
    """Таблица с анкетами всех пользователей"""

    __tablename__ = "forms"
    form_user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    user_fio = Column(String(255), default=None, index=True)
    user_number = Column(String(255), default=None, index=True)
    citizenship = Column(String(255), default=None, index=True)
    estimated_mortgage_amount = Column(BigInteger, default=None, index=True)
    accommodation_type = Column(String(255), default=None, index=True)
    down_payment_amount = Column(BigInteger, default=None, index=True)
    mortgage_term = Column(BigInteger, default=None, index=True)
    children_after_2018 = Column(Boolean, default=None, index=True)
    credits_in_the_past = Column(Boolean, default=None, index=True)
    official_job = Column(Boolean, default=None, index=True)
    convictions = Column(Boolean, default=None, index=True)
    bankruptcy = Column(Boolean, default=None, index=True)
    late_payments = Column(Boolean, default=None, index=True)
    marriage = Column(Boolean, default=None, index=True)
    children_amount = Column(BigInteger, default=None, index=True)



class Contract(Base):
    """Таблица с договорами всех пользователей"""

    __tablename__ = "contracts"
    contract_user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    contract_creation_date = Column(DateTime, nullable=True, default=func.now(), index=True)
    contract_path = Column(String(255), default=None, index=True)
    contract_status = Column(Boolean, default=None, index=True)


class CreditHistory(Base):
    """Таблица c кредитной историей всех пользователей"""

    __tablename__ = "credit_history"
    credit_history_user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    credit_history_user_okb = Column(String(255), default=None, index=True)
    credit_history_user_bki = Column(String(255), default=None, index=True)
    credit_history_user_debts = Column(Boolean, default=None, index=True)


class UserDocuments(Base):
    """Таблица со ссылками (на google drive) на документы всех пользователей"""

    __tablename__ = "user_documents"
    user_documents_user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    user_documents_passport23 = Column(String(255), default=None, index=True)
    user_documents_passport45 = Column(String(255), default=None, index=True)
    user_documents_snils = Column(String(255), default=None, index=True)
    user_documents_drive_folder_link = Column(String(255), server_default="Документы не загружены", default="Документы не загружены", index=True)


class Payments(Base):
    """Таблица с платежами всех пользователей"""

    __tablename__ = "payments"
    payment_user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    payment_amount = Column(BigInteger, default=None, index=True)
    payment_link = Column(String(255), default=None, index=True)
    payment_status = Column(Boolean, server_default="0", default=False, index=True)
    payment_date = Column(DateTime, nullable=True, index=True)


class UserArchive(Base):
    """Таблица с архивом всех пользователей, которые уже получили услугу, или просто обращались в бот"""

    __tablename__ = "user_archive"
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    user_tg_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=True)
    user_fio = Column(String(255), default=None, index=True)
    user_number = Column(String(255), default=None, index=True)
    user_added_manually = Column(Boolean, server_default="0", default=False, index=True)
    user_status = Column(Boolean, nullable=False, index=True) #1 - Услуга оказана, 0 - Не оказана
    added_to_archive_date = Column(DateTime, nullable=False, index=True)
    last_check_date = Column(DateTime, nullable=True, index=True)
    mark_from_partner = Column(String(1024), nullable=True, index=True)



class ClientReferralSystem(Base):
    "Таблица с реферальной системой для клиентов"

    __tablename__ = "client_refferal_system"
    client_user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True, nullable=False)
    client_referrer_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=True, index=True)
    payment_amount = Column(BigInteger, default=0, index=True)
    payment_status = Column(Boolean, server_default="0", default=False, index=True)
    payment_date = Column(DateTime, nullable=True, index=True)



Base.metadata.create_all(engine)