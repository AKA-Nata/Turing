"""
Animated Cow Overlay for turing-smart-screen-python.

Behavior cycle:
1) Walk from left to right
2) Stop and eat grass
3) Walk from right to left
4) Stop and sleep
5) Repeat

Runs inside the same process and the same display update queue.
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
TRACK_Y = 266
MAX_QUEUE_DEPTH = 6

GRAZE_SECONDS = 8
SLEEP_SECONDS = 30

ALLOWED_THEMES = {"CodexSystemCowAnimated"}

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
    return Path(__file__).resolve().parent / "res" / "codex_cow"

def _load_frames():
    assets = _asset_dir()
    result = {
        "walk_right": [],
        "walk_left": [],
        "eat_right": [],
        "eat_left": [],
        "sleep": [],
    }
    for i in range(4):
        result["walk_right"].append(Image.open(assets / f"cow_walk_right_{i}.png").convert("RGBA"))
        result["walk_left"].append(Image.open(assets / f"cow_walk_left_{i}.png").convert("RGBA"))
        result["eat_right"].append(Image.open(assets / f"cow_eat_right_{i}.png").convert("RGBA"))
        result["eat_left"].append(Image.open(assets / f"cow_eat_left_{i}.png").convert("RGBA"))
        result["sleep"].append(Image.open(assets / f"cow_sleep_any_{i}.png").convert("RGBA"))
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
        logger.info("Codex Cow: theme '%s' not enabled", theme)
        return

    if display.lcd.get_width() != 480 or display.lcd.get_height() != 320:
        logger.warning(
            "Codex Cow disabled: expected 480x320, got %sx%s",
            display.lcd.get_width(), display.lcd.get_height()
        )
        return

    bg_path = _theme_background()
    if not bg_path:
        logger.warning("Codex Cow disabled: background.png not found")
        return

    try:
        background = Image.open(bg_path).convert("RGB")
        frames = _load_frames()
    except Exception as exc:
        logger.warning("Codex Cow disabled: error loading assets: %s", exc)
        return

    sprite_w, sprite_h = frames["walk_right"][0].size
    x = TRACK_X_MIN
    prev_x = None
    phase = "walk_right"
    phase_started = time.monotonic()
    anim_index = 0
    interval = 1.0 / max(FPS, 0.5)

    logger.info("Codex Cow started at %.1f FPS", FPS)

    while not scheduler.STOPPING:
        started = time.monotonic()

        try:
            if config.update_queue.qsize() > MAX_QUEUE_DEPTH:
                time.sleep(interval)
                continue
        except Exception:
            pass

        now = time.monotonic()

        # State machine
        if phase == "walk_right":
            sprite = frames["walk_right"][anim_index % 4]
            if x >= TRACK_X_MAX:
                x = TRACK_X_MAX
                phase = "eat_right"
                phase_started = now
                anim_index = 0
                sprite = frames["eat_right"][0]
            else:
                x += STEP_PX
        elif phase == "eat_right":
            sprite = frames["eat_right"][anim_index % 4]
            if now - phase_started >= GRAZE_SECONDS:
                phase = "walk_left"
                phase_started = now
                anim_index = 0
        elif phase == "walk_left":
            sprite = frames["walk_left"][anim_index % 4]
            if x <= TRACK_X_MIN:
                x = TRACK_X_MIN
                phase = "sleep"
                phase_started = now
                anim_index = 0
                sprite = frames["sleep"][0]
            else:
                x -= STEP_PX
        else:  # sleep
            sprite = frames["sleep"][anim_index % 4]
            if now - phase_started >= SLEEP_SECONDS:
                phase = "walk_right"
                phase_started = now
                anim_index = 0

        try:
            if prev_x is not None:
                _restore(background, prev_x, TRACK_Y, sprite_w, sprite_h)
            _draw(background, sprite, x, TRACK_Y)
        except Exception as exc:
            logger.warning("Codex Cow frame error: %s", exc)
            time.sleep(1)
            continue

        prev_x = x
        anim_index += 1

        elapsed = time.monotonic() - started
        if elapsed < interval:
            time.sleep(interval - elapsed)

    if prev_x is not None:
        try:
            _restore(background, prev_x, TRACK_Y, sprite_w, sprite_h)
        except Exception:
            pass

    logger.info("Codex Cow stopped")

def start_cow_overlay():
    global _started, _thread
    if _started:
        return _thread

    _started = True
    _thread = threading.Thread(target=_run, name="Codex_Cow_Overlay", daemon=True)
    _thread.start()
    return _thread
