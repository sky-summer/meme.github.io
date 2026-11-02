from datetime import datetime
from pathlib import Path

from PIL.Image import Image as IMG
from pil_utils import BuildImage

from meme_generator import add_meme
from meme_generator.utils import save_gif

img_dir = Path(__file__).parent / "images"

# 脸部圆形空洞的位置与半径
# 由模板图（空心毛茸茸外圈）的挖空区域得出，其他帧均已对齐到该圆心
FACE_CENTER = (75, 75)
FACE_RADIUS = 36.5
# 抬爪帧数（1.png ~ 15.png）
FRAME_NUM = 15
# 每帧间隔，单位秒
DURATION = 0.06


def xiugou_jingli(images: list[BuildImage], texts, args):
    img = images[0].convert("RGBA").square()

    face_size = int(round(FACE_RADIUS * 2))
    face = img.resize((face_size, face_size)).circle()
    face_loc = (
        int(round(FACE_CENTER[0] - face_size / 2)),
        int(round(FACE_CENTER[1] - face_size / 2)),
    )

    frames: list[IMG] = []
    for i in range(1, FRAME_NUM + 1):
        frame = BuildImage.open(img_dir / f"{i}.png")
        canvas = BuildImage.new("RGBA", frame.size, (255, 255, 255, 0))
        canvas.paste(face, face_loc, alpha=True)
        canvas.paste(frame, (0, 0), alpha=True)
        frames.append(canvas.image)
    return save_gif(frames, DURATION)


add_meme(
    "xiugoujingli",
    xiugou_jingli,
    min_images=1,
    max_images=1,
    keywords=["修狗敬礼"],
    date_created=datetime(2026, 10, 30),
    date_modified=datetime(2026, 10, 30),
)
