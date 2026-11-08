from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models import User
from app.routes.user import router as users_router
from app.routes.audit import router as audit_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": settings.environment}

app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(users_router, prefix=settings.api_prefix)
app.include_router(audit_router, prefix=settings.api_prefix)
