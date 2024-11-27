import asyncio
import matplotlib.pyplot as plt
from collections import deque
import time
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート
# 注意）Core2の場合はserial_numberとpacket_numberは取得できません。

plot_buffer_size = 512  # バッファサイズを指定
update_interval = 0.03  # 描画更新間隔（秒）

async def main():
    # データ配列を初期化（固定長のデックを使用）
    acc_x = deque(maxlen=plot_buffer_size)
    acc_y = deque(maxlen=plot_buffer_size)
    acc_z = deque(maxlen=plot_buffer_size)

    # プロットを初期化
    plt.ion()
    fig, ax = plt.subplots()
    line_x, = ax.plot([], [], label='Acc X')
    line_y, = ax.plot([], [], label='Acc Y')
    line_z, = ax.plot([], [], label='Acc Z')
    ax.legend()

    # 前回の描画時間を記録
    last_update_time = time.time()

    def got_converted_acc(acc):
        nonlocal last_update_time

        # 加速度センサの値を取得し、配列に追加
        acc_x.append(acc.x)
        acc_y.append(acc.y)
        acc_z.append(acc.z)

        current_time = time.time()
        # 一定時間経過したら描画を更新
        if current_time - last_update_time >= update_interval:
            last_update_time = current_time

            # プロットデータを更新
            line_x.set_data(range(len(acc_x)), acc_x)
            line_y.set_data(range(len(acc_y)), acc_y)
            line_z.set_data(range(len(acc_z)), acc_z)

            # プロットの範囲を自動調整
            ax.relim()
            ax.autoscale_view()

            # プロットのラベル位置を左上に固定
            ax.legend(loc='upper left')

            # プロットの範囲を上下 3,-3 に設定
            # ax.set_ylim(-3, 3)


            # グラフを再描画
            plt.draw()
            plt.pause(0.001)

    def on_disconnect():
        print("Disconnected from the ORPHE CORE device.")

    def lost_data(serial_number_prev, serial_number):
        print(
            f"Data loss detected. {serial_number_prev} <-> {serial_number}")

    orphe = Orphe()

    # コールバックを設定
    orphe.set_got_converted_acc_callback(got_converted_acc)
    orphe.set_lost_data_callback(lost_data)

    # デバイスに接続
    if not await orphe.connect():
        return

    await orphe.set_led(1, 0)
    await orphe.set_acc_range(16)
    await orphe.start_sensor_values_notification()

    try:
        while True:
            await asyncio.sleep(1)
            if not orphe.is_connected():
                break

    finally:
        if orphe.is_connected():
            print("Stopping notification...")
            await orphe.stop_sensor_values_notification()
            print("Notification stopped. Disconnecting from the device.")
            await orphe.disconnect()
        print("Disconnected.")

# プログラムのエントリポイント
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
