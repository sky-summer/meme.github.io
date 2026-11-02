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


def pangwu(images: list[BuildImage], texts: list[str], args: Model):
    location = [
        (55,50),
        (40,50),
    ]
    head = images[0].convert("RGBA").circle().resize((130, 130), keep_ratio=True)
    frames: list[IMG] = []
    for i in range(1,150):
        frame = BuildImage.open(img_dir / f"{i}.png")
        if i < 85:
            frame.paste(head, location[0], below=True)
            frames.append(frame.image)
        else:
            frame.paste(head, location[1], below=True)
            frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "pangwu",
    pangwu,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["胖舞"],
    date_created=datetime(2026, 4, 21),
    date_modified=datetime(2026, 4, 21),
)
