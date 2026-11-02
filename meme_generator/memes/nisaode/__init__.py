from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def ty_pig(images: list[BuildImage], texts, args):

    user_img1 = images[0].convert("RGBA").resize((350, 350), keep_ratio=True)
    user_img2 = images[1].convert("RGBA").resize((350, 350), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img1, (43, 150), below=True)
    frame.paste(user_img2, (526, 270), below=True)
    return frame.save_jpg()


add_meme(
    "nisaode",
    ty_pig,
    min_images=2,
    max_images=2,
    keywords=["你看看你骚的", "骚的"],
    date_created=datetime(2026, 3, 26),
    date_modified=datetime(2026, 3, 26),
)