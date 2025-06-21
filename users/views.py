from rest_framework import status
from rest_framework.views import APIView
from .models import User, UserDevice, Sessions
from .serializers import UserRegisterSerializer, UserDeviceSerializer, SessionSerializer
from middleware.authenticate import APIKeyAuthentication, TokenAuthentication
from utils.utilities import json_response, CheckValidations,get_tokens
from django.contrib.auth import authenticate
from utils.constantsMessages import ErrorConst,UserErrorConst
from django.core.mail import send_mail
from dotenv import load_dotenv
from django.db import transaction
from config.environment import EMAIL_HOST_USER

load_dotenv()

from celery import shared_task

@shared_task
def send_welcome_email(user_email):
    send_mail(
        subject="Welcome in My App",
        message=f"Thankyou for signing up .",
        from_email=EMAIL_HOST_USER,
        recipient_list=[user_email],
    )


class UserRegisterView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data
                email = data.get('email', None)
                password = data.get('password', None)
                fullname = data.get('fullname', None)
                phone_no = data.get('phone_no', None)
                country_code = data.get('country_code', None)
                profile_pic_url=data.get('profile_pic_url',None)
                device_token = data.get('device_token', None)
                device_id = data.get('device_id', None)
                device_type = data.get('device_type', None)
                os = data.get('os', None)

                required_fields = {"Email": email,
                                "Password": password,
                                "Fullname": fullname,
                                "Phone number": phone_no,
                                "Country code": country_code,
                                "Profile pic": profile_pic_url,
                                "Device token": device_token,
                                "Device id": device_id,
                                "Device type": device_type,
                                "OS": os,
                                }

                if (validation_response := CheckValidations.check_missing_fields(required_fields=required_fields)):
                    return validation_response

                if not CheckValidations.validate_email(email):
                    return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False,  result={}, message=ErrorConst.INVALID_EMAIL, error=ErrorConst.INVALID_EMAIL)

                if not CheckValidations.validate_password(password):
                    return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False,  result={}, message=ErrorConst.INVALID_PASSWORD, error=ErrorConst.INVALID_PASSWORD)
                
                if not CheckValidations.validate_country_code(code=country_code):
                    return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False,  result={}, message=ErrorConst.INVALID_COUNTRY_CODE, error=ErrorConst.INVALID_COUNTRY_CODE)

                email = email.lower()
                if User.objects.filter(email=email).exists():
                    return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False,  result={}, message=UserErrorConst.USER_ALREADY_EXIST, error=UserErrorConst.USER_ALREADY_EXIST)

                if not CheckValidations.validate_phone(phone_no):
                    return json_response(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        success=False,
                        result={},
                        message="Invalid phone number",
                        error="Invalid phone number"
                    )
                
                user_data = {
                    'fullname': fullname,
                    'email': email,
                    'password': password,
                    'profile_pic_url':profile_pic_url,
                    'phone_no': phone_no,
                    'country_code': country_code,
                }
                # Serializer
                register_serializer = UserRegisterSerializer(data=user_data)
                if register_serializer.is_valid():
                    user = register_serializer.save()
                    tokens = get_tokens(user)

                    try:
                        UserDevice.objects.filter(device_id=device_id).delete()
                    except Exception as e:
                        return json_response(success=False, message="Device not deleted properly", error=str(e), result={}, status_code=status.HTTP_400_BAD_REQUEST)

                    serialize_device_data = {
                        'user_id': user.id,
                        'device_token': device_token,
                        'device_id': device_id,
                        'device_type': device_type,
                        'os': os,
                    }
                    user_device_serializer = UserDeviceSerializer(
                        data=serialize_device_data)
                    if user_device_serializer.is_valid():
                        user_device_serializer.save()
                    else:
                        return json_response(success=False, message="Device not valid", error=user_device_serializer.errors, result={}, status_code=status.HTTP_401_UNAUTHORIZED)


                    # Delete all entries for device_id(from body) and then do new entry here
                    try:
                        Sessions.objects.filter(user_device_id=user_device_serializer.data['id']).delete()
                    except Exception as e:
                        return json_response(success=False, message="Sessions not deleted properly", error=str(e), result={}, status_code=status.HTTP_400_BAD_REQUEST)
                    
                    serialize_session_data = {
                        'user_id': user.id,
                        'access_token': tokens.get('access_token'),
                        'refresh_token': tokens.get('refresh_token'),
                        'user_device_id': user_device_serializer.data.get("id")
                    }
                    session_serializer = SessionSerializer(
                        data=serialize_session_data)
                    if session_serializer.is_valid():
                        session_serializer.save()
                    else:
                        return json_response(success=False, message="Session not valid", error=session_serializer.errors, result={}, status_code=status.HTTP_401_UNAUTHORIZED)
                  
                    response_data = {
                        "user_data":{
                            "id": user.id,
                            "fullname": user.fullname,
                            "mobile_no": user.phone_no,
                            "profile_pic_url":user.profile_pic_url,
                            "email": user.email,
                            "country_code":user.country_code,
                            "createdAt": user.created_at,
                            "updatedAt": user.updated_at,
                            "deletedAt": user.deleted_at,
                        },
                        "token": tokens,
                    }

                    send_welcome_email.delay(user.email)

                    return json_response(status_code=status.HTTP_201_CREATED, result=response_data, message="User registered successfully")
            
                return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False, result=register_serializer.errors, message="Invalid data")
            
        except Exception as e:
            return json_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, success=False,  result={}, message=ErrorConst.SOMETHING_WENT_WRONG, error=str(e))

