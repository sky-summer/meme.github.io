import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def ziwei(images: list[BuildImage], texts, args):

    user_img = images[0].convert("RGBA").resize((390, 390), keep_ratio=True)

    # 随机选择 0.png 或 1.png
    choice = random.randint(0, 1)

    if choice == 0:
        frame = BuildImage.open(img_dir / "0.png")
        frame.paste(user_img, (373, 310), below=True)
    else:
        frame = BuildImage.open(img_dir / "1.png")
        frame.paste(user_img, (420, 410), below=True)

    return frame.save_jpg()

add_meme(
    "ziwei",
    ziwei,
    min_images=1,
    max_images=1,
    keywords=["紫薇","在群里紫薇"],
    date_created=datetime(2026, 3, 27),
    date_modified=datetime(2026, 3, 27),
)