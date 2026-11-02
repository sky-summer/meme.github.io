from PIL.Image import Image as IMG
from datetime import datetime
from pathlib import Path
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.exception import TextOverLength
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def jieke(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").circle().resize((45, 45), keep_ratio=True)
    frame = BuildImage.open(img_dir / "0.png")
    frame.paste(img, (145, 16), below=True)

    text = texts[0].strip()
    try:
        frame.draw_text(
            (67, 252, 120, 270),
            text,
            font_style="bold",
            fill=(255, 255, 255),
            font_families=["Aller_Bd"],
            max_fontsize=50,
            min_fontsize=10,
            allow_wrap=True
        )
    except ValueError:
        raise TextOverLength(text)


    return frame.save_jpg()

add_meme(
    "jieke",
    jieke,
    min_images=1,
    max_images=1,
    max_texts=1,
    min_texts=1,
    keywords=["接客"],
    date_created=datetime(2026, 5, 11),
    date_modified=datetime(2026, 5, 11),
)
