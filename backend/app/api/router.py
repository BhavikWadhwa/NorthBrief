from fastapi import APIRouter

from app.api.routes import admin, auth, bookmarks, feed, health, meta, preferences, sources

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(preferences.router)
api_router.include_router(feed.router)
api_router.include_router(bookmarks.router)
api_router.include_router(meta.router)
api_router.include_router(admin.router)
api_router.include_router(sources.router)
