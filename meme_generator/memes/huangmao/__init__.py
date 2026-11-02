import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

from meme_generator.exception import TextOverLength

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def huangmao(images: list[BuildImage], texts, args):
    # rotate 旋转插入图片度数
    user_img = images[0].convert("RGBA").rotate(-13).resize((275, 275), keep_ratio=True)

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (395, 318), below=True)

    return frame.save_jpg()

add_meme(
    "huangmao",
    huangmao,
    min_images=1,
    max_images=1,
    keywords=["黄毛"],
    date_created=datetime(2026, 4, 22),
    date_modified=datetime(2026, 4, 22),
)