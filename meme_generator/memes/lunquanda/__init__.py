from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def lunquanda(images: list[BuildImage], texts, args):
    # 两个头像分别替换左、右两个人物的圆形脑袋，并逐帧跟随头部移动
    left = images[1].convert("RGBA").circle()
    right = images[0].convert("RGBA").circle()

    # 每帧: (左头像中心, 左头像直径, 右头像中心, 右头像直径)
    # 右侧人物被抡飞的末帧没有右孔，右头像中心记为 None
    # f0-9   两人分立两侧，头像盖在各自圆头中心
    # f10-11 两人拧成麻花，左头右移，右头下沉
    # f12    右头缩小
    # f13-14 右头甩向右下
    # f15    右侧人物被打开，仅剩左侧圆头
    # fmt: off
    locs = [
        ((50, 137), 71, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((50, 134), 69, (188, 136), 72),
        ((60, 134), 69, (188, 136), 72),
        ((72, 134), 69, (190, 141), 72),
        ((72, 134), 69, (193, 148), 59),
        ((72, 134), 69, (193, 148), 59),
        ((72, 134), 69, (212, 172), 59),
        ((72, 134), 69, None, 0),
    ]
    # fmt: on

    frames: list[IMG] = []
    for i, (lc, ls, rc, rs) in enumerate(locs):
        frame = BuildImage.open(img_dir / f"图层 {i + 1}.png")
        # 贴在底层，由线稿的透明圆孔和黑色轮廓自然裁剪头像
        frame.paste(
            left.resize((ls, ls), keep_ratio=True),
            (lc[0] - ls // 2, lc[1] - ls // 2),
            below=True,
        )
        if rc is not None:
            frame.paste(
                right.resize((rs, rs), keep_ratio=True),
                (rc[0] - rs // 2, rc[1] - rs // 2),
                below=True,
            )
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "lunquanda",
    lunquanda,
    min_images=2,
    max_images=2,
    keywords=["抡拳打"],
    date_created=datetime(2026, 10, 8),
    date_modified=datetime(2026, 10, 9),
)
