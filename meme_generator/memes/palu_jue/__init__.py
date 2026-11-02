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


def palujue(images: list[BuildImage], texts: list[str], args: Model):
    location = [
        (85,106),
        (85,106),
        (85,106),
        (85,106),
        (75,106),
        (75,106),
        (75,106),
        (75,106),
        (75,106),
        (75,106),
        (75,106),
        (61,100),
        (61,100),
        (61,100),
        (66,110),
        (66,110),
        (66,110),
        (66,110),
        (66,110),
        (66,110),
        (66,110),
        (90,116),
        (90,116),
        (90,116),
        (90,116),
        (90,116),
        (90,116),
        (90,116),
        (90,100),
        (90,100),
    ]
    head = images[0].convert("RGBA").circle().resize((95, 95), keep_ratio=True)
    frames: list[IMG] = []
    for i in range(1,31):
        frame = BuildImage.open(img_dir / f"图层 {i}.png")
        frame.paste(head, location[i-1], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


add_meme(
    "palujue",
    palujue,
    min_images=1,
    max_images=1,
    args_type=args_type,
    tags={"帕鲁"},
    keywords=["帕鲁撅"],
    date_created=datetime(2026, 4, 23),
    date_modified=datetime(2026, 4, 23),
)
