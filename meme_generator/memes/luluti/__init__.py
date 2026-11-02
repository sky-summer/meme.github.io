from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import MemeArgsModel, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def luluti(images: list[BuildImage], texts: list[str], args: MemeArgsModel):
    img = images[0].convert("RGBA").square()
    frames: list[IMG] = []
    # fmt: off
    locs = [
        (171, 178, 220), (194, 185, 214), (189, 189, 209),
        (199, 171, 227), (193, 176, 224), (199, 166, 223),
        (200, 168, 220), (202, 180, 226), (216, 178, 206),
        (184, 180, 240), (222, 183, 199), (186, 171, 236),
        (194, 171, 228), (169, 180, 249), (177, 187, 249),
        (192, 187, 219), (186, 173, 233), (187, 170, 229),
        (179, 175, 235), (192, 188, 234), (201, 181, 229),
        (202, 189, 220), (214, 183, 207), (191, 167, 240),
        (224, 187, 197), (215, 179, 208), (182, 185, 250),
        (185, 160, 246), (171, 155, 261), (178, 165, 247),
        (183, 188, 236), (161, 165, 275), (182, 167, 242),
        (186, 191, 235), (181, 176, 251), (186, 180, 231),
        (186, 183, 245), (196, 184, 220), (212, 199, 215),
        (235, 217, 202), (238, 213, 189), (220, 177, 236),
        (206, 153, 232), (228, 197, 201), (216, 111, 264),
        (242, 186, 214), (251, 186, 188), (228, 158, 221),
    ]
    # fmt: on
    for i, (x, y, s) in enumerate(locs):
        frame = BuildImage.open(img_dir / f"图层 {i + 1}.png")
        frame.paste(img.resize((s, s)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme(
    "luluti",
    luluti,
    min_images=1,
    max_images=1,
    keywords=["噜噜踢"],
    date_created=datetime(2026, 10, 14),
    date_modified=datetime(2026, 10, 14),
)
