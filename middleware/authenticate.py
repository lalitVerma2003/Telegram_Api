from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from config.environment import *

class APIKeyAuthentication(BaseAuthentication):

    def authenticate(self, request):
        api_key = request.headers.get('X-API-KEY')
        
        if request.path.startswith('/swagger/'):
            return None

        if api_key != X_API_KEY:
            raise PermissionDenied('Invalid or missing API key.')

        return None


class TokenAuthentication(BaseAuthentication):
    authentication_classes = [JWTAuthentication]

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise AuthenticationFailed('Token not found')
        try:
            jwt_object = JWTAuthentication()
            validated_token = jwt_object.get_validated_token(
                token.split(" ")[1])
            current_user = jwt_object.get_user(validated_token)
            
        except AuthenticationFailed as e:
            raise AuthenticationFailed('Invalid Token')

        if not current_user:
            raise AuthenticationFailed('Invalid user')

        request.cur_user = current_user
        return None

