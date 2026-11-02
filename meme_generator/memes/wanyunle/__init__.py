import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

from meme_generator.exception import TextOverLength

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def wanyun(images: list[BuildImage], texts, args):
    user_img = images[0].convert("RGBA").circle().resize((275, 275), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (400, 210), below=True)

    return frame.save_jpg()

add_meme(
    "wanyun",
    wanyun,
    min_images=1,
    max_images=1,
    keywords=["玩晕了"],
    date_created=datetime(2026, 4, 22),
    date_modified=datetime(2026, 4, 22),
)