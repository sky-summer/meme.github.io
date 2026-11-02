from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def ketou(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square().resize((78, 78))
    # fmt: off
    locs = [
        (25, -3),
        (31, 132),
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(2):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(img.rotate(-24 * i), locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


add_meme(
    "ketou",
    ketou,
    min_images=1,
    max_images=1,
    keywords=["你磕头"],
    date_created=datetime(2026, 10, 12),
    date_modified=datetime(2026, 10, 12),
)

