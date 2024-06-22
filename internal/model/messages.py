
class response:
    dictionary={}
    def __init__(self,message,data: dict = {}):
        self.dictionary["message"]=message
        self.dictionary["data"]=data


class response_user_data(response):
    dictionary={}
    def __init__(self,code,message,user_data):
        self.dictionary["status_code"]=code
        self.dictionary["message"]=message
        self.dictionary["user_data"]=user_data

class status:
    OK="200"
    Redirect="302"
    BadRequest="400"
    Unauthorized="401"
    Forbidden="403"
    NotFound="404"
    MethodNotAllowed="405"
    InternalServerError="500"
    teaPot="503"

class response_messages:
    wrong_username_or_password="Username or password is wrong"
    user_not_exist="User does not exist"
    unauthorized_access="Unauthorized access"
    user_already_exist="User already exist"
    user_name_already_exist="User name already exist"
    email_already_exist="Email already exist"
    phone_number_already_exist="Phone number already exist"
    should_not_be_empty="Should not be empty"
    already_looged_in="Already logged in"
    no_address_parameter="There is no address parameter in request data"
class status_message:
    ok_message="OK"
    redirect_message="Redirect"
    bad_request_message="Bad Request"
    unauthorized_message="Unauthorized"
    forbidden_message="You Should be Admin"
    not_found_message="Not Found"
    method_not_allowed_message="Method Not Allowed"
    internal_server_error_message="Internal Server Error"
class regex:
    user_name_nv="User name is not valid"
    password_nv="Password is not valid"
    email_nv="Email is not valid"
    phone_nv="Phone number is not valid"
    url_nv="Url is not valid"
class other:
    not_json_array="Input is not a json array"
    token_invalid="Token is invalid"
    token_expired="Token is expired"
    rate_limit="Rate limit exceeded"
    tea_pot="I'm a teapot"


