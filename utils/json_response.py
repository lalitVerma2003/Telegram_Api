from rest_framework.response import Response
from rest_framework import status
import time
def json_response(success = False, status_code = status.HTTP_400_BAD_REQUEST, message='', error={}, result={} ):

    

    return Response({
        'success': success,
        'status_code': status_code,
        'message': message,
        'result': result,
        'error': error,
        'time': time.time()*1000
    }, status=status_code)
