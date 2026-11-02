from datetime import datetime
from pathlib import Path
from PIL import Image

from pil_utils import BuildImage
from meme_generator import add_meme

from pydantic import Field

from meme_generator.exception import TextOverLength

# 图片文件夹路径
img_dir = Path(__file__).parent / "images"

default_text = "这个是🐷！"

def lulukajupai(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "0.png")

    text = texts[0] if texts else default_text.format()
    try:
        frame.draw_text(
            (300, 900, 550,950),
            text,
            font_style="bold",
            fill=(72, 110, 173),
            font_families=["FZShaoEr-M11S"],
            max_fontsize=50,
            min_fontsize=10,
            allow_wrap=True
        )
    except ValueError:
        raise TextOverLength(text)

    # 你的配置：位置 + 角度
    USER_IMG_X = 170  # 左上角 X 坐标
    USER_IMG_Y = 695  # 左上角 Y 坐标
    ROTATE_ANGLE = 2  # 旋转角度（正数=逆时针，负数=顺时针）
    USER_IMG_W = 510  # 你要的宽度
    USER_IMG_H = 290  # 你要的高度

    # 1. 处理用户图片（等比例缩放）
    user_img = images[0].convert("RGBA").resize((USER_IMG_W, USER_IMG_H), keep_ratio=True)

    # 2. 旋转图片（关键！旋转并保持透明，不裁剪）
    user_img_rotated = user_img.rotate(
        ROTATE_ANGLE,
        expand=True,  # 自动扩展画布，保证图片不被切掉
        resample=Image.Resampling.BICUBIC,  # 高质量旋转
        fillcolor=(0, 0, 0, 0)  # 透明背景
    )

    # 4. 贴到指定位置（支持角度）
    frame.paste(user_img_rotated, (USER_IMG_X, USER_IMG_Y), below=True)
    return frame.save_jpg()


add_meme(
    "lulukajupai",
    lulukajupai,
    min_images=1,
    max_images=1,
    min_texts=0,
    max_texts=1,
    keywords=["露露卡举牌子"],
    date_created=datetime(2026, 3, 31),
    date_modified=datetime(2026, 3, 31),
)