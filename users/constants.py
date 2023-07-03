import re


PATTERN_PASSWORD = re.compile(r"^[\w]{4,}$")
PATTERN_USERNAME = re.compile(r"^[\w!@#$%^&*-]{5,}$")
