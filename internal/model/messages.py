
class response:
    dictionary={}
    def __init__(self,code,message,data: dict = {}):
        self.dictionary["status_code"]=code
        self.dictionary["message"]=message
        self.dictionary["data"]=data


class response_user_data(response):
    dictionary={}
    def __init__(self,code,message,user_data):
        self.dictionary["status_code"]=code
        self.dictionary["message"]=message
        self.dictionary["user_data"]=user_data

class response_messages:
    wrong_username_or_password="Username or password is wrong"
    user_not_exist="User does not exist"
    unauthorized_access="Unauthorized access"
    user_already_exist="User already exist"
    should_not_be_empty="Should not be empty"
    already_looged_in="Already logged in"
    no_address_parameter="There is no address parameter in url"

class status:
    OK="200"
    Redirect="302"
    BadRequest="400"
    Unauthorized="401"
    Forbidden="403"
    NotFound="404"
    MethodNotAllowed="405"
    InternalServerError="500"

    ok_message="OK"
    redirect_message="Redirect"
    bad_request_message="Bad Request"
    unauthorized_message="Unauthorized"
    forbidden_message="Forbidden"
    not_found_message="Not Found"
    method_not_allowed_message="Method Not Allowed"
    internal_server_error_message="Internal Server Error"

