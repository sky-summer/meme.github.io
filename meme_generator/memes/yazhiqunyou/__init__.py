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


def yazhiqunyou(images: list[BuildImage], texts: list[str], args: Model):
    head = images[0].convert("RGBA").circle().resize((114, 114), keep_ratio=True)
    locals = [
        (28,110),
        (28,110),
        (18,100),
        (30,110),
        (30,110),
        (30,110),
        (30,110),
        (30,110),
        (30,110),
        (16,105),
        (16,105),
        (16,100),
        (30,110),
        (30,110),
        (32,105),
        (32,105),
        (32,105),
        (25,95),
        (30,95),
        (30,95),
    ]
    frames: list[IMG] = []
    for i in range(1,21):
        frame = BuildImage.open(img_dir / f"图层 {i}.png")
        frame.paste(head, locals[i-1], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "yazhiqunyou",
    yazhiqunyou,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["压制群友"],
    date_created=datetime(2026, 5, 3),
    date_modified=datetime(2026, 5, 3),
)
