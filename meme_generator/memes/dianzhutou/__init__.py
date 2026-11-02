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


def dian_pig_head(images: list[BuildImage], texts: list[str], args: Model):
    head = images[0].convert("RGBA").resize((120, 120), keep_ratio=True)
    localtion = [
        (40, 30),
        (45, 30),
        (40, 30),
    ]
    if args.circle:
        head = head.circle()
    frames: list[IMG] = []
    for i in range(3):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(head, localtion[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.03)


add_meme(
    "dian_pig_head",
    dian_pig_head,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["电猪头"],
    date_created=datetime(2026, 5, 6),
    date_modified=datetime(2026, 5, 6),
)
