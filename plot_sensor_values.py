import asyncio
import matplotlib.pyplot as plt
from collections import deque
from orphe_core import Orphe
import matplotlib.animation as animation

plot_buffer_size = 512  # バッファサイズ
update_interval = 0.02  # 描画更新間隔（秒）

# データ配列（固定長デック）
acc_x = deque(maxlen=plot_buffer_size)
acc_y = deque(maxlen=plot_buffer_size)
acc_z = deque(maxlen=plot_buffer_size)

# プロットの初期設定
fig, ax = plt.subplots()
line_x, = ax.plot([], [], label='Acc X')
line_y, = ax.plot([], [], label='Acc Y')
line_z, = ax.plot([], [], label='Acc Z')
ax.legend()
ax.set_xlim(0, plot_buffer_size)
ax.set_ylim(-3, 3)  # 適宜調整

# アニメーション更新関数
def update(frame):
    # すでに更新されている acc データをプロット
    line_x.set_data(range(len(acc_x)), acc_x)
    line_y.set_data(range(len(acc_y)), acc_y)
    line_z.set_data(range(len(acc_z)), acc_z)
    return line_x, line_y, line_z

async def main():

    def got_converted_acc(acc):
        print(f"Acc: {acc.x:.2f}, {acc.y:.2f}, {acc.z:.2f}")
        acc_x.append(acc.x)
        acc_y.append(acc.y)
        acc_z.append(acc.z)

    def on_disconnect():
        print("Disconnected from the ORPHE CORE device.")

    def lost_data(serial_number_prev, serial_number):
        print(f"Data loss detected. {serial_number_prev} <-> {serial_number}")

    orphe = Orphe()
    orphe.set_got_converted_acc_callback(got_converted_acc)
    orphe.set_lost_data_callback(lost_data)

    if not await orphe.connect():
        return

    await orphe.set_led(1, 0)
    await orphe.set_acc_range(16)
    await orphe.start_sensor_values_notification()

    # アニメーション設定（frames指定を省略して無限更新）
    ani = animation.FuncAnimation(fig, update, interval=20, blit=True)
    
    # ブロッキングせず（他のコールバック関数処理を止めないため）にウィンドウを表示
    plt.show(block=False)

    # BLE接続中は定期的にGUIイベント処理を行う
    try:
        while orphe.is_connected():
            plt.pause(update_interval)  # GUI更新
            await asyncio.sleep(update_interval)
    finally:
        if orphe.is_connected():
            print("Stopping notification...")
            await orphe.stop_sensor_values_notification()
            print("Notification stopped. Disconnecting from the device.")
            await orphe.disconnect()
        print("Disconnected.")

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
