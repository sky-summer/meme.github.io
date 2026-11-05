"""带网页界面的本地启动入口。

在原 ``meme_generator.app`` 的基础上挂载静态前端，并在服务启动后自动打开浏览器。

用法::

    python -m meme_generator.webui
    python webui.py                    # 项目根目录下的同名入口
    python webui.py --port 8080        # 指定端口
    python webui.py --no-browser       # 不自动打开浏览器
"""

import argparse
import re
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any, Optional

WEB_DIR = Path(__file__).parent / "web"

# QQ 头像源，按顺序回退；服务端代取可以绕开浏览器的跨域限制
QQ_RE = re.compile(r"^[1-9]\d{4,11}$")
QQ_AVATAR_SOURCES = (
    "https://q1.qlogo.cn/g?b=qq&nk={qq}&s=640",
    "https://qlogo2.store.qq.com/qzone/{qq}/{qq}/640",
)

# 这些表情在本仓库里缺少图片资源，或依赖外部服务，无法生成预览，
# 仅在网页端隐藏，命令行/接口不受影响
UNAVAILABLE_MEMES = {
    "baitui",  # 缺少 images/0.png
    "rou",  # 缺少 images/*.png
    "tian",  # 表情名 xingqiutian，缺少 images/0.png
    "yaopian",  # 缺少 images/*.png
    "ziwei",  # 缺少 images/1.png
    "charpic",  # 字符画尺寸溢出，JPEG 编码失败
    "dianzhongdian",  # 需要配置百度翻译 api key
}


def register_web_api(app: Any):
    """为前端补充一个聚合接口，避免逐条请求每个表情的详细信息。"""
    from meme_generator.manager import get_memes

    @app.get("/api/memes", tags=["webui"])
    def api_memes():
        return [
            {
                "key": meme.key,
                "keywords": meme.keywords,
                "tags": sorted(meme.tags),
                "min_images": meme.params_type.min_images,
                "max_images": meme.params_type.max_images,
                "min_texts": meme.params_type.min_texts,
                "max_texts": meme.params_type.max_texts,
                "default_texts": meme.params_type.default_texts,
            }
            for meme in sorted(get_memes(), key=lambda meme: meme.key)
            if meme.key not in UNAVAILABLE_MEMES
        ]

    @app.get("/api/memes/keys", tags=["webui"])
    def api_meme_keys():
        """表情 key 列表，过滤掉仓库里缺资源、网页端生成不了的表情。"""
        from meme_generator.manager import get_meme_keys

        return [key for key in get_meme_keys() if key not in UNAVAILABLE_MEMES]

    @app.get("/api/qq-avatar", tags=["webui"])
    async def api_qq_avatar(qq: str):
        """按 QQ 号取头像，直接以图片流返回，前端当作上传的图片使用。"""
        import httpx
        from fastapi import HTTPException
        from fastapi.responses import Response

        qq = (qq or "").strip()
        if not QQ_RE.match(qq):
            raise HTTPException(status_code=400, detail="QQ 号格式不对（5~12 位数字）")

        last_error = ""
        async with httpx.AsyncClient(follow_redirects=True, timeout=8) as client:
            for template in QQ_AVATAR_SOURCES:
                try:
                    resp = await client.get(
                        template.format(qq=qq),
                        headers={"user-agent": "Mozilla/5.0", "accept": "image/*"},
                    )
                    resp.raise_for_status()
                except httpx.HTTPError as e:
                    last_error = f"{type(e).__name__}"
                    continue
                content = resp.content
                content_type = resp.headers.get("content-type", "").split(";")[0]
                if not content or not content_type.startswith("image/"):
                    last_error = "返回内容不是图片"
                    continue
                return Response(
                    content=content,
                    media_type=content_type,
                    headers={"cache-control": "public, max-age=3600"},
                )
        raise HTTPException(
            status_code=502, detail=f"头像获取失败：{last_error or '全部来源不可用'}"
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Any, exc: Exception):
        """把未预期的异常收敛成 JSON，避免整个控制台被堆栈刷屏。"""
        from fastapi.responses import JSONResponse

        from meme_generator.log import logger

        logger.opt(colors=True).warning(
            f"<y>{request.method} {request.url.path}</y> 处理失败："
            f"<r>{type(exc).__name__}</r> {exc}"
        )
        return JSONResponse(
            status_code=500,
            content={"detail": f"表情生成失败（{type(exc).__name__}）"},
        )

    return app


def create_app():
    """注册全部路由并挂载前端静态目录。"""
    from fastapi.staticfiles import StaticFiles

    from meme_generator.app import app, register_routers

    class NoCacheStaticFiles(StaticFiles):
        """前端只有 3 个文件，统一加 no-cache，换版后浏览器不会继续用旧页面。"""

        async def get_response(self, path, scope):
            response = await super().get_response(path, scope)
            response.headers["cache-control"] = "no-cache"
            return response

    register_web_api(app)
    register_routers()
    if not WEB_DIR.is_dir():
        raise RuntimeError(f"前端目录不存在：{WEB_DIR}")
    # 必须最后挂载，否则 "/" 会抢占前面的接口路由
    app.mount(
        "/", NoCacheStaticFiles(directory=str(WEB_DIR), html=True), name="webui"
    )
    return app


def wait_and_open(url: str, timeout: float = 60.0):
    """等待服务就绪后打开浏览器。"""
    import urllib.request

    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(f"{url}/meme/version", timeout=3):
                break
        except Exception:
            time.sleep(0.3)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="meme-webui", description="启动表情包生成器本地网页版"
    )
    parser.add_argument("--host", default=None, help="监听地址，默认读取配置文件")
    parser.add_argument("-p", "--port", type=int, default=None, help="监听端口，默认读取配置文件")
    parser.add_argument(
        "--no-browser", action="store_true", help="启动后不自动打开浏览器"
    )
    return parser


def main(argv: Optional[list[str]] = None):
    args = build_parser().parse_args(argv)

    from meme_generator.config import meme_config
    from meme_generator.log import LOGGING_CONFIG, logger, setup_logger

    setup_logger()

    host = args.host or meme_config.server.host
    port = args.port or meme_config.server.port
    # 0.0.0.0 这类监听地址不能直接用于浏览器访问
    visit_host = "127.0.0.1" if host in ("0.0.0.0", "::", "") else host
    url = f"http://{visit_host}:{port}"

    app = create_app()

    logger.opt(colors=True).info(
        f"表情包生成器网页版已启动，浏览器访问： <g><u>{url}</u></g>"
    )
    if not args.no_browser:
        threading.Thread(target=wait_and_open, args=(url,), daemon=True).start()

    import uvicorn

    uvicorn.run(app, host=host, port=port, log_config=LOGGING_CONFIG)


if __name__ == "__main__":
    main()
