import asyncio
from functools import partial

from aiogram import Router
from aiogram.exceptions import TelegramBadRequest, TelegramEntityTooLarge
from aiogram.types import FSInputFile, Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from download_video import download
from utils import convert_vk_url, logger

from .state import VideoDetails


router = Router(name=__name__)


@router.message(CommandStart())
async def start_message_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Введите ссылку на видео (tiktok, yt, vk, od)")
    await state.set_state(VideoDetails.link)


@router.message(VideoDetails.link, lambda msg: "https" in msg.text)
async def video_link_handler(message: Message, state: FSMContext):
    url = message.text
    if "vkvideo" in message.text:
        url = convert_vk_url(url=url)

    downloaded_video_path = await download(message, link=url)

    file_to_send = FSInputFile(path=downloaded_video_path)
    try:
        await message.answer_document(document=file_to_send)
    except (TelegramBadRequest, Exception) as error:
        logger.error(f"Ошибка при отправке файла {downloaded_video_path}: {error}")
        await message.answer(f'Не удалось отправить файл. Можете посмотреть его на сервере по пути "{downloaded_video_path}"')
    except TelegramEntityTooLarge as error:
        logger.error(f"Ошибка при отправке файла {downloaded_video_path}: {error}")
        await message.answer(f'Файл слишком большой. Можете посмотреть его на сервере по пути "{downloaded_video_path}"')



@router.message(VideoDetails.link)
async def video_link_handler_invalid(message: Message, state: FSMContext):
    await message.answer(f"Введите корректную ссылку")
