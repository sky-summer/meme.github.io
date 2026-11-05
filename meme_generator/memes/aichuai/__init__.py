from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

# 模板每帧都留了一个直径 152 的圆形镂空：bbox 为 (0, 172) - (116, 323)，
# 左半边超出画布，所以圆心约为 (40, 248)。头像贴在这个圆心上，
# 比镂空略大 4px，避免缩放后边缘出现白缝，多出的部分会被模板遮住。
FACE_DIAMETER = 160
FACE_CENTER = (40, 248)


def aichuai(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((FACE_DIAMETER, FACE_DIAMETER)).circle()
    x = FACE_CENTER[0] - FACE_DIAMETER // 2
    y = FACE_CENTER[1] - FACE_DIAMETER // 2
    frames: list[IMG] = []
    for i in range(7):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img, (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "aichuai",
    aichuai,
    min_images=1,
    max_images=1,
    keywords=["挨踹"],
    date_created=datetime(2023, 1, 8),
    date_modified=datetime(2026, 11, 5),
)
