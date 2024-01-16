import datetime
from typing import Union
from sqlalchemy.orm import sessionmaker


from database.models import UserArchive


class UserArchiveControl:
    """UserArchive control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, user_id: int) -> Union[UserArchive, None]:
        """Get UserArchive from database"""
        get_user_archive = self.session.get(UserArchive, user_id)
        if not get_user_archive:
            return None
        return get_user_archive

    # Добавить новый user archive в базу
    async def add(self,
                  user_id: int,
                  user_fio: str,
                  user_number: int,
                  user_added_manually: bool,
                  user_status: bool,
                  mark_from_partner: str
                  ) -> bool:
        """Add new user archive to database"""

        user_archive = UserArchive(
            user_id=user_id,
            user_fio=user_fio,
            user_number=user_number,
            user_added_manually=user_added_manually,
            user_status=user_status,
            mark_from_partner=mark_from_partner,
            added_to_archive_date=datetime.datetime.now(),
        )
        self.session.add(user_archive)
        return True


    async def get_all(self):
        return self.session.query(UserArchive).all()