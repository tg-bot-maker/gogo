from typing import Optional, Union
from sqlalchemy.orm import sessionmaker


from database.models import User
from database.models import Payments
from database.models import Contract


class UserControl:
    """User control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, user_id: int) -> Union[User, None]:
        """Get user from database"""
        get_user = self.session.get(User, user_id)
        if not get_user:
            return None
        return get_user

    # Добавить нового пользователя в базу
    async def add(self,
                  user_id: int,
                  user_name: Optional[str] = None,
                  user_manager_id: int = 0,
                  ) -> bool:
        """Add new user to database"""

        user = User(
            user_id=user_id,
            user_name=user_name,
            user_stage='greetings',
            user_manager_id=user_manager_id
        )
        self.session.add(user)
        return True


    # Обновить этап пользователя
    async def update_stage(self,
                           user_id: int,
                           user_stage: str,
                           ) -> bool:
        """Update user stage"""
        user = await self.get(user_id)
        user.user_stage = user_stage
        self.session.commit()
        return True


    async def get_all(self):
        """Get all users from database"""
        return self.session.query(User).all()


    async def get_clients_of_referrer(self, referrer_id):
        return self.session.query(User).filter(User.user_manager_id==referrer_id).all()


    async def get_client_fio_by_id(self, client_id):
        client = self.session.query(User).filter(User.user_id==client_id).one()
        return client.user_fio

    async def get_contract_waiting_users(self):
        return self.session.query(User).outerjoin(Contract).filter(Contract.contract_user_id.is_(None)).all()


    async def get_contract_waiting_users_for_partner(self, partner_id):
        return self.session.query(User).outerjoin(Contract).filter(Contract.contract_user_id.is_(None)).filter(User.user_manager_id==partner_id).filter(User.user_stage!="greetings").filter(User.user_stage!="form").all()


    async def get_users_who_paid(self):
        return self.session.query(User).filter(User.user_stage=="payment_done").all()


    async def get_users_who_paid_for_partner(self, partner_id):
        return self.session.query(User).filter(User.user_stage=="payment_done").filter(User.user_manager_id==partner_id).all()


    async def get_partners_list(self):
        return self.session.query(User).filter(User.is_partner==True).all()


    async def get_clients_without_invoice(self):
        #return self.session.query(User).filter(Payments.payment_user_id!=User.user_id).all()
        return self.session.query(User).outerjoin(Payments).filter(Payments.payment_user_id.is_(None)).all()


    async def get_clients_without_invoice_for_partner(self, partner_id):
        return self.session.query(User).outerjoin(Payments).filter(Payments.payment_user_id.is_(None)).filter(User.user_manager_id==partner_id).all()


    async def get_partner_clients(self, partner_id):
        return self.session.query(User).filter(User.user_manager_id == partner_id).all()


    async def get_users_without_partner(self):
        return self.session.query(User).filter(User.user_manager_id == 0000000000).filter(User.is_partner == 0).all()
