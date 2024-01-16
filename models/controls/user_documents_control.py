from typing import Union
from sqlalchemy.orm import sessionmaker


from database.models import UserDocuments


class UserDocumentsControl:
    """UserDocuments control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, user_id: int) -> Union[UserDocuments, None]:
        """Get user docs from database"""
        get_docs = self.session.get(UserDocuments, user_id)
        if not get_docs:
            return None
        return get_docs

    async def add(self, user_documents_user_id: int) -> bool:
        """Add new history to database"""

        user_documents = UserDocuments(
            user_documents_user_id=user_documents_user_id,
        )
        self.session.add(user_documents)
        return True