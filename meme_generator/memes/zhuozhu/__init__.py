import random
from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

from meme_generator.exception import TextOverLength

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"


def zhuozhu(images: list[BuildImage], texts, args):

    user_img = images[0].convert("RGBA").circle().resize((150, 150), keep_ratio=True)
    text = texts[0].strip()  # 去除空字符，防止崩溃

    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(user_img, (40, 38), below=True)

    try:
        frame.draw_text(
            (68, 200, 160, 260),  # 必须给高度！你之前高度和顶部一样，导致崩溃
            text,
            fill=(72, 110, 173),
            allow_wrap=True,
            font_families=["FZShaoEr-M11S"],
            max_fontsize=20,  # 缩小一点防止溢出
            min_fontsize=20,
            lines_align="center",
        )
    except Exception:  # 捕获所有绘制错误
        raise TextOverLength(text)

    return frame.save_jpg()

add_meme(
    "zhuozhu",
    zhuozhu,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["捉住"],
    date_created=datetime(2026, 4, 22),
    date_modified=datetime(2026, 4, 22),
)