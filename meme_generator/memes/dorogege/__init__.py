from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def dorogege(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    img = images[0].convert("RGBA").square()
    frames: list[IMG] = []
    # (x, y, size)：由各帧脸部透明空洞的包围盒计算得出，
    # 方块贴在空洞后方且不超出角色轮廓，恰好被头发遮住边缘
    # fmt: off
    locs = [
        (51, 85, 84), (51, 84, 83), (53, 83, 84),
        (51, 75, 129), (51, 73, 127), (53, 78, 121),
        (53, 78, 121), (55, 75, 116), (56, 71, 116),
        (50, 78, 120),
    ]
    # fmt: on
    for i, (x, y, s) in enumerate(locs):
        frame = BuildImage.open(img_dir / f"图层 {i + 1}.png")
        frame.paste(img.resize((s, s)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "dorogege",
    dorogege,
    min_images=1,
    max_images=1,
    keywords=["叫哥哥"],
    date_created=datetime(2026, 10, 14),
    date_modified=datetime(2026, 10, 14),
)
