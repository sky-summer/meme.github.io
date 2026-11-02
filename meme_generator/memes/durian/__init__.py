import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def durian(images: list[BuildImage], texts, args):

    user_img = images[0].convert("RGBA").resize((412, 322), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (276, 516), below=True)

    return frame.save_jpg()

add_meme(
    "durian",
    durian,
    min_images=1,
    max_images=1,
    keywords=["榴莲"],
    date_created=datetime(2026, 4, 20),
    date_modified=datetime(2026, 4, 20),
)