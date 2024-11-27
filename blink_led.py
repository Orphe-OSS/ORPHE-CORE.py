import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート


async def main():
    orphe = Orphe()

    # 接続するデバイスを指定する場合はコアモジュールのaddressをconnect()の引数に文字列として渡してください。addressを知りたい場合はコアモジュールに接続するとコンソールに表示されます。文字列が空の場合はSERVICE UUIDがORPHEと合致する最初に見つかったデバイスに接続します。
    if not await orphe.connect():
        return

    await orphe.print_device_information()
    await orphe.set_led_brightness(255)
    print(orphe.client.mtu_size)
    try:
        while True:
            await orphe.set_led(1, 0)
            await asyncio.sleep(1)
            await orphe.set_led(0, 0)
            await asyncio.sleep(1)
    finally:
        print("Disconnecting from the device.")
        await orphe.disconnect()

# 色々記述していますが，Ctrl+Cでプログラムを終了した場合にきれいに終了処理するためのものです．最悪 asyncio.run(main()) だけでも動きます．
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    main_task = loop.create_task(main())

    try:
        loop.run_until_complete(main_task)
    except KeyboardInterrupt:
        print("KeyboardInterrupt(Ctrl+C) received. Canceling the main task...")
        main_task.cancel()
        try:
            loop.run_until_complete(main_task)
        except asyncio.CancelledError:
            pass
    finally:
        loop.close()
        print("Event loop closed.")
