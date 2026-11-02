import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def yaopian(images: list[BuildImage], texts, args):

    user_img = images[0]

    # 随机选择 0.png 或 1.png
    choice = random.randint(0, 1)
    local1 = [
        (675,145),
        (451,460),
        (431,1070)
    ]

    local2 = [
        (750, 200),
        (510, 460),
        (1045, 1135)
    ]

    if choice == 0:
        frame = BuildImage.open(img_dir / "0.png")
        frame.paste(user_img.circle().resize((280,280), keep_ratio=True), local1[0], below=True)
        frame.paste(user_img.circle().resize((150,150),keep_ratio=True), local1[1], below=True)
        frame.paste(user_img.circle().resize((60,60), keep_ratio=True), local1[2], below=True)
    else:
        frame = BuildImage.open(img_dir / "1.png")
        frame.paste(user_img.circle().resize((200,200),keep_ratio=True), local2[0], below=True)
        frame.paste(user_img.circle().resize((120,120),keep_ratio=True), local2[1], below=True)
        frame.paste(user_img.circle().resize((105,105) , keep_ratio=True), local2[2], below=True)

    return frame.save_jpg()

add_meme(
    "yaopian",
    yaopian,
    min_images=1,
    max_images=1,
    keywords=["药片"],
    date_created=datetime(2026, 4, 23),
    date_modified=datetime(2026, 4, 23),
)