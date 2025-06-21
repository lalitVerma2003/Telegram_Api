from django.core.exceptions import ValidationError
import re

def validate_password(password):
    # Minimum length 8 characters
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    
    # At least one uppercase letter
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    
    # At least one lowercase letter
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    
    # At least one digit
    if not re.search(r'\d', password):
        raise ValidationError("Password must contain at least one digit.")
    
    # At least one special character (e.g., @, #, $, etc.)
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")

    return True


def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, email):
        return True
    else:
        return False

def is_valid_username(username):
     
    pattern = r'^[^\s]{3,16}$'
    
    if re.match(pattern, username):
        return True
    return False


