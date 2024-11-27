import asyncio
import threading
from tkinter import *
from tkinter import ttk
from orphe_core import Orphe  # orphe_core.pyからOrpheクラスをインポート

# コールバック関数の定義


def got_acc(acc):
    acc.print()


def got_converted_acc(acc):
    # acc.print()
    pass


def got_gyro(gyro):
    gyro.print()


def got_converted_gyro(gyro):
    gyro.print()


def got_quat(quat):
    quat.print()


def lost_data(serial_number_prev, serial_number):
    print(f"Data loss detected. {serial_number_prev} <-> {serial_number}")

# OrpheAppクラスの定義


class OrpheApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Orphe Connection")

        # ウィンドウにフォーカスを当てる
        self.master.focus_force()

        # ウィンドウサイズを設定して画面中央に配置
        # self.master.geometry('400x400')
        self.center_window(300, 400)

        # Orpheインスタンスを2つ作成
        self.orphe1 = Orphe()
        self.orphe2 = Orphe()

        # コールバックの設定
        self.orphe1.set_got_converted_acc_callback(got_converted_acc)
        self.orphe1.set_lost_data_callback(lost_data)
        self.orphe1.set_on_disconnect_callback(self.on_disconnect1)

        self.orphe2.set_got_converted_acc_callback(got_converted_acc)
        self.orphe2.set_lost_data_callback(lost_data)
        self.orphe2.set_on_disconnect_callback(self.on_disconnect2)

        # デバイス1のフレーム作成
        frame1 = LabelFrame(self.master, text="Core1")
        frame1.pack(pady=10, padx=10, fill="both", expand="yes")

        # デバイス1のボタン作成
        self.connect_button1 = Button(
            frame1, text="Connect", command=self.connect1)
        self.connect_button1.pack(pady=5)

        self.disconnect_button1 = Button(
            frame1, text="Disconnect", command=self.disconnect1, state=DISABLED)
        self.disconnect_button1.pack(pady=5)

        # バッテリーレベル表示用のラベルを追加
        self.battery_label1 = Label(frame1, text="Battery Level: -")
        self.battery_label1.pack(pady=5)

        # デバイス1のステータスラベルを追加
        self.status_label1 = Label(frame1, text="Status: Disconnected")
        self.status_label1.pack(pady=5)

        # デバイス2のフレーム作成
        frame2 = LabelFrame(self.master, text="Core2")
        frame2.pack(pady=(0, 15), padx=10, fill="both", expand="yes")

        # デバイス2のボタン作成
        self.connect_button2 = Button(
            frame2, text="Connect", command=self.connect2)
        self.connect_button2.pack(pady=5)

        self.disconnect_button2 = Button(
            frame2, text="Disconnect", command=self.disconnect2, state=DISABLED)
        self.disconnect_button2.pack(pady=5)

        # バッテリーレベル表示用のラベルを追加
        self.battery_label2 = Label(frame2, text="Battery Level: -")
        self.battery_label2.pack(pady=5)

        # デバイス2のステータスラベルを追加
        self.status_label2 = Label(frame2, text="Status: Disconnected")
        self.status_label2.pack(pady=5)

        # イベントループを別スレッドで実行
        self.loop = asyncio.new_event_loop()
        self.loop_thread = threading.Thread(
            target=self.start_loop, args=(self.loop,))
        self.loop_thread.start()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self, width, height):
        # 画面の幅と高さを取得
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # 中央に配置する位置を計算
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))

        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def connect1(self):
        # Connectボタンを無効化
        self.connect_button1.config(state=DISABLED)
        # ステータスラベルを更新
        self.master.after(0, self.status_label1.config, {
                          'text': 'Status: Connecting...'})
        asyncio.run_coroutine_threadsafe(self.connect_task1(), self.loop)

    async def connect_task1(self):
        try:
            if not await self.orphe1.connect():
                print("Failed to connect to Core 1.")
                # 接続失敗時にConnectボタンを有効化
                self.master.after(
                    0, self.connect_button1.config, {'state': NORMAL})
                # ステータスラベルを更新
                self.master.after(0, self.status_label1.config, {
                                  'text': 'Status: Failed to connect'})
                return
            await self.orphe1.set_led(1, 0)
            await self.orphe1.set_acc_range(16)
            await self.orphe1.start_sensor_values_notification()
            print("Connected to Core 1 and started notifications.")

            # バッテリーレベルを表示
            bl = self.orphe1.device_information.battery
            # 0:LOW, 1:MID, 2:HIGH
            if bl == 0:
                self.battery_label1.config(
                    {'text': f'Battery Level: {bl} (LOW)'})
            elif bl == 1:
                self.battery_label1.config(
                    {'text': f'Battery Level: {bl} (MID)'})
            elif bl == 2:
                self.battery_label1.config(
                    {'text': f'Battery Level: {bl} (HIGH)'})

            # 接続成功時にDisconnectボタンを有効化
            self.master.after(
                0, self.disconnect_button1.config, {'state': NORMAL})
            # ステータスラベルを更新
            self.master.after(0, self.status_label1.config,
                              {'text': 'Status: Connected'})

            # 接続成功時にConnectボタンはそのまま無効化

        except Exception as e:
            print(f"Exception during connecting to Core 1: {e}")
            # エラー時にConnectボタンを有効化
            self.master.after(0, self.connect_button1.config,
                              {'state': NORMAL})
            # ステータスラベルを更新
            self.master.after(0, self.status_label1.config, {
                              'text': 'Status: Connection error'})

    def disconnect1(self):
        # Disconnectボタンを無効化
        self.disconnect_button1.config(state=DISABLED)
        # ステータスラベルを更新
        self.master.after(0, self.status_label1.config, {
                          'text': 'Status: Disconnecting...'})
        asyncio.run_coroutine_threadsafe(self.disconnect_task1(), self.loop)

    async def disconnect_task1(self):
        if self.orphe1.is_connected():
            print("Stopping notification for Core 1...")
            await self.orphe1.stop_sensor_values_notification()
            print("Notification stopped. Disconnecting Core 1.")
            await self.orphe1.disconnect()
            print("Disconnected from Core 1.")
            # 切断後にConnectボタンを有効化
            self.master.after(0, self.connect_button1.config,
                              {'state': NORMAL})
            # ステータスラベルを更新
            self.master.after(0, self.status_label1.config, {
                              'text': 'Status: Disconnected'})
            # 切断後にDisconnectボタンを無効化
            self.master.after(0, self.disconnect_button1.config, {
                              'state': DISABLED})

    def on_disconnect1(self):
        print("Disconnected from Core 1.")
        # UIを更新
        self.master.after(0, self.connect_button1.config, {'state': NORMAL})
        self.master.after(0, self.disconnect_button1.config,
                          {'state': DISABLED})
        self.master.after(0, self.status_label1.config, {
                          'text': 'Status: Disconnected'})
        self.master.after(0, self.battery_label1.config,
                          {'text': 'Battery Level: -'})

    def connect2(self):
        # Connectボタンを無効化
        self.connect_button2.config(state=DISABLED)
        # ステータスラベルを更新
        self.master.after(0, self.status_label2.config, {
                          'text': 'Status: Connecting...'})
        asyncio.run_coroutine_threadsafe(self.connect_task2(), self.loop)

    async def connect_task2(self):
        try:
            if not await self.orphe2.connect():
                print("Failed to connect to Core 2.")
                # 接続失敗時にConnectボタンを有効化
                self.master.after(
                    0, self.connect_button2.config, {'state': NORMAL})
                # ステータスラベルを更新
                self.master.after(0, self.status_label2.config, {
                                  'text': 'Status: Failed to connect'})
                return
            await self.orphe2.set_led(1, 0)
            await self.orphe2.set_acc_range(16)
            await self.orphe2.start_sensor_values_notification()
            print("Connected to Core 2 and started notifications.")

            # バッテリーレベルを表示
            bl = self.orphe2.device_information.battery
            # 0:LOW, 1:MID, 2:HIGH
            if bl == 0:
                self.battery_label2.config(
                    {'text': f'Battery Level: {bl} (LOW)'})
            elif bl == 1:
                self.battery_label2.config(
                    {'text': f'Battery Level: {bl} (MID)'})
            elif bl == 2:
                self.battery_label2.config(
                    {'text': f'Battery Level: {bl} (HIGH)'})

            # 接続成功時にDisconnectボタンを有効化
            self.master.after(
                0, self.disconnect_button2.config, {'state': NORMAL})
            # ステータスラベルを更新
            self.master.after(0, self.status_label2.config,
                              {'text': 'Status: Connected'})

            # 接続成功時にConnectボタンはそのまま無効化

        except Exception as e:
            print(f"Exception during connecting to Core 2: {e}")
            # エラー時にConnectボタンを有効化
            self.master.after(0, self.connect_button2.config,
                              {'state': NORMAL})
            # ステータスラベルを更新
            self.master.after(0, self.status_label2.config, {
                              'text': 'Status: Connection error'})

    def disconnect2(self):
        # Disconnectボタンを無効化
        self.disconnect_button2.config(state=DISABLED)
        # ステータスラベルを更新
        self.master.after(0, self.status_label2.config, {
                          'text': 'Status: Disconnecting...'})
        asyncio.run_coroutine_threadsafe(self.disconnect_task2(), self.loop)

    async def disconnect_task2(self):
        if self.orphe2.is_connected():
            print("Stopping notification for Core 2...")
            await self.orphe2.stop_sensor_values_notification()
            print("Notification stopped. Disconnecting Core 2.")
            await self.orphe2.disconnect()
            print("Disconnected from Core 2.")
            # 切断後にConnectボタンを有効化
            self.master.after(0, self.connect_button2.config,
                              {'state': NORMAL})
            # ステータスラベルを更新
            self.master.after(0, self.status_label2.config, {
                              'text': 'Status: Disconnected'})
            # 切断後にDisconnectボタンを無効化
            self.master.after(0, self.disconnect_button2.config, {
                              'state': DISABLED})

    def on_disconnect2(self):
        print("Disconnected from Core 2.")
        # UIを更新
        self.master.after(0, self.connect_button2.config, {'state': NORMAL})
        self.master.after(0, self.disconnect_button2.config,
                          {'state': DISABLED})
        self.master.after(0, self.status_label2.config, {
                          'text': 'Status: Disconnected'})
        self.master.after(0, self.battery_label2.config,
                          {'text': 'Battery Level: -'})

    def on_closing(self):
        # クリーンアップ処理
        asyncio.run_coroutine_threadsafe(self.shutdown(), self.loop)
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.loop_thread.join()
        self.master.destroy()

    async def shutdown(self):
        tasks = []
        if self.orphe1.is_connected():
            tasks.append(self.orphe1.disconnect())
        if self.orphe2.is_connected():
            tasks.append(self.orphe2.disconnect())
        if tasks:
            await asyncio.gather(*tasks)


# メイン部分
if __name__ == "__main__":
    root = Tk()
    app = OrpheApp(root)
    root.mainloop()
