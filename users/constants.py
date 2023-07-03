import re


PATTERN_PASSWORD = re.compile(r"^[\w]{4,}$")
PATTERN_USERNAME = re.compile(r"^[\w!@#$%^&*-]{5,}$")


INVALID_USERNAME_ERROR = 'An username must be no shorter than 5 characters and\
 contain letters, numbers and !@#$%^&*-_'
INVALID_PASSWORD_ERROR = 'A password must be no shorter than 4 characters and\
 contain the letters, digits and the sign _'

INCORRECT_CREDENTIALS_ERROR = 'Incorrect username or password'
