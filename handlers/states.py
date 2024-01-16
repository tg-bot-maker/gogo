from aiogram.dispatcher.filters.state import StatesGroup, State


class SG(StatesGroup):
    # form
    number = State()
    citizenship = State()
    accommodation_type = State()
    mortgage_term = State()
    children_after_2018 = State()
    check_form = State()
    form_final = State()


    #generate_contract
    enter_birth_date = State()
    enter_passport_data = State()
    enter_passport_issuer = State()
    enter_client_email = State()
    generate_contract_final = State()
    enter_date = State()
    enter_credit_sum = State()
    enter_passport_issue_date = State()
    enter_passport_issue_code = State()
    enter_credit_sum_words = State()
    enter_cost_sum_digits = State()
    enter_cost_sum_words = State()
    enter_percent_digits = State()
    enter_percent_words = State()



    #check_history
    upload_file_okb = State()
    upload_file_bki = State()

    #upload_documents
    upload_documents_passport_page23 = State()
    upload_documents_passport_page45 = State()
    upload_snils = State()

    #invoice_creation
    invoice_creation = State()
    invoice_creation_final = State()


    #add_to_archive
    add_to_archive_fio = State()
    add_to_archive_number = State()
    add_to_archive_mark = State()
    add_to_archive_final = State()

    #partners_panel_for_admin
    create_partner_final = State()
    change_partner_choose_partner = State()
    change_partner_final = State()


    #registration
    reg_get_fio_enter_number = State()
    reg_final = State()








# ------------------------------------------------------ #
    #pagination
    user_list_pagination = State()
    user_list_pagination_payments = State()
    clients_waiting_contract_pagination = State()
    users_who_paid_pagination = State()
    archive_users_list_pagination = State()
    partner_clients_list_pagination = State()
    partners_list_pagination = State()
    users_without_partner = State()
    partners_pagination = State()


