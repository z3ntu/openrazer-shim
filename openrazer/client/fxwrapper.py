from .common import *


class _FxWrapper:
    def __init__(self, device, leds: dict):
        self._device = device
        self._leds = leds
        self._misc_wrapper = _MiscFxWrapper(device, leds)

    @property
    def advanced(self):
        raise RuntimeError("not implemented yet")

    @property
    def misc(self):
        return self._misc_wrapper

    def has(self, capability: str) -> bool:
        return self._device.has("lighting_" + capability)

    def blinking(self, red: int, green: int, blue: int) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].blinking(red, green, blue)

    def breath_single(self, red: int, green: int, blue: int) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].breath_single(red, green, blue)

    def breath_dual(self, red: int, green: int, blue: int, red2: int, green2: int, blue2: int) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].breath_dual(red, green, blue, red2, green2, blue2)

    def breath_random(self) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].breath_random()

    def none(self) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].none()

    def pulsate(self, red: int, green: int, blue: int) -> bool:
        # Same as breath_single
        return self.pulsate(red, green, blue)

    def reactive(self, red: int, green: int, blue: int, time: int) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].reactive(red, green, blue, time)

    def spectrum(self):
        return self._leds[self._device.DEVICE_MAIN_LED].spectrum()

    def static(self, red: int, green: int, blue: int) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].static(red, green, blue)

    def wave(self, direction: int) -> bool:
        return self._leds[self._device.DEVICE_MAIN_LED].wave(direction)


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
