"""
Animated Dino Overlay for turing-smart-screen-python.

Runs inside the same process and same update queue as main.py.
It does not open COM5 separately.
"""

from __future__ import annotations

import threading
import time
from pathlib import Path
from PIL import Image

from library import config
from library.display import display
import library.scheduler as scheduler
from library.log import logger

FPS = 3.0
STEP_PX = 6
TRACK_X_MIN = 96
TRACK_X_MAX = 352
TRACK_Y = 277
MAX_QUEUE_DEPTH = 6
ALLOWED_THEMES = {"CodexSystemDinoAnimated"}

_started = False
_thread = None

def _theme_name() -> str:
    try:
        return str(config.CONFIG_DATA.get("config", {}).get("THEME", ""))
    except Exception:
        return ""

def _theme_background() -> Path | None:
    try:
        theme_path = Path(str(config.THEME_DATA["PATH"]))
        bg = theme_path / "background.png"
        return bg if bg.exists() else None
    except Exception:
        return None

def _asset_dir() -> Path:
    return Path(__file__).resolve().parent / "res" / "codex_dino"

def _load_frames():
    assets = _asset_dir()
    result = {"right": [], "left": []}
    for direction in result:
        for i in range(4):
            p = assets / f"dino_{direction}_{i}.png"
            result[direction].append(Image.open(p).convert("RGBA"))
    return result

def _restore(background: Image.Image, x: int, y: int, w: int, h: int):
    patch = background.crop((x, y, x + w, y + h))
    display.lcd.DisplayPILImage(patch, x, y)

def _draw(background: Image.Image, sprite: Image.Image, x: int, y: int):
    w, h = sprite.size
    patch = background.crop((x, y, x + w, y + h)).convert("RGBA")
    patch.alpha_composite(sprite, (0, 0))
    display.lcd.DisplayPILImage(patch.convert("RGB"), x, y)

def _run():
    theme = _theme_name()

    if theme not in ALLOWED_THEMES:
        logger.info("Codex Dino: tema '%s' nao habilitado", theme)
        return

    if display.lcd.get_width() != 480 or display.lcd.get_height() != 320:
        logger.warning(
            "Codex Dino desabilitado: esperado 480x320, recebido %sx%s",
            display.lcd.get_width(),
            display.lcd.get_height()
        )
        return

    bg_path = _theme_background()
    if not bg_path:
        logger.warning("Codex Dino desabilitado: background.png nao encontrado")
        return

    try:
        background = Image.open(bg_path).convert("RGB")
        frames = _load_frames()
    except Exception as exc:
        logger.warning("Codex Dino desabilitado: erro ao carregar assets: %s", exc)
        return

    sprite_w, sprite_h = frames["right"][0].size
    x = TRACK_X_MIN
    prev_x = None
    direction = 1
    animation_index = 0
    interval = 1.0 / max(FPS, 0.5)

    logger.info("Codex Dino iniciado em %.1f FPS", FPS)

    while not scheduler.STOPPING:
        started = time.monotonic()

        try:
            if config.update_queue.qsize() > MAX_QUEUE_DEPTH:
                time.sleep(interval)
                continue
        except Exception:
            pass

        facing = "right" if direction > 0 else "left"
        sprite = frames[facing][animation_index % len(frames[facing])]

        try:
            if prev_x is not None:
                _restore(background, prev_x, TRACK_Y, sprite_w, sprite_h)
            _draw(background, sprite, x, TRACK_Y)
        except Exception as exc:
            logger.warning("Codex Dino frame error: %s", exc)
            time.sleep(1)
            continue

        prev_x = x
        animation_index += 1
        x += STEP_PX * direction

        if x >= TRACK_X_MAX:
            x = TRACK_X_MAX
            direction = -1
        elif x <= TRACK_X_MIN:
            x = TRACK_X_MIN
            direction = 1

        elapsed = time.monotonic() - started
        if elapsed < interval:
            time.sleep(interval - elapsed)

    if prev_x is not None:
        try:
            _restore(background, prev_x, TRACK_Y, sprite_w, sprite_h)
        except Exception:
            pass

    logger.info("Codex Dino parado")

def start_dino_overlay():
    global _started, _thread

    if _started:
        return _thread

    _started = True
    _thread = threading.Thread(
        target=_run,
        name="Codex_Dino_Overlay",
        daemon=True,
    )
    _thread.start()
    return _thread
