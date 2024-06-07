import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート

# 注意）Core2の場合はserial_numberとpacket_numberは取得できません。


def got_acc(acc):
    acc.print()


def got_converted_acc(acc):
    acc.print()


def got_gyro(gyro):
    gyro.print()


def got_converted_gyro(gyro):
    gyro.print()


def got_quat(quat):
    quat.print()


async def main():
    orphe = Orphe()

    # 確認したいコールバックをセットする。コールバック関数定義は上記を参照。
    # orphe.set_got_acc_callback(got_acc)
    # orphe.set_got_gyro_callback(got_gyro)
    orphe.set_got_converted_acc_callback(got_converted_acc)
    # orphe.set_got_converted_gyro_callback(got_converted_gyro)
    # orphe.set_got_quat_callback(got_quat)

    # 接続するデバイスを指定する場合はコアモジュールのaddressをconnect()の引数に文字列として渡してください。addressを知りたい場合はコアモジュールに接続するとコンソールに表示されます。文字列が空の場合はSERVICE UUIDがORPHEと合致する最初に見つかったデバイスに接続します。
    if not await orphe.connect():
        return

    await orphe.set_led(1, 0)
    await orphe.set_acc_range(16)
    # await orphe.print_device_information()
    # await orphe.start_sensor_values_notification()

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
