from fastapi import APIRouter
from app.routes import ai, analytics, auth, candidates, health, history, jobs, search, users


api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(candidates.router)
api_router.include_router(jobs.router)
api_router.include_router(ai.router)
api_router.include_router(analytics.router)
api_router.include_router(search.router)
api_router.include_router(history.router)

root_router = APIRouter()
root_router.include_router(health.router)
