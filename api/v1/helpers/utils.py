from datetime import datetime, timedelta
import string, secrets, os, re, random, jwt

def generate_random_password(username: str, special_chars: str = "@#", length: int = 12) -> str:
    year = str(datetime.now().year)
    name_part = username[:4].capitalize()
    allowed_chars = string.ascii_letters + string.digits + special_chars
    remaining_length = length - len(name_part) - len(year)
    random_part = ''.join(secrets.choice(allowed_chars) for _ in range(remaining_length))
    full_password = name_part + year + random_part
    scrambled = ''.join(secrets.choice(full_password) for _ in range(length))
    adjusted_password = ''.join(
        c.upper() if c.lower() == 'l' else c.lower() if c.lower() == 'i' else c
        for c in scrambled
    )

    return adjusted_password