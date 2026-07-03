from fastapi import APIRouter
from . import ai, analytics, auth, candidates, jobs


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(candidates.router)
api_router.include_router(jobs.router)
api_router.include_router(ai.router)
api_router.include_router(analytics.router)
