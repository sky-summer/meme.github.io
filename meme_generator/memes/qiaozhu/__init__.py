from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def qiao_pig(images: list[BuildImage], texts, args):
    user_head = images[0].convert("RGBA").circle().resize((420, 420))
    self_head = images[1].convert("RGBA").circle().resize((290, 290))
    # fmt: off
    self_locs = [
         (80, 1060),  (60, 1100)
    ]
    # fmt: on
    frames: list[IMG] = []

    for i in (0,1):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(user_head,(568,235), below = True)
        frame.paste(self_head, self_locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme(
    "qiao_pig",
    qiao_pig,
    min_images=2,
    max_images=2,
    keywords=["敲猪"],
    date_created=datetime(2026, 4, 23),
    date_modified=datetime(2026, 4, 23),
)
