from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def liangbaz(images: list[BuildImage], texts, args):
    user_head = images[0]
    self_head = images[1].convert("RGBA").circle().resize((140, 140))
    # fmt: off
    user_locs = [
        (25, 69),
        (25, 69),
        (16, 69),
        (13, 57),
        (25, 82),
        (25, 82),
        (25, 82),
        (25, 69),
        (25, 69),
        (25,48),
        (11,70),
        (15,44),
        (28,49),
        (41,65),
        (31,79),
        (6,67),
        (-20,70),
        (-20,46),
        (-20,26),
        (-6,6)
    ]
    self_locs = [
        (117,35),
        (95,27),
        (81,14),
        (81,14),
        (81,14),
        (151,20),
        (119,16),
        (127,1),
        (140,7),
        (154,16),
        (153,38),
        (141,57),
        (122,58),
        (124,43),
        (124,43),
        (124,43),
    ]
    # fmt: on
    frames: list[IMG] = []
    for i in range(1, 37):
        if i <= 6:
            user_head = user_head.convert("RGBA").circle().resize((80, 80))
        elif 7 < i <= 10:
            user_head = user_head.convert("RGBA").circle().resize((100, 100))
        elif 10 < i <= 14:
            user_head = user_head.convert("RGBA").circle().resize((130, 130))
        elif 14 < i <= 18:
            user_head = user_head.convert("RGBA").circle().resize((150, 150))
        elif 18 < i <= 20:
            user_head = user_head.convert("RGBA").circle().resize((170, 170))

        frame = BuildImage.open(img_dir / f"图层 {i}.png")
        if i < 21:
            frame.paste(user_head, user_locs[i-1], below=True)
        elif i >= 21:
            frame.paste(self_head, self_locs[i-21], below=True)

        frames.append(frame.image)

    return save_gif(frames, 0.1)


add_meme(
    "liangbaz",
    liangbaz,
    min_images=2,
    max_images=2,
    keywords=["给他两巴掌"],
    date_created=datetime(2026, 4, 21),
    date_modified=datetime(2026, 4, 21),
)
