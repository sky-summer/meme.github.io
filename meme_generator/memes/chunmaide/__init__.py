from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def chunmaide(images: list[BuildImage], texts, args):

    user_img1 = images[0].convert("RGBA").resize((300, 300), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img1, (250, 210), below=True)
    return frame.save_jpg()


add_meme(
    "chunmaide",
    chunmaide,
    min_images=1,
    max_images=1,
    keywords=["纯卖的"],
    date_created=datetime(2026, 3, 27),
    date_modified=datetime(2026, 3, 27),
)