from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def pigzhaojing(images: list[BuildImage], texts, args):

    user_img = images[0].convert("RGBA").resize((500, 500), keep_ratio=True).circle()
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (750, 145), below=True)
    return frame.save_jpg()


add_meme(
    "pigzhaojing",
    pigzhaojing,
    min_images=1,
    max_images=1,
    keywords=["猪照镜"],
    date_created=datetime(2026, 3, 26),
    date_modified=datetime(2026, 3, 26),
)