from PIL.Image import Image as IMG
from arclet.alconna import store_true
from datetime import datetime
from pathlib import Path
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


def aixinjue(images: list[BuildImage], texts: list[str], args: Model):
    location = [
        (100,40),
        (100,40),
        (100,55),
        (100,55),
        (100,65),
        (100,65),
        (100,50),
        (100,50)
    ]
    head = images[0].convert("RGBA").circle().resize((120, 120), keep_ratio=True)
    frames: list[IMG] = []
    for i in range(8):
        frame = BuildImage.open(img_dir / f"{i}.png")
        frame.paste(head, location[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "aixinjue",
    aixinjue,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["爱心撅"],
    date_created=datetime(2026, 5, 3),
    date_modified=datetime(2026, 5, 3),
)
