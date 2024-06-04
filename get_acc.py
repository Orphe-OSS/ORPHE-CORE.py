import asyncio
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート

# 注意）Core2の場合はserial_numberとpacket_numberは取得できません。


def got_acc(acc):
    """
    加速度センサの値を取得したときに呼び出されるコールバック関数。
    それぞれの値は加速度センサのレンジによって変換されません。
    例えば静止状態ではz方向の1Gの値はレンジ設定によって変わります。加速度レンジが2であれば 0.5 、16であれば 0.0625 （値は理論値なので誤差が生じます）です。
    """
    print(
        f"Acc[{acc.serial_number}][{acc.packet_number}][{acc.timestamp}]: {acc.x}, {acc.y}, {acc.z}")


def got_converted_acc(acc):
    """
    加速度センサの値を取得したときに呼び出されるコールバック関数
    それぞれの値は加速度レンジの値によって変換されます。
    例えば静止状態ではz方向の1Gの値は常に1.0です。
    """
    print(
        f"Acc[{acc.serial_number}][{acc.packet_number}][{acc.timestamp}]: {acc.x}, {acc.y}, {acc.z}")


async def main():
    orphe = Orphe()
    orphe.set_got_acc_callback(got_acc)
    # orphe.set_got_converted_acc_callback(got_converted_acc)

    if not await orphe.connect():
        return

    await orphe.set_led(1, 0)
    await orphe.set_acc_range(16)
    await orphe.print_device_information()
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
