from .common import *
from .fxwrapper import _FxWrapper
from .razerled import _RazerLed, _DummyLed

capability_to_features_map = {
    "dpi": "dpi",
    "poll_rate": "poll_rate"
}

# Missing:
# active, breathing_triple, game_mode_led, led_matrix, macro_logic, ripple, starlight_dual, starlight_random,
# starlight_single, starlight_triple
capability_to_fx_map = {
    "none": "off",
    "blinking": "blinking",
    "breath_dual": "breathing_dual",
    "breath_random": "breathing_random",
    "breath_single": "breathing",
    "brightness": "brightness",
    "led_matrix": "custom_frame",
    "pulsate": "breathing",
    "reactive": "reactive",
    "spectrum": "spectrum",
    "static": "static",
    "wave": "wave"
}

# Intentionally missing / unimplemented capabilities
missing_capabilities = [
    "active", "breath_triple", "game_mode_led", "macro_logic", "ripple",
    "starlight_dual", "starlight_random", "starlight_single", "starlight_triple"
]


class RazerDevice:
    def __init__(self, device_path):
        self._device = bus.get(BUS_NAME, device_path)
        # TODO Maybe sometimes is logo led
        self.DEVICE_MAIN_LED = RLED_ID_BACKLIGHT

        self._leds = {}
        # Initialize real LEDs
        for led_path in self._device.Leds:
            led = _RazerLed(self, led_path)
            self._leds[led._led_id] = led

        # Initialize all other LEDs with _DummyLed
        for LED_ID in [RLED_ID_SCROLL, RLED_ID_LOGO, RLED_ID_BACKLIGHT]:
            if LED_ID not in self._leds:
                self._leds[LED_ID] = _DummyLed()

        self._fx_wrapper = _FxWrapper(self, self._leds)

        # Values used by applications
        self.macro = None
        # FIXME VID/PID stub
        self._vid = 0x0001
        self._pid = 0x0001

    @property
    def brightness(self) -> float:
        return self._leds[self.DEVICE_MAIN_LED].brightness

    @brightness.setter
    def brightness(self, brightness: float):
        self._leds[self.DEVICE_MAIN_LED].brightness = brightness

    @property
    def dpi(self) -> tuple:
        return self._device.getDPI()

    @dpi.setter
    def dpi(self, value: tuple):
        return self._device.setDPI(value)

    @property
    def firmware_version(self) -> str:
        return self._device.getFirmwareVersion()

    @property
    def fx(self):
        return self._fx_wrapper

    @property
    def max_dpi(self) -> int:
        return self._device.getMaxDPI()

    @property
    def name(self) -> str:
        return self._device.Name

    @property
    def poll_rate(self) -> int:
        return self._device.getPollRate()

    @poll_rate.setter
    def poll_rate(self, poll_rate: int):
        return self._device.setPollRate(poll_rate)

    @property
    def razer_urls(self) -> dict:
        # TODO Stub
        return {"top_img": "https://assets.razerzone.com/eeimages/products/17531/deathadder_chroma_gallery_2.png", }

    @property
    def serial(self) -> str:
        return self._device.getSerial()

    @property
    def type(self) -> str:
        return self._device.Type

    def has(self, capability: str) -> bool:
        val = self._has_internal(capability)
        # print("has(" + capability + ") resulted in " + str(val))
        return val

    def _has_internal(self, capability: str) -> bool:
        # Check against Features
        if capability in capability_to_features_map:
            return capability_to_features_map[capability] in self._device.SupportedFeatures

        if capability == "lighting":
            return self._is_real_led(self.DEVICE_MAIN_LED)
        if capability == "lighting_scroll":
            return self._is_real_led(RLED_ID_SCROLL)
        if capability == "lighting_logo":
            return self._is_real_led(RLED_ID_LOGO)
        if capability == "lighting_backlight":
            return self.DEVICE_MAIN_LED != RLED_ID_BACKLIGHT and self._is_real_led(RLED_ID_BACKLIGHT)

        # "brightness" is not prefixed with "lighting_"
        if capability == "brightness":
            if not self._is_real_led(self.DEVICE_MAIN_LED):
                return False

        # Remove FX prefixes
        if capability.startswith("lighting_scroll_"):
            if not self._is_real_led(RLED_ID_SCROLL):
                return False
            capability = capability.replace("lighting_scroll_", "")
        elif capability.startswith("lighting_logo"):
            if not self._is_real_led(RLED_ID_LOGO):
                return False
            capability = capability.replace("lighting_logo_", "")
        elif capability.startswith("lighting_backlight_"):
            if self.DEVICE_MAIN_LED == RLED_ID_BACKLIGHT or not self._is_real_led(RLED_ID_BACKLIGHT):
                return False
            capability = capability.replace("lighting_backlight_", "")
        elif capability.startswith("lighting_"):
            if not self._is_real_led(self.DEVICE_MAIN_LED):
                return False
            # No zero-argument pulsate in razer_test
            if capability == "lighting_pulsate":
                return False
            capability = capability.replace("lighting_", "")

        # Check against FX
        if capability in capability_to_fx_map:
            return capability_to_fx_map[capability] in self._device.SupportedFx

        if capability in missing_capabilities:
            return False

        print("WARNING: Unhandled capability: " + capability)
        return False

    def _is_real_led(self, led_id):
        return isinstance(self._leds[led_id], _RazerLed)
