from .common import bus, BUS_NAME
from .razerdevice import RazerDevice


class DeviceManager:
    def __init__(self):
        self.manager = bus.get(BUS_NAME)

        self._devices = []
        devices_paths = self.manager.Devices
        for device_path in devices_paths:
            device = RazerDevice(device_path)
            self._devices.append(device)

    @property
    def version(self):
        return self.manager.Version

    @property
    def daemon_version(self):
        return self.manager.Version

    @property
    def devices(self):
        return self._devices

    @property
    def sync_effects(self):
        # TODO Stub
        return True

    @sync_effects.setter
    def sync_effects(self, sync):
        # TODO Stub
        pass
