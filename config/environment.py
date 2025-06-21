from decouple import config, Csv

# DATABASE Configuration for Development
DB_NAME=config('DB_NAME')
DB_USER=config('DB_USER')
DB_PORT=config('DB_PORT')
DB_HOST=config('DB_HOST')
DB_PASSWORD=config('DB_PASSWORD')
 
# X-API-KEY Credentials
X_API_KEY=config('X-API-KEY')

CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')