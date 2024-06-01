import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート


def got_acc(acc):
    # sensor_valuesデータを処理する
    print(
        f"Acc[{acc.serial_number}][{acc.packet_number}][{acc.timestamp}]: {acc.x}, {acc.y}, {acc.z}")


async def main():
    orphe = Orphe()
    orphe.set_got_acc_callback(got_acc)

    if not await orphe.connect():
        return

    await orphe.start_sensor_values_notification()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping notification...")
        await orphe.stop_notification()
        print("Notification stopped. Disconnecting from the device.")
        await orphe.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
