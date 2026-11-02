from datetime import datetime
from pathlib import Path

from arclet.alconna import store_true
from PIL.Image import Image as IMG
from pil_utils import BuildImage
from pydantic import Field

from meme_generator import MemeArgsModel, MemeArgsType, ParserOption, add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

help_text = "是否将图片变为圆形"


class Model(MemeArgsModel):
    circle: bool = Field(False, description=help_text)


args_type = MemeArgsType(
    args_model=Model,
    args_examples=[Model(circle=False), Model(circle=True)],
    parser_options=[
        ParserOption(
            names=["--circle", "圆"],
            default=False,
            action=store_true,
            help_text=help_text,
        ),
    ],
)


def dian_pig(images: list[BuildImage], texts: list[str], args: Model):
    location = [
        (10,130),
        (10,130),
        (10,130),
        (10,130),
        (10,130),
        (10,130),
        (28,110),
        (28,110),
        (43,80),
        (80,20),
        (80,20),
        (95,0),
        (95,0),
        (110,0),
        (125,25),
        (125,25),
        (123,90),
        (130,120),
        (130,120),
        (130,130),
        (110,130),
        (110,130),
        (110,130),
        (110,130),
        (110,160),
        (108,156),
        (108,156),
        (108,156),
        (108,156),
        (98,160),
        (93,160),
        (93,160),
    ]
    head = images[0].convert("RGBA").circle().resize((80, 80), keep_ratio=True)
    if args.circle:
        head = head.circle()
    frames: list[IMG] = []
    for i in range(1,32):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(head, location[i-1], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "dian_pig",
    dian_pig,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["电猪"],
    date_created=datetime(2026, 4, 21),
    date_modified=datetime(2026, 4, 21),
)
