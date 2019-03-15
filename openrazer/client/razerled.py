from .common import *


class _RazerLed:
    def __init__(self, led_path):
        self.led = bus.get(BUS_NAME, led_path)

    @property
    def brightness(self) -> float:
        return self.led.getBrightness() / 255 * 100

    @brightness.setter
    def brightness(self, brightness: float):
        self.led.setBrightness(brightness / 100 * 255)

    @property
    def led_id(self) -> int:
        return self.led.LedId[0]

    def blinking(self, red: int, green: int, blue: int) -> bool:
        return self.led.setBlinking((red, green, blue))

    def breath_single(self, red: int, green: int, blue: int) -> bool:
        return self.led.setBreathing((red, green, blue))

    def breath_dual(self, red: int, green: int, blue: int, red2: int, green2: int, blue2: int) -> bool:
        return self.led.setBreathingDual((red, green, blue), (red2, green2, blue2))

    def breath_random(self) -> bool:
        return self.led.setBreathingRandom()

    def none(self) -> bool:
        return self.led.setOff()

    def pulsate(self, red: int, green: int, blue: int) -> bool:
        # Same as breath_single
        return self.breath_single(red, green, blue)

    def spectrum(self):
        return self.led.setSpectrum()

    def static(self, red: int, green: int, blue: int) -> bool:
        return self.led.setStatic((red, green, blue))

    def wave(self, direction: int) -> bool:
        return self.led.setWave((direction,))


class _DummyLed:
    @property
    def brightness(self) -> float:
        print("WARNING: DummyLed returning 0.00")
        return 0.00

    @brightness.setter
    def brightness(self, brightness: float):
        print("WARNING: DummyLed not doing anything")
        pass


class _FxWrapper(_RazerLed):
    def __init__(self, leds: dict):
        self._misc_wrapper = _MiscFxWrapper(leds)

    @property
    def advanced(self):
        raise RuntimeError("not implemented yet")

    @property
    def misc(self):
        return self._misc_wrapper


class _MiscFxWrapper:
    def __init__(self, leds: dict):
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