class UserLoginView(APIView):
    authentication_classes = [APIKeyAuthentication]

    def post(self, request):
        try:
            with transaction.atomic():
                data = request.data
                email = data.get('email', None)
                password = data.get('password', None)
                device_token = data.get('device_token', None)
                device_id = data.get('device_id', None)
                device_type = data.get('device_type', None)
                os = data.get('os', None)

                required_fields = {
                    "Email": email,
                    "Password": password,
                    "Device token": device_token,
                    "Device id": device_id,
                    "Device type": device_type,
                    "OS": os,
                }

                if (validation_response := CheckValidations.check_missing_fields(required_fields=required_fields)):
                    return validation_response

                if not CheckValidations.validate_email(email):
                    return json_response(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        success=False,
                        result={},
                        message=ErrorConst.INVALID_EMAIL,
                        error=ErrorConst.INVALID_EMAIL
                    )

                if not CheckValidations.validate_password(password):
                    return json_response(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        success=False,
                        result={},
                        message=ErrorConst.INVALID_PASSWORD,
                        error=ErrorConst.INVALID_PASSWORD
                    )
                    
                email = email.lower()
                try:
                    user = User.objects.get(email=email, deleted_at__isnull=True)
                except User.DoesNotExist as e:
                    return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False, result={}, message="User does not exist. Please register", error="User does not exist. Please register")

                user = authenticate(email=email, password=password)
                if not user:
                    return json_response(status_code=status.HTTP_400_BAD_REQUEST, success=False,  result={}, message=ErrorConst.INVALID_CREDENTIALS, error=ErrorConst.INVALID_CREDENTIALS)
            
                tokens = get_tokens(user)

                try:
                    # Validate device data using serializer
                    device_data = {
                        'user_id': user.id,
                        'device_token': device_token,
                        'device_id': device_id,
                        'device_type': device_type,
                        'os': os,
                    }

                    # Check if the device already exists for the user
                    existing_device = UserDevice.objects.filter(user_id=user.id, device_id=device_id).first()

                    if existing_device:
                        # Update the existing device record
                        existing_device.device_token = device_token
                        existing_device.device_type = device_type
                        existing_device.os = os
                        existing_device.save()
                        user_device_serializer = None
                    else:
                        # Create a new device entry if not found
                        user_device_serializer = UserDeviceSerializer(data=device_data)
                        
                        if not user_device_serializer.is_valid():
                            return json_response(
                                success=False,
                                message="Invalid device data",
                                error=user_device_serializer.errors,
                                result={},
                                status_code=status.HTTP_400_BAD_REQUEST
                            )
                        
                        user_device_serializer.save()

                        # Check if a session already exists for the user and device_id
                        existing_session = Sessions.objects.filter(user_id=user.id, user_device_id=user_device_serializer.data.get("id")).first()
                        if existing_session:
                            # Update the existing session with new tokens
                            existing_session.access_token = tokens.get('access_token')
                            existing_session.refresh_token = tokens.get('refresh_token')
                            # existing_session.last_login = timezone.now()
                            existing_session.save()
                        else:
                            # Create a new session if not found
                            serialize_session_data = {
                                'user_id': user.id,
                                'access_token': tokens.get('access_token'),
                                'refresh_token': tokens.get('refresh_token'),
                                'user_device_id': user_device_serializer.data.get("id") if user_device_serializer else existing_device.id,
                            }
                            session_serializer = SessionSerializer(data=serialize_session_data)
                            if session_serializer.is_valid():
                                session_serializer.save()
                            else:
                                return json_response(
                                    success=False,
                                    message="Session not valid",
                                    error=session_serializer.errors,
                                    result={},
                                    status_code=status.HTTP_401_UNAUTHORIZED
                                )
                except Exception as e:
                    return json_response(
                        success=False,
                        message="Error processing device data",
                        error=str(e),
                        result={},
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                    
                response_data = {
                        "user_data":{
                        "id": user.id,
                        "fullname": user.fullname,
                        "mobile_no": user.phone_no,
                        "profile_pic_url":user.profile_pic_url,
                        "email": user.email,
                        "country_code":user.country_code,
                        "createdAt": user.created_at,
                        "updatedAt": user.updated_at,
                        "deletedAt": user.deleted_at,
                    },
                        "token": tokens,
                    }
                return json_response(
                    status_code=status.HTTP_200_OK,
                    result=response_data,
                    success=True,
                    message="Login successful",
                    error=""
                )
            
        except Exception as e:
            return json_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                result={},
                message=ErrorConst.SOMETHING_WENT_WRONG,
                error=str(e)
            )

class UserDetailView(APIView):
    authentication_classes = [APIKeyAuthentication, TokenAuthentication]

    def get(self, request):
        try:
            user_id = request.cur_user.id
            user = User.objects.get(id=user_id, deleted_at__isnull=True)
            
            response_data = {
                        "id": user.id,
                        "fullname": user.fullname,
                        "mobile_no": user.phone_no,
                        "profile_pic_url":user.profile_pic_url,
                        "email": user.email,
                        "country_code":user.country_code,
                        "createdAt": user.created_at,
                        "updatedAt": user.updated_at,
                        "deletedAt": user.deleted_at,
                    }
                
            return json_response(
                status_code=status.HTTP_200_OK,
                result=response_data,
                message="User details fetched successfully",
                error=""
            )

        except User.DoesNotExist:
            return json_response(
                status_code=status.HTTP_404_NOT_FOUND,
                success=False,
                message="User not found",
                error="User not found"
            )

        except Exception as e:
            return json_response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message="Something went wrong",
                error=str(e)
            )
  

