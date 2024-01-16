from typing import Union
from sqlalchemy.orm import sessionmaker

from database.models import UserForm



class UserFormControl:
    """UserForm control class"""

    def __init__(self, session: sessionmaker):
        self.session = session

    async def get_all(self):
        return self.session.query(UserForm).all()



    async def get(self, form_user_id: int) -> Union[UserForm, None]:
        """Get form from database"""
        get_form = self.session.get(UserForm, form_user_id)
        if not get_form:
            return None
        return get_form

    # Добавить новую форму в базу
    async def add(self,
                  form_user_id: int,
                  user_fio: str,
                  user_number: int,
                  citizenship: str,
                  estimated_mortgage_amount: int,
                  accommodation_type: str,
                  down_payment_amount: int,
                  mortgage_term: int,
                  children_after_2018: bool,
                  credits_in_the_past: bool,
                  official_job: bool,
                  convictions: bool,
                  bankruptcy: bool,
                  late_payments: bool,
                  marriage: bool,
                  children_amount: int
                  ) -> bool:
        """Add new form to database"""
        form = UserForm(
            form_user_id=form_user_id,
            user_fio=user_fio,
            user_number=user_number,
            citizenship=citizenship,
            estimated_mortgage_amount=estimated_mortgage_amount,
            accommodation_type=accommodation_type,
            down_payment_amount=down_payment_amount,
            mortgage_term=mortgage_term,
            children_after_2018=children_after_2018,
            credits_in_the_past=credits_in_the_past,
            official_job=official_job,
            convictions=convictions,
            bankruptcy=bankruptcy,
            late_payments=late_payments,
            marriage=marriage,
            children_amount=children_amount
        )
        self.session.add(form)
        return True