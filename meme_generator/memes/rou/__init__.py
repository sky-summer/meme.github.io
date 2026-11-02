import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def rou(images: list[BuildImage], texts, args):


    user_img = images[0].convert("RGBA").resize((390, 390), keep_ratio=True)

    # 随机选择 0.png 或 1.png
    choice = random.randint(0, 6)

    locals = [
        (575,113),
        (490,150),
        (375,140),
        (375,140),
        (440,170),
        (310,140),
        (290,188),
    ]

    if choice == 0:
        frame = BuildImage.open(img_dir / "0.png")
        frame.paste(user_img, locals[choice], below=True)
    elif choice == 1:
        frame = BuildImage.open(img_dir / "1.png")
        frame.paste(user_img, locals[choice], below=True)
    elif choice == 2:
        frame = BuildImage.open(img_dir / "3.png")
        frame.paste(user_img, locals[choice], below=True)
    elif choice == 3:
        frame = BuildImage.open(img_dir / "4.png")
        frame.paste(user_img, locals[choice], below=True)
    elif choice == 4:
        frame = BuildImage.open(img_dir / "5.png")
        frame.paste(user_img, locals[choice], below=True)
    elif choice == 5:
        frame = BuildImage.open(img_dir / "6.png")
        frame.paste(user_img, locals[choice], below=True)
    elif choice == 6:
        frame = BuildImage.open(img_dir / "7.png")
        frame.paste(user_img, locals[choice], below=True)

    return frame.save_jpg()

add_meme(
    "rou",
    rou,
    min_images=1,
    max_images=1,
    keywords=["揉"],
    date_created=datetime(2026, 5, 3),
    date_modified=datetime(2026, 5, 3),
)