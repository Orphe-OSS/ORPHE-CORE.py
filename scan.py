import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート


async def main():
    orphe = Orphe()
    devices = await orphe.scan_all_devices()
    for device in devices:
        print(
            f"Device: {device.name}(name), {device.address}(address), {device.rssi}(rssi)")

if __name__ == "__main__":
    asyncio.run(main())
