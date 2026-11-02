from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def da_pig(images: list[BuildImage], texts, args):
    self_head = images[0].convert("RGBA").circle().resize((90, 90))
    user_head = images[1].convert("RGBA").circle().resize((130, 130))
    # fmt: off
    user_locs = [
        (110, 90), (110, 90), (110, 90), (110, 90), (110, 90),
        (110, 90), (110, 90), (110, 90), (110, 90), (110, 90),
        (110, 90), (110, 90), (110, 90), (110, 90), (110, 90),
        (110, 90), (110, 90), (110, 90), (110, 90), (111, 70),
        (120, 62), (113, 70), (115, 80), (115, 80),(115, 80),
        (115, 80), (115, 80),(115, 80),(115, 80), (115, 80),
        (115, 80), (115, 80),(115, 80),(115, 80), (115, 80),
        (115, 80), (115, 80), (115, 80), (115, 80), (115, 80),
        (115, 80), (115, 80), (115, 80), (115, 80), (115, 80)
    ]
    self_locs = [
         (0, 70),  (0, 70), (0, 70), (0, 70), (0, 70),
        (0, 70), (0, 70),(0, 50), (10, 40), (10, 30),
        (15, 30), (20, 35), (20, 35), (15, 55), (21, 70),
        (21, 70),(21, 70),(21, 70), (20, 50), (20, 50),
        (20, 50),(20, 50), (0, 80), (0, 80),(0, 80),
        (0, 80), (0, 80), (0, 80),(0, 80), (0, 80),
        (0, 80), (0, 80), (0, 80), (0, 80), (0, 80),
        (0, 80), (0, 80), (0, 80), (0, 80), (0, 80),
        (0, 80), (0, 80), (0, 80), (0, 80), (0, 80)
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(1,46):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(user_head, user_locs[i-1], below=True)
        frame.paste(self_head, self_locs[i-1], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


add_meme(
    "da_pig",
    da_pig,
    min_images=2,
    max_images=2,
    keywords=["打猪"],
    date_created=datetime(2026, 4, 21),
    date_modified=datetime(2026, 4, 21),
)
