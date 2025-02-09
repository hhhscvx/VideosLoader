


def convert_vk_url(url: str) -> str:
    video_hash = url.split('/')[-1]
    return f"https://vk.com/{video_hash}"
