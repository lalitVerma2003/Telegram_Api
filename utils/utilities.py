from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import time
from rest_framework import status
import re
from datetime import datetime
import random
import os
from dotenv import load_dotenv
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from .country_codes import country_codes

load_dotenv()

def json_response(status_code, success=True, result={}, message="No message", error=""):
    return Response({
        "success": success,
        "status": status_code,
        "result": result,
        "message": message,
        "error": error,
        "time": get_timestamp(),
    }, status=status_code)

def get_tokens(data):
    # Delete previous tokens from database
    previous_tokens =  OutstandingToken.objects.filter(user_id=data.id)
    previous_tokens.delete()
    refreshToken = RefreshToken.for_user(data)
    accessToken = refreshToken.access_token
    return {
        "refresh_token": str(refreshToken),
        "access_token": str(accessToken),
        'access_expiry': refreshToken.access_token.payload['exp'],
        'refresh_expiry': refreshToken.payload['exp'],
    }

def get_timestamp():
    timestamp = int(time.time() * 1000)
    return timestamp

def get_format_date(value):
    print("Hello", type(value))
    if isinstance(value, datetime):
        print(value)
    #   "cteated_at": add_on_item.created_at.strftime('%d/%m/%Y'),
    return value.strftime('%d/%m/%Y')

class CheckValidations:
    def check_missing_fields(required_fields):
        missing_fields = [key for key,
                          value in required_fields.items() if value is None]
        if missing_fields:
            return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False, result={}, message=f"Missing Fields : {', '.join(missing_fields)}", error=f"Missing Fields : {', '.join(missing_fields)}")

    def validate_email(email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False
        return True
    
    def validate_phone(phone_no):
        phone_pattern = re.compile(r"^\+?[0-9]{10,15}$")  # Supports optional + and 10-15 digits
        return bool(phone_pattern.match(phone_no))

    def validate_password(value):
        regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$"
        if not re.match(regex, value):
            return False
        return True
    
    def validate_role(role):
        return True

    def check_status(status):
        print("Status : ", status)
        return True

    def validate_country_code(code):
        print(code)
        if code in country_codes.values():
            return True
        return False

def generate_random_password():
    return "Admin@12321"

def generate_otp():
    # if os.getenv('OTP_MODE')=="development":
    #     return 123456
    # else:
    return random.randint(100000, 999999)
