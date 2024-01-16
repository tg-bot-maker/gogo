from typing import Optional, Union
from sqlalchemy.orm import sessionmaker


from database.models import ClientReferralSystem


class ClientReferralSystemControl:
    """ClientReferralSystemControl control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, client_id: int) -> Union[ClientReferralSystem, None]:
        """Get referral from database"""
        get_referral = self.session.get(ClientReferralSystem, client_id)
        if not get_referral:
            return None
        return get_referral


    async def add(self,
                  client_user_id: int,
                  client_referrer_id: int
                  ) -> bool:
        """Add new referral to database"""

        referral = ClientReferralSystem(
            client_user_id=client_user_id,
            client_referrer_id=client_referrer_id,
        )
        self.session.add(referral)
        return True


    async def get_all_referrals(self, referrer_id):
        return self.session.query(ClientReferralSystem).filter(ClientReferralSystem.client_referrer_id == referrer_id).all()