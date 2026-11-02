from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def baitui(images: list[BuildImage], texts, args):

    user_img1 = images[0].convert("RGBA").circle().resize((200, 200), keep_ratio=True)
    user_img2 = images[1].convert("RGBA").circle().resize((200, 200), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img2, (380, 150), below=True)
    frame.paste(user_img1, (660, 450), below=True)
    return frame.save_jpg()


add_meme(
    "baitui",
    baitui,
    min_images=2,
    max_images=2,
    keywords=["掰腿"],
    date_created=datetime(2026, 4, 23),
    date_modified=datetime(2026, 4, 23),
)