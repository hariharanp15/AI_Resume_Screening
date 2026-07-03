from fastapi import FastAPI
from app.config.database import Base, engine
from app.config.logging import configure_logging
from app.config.settings import get_settings
from app.middleware.cors import add_cors_middleware
from app.middleware.logging import RequestLoggingMiddleware
from app.routes import api_router, root_router
from app import models  # noqa: F401


configure_logging()
settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="1.0.0")
add_cors_middleware(app)
app.add_middleware(RequestLoggingMiddleware)
app.include_router(api_router, prefix=settings.api_prefix)
app.include_router(root_router)
