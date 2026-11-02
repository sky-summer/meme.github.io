import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif, Maker

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def moistening_water(images: list[BuildImage], texts, args):
    def make_frame(imgs: list[BuildImage]) -> BuildImage:
        user_img = imgs[0].convert("RGBA").resize((165, 125), keep_ratio=True, inside=False).rotate(25)
        
        frame = BuildImage.open(img_dir / "0.png")
        frame.paste(user_img, (505, 300), below=True)
        
        return frame
    
    return make_jpg_or_gif(images, make_frame)

add_meme(
    "moistening_water",
    moistening_water,
    min_images=1,
    max_images=1,
    keywords=["滋水"],
    date_created=datetime(2026, 4, 20),
    date_modified=datetime(2026, 4, 20),
)