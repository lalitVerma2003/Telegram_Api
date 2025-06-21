class RoleStatusChoices:
    ROLE_CHOICES = [
        (0, "user"),
        (1, "admin"),
        (2, "super admin")
    ]
    STATUS_CHOICES = [
        (0, "active"),
        (1, "inactive")
    ]
    USER_ROLE = 0
    ADMIN_ROLE = 1
    SUPER_ADMIN = 2

    ACTIVE_STATUS = 0
    INACTIVE_STATUS = 1
    
class ErrorConst:
    ''' Error constants messages '''
    
    SOMETHING_WENT_WRONG = "Something went wrong."
    VALIDATION_FAILED = "Validation failed."
    INVALID_CREDENTIALS = "Invalid Credentials."
    INVALID_EMAIL = "Invalid email."
    INVALID_PASSWORD = "Invalid Password."
    INVALID_NEW_PASSWORD = "Invalid new password"
    INVALID_OLD_PASSWORD = "Invalid old password"
    INVALID_CONFIRM_PASSWORD = "Invalid confirm password"
    CONFIRM_PASSWORD_NOT_MATCH_TO_NEW_PASSWORD = "Confirm password does not match to new password"
    PASSWORD_CHANGED = "Password changed successfully please login again"
    INVALID_ROLE = "Invalid role."
    ACCESS_DENIED = "Access Denied."
    # ONLY_ADMIN_CAN_ACCESS = "Only admin can access."
    INVALID_DATA_CONST = "Invalid data."
    INTERNAL_PROCESS_FAILED_CONST ="Internal process failed."
    WRONG_EMAIL_ID_CONST ="Wrong email id."
    NOT_AUTHORIZED = "Not Authorized"
    LOGIN_FAILED = "Login failed"
    REFRESH_TOKEN_REQUIRED = "Refresh token is required."
    DEVICE_TOKEN_REQUIRED = "Device token is required."
    DEVICE_ID_REQUIRED = "Device id is required."
    USER_LOGGED_OUT_SUCCESSFULLY = "Logged Out"
    RESET_CODE_SENT_TO_YOUR_MAIL = "Reset code sent to your email"
    OTP_NOT_FOUND = "OTP not found. Generate Again" 
    OTP_HAS_EXPIRED = "OTP has expired. Generate Again"
    OTP_NOT_VALID = "OTP is not valid"
    OTP_VERIFIED = "OTP verified successfully."
    SESSION_CREATION_FAILED = "Session creation failed."
    MISSING_PARAMETER = 'Missing parameter'
    INVALID_LAT_LONG = "Invalid latitude or longitude format."
    INVALID_FILTER = "Invalid filter type. Choose from {'most_viewed', 'most_commented', 'most_saved', 'friends_posts'}."
    INVALID_COUNTRY_CODE = "Invalid country code"

class UserErrorConst:
    USER_PROFILE_FETCHED = "User profile fetched successfully"
    USER_PROFILE_UPDATED = "User profile updated successfully"
    USER_NOT_FOUND = "User not found."
    USER_ALREADY_EXIST = "User already exists"
    USER_LOGGED_IN_SUCCESSFULLY = "User logged in successfully"
    USER_INACTIVE = "User is inactive"
    INVALID_USER_CONST = "Invalid user."
    USER_ALREADY_DELETED="User already deleted."
