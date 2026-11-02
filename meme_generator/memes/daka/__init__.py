from datetime import datetime
from pathlib import Path

import numpy as np
from PIL import Image as PILImage
from PIL.Image import Image as IMG
from pil_utils import BuildImage
from scipy import ndimage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"


def _build_panda_masks(frame_img: IMG):
    """根据模板图片的轮廓生成大熊猫与小熊猫的面部遮罩。

    返回 ``(big_mask, small_mask)``，二者都是 ``"L"`` 模式的 ``PIL.Image``，
    白色区域表示允许显示用户头像的区域。
    """
    arr = np.array(frame_img.convert("RGBA"))
    rgb = arr[:, :, :3].astype(int)
    alpha = arr[:, :, 3]

    is_dark = (rgb[:, :, 0] < 100) & (rgb[:, :, 1] < 80) & (rgb[:, :, 2] < 80) & (alpha > 100)
    dilated = ndimage.binary_dilation(is_dark, iterations=5)
    closed = ndimage.binary_closing(dilated, iterations=3)

    h, w = arr.shape[:2]
    outside = np.zeros((h, w), dtype=bool)
    stack = [(0, 0)]
    while stack:
        y, x = stack.pop()
        if y < 0 or y >= h or x < 0 or x >= w:
            continue
        if outside[y, x] or closed[y, x]:
            continue
        outside[y, x] = True
        stack.extend([(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)])

    inside = ~outside & ~closed
    labeled, num = ndimage.label(inside)

    regions = []
    for i in range(1, num + 1):
        region = labeled == i
        size = int(region.sum())
        if size < 500:
            continue
        rows = np.where(region.any(axis=1))[0]
        cy = int((rows[0] + rows[-1]) // 2)
        regions.append((i, size, cy))

    regions.sort(key=lambda r: r[2])

    if len(regions) >= 2:
        big_id, small_id = regions[0][0], regions[1][0]
        big_mask = (labeled == big_id).astype("uint8") * 255
        small_mask = (labeled == small_id).astype("uint8") * 255
    elif len(regions) == 1:
        big_mask = (labeled == regions[0][0]).astype("uint8") * 255
        small_mask = np.zeros((h, w), dtype="uint8")
    else:
        big_mask = np.zeros((h, w), dtype="uint8")
        small_mask = np.zeros((h, w), dtype="uint8")

    return PILImage.fromarray(big_mask), PILImage.fromarray(small_mask)


def _mask_bbox(mask: IMG):
    """返回遮罩有效像素的 ``(x_min, y_min, x_max, y_max)`` 包围盒。"""
    arr = np.array(mask)
    if not arr.any():
        return None
    rows = np.where(arr.any(axis=1))[0]
    cols = np.where(arr.any(axis=0))[0]
    return int(cols[0]), int(rows[0]), int(cols[-1]), int(rows[-1])


def _paste_clipped(canvas: IMG, head: IMG, mask: IMG, pos):
    """把头像贴到画布上并用 ``mask`` 裁剪到指定区域内。"""
    layer = PILImage.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(head, pos, mask=head)
    clipped = PILImage.new("RGBA", canvas.size, (0, 0, 0, 0))
    clipped.paste(layer, mask=mask)
    return clipped


def da_ka(images: list[BuildImage], texts, args):
    self_img = images[1]
    user_img = images[0]
    frames: list[IMG] = []
    for i in range(2):
        frame = BuildImage.open(img_dir / f"{i}.png")
        w, h = frame.size
        big_mask, small_mask = _build_panda_masks(frame.image)

        big_bbox = _mask_bbox(big_mask)
        small_bbox = _mask_bbox(small_mask)

        # 根据大熊猫包围盒的较大边长确定 user 头像尺寸（多预留一点像素防止边缘裁切）
        big_w = big_bbox[2] - big_bbox[0] + 1
        big_h = big_bbox[3] - big_bbox[1] + 1
        big_size = max(big_w, big_h) + 10
        big_cx = (big_bbox[0] + big_bbox[2]) // 2
        big_cy = (big_bbox[1] + big_bbox[3]) // 2
        user_pos = (big_cx - big_size // 2, big_cy - big_size // 2)

        # 小熊猫同理
        small_w = small_bbox[2] - small_bbox[0] + 1
        small_h = small_bbox[3] - small_bbox[1] + 1
        small_size = max(small_w, small_h) + 10
        small_cx = (small_bbox[0] + small_bbox[2]) // 2
        small_cy = (small_bbox[1] + small_bbox[3]) // 2
        self_pos = (small_cx - small_size // 2, small_cy - small_size // 2)

        user_head = user_img.convert("RGBA").resize((big_size, big_size), keep_ratio=True)
        self_head = self_img.convert("RGBA").resize((small_size, small_size), keep_ratio=True)

        user_clipped = _paste_clipped(frame.image, user_head.image, big_mask, user_pos)
        self_clipped = _paste_clipped(frame.image, self_head.image, small_mask, self_pos)

        composed = PILImage.alpha_composite(user_clipped, self_clipped)
        composed = PILImage.alpha_composite(composed, frame.image)
        frames.append(composed)
    return save_gif(frames, 0.04)


add_meme(
    "da_ka",
    da_ka,
    min_images=2,
    max_images=2,
    keywords=["打卡"],
    date_created=datetime(2026, 9, 30),
    date_modified=datetime(2026, 9, 30),
)