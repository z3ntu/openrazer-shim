from .common import *


class _FxWrapper:
    def __init__(self, device, leds: dict):
        self._device = device
        self._misc_wrapper = _MiscFxWrapper(device, leds)

    @property
    def advanced(self):
        raise RuntimeError("not implemented yet")

    @property
    def misc(self):
        return self._misc_wrapper

    def has(self, capability: str) -> bool:
        return self._device.has("lighting_" + capability)


class _MiscFxWrapper:
    def __init__(self, device, leds: dict):
        self._device = device
        self._leds = leds

    @property
    def logo(self):
        return self._leds[RLED_ID_LOGO]

    @property
    def scroll_wheel(self):
        return self._leds[RLED_ID_SCROLL]

    @property
    def backlight(self):
        return self._leds[RLED_ID_BACKLIGHT]

    def has(self, capability: str) -> bool:
        return self._device.has("lighting_" + capability)
