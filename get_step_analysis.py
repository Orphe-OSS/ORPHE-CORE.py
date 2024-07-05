import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート

# 注意）Core2の場合はserial_numberとpacket_numberは取得できません。


def got_gait(gait):
    gait.print()


def got_stride(stride):
    stride.print()


def got_pronation(pronation):
    pronation.print()


def got_quat_distance(quat_distance):
    quat_distance.print()


async def main():
    orphe = Orphe()
    orphe.set_got_gait_callback(got_gait)
    orphe.set_got_stride_callback(got_stride)
    orphe.set_got_pronation_callback(got_pronation)
    # 以下のコールバックは空いてる時間中たくさん送られてくるので、このサンプルでは見易さの為コメントアウトしています
    # orphe.set_got_quat_distance_callback(got_quat_distance)

    # 接続するデバイスを指定する場合はコアモジュールのaddressをconnect()の引数に文字列として渡してください。addressを知りたい場合はコアモジュールに接続するとコンソールに表示されます。文字列が空の場合はSERVICE UUIDがORPHEと合致する最初に見つかったデバイスに接続します。
    if not await orphe.connect():
        return

    await orphe.print_device_information()
    await orphe.start_step_analysis_notification()

    try:
        while True:
            await asyncio.sleep(1)
            if not orphe.is_connected():
                break
    finally:
        if orphe.is_connected():
            print("Stopping notification...")
            await orphe.stop_step_analysis_notification()
            print("Notification stopped. Disconnecting from the device.")
            await orphe.disconnect()
        print("Disconnected.")


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
