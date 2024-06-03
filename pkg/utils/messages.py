import internal.model.messages as messages
from typing import Tuple

def create_response(number: int,data: dict = {}) -> Tuple[messages.response, str]:
    d4 = number // 1000
    d3 = (number % 1000) // 100
    d2 = (number % 100) // 10
    d1 = number % 10

    d1_2 = d1 + (d2*10)

    if d4 ==0:
        d4 = messages.status.OK
    elif d4 ==1:
        d4 = messages.status.Redirect
    elif d4 ==2:
        d4 = messages.status.BadRequest
    elif d4 ==3:
        d4 = messages.status.Unauthorized
    elif d4 ==4:
        d4 = messages.status.Forbidden
    elif d4 ==5:
        d4 = messages.status.NotFound
    elif d4 ==6:
        d4 = messages.status.MethodNotAllowed
    elif d4 ==7:
        d4 = messages.status.InternalServerError
    else:
        d4 = messages.status.teaPot
    
    if d3 ==0:
        if d1_2 == 0:
            return messages.response(f"{messages.response_messages.wrong_username_or_password}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 1:
            return messages.response(f"{messages.response_messages.user_not_exist}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 2:
            return messages.response(f"{messages.response_messages.unauthorized_access}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 3:
            return messages.response(f"{messages.response_messages.user_already_exist}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 4:
            return messages.response(f"{messages.response_messages.user_name_already_exist}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 5:
            return messages.response(f"{messages.response_messages.email_already_exist}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 6:
            return messages.response(f"{messages.response_messages.phone_number_already_exist}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 7:
            return messages.response(f"{messages.response_messages.should_not_be_empty}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 8:
            return messages.response(f"{messages.response_messages.already_looged_in}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 9:
            return messages.response(f"{messages.response_messages.no_address_parameter}", f"{data}").dictionary,f"{d4}"
        else:
            return messages.response(f"{messages.other.tea_pot}", f"{data}").dictionary,f"{d4}"

    elif d3 ==1:
        if d1_2 == 0:
            return messages.response(f"{messages.status_message.ok_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 1:
            return messages.response(f"{messages.status_message.redirect_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 2:
            return messages.response(f"{messages.status_message.bad_request_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 3:
            return messages.response(f"{messages.status_message.unauthorized_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 4:
            return messages.response(f"{messages.status_message.forbidden_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 5:
            return messages.response(f"{messages.status_message.not_found_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 6:
            return messages.response(f"{messages.status_message.method_not_allowed_message}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 7:
            return messages.response(f"{messages.status_message.internal_server_error_message}", f"{data}").dictionary,f"{d4}"
        else:
            return messages.response(f"{messages.other.tea_pot}", f"{data}").dictionary,f"{d4}"

    elif d3 ==2:
        if d1_2 == 0:
            return messages.response(f"{messages.regex.user_name_nv}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 1:
            return messages.response(f"{messages.regex.password_nv}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 2:
            return messages.response(f"{messages.regex.email_nv}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 3:
            return messages.response(f"{messages.regex.phone_nv}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 4:
            return messages.response(f"{messages.regex.url_nv}", f"{data}").dictionary,f"{d4}"
        else:
            return messages.response(f"{messages.other.tea_pot}", f"{data}").dictionary,f"{d4}"

    elif d3 ==3:
        if d1_2 == 0:
            return messages.response(f"{messages.other.token_invalid}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 1:
            return messages.response(f"{messages.other.token_expired}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 2:
            return messages.response(f"{messages.other.rate_limit}", f"{data}").dictionary,f"{d4}"
        elif d1_2 == 3:
            return messages.response(f"{messages.other.not_json_array}", f"{data}").dictionary,f"{d4}"
        else:
            return messages.response(f"{messages.other.tea_pot}", f"{data}").dictionary,f"{d4}"
    else:
        return messages.response(f"{messages.other.tea_pot}", f"{data}").dictionary,f"{d4}"
