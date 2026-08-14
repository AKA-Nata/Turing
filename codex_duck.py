"""
Codex Duck Overlay for turing-smart-screen-python.

Animates a small pixel-art duck in the free footer area of CodexSystemPCv3.
It uses the same LCD update queue as the system monitor, so it does not open
COM5 independently.

Default track:
  x: 95 .. 355
  y: 299
  sprite: 24 x 18 px
  FPS: 3

Adjust constants below if desired.
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
TRACK_X_MIN = 95
TRACK_X_MAX = 355
TRACK_Y = 299

# Prevent animation from flooding the serial update queue.
MAX_QUEUE_DEPTH = 6

# Only starts automatically for the theme we validated.
ALLOWED_THEMES = {"CodexSystemPCv3"}

_started = False
_thread = None


def _current_theme_name() -> str:
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
    return Path(__file__).resolve().parent / "res" / "codex_duck"


def _load_frames() -> dict[str, list[Image.Image]]:
    assets = _asset_dir()
    result = {"right": [], "left": []}
    for direction in result:
        for i in range(4):
            path = assets / f"duck_{direction}_{i}.png"
            result[direction].append(Image.open(path).convert("RGBA"))
    return result


def _restore_region(background: Image.Image, x: int, y: int, w: int, h: int) -> None:
    patch = background.crop((x, y, x + w, y + h))
    display.lcd.DisplayPILImage(patch, x, y)


def _draw_sprite(background: Image.Image, sprite: Image.Image, x: int, y: int) -> None:
    w, h = sprite.size
    patch = background.crop((x, y, x + w, y + h)).convert("RGBA")
    patch.alpha_composite(sprite, (0, 0))
    display.lcd.DisplayPILImage(patch.convert("RGB"), x, y)


def _run() -> None:
    theme = _current_theme_name()
    if theme not in ALLOWED_THEMES:
        logger.info(
            "Codex Duck: theme '%s' not enabled; expected one of %s",
            theme,
            sorted(ALLOWED_THEMES),
        )
        return

    if display.lcd.get_width() != 480 or display.lcd.get_height() != 320:
        logger.warning(
            "Codex Duck disabled: expected 480x320 landscape, got %sx%s",
            display.lcd.get_width(),
            display.lcd.get_height(),
        )
        return

    bg_path = _theme_background()
    if not bg_path:
        logger.warning("Codex Duck disabled: theme background.png not found")
        return

    try:
        background = Image.open(bg_path).convert("RGB")
        frames = _load_frames()
    except Exception as exc:
        logger.warning("Codex Duck disabled: cannot load assets: %s", exc)
        return

    sprite_w, sprite_h = frames["right"][0].size
    x = TRACK_X_MIN
    previous_x = None
    direction = 1
    animation_index = 0
    interval = 1.0 / max(FPS, 0.5)

    logger.info("Codex Duck started at %.1f FPS", FPS)

    while not scheduler.STOPPING:
        started = time.monotonic()

        # Let CPU/GPU/RAM updates take priority if the serial queue is busy.
        try:
            if config.update_queue.qsize() > MAX_QUEUE_DEPTH:
                time.sleep(interval)
                continue
        except Exception:
            pass

        facing = "right" if direction > 0 else "left"
        sprite = frames[facing][animation_index % len(frames[facing])]

        try:
            if previous_x is not None:
                _restore_region(background, previous_x, TRACK_Y, sprite_w, sprite_h)

            _draw_sprite(background, sprite, x, TRACK_Y)
        except Exception as exc:
            logger.warning("Codex Duck frame error: %s", exc)
            time.sleep(1)
            continue

        previous_x = x
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

    # Restore the last duck position before shutdown when possible.
    if previous_x is not None:
        try:
            _restore_region(background, previous_x, TRACK_Y, sprite_w, sprite_h)
        except Exception:
            pass

    logger.info("Codex Duck stopped")


def start_duck_overlay() -> threading.Thread | None:
    global _started, _thread

    if _started:
        return _thread

    _started = True
    _thread = threading.Thread(
        target=_run,
        name="Codex_Duck_Overlay",
        daemon=True,
    )
    _thread.start()
    return _thread
