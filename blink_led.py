import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート


async def main():
    orphe = Orphe()

    # 接続するデバイスを指定する場合はコアモジュールのaddressをconnect()の引数に文字列として渡してください。addressを知りたい場合はコアモジュールに接続するとコンソールに表示されます。文字列が空の場合はSERVICE UUIDがORPHEと合致する最初に見つかったデバイスに接続します。
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
