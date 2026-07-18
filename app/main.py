from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import  _rate_limit_exceeded_handler

from app.routers.v1 import auth,forget_password,task
from app.core.limiter import limiter
app = FastAPI(title="Auth API", description="Authentication and Authorization API built with FastAPI")

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)
app.include_router(auth.router)
app.include_router(forget_password.router)
app.include_router(task.router)

