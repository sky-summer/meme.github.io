from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops
from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.tags import MemeTags
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def head_mask(frame: IMG) -> IMG:
    """取出头部空腔的遮罩，即被熊猫头轮廓包围且不与画布边缘相连的透明区域"""
    alpha = np.array(frame.getchannel("A"))
    height, width = alpha.shape
    count, labels = cv2.connectedComponents(
        (alpha == 0).astype(np.uint8), connectivity=4
    )
    mask = np.zeros((height, width), dtype=np.uint8)
    max_area = 0
    for label in range(1, count):
        region = labels == label
        ys, xs = np.where(region)
        # 与画布边缘相连的是外部背景，不是头部
        if xs.min() == 0 or xs.max() == width - 1:
            continue
        if ys.min() == 0 or ys.max() == height - 1:
            continue
        if region.sum() > max_area:
            max_area = int(region.sum())
            mask = region.astype(np.uint8) * 255
    return Image.fromarray(mask)


def xiaoheizi(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA")
    frames: list[IMG] = []
    for i in range(5):
        frame = BuildImage.open(img_dir / f"{i}.png")
        mask = head_mask(frame.image)
        x0, y0, x1, y1 = mask.getbbox()
        head = img.resize((x1 - x0 + 1, y1 - y0 + 1), keep_ratio=True)
        # 图片裁剪成头部空腔的形状后垫在熊猫头轮廓下方，贴合深色描边
        layer = BuildImage.new("RGBA", frame.size)
        layer.paste(head, (x0, y0), alpha=True)
        layer.image.putalpha(ImageChops.multiply(layer.image.getchannel("A"), mask))
        frame.paste(layer, (0, 0), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


add_meme(
    "xiaoheizi",
    xiaoheizi,
    min_images=1,
    max_images=1,
    keywords=["你个小黑子"],
    date_created=datetime(2026, 10, 8),
    date_modified=datetime(2026, 10, 8),
)
