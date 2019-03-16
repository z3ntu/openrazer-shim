from pydbus import SystemBus

BUS_NAME = "io.github.openrazer1"
bus = SystemBus()

RLED_ID_SCROLL = 0x01
RLED_ID_LOGO = 0x04
RLED_ID_BACKLIGHT = 0x05
