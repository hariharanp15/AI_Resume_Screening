from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.analytics import AnalyticsResponse
from app.services.analytics_service import get_analytics


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsResponse)
def analytics(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_analytics(db)
