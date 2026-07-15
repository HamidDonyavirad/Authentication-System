from fastapi import FastAPI

from app.routers.v1 import auth,forget_password,task

app = FastAPI(title="Auth API", description="Authentication and Authorization API built with FastAPI")


app.include_router(auth.router)
app.include_router(forget_password.router)
app.include_router(task.router)

