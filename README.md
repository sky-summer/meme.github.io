<div align="center">

# 表情包生成器 · meme-generator（带网页版）

_✨ 900+ 表情模板，浏览器里选模板、填内容、出图 ✨_

MIT License · Python 3.9+ · FastAPI + Skia

</div>

> [!IMPORTANT]
> **借用说明**：本仓库是 [**MemeCrafters/meme-generator**](https://github.com/MemeCrafters/meme-generator) 的副本，遵循上游 **MIT License**（`Copyright (c) 2021 MeetWq`，见 [LICENSE](./LICENSE)）。
> 表情渲染核心、表情素材、CLI 与 HTTP 接口均来自上游；**本仓库维护者在此基础上新增了网页版界面（WebUI）与 QQ 头像取图能力**，详见下方「本仓库相对上游的改动」。
> 表情素材均来自网络，版权归原作者所有，如有侵权请联系删除。二次分发请保留 `LICENSE` 与本段说明。

---

## 功能一览

| 能力 | 说明 |
| --- | --- |
| 表情模板 | 内置 900+ 模板，网页版实际可用 **923** 个（缺资源的 7 个已自动隐藏） |
| 网页版（本仓库新增） | 深色界面、模板搜索、示例图预览、参数表单、一键生成与下载、模板总览图 |
| QQ 头像（本仓库新增） | 输入 QQ 号即可把头像当作图片素材，无需先存到本地再上传 |
| 图片输入 | 点击上传 / 拖拽 / `Ctrl+V` 粘贴 / QQ 号取头像 |
| 输出格式 | PNG / JPEG / GIF（动图模板） |
| 其他接入 | 命令行 `meme`、FastAPI 接口（可被 Bot 或脚本调用） |

---

## 快速开始

### 1. 环境要求

- Python **3.9+**
- Windows 若出现「无报错直接退出」，请安装 [Visual C++ 运行时](https://aka.ms/vs/17/release/VC_redist.x64.exe)

### 2. 安装依赖

```bash
# 方式一：poetry（仓库自带 poetry.lock）
poetry install

# 方式二：pip（可先建虚拟环境）
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / macOS
pip install -e .
```

### 3. 启动网页版

```bash
python webui.py
```

启动后会自动打开浏览器（默认 <http://127.0.0.1:2233>）。

常用参数：

```bash
python webui.py --port 8080          # 换端口
python webui.py --host 0.0.0.0       # 允许局域网/外网访问
python webui.py --no-browser         # 不自动打开浏览器

python -m meme_generator.webui       # 等价写法
meme-webui                           # poetry / pip 安装后的命令行入口
```

### 4. 网页版怎么用

1. 左栏搜索或直接点选表情模板（如 `petpet`、`always_like`）；
2. 中间是模板示例图，右侧「开始制作」是参数表单；
3. **图片**：点方块上传、拖进来、`Ctrl+V` 粘贴，或直接在输入框填 **QQ 号** 点「取头像」；
4. **文字**、**高级参数**（个别模板才需要，JSON 格式）按提示填写；
5. 点「生成表情」→ 出现结果图 → 点「下载」保存；
6. 「模板总览图」会把当前筛选结果拼成一张索引图，方便挑模板。

---

## QQ 号取头像（本仓库新增）

- 入口：网页版「图片」区里的 `QQ 号 …` + `取头像` 按钮，**所有需要图片的模板**都有；
- 多个号一起填：`10001, 10002`（逗号 / 空格 / 顿号分隔），按图片位顺序依次填入；
- 头像来源依次回退：`q1.qlogo.cn` → `qlogo2.store.qq.com`；
- 由**服务端**代取（`GET /api/qq-avatar?qq=`）后再交给前端当普通图片上传，因此不受浏览器跨域限制；
- 该号没设置头像时会拿到官方默认图，界面会提示；
- 服务器需要能访问外网；离线环境请直接上传图片。

---

## 本仓库相对上游的改动

| 类型 | 内容 |
| --- | --- |
| 新增 | `webui.py`、`meme_generator/webui.py`、`meme_generator/web/`（网页版界面与启动逻辑） |
| 新增 | `GET /api/memes`、`GET /api/memes/keys`（网页版聚合接口，过滤缺资源的表情） |
| 新增 | `GET /api/qq-avatar?qq=`（服务端取 QQ 头像） |
| 调整 | 静态资源统一返回 `cache-control: no-cache`，避免换版后浏览器继续显示旧页面 |
| 保持不变 | 表情渲染核心、素材、CLI 与上游接口（`/memes/*`、`/meme/version`）完全兼容 |

> 若页面仍是旧版，按一次 `Ctrl+Shift+R` 强制刷新即可。

---

## 目录结构

```
webui.py                     网页版启动入口（--host / --port / --no-browser）
meme_generator/
  app.py                     FastAPI 路由（生成、模板信息、示例图、总览图）
  webui.py                   网页版路由（/api/*）+ 静态托管 + 自动开浏览器
  web/                       前端：index.html / app.js / style.css
  memes/                     各表情实现与素材
  manager.py / meme.py       表情加载、参数模型、渲染调度
  download.py                缺失素材下载（CLI 启动时自动检查）
resources/                   字体等共享资源
docker/  Dockerfile          容器化相关
tools/                       辅助脚本
```

---

## 配置

配置文件路径（首次启动自动生成空文件）：

- Windows：`%APPDATA%\meme_generator\config.toml`
- Linux / macOS：`~/.config/meme_generator/config.toml`

| 配置项 | 默认值 | 说明 |
| --- | --- | --- |
| `server.host` | `127.0.0.1` | 监听地址，填 `0.0.0.0` 才允许外部访问 |
| `server.port` | `2233` | 监听端口 |
| `meme.load_builtin_memes` | `true` | 是否加载内置表情 |
| `meme.meme_dirs` | `[]` | 额外表情目录 |
| `meme.meme_disabled_list` | `[]` | 禁用的表情 key |
| `gif.gif_max_size` | `10` | GIF 体积上限（MB） |
| `gif.gif_max_frames` | `100` | GIF 帧数上限 |
| `translate.baidu_trans_appid` / `baidu_trans_apikey` | 空 | 仅个别表情需要（如「店中点」） |
| `log.log_level` | `INFO` | 日志级别 |
| `resource.resource_url` / `resource_urls` | 官方源 | 缺失素材的下载源 |

---

## HTTP 接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/meme/version` | 版本号 |
| GET | `/memes/keys` | 全部表情 key（未过滤） |
| GET | `/memes/{key}/info` | 模板参数：图片/文字数量、默认文字、高级参数 schema |
| GET | `/memes/{key}/preview` | 模板示例图 |
| POST | `/memes/{key}/` | 生成表情（multipart：`images` + `texts` + `args`） |
| POST | `/memes/render_list` | 模板总览图（JSON：`meme_list` / `text_template` / `add_category_icon`） |
| GET | `/api/memes` | 网页版聚合列表（已过滤不可用表情） |
| GET | `/api/memes/keys` | 网页版 key 列表（已过滤不可用表情） |
| GET | `/api/qq-avatar?qq=10001` | 取 QQ 头像，返回图片流 |

示例：

```bash
curl -X POST http://127.0.0.1:2233/memes/petpet/ -F "images=@cat.png" -o petpet.gif
```

---

## 命令行

```bash
meme --help          # 安装后可用，首次运行会检查并下载缺失素材
python -m meme_generator.cli --help
```

上游详细用法见 [Wiki](https://github.com/MemeCrafters/meme-generator/wiki)。

---

## 常见问题

| 现象 | 处理 |
| --- | --- |
| 页面还是旧版界面 | `Ctrl+Shift+R` 强刷；前端已加 `no-cache` |
| 浏览器打不开 | 服务是否启动；外部访问需 `--host 0.0.0.0` 并放行端口 / 安全组 |
| 页面提示「无法连接接口」 | 服务未启动或端口不一致，确认终端里的访问地址 |
| 上传图片报错 | 缺少 `python-multipart`，重新 `pip install -e .` |
| Windows 下无报错退出 | 安装 [VC++ 运行时](https://aka.ms/vs/17/release/VC_redist.x64.exe)（[skia-python#289](https://github.com/kyamagu/skia-python/issues/289)） |
| Linux 下字体异常 | `export LANG=en_US.UTF-8`（[rust-skia#963](https://github.com/rust-skia/rust-skia/issues/963)） |
| 某些表情点不开 / 生成失败 | 多为缺素材或依赖外部服务，网页版已隐藏 7 个此类表情；可检查 `meme.meme_disabled_list` |
| QQ 头像一直失败 | 服务器需能访问 `q1.qlogo.cn`；内网可改为直接上传图片 |

---

## 声明

- 本仓库表情素材均来自网络，如有侵权请联系作者删除。
- 本项目仅供学习与自用，请勿用于商业用途或生成违法违规内容。
- QQ 头像由腾讯公开接口提供，本仓库不存储任何用户头像。

## 鸣谢

- 上游项目：[MemeCrafters/meme-generator](https://github.com/MemeCrafters/meme-generator)（作者 MeetWq），本项目的新增功能均建立在其之上。
- 表情素材整合自 [nonebot-plugin-petpet](https://github.com/noneplugin/nonebot-plugin-petpet) 与 [nonebot-plugin-memes](https://github.com/noneplugin/nonebot-plugin-memes)。
- 部分素材或代码参考了以下项目，感谢这些开发者：

  - [Ailitonia/omega-miya](https://github.com/Ailitonia/omega-miya) — 基于 nonebot2 的 QQ 机器人
  - [FloatTech/ZeroBot-Plugin](https://github.com/FloatTech/ZeroBot-Plugin) — 基于 ZeroBot 的 OneBot 插件
  - [HibiKier/zhenxun_bot](https://github.com/HibiKier/zhenxun_bot) — 基于 Nonebot2 与 go-cqhttp 的绪山真寻 bot
  - [SAGIRI-kawaii/sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot) — 基于 Graia Ariadne 与 Mirai 的机器人
  - [Dituon/petpet](https://github.com/Dituon/petpet) — Mirai 插件，生成各种奇怪图片
  - [kexue-z/nonebot-plugin-nokia](https://github.com/kexue-z/nonebot-plugin-nokia) — 诺基亚手机图生成
  - [RafuiiChan/nonebot_plugin_charpic](https://github.com/RafuiiChan/nonebot_plugin_charpic) — 字符画生成插件
  - [nonebot/plugin-localstore](https://github.com/nonebot/plugin-localstore) — 配置/缓存目录规范（`dirs.py`）

其他表情仓库：[meme-generator-contrib](https://github.com/MemeCrafters/meme-generator-contrib)、[meme_emoji](https://github.com/anyliew/meme_emoji)、[tudou-meme](https://github.com/LRZ9712/tudou-meme)。
