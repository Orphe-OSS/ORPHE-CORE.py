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
    # このコールバックは空いてる時間中たくさん送られてくるので、最初はコメントアウトしておくことをおすすめします。
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
    except KeyboardInterrupt:
        print("Stopping due to KeyboardInterrupt...")
    finally:
        if orphe.is_connected():
            print("Stopping notification...")
            await orphe.stop_sensor_values_notification()
            print("Notification stopped. Disconnecting from the device.")
            await orphe.disconnect()
        print("Disconnected.")

if __name__ == "__main__":
    asyncio.run(main())
