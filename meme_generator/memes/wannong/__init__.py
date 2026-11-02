from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def wannong(images: list[BuildImage], texts, args):

    user_img1 = images[0].convert("RGBA").circle().resize((336, 336), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img1, (80, 233), below=True)
    return frame.save_jpg()


add_meme(
    "wannong",
    wannong,
    min_images=1,
    max_images=1,
    keywords=["玩弄"],
    date_created=datetime(2026, 5, 3),
    date_modified=datetime(2026, 5, 3),
)