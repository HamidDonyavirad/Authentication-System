from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import TESTING

if TESTING:
    limiter = Limiter(
        key_func=get_remote_address,
        enabled=False
    )
else:
    limiter = Limiter(
        key_func=get_remote_address
    )