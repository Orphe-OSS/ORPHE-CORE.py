import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート


async def main():
    orphe = Orphe()

    if not await orphe.connect():
        return

    await orphe.print_device_information()

    try:
        while True:
            await orphe.set_led(1, 0)
            await asyncio.sleep(1)
            await orphe.set_led(0, 0)
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("Stopping notification...")
        await orphe.stop_notification()
        print("Notification stopped. Disconnecting from the device.")
        await orphe.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
