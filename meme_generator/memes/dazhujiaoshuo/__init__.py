from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength

img_dir = Path(__file__).parent / "images"


def dazhujiao_shuo(images, texts: list[str], args):
    text = texts[0].strip()  # 去除空字符，防止崩溃
    frame = BuildImage.open(img_dir / "0.png")

    # 修复：draw_text 坐标格式错误 + 自动换行+居中+容错
    try:
        frame.draw_text(
            (177, 531, 670, 631),  # 必须给高度！你之前高度和顶部一样，导致崩溃
            text,
            fill=(72, 110, 173),
            allow_wrap=True,
            font_families=["FZShaoEr-M11S"],
            max_fontsize=50,  # 缩小一点防止溢出
            min_fontsize=20,
            lines_align="center",
        )
    except Exception:  # 捕获所有绘制错误
        raise TextOverLength(text)

    return frame.save_jpg()


add_meme(
    "dazhujiao_shuo",
    dazhujiao_shuo,
    min_texts=1,
    max_texts=1,
    default_texts=["这就是圣堂武士的下场"],
    keywords=["大主教说", "阿塔尼斯说"],
    date_created=datetime(2026, 3, 26),
    date_modified=datetime(2026, 3, 26),
)