from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from utils.utilities import json_response

def custom_exception_handler(exc, context):
    # Call the default exception handler to get the standard error response
    response = exception_handler(exc, context)
    print("Exception Handler called", str(exc))

    # Custom handling for AuthenticationFailed
    if isinstance(exc, PermissionDenied):
        return json_response(status_code=status.HTTP_403_FORBIDDEN, success=False,  result={}, message="Permission not granted", error=str(exc))
    
    if isinstance(exc,AuthenticationFailed):
        return json_response(status_code=status.HTTP_401_UNAUTHORIZED, success=False,  result={}, message=str(exc), error=str(exc))
    
    # Return the standard response
    return response
