from typing import Optional, Union
from sqlalchemy.orm import sessionmaker


from database.models import CreditHistory


class CreditHistoryControl:
    """User control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, credit_history_user_id: int) -> Union[CreditHistory, None]:
        """Get user from database"""
        get_history = self.session.get(CreditHistory, credit_history_user_id)
        if not get_history:
            return None
        return get_history



    async def add(self, credit_history_user_id: int) -> bool:
        """Add new history to database"""

        history = CreditHistory(
            credit_history_user_id=credit_history_user_id,
        )
        self.session.add(history)
        return True