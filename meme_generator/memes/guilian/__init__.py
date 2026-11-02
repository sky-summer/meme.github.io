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


def guilian(images: list[BuildImage], texts: list[str], args: Model):
    head = images[0].convert("RGBA").resize((130, 130), keep_ratio=True)
    location = [
        (120, 210),
        (120, 146),
    ]
    frames: list[IMG] = []
    for i in range(11):
        if i == 2 or i == 10:  # 这里用 or（或者）
            frame = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(head, location[0], below=True)
            frames.append(frame.image)
        elif 2 < i < 10:  # 简洁写法
            frame = BuildImage.open(img_dir / f"{i}.png")
            frame.paste(head, location[1], below=True)
            frames.append(frame.image)
        else:
            frame = BuildImage.open(img_dir / f"{i}.png")
            frames.append(frame.image)
    return save_gif(frames, 0.2)


add_meme(
    "guilian",
    guilian,
    min_images=1,
    max_images=1,
    args_type=args_type,
    keywords=["鬼脸"],
    date_created=datetime(2026, 5, 6),
    date_modified=datetime(2026, 5, 6),
)
