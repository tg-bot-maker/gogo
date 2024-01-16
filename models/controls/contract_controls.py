from typing import Optional, Union
from sqlalchemy.orm import sessionmaker


from database.models import Contract


class ContractControl:
    """Contract control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get(self, client_id: int) -> Union[Contract, None]:
        """Get contract from database"""
        get_contract = self.session.get(Contract, client_id)
        if not get_contract:
            return None
        return get_contract

    # Добавить новый contract в базу
    async def add(self,
                  client_id: int,
                  contract_path: Optional[str] = None,
                  contract_status: int = 0
                  ) -> bool:
        """Add new contract to database"""

        contract = Contract(
            contract_user_id=client_id,
            contract_status=contract_status,
            contract_path=contract_path
        )
        self.session.add(contract)
        return True

