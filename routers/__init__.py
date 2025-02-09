__all__ = ("router",)

from aiogram import Router

from .video_loader import router as video_loader_router


router = Router(name=__name__)


router.include_routers(
    video_loader_router,
)