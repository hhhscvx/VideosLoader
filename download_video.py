import re
from aiogram.types import Message
import yt_dlp

from utils import logger


async def download(
    message: Message,
    link: str,
) -> str:
    await message.answer(f"Начинаем скачивать..")
    try:
        ydl_opts_info = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            title = info_dict.get('title', 'video')
        
        title = re.sub(r'[\\/:"*?<>|]', '', title)
        
        if len(title) > 30:
            title = f"{title[:25]}.."

        ydl_opts = {
            'format': (
                '135+140/'
                '134+140/'
                '133+140/'
                'dash_sep-4+dash_sep-12/'  # 480p видео + 135k аудио
                'hls-550+dash_sep-12/'     # 480p HLS + 135k аудио
                'dash_sep-3+dash_sep-12/'  # 360p видео + 135k аудио
                'hls-426+dash_sep-12/'     # 360p HLS + 135k аудио
                'dash_sep-2+dash_sep-12/'  # 240p видео + 135k аудио
                'hls-266+dash_sep-12/'     # 240p HLS + 135k аудио
                'dash_sep-1+dash_sep-12/'  # 144p видео + 135k аудио
                'best[height<=480]+bestaudio/'  # Если ничего не подошло, берем лучшее ≤480p
                'bestvideo+bestaudio/'
                'best'
            ),
            'merge_output_format': 'mp4',
            'outtmpl': 'downloads/{}.%(ext)s'.format(title),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            downloaded_file_path = ydl.prepare_filename(info_dict)
        logger.success(f"Видео {downloaded_file_path} успешно загружено!")
        await message.answer(f"Видео успешно загружено! Отправляем..")
        return downloaded_file_path
    except Exception as error:
        msg = f"Неизвестная ошибка при скачивании: {error}"
        logger.error(msg)
        await message.answer(msg)
