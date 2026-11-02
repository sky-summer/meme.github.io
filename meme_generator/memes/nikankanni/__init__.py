from datetime import datetime
from pathlib import Path

from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import make_jpg_or_gif

img_dir = Path(__file__).parent / "images"


def nikankanni(images: list[BuildImage], texts, args):
    frame = BuildImage.open(img_dir / "图层 0.png")

    def make(imgs: list[BuildImage]) -> BuildImage:
        # 左洞（人物脸）(52, 61) - (127, 134)，右洞（猪脸）(128, 80) - (190, 137)
        img1 = imgs[0].convert("RGBA").square().resize((78, 78))
        img2 = imgs[1].convert("RGBA").square().resize((65, 62))
        return (
            frame.copy()
            .paste(img1, (50, 58), below=True)
            .paste(img2, (128, 78), below=True)
        )

    return make_jpg_or_gif(images, make)


add_meme(
    "nikankanni",
    nikankanni,
    min_images=2,
    max_images=2,
    keywords=["你看看你", "看看你"],
    date_created=datetime(2026, 10, 13),
    date_modified=datetime(2026, 10, 13),
)
