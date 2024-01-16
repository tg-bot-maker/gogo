from typing import Optional, Union
from sqlalchemy.orm import sessionmaker


from database.models import Payments


class PaymentsControl:
    """Payments control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, client_id: int) -> Union[Payments, None]:
        """Get payment from database"""
        get_payment = self.session.get(Payments, client_id)
        if not get_payment:
            return None
        return get_payment

    # Добавить новый платеж в базу
    async def add(self,
                  client_id: int,
                  payment_link: Optional[str] = None,
                  payment_amount: int = 0
                  ) -> bool:
        """Add new payment to database"""

        payment = Payments(
            payment_user_id=client_id,
            payment_link=payment_link,
            payment_amount=payment_amount
        )
        self.session.add(payment)
        return True

