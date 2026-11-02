import random
from datetime import datetime
from pathlib import Path
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import add_meme

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def get_rich(images: list[BuildImage], texts, args):

    user_img = images[0].convert("RGBA").resize((1140, 1140), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (877, 299), below=True)

    return frame.save_jpg()

add_meme(
    "get_rich",
    get_rich,
    min_images=1,
    max_images=1,
    keywords=["恭喜发财"],
    date_created=datetime(2026, 4, 20),
    date_modified=datetime(2026, 4, 20),
)