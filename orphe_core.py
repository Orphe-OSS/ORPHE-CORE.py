import asyncio
from datetime import datetime, timedelta
from bleak import BleakClient, BleakScanner


# キャラクタリスティックUUID
CHARACTERISTIC_SENSOR_VALUES_UUID = "f3f9c7ce-46ee-4205-89ac-abe64e626c0f"
CHARACTERISTIC_STEP_ANALYSIS_UUID = "f3f9c7ce-46ee-4205-89ac-abe64e626c0f"
CHARACTERISTIC_DEVICE_INFORMATION_UUID = "24354f22-1c46-430e-a4ab-a1eeabbcdfc0"
# デバイスのサービスUUID（例：OrpheのサービスUUID）
SERVICE_ORPHE_INFORMATION_UUID = "01a9d6b5-ff6e-444a-b266-0be75e85c064"
SERVICE_OTHER_UUID = "01a9d6b5-ff6e-444a-b266-0be75e85c064"


def to_timestamp(hours, minutes, seconds, ms_high, ms_low):
    # 現在の日付を取得
    now = datetime.now()

    # ミリ秒を上位バイトと下位バイトから計算
    milliseconds = (ms_high << 8) | ms_low

    # 日付を置き換えて、新しいdatetimeオブジェクトを作成
    dt = now.replace(hour=hours, minute=minutes, second=seconds,
                     microsecond=milliseconds * 1000)

    # UNIXタイムスタンプを返す（MSまで含めた整数）
    return int(dt.timestamp()*1000)


class AccData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.timestamp = 0
        self.serial_number = 0
        self.packet_number = 0


class GyroData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.timestamp = 0
        self.serial_number = 0
        self.packet_number = 0


class QuatData:
    def __init__(self):
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.timestamp = 0
        self.serial_number = 0
        self.packet_number = 0


class Range:
    def __init__(self):
        self.acc = 0
        self.gyro = 0


class SensorValuesData:
    def __init__(self, owner, data):
        if len(data) == 92:
            self.data = data
            self.type = int.from_bytes(
                data[0:1], byteorder='big', signed=False)
            self.serial_number = int.from_bytes(
                data[1:3], byteorder='big', signed=False)
            self.timestamp = to_timestamp(
                data[3], data[4], data[5], data[6], data[7])
            each_timestamp = self.timestamp
            for i in range(3, -1, -1):
                step = 21*i
                self.acc = AccData()
                self.acc.x = int.from_bytes(
                    data[22+step:24+step], byteorder='big', signed=True)
                self.acc.y = int.from_bytes(
                    data[24+step:26+step], byteorder='big', signed=True)
                self.acc.z = int.from_bytes(
                    data[26+step:28+step], byteorder='big', signed=True)

                self.gyro = GyroData()
                self.gyro.x = int.from_bytes(
                    data[16+step:18+step], byteorder='big', signed=True)
                self.gyro.y = int.from_bytes(
                    data[18+step:20+step], byteorder='big', signed=True)
                self.gyro.z = int.from_bytes(
                    data[20+step:22+step], byteorder='big', signed=True)

                self.quat = QuatData()
                self.quat.w = int.from_bytes(
                    data[8+step:10+step], byteorder='big', signed=True)
                self.quat.x = int.from_bytes(
                    data[10+step:12+step], byteorder='big', signed=True)
                self.quat.y = int.from_bytes(
                    data[12+step:14+step], byteorder='big', signed=True)
                self.quat.z = int.from_bytes(
                    data[14+step:16+step], byteorder='big', signed=True)

                self.acc.serial_number = self.serial_number
                self.gyro.serial_number = self.serial_number
                self.quat.serial_number = self.serial_number
                self.acc.packet_number = 3-i
                self.gyro.packet_number = 3-i
                self.quat.packet_number = 3-i

                if i == 3:
                    self.acc.timestamp = each_timestamp
                    self.gyro.timestamp = each_timestamp
                    self.quat.timestamp = each_timestamp
                else:
                    each_timestamp = each_timestamp + data[28+step]
                    self.acc.timestamp = each_timestamp
                    self.gyro.timestamp = each_timestamp
                    self.quat.timestamp = each_timestamp

                # コールバック関数が設定されている場合、コールバック関数を呼び出す
                if hasattr(owner, 'got_acc_callback') and owner.got_acc_callback:
                    owner.got_acc_callback(self.acc)
                if hasattr(owner, 'got_gyro_callback') and owner.got_gyro_callback:
                    owner.got_gyro_callback(self.gyro)
                if hasattr(owner, 'got_quat_callback') and owner.got_quat_callback:
                    owner.got_quat_callback(self.quat)


class DeviceInformation:
    def __init__(self, data):
        self.data = data
        self.battery = int.from_bytes(data[0:1], byteorder='big', signed=False)
        self.lr = int.from_bytes(data[1:2], byteorder='big', signed=False)
        self.rec = int.from_bytes(data[2:3], byteorder='big', signed=False)
        self.auto_run = int.from_bytes(
            data[3:4], byteorder='big', signed=False)
        self.led = int.from_bytes(data[4:5], byteorder='big', signed=False)
        self.range = Range()
        self.range.acc = int.from_bytes(
            data[8:9], byteorder='big', signed=False)
        self.range.gyro = int.from_bytes(
            data[9:10], byteorder='big', signed=False)


class Orphe:
    def __init__(self):
        self.serial_number_prev = 0
        self.client = None

    def set_got_acc_callback(self, callback):
        self.got_acc_callback = callback

    def set_got_gyro_callback(self, callback):
        self.got_gyro_callback = callback

    def set_got_quat_callback(self, callback):
        self.got_quat_callback = callback

    async def connect(self):
        print("Scanning for ORPHE CORE BLE device...")
        devices = await BleakScanner.discover()

        target_device = None
        for device in devices:
            if SERVICE_ORPHE_INFORMATION_UUID.lower() in [uuid.lower() for uuid in device.metadata.get("uuids", [])]:
                target_device = device
                print(f"Found target device: {device.name}, {device.address}")
                break

        if target_device is None:
            print("Target device not found.")
            return False

        self.client = BleakClient(target_device.address)
        await self.client.connect()
        if await self.client.is_connected():
            print("Connected to the device")
            return True
        else:
            print("Failed to connect to the device")
            return False

    async def read_device_information(self):
        device_information = await self.client.read_gatt_char(CHARACTERISTIC_DEVICE_INFORMATION_UUID)
        device_information = DeviceInformation(device_information)

        return device_information

    async def write_device_information(self):
        await self.client.write_gatt_char(CHARACTERISTIC_DEVICE_INFORMATION_UUID, bytearray([0x02, 0x01, 0x03] + [0x00] * 17))

    async def sensor_values_notification_handler(self, sender, data):
        # データの長さを確認
        if len(data) == 92:
            sensor_values = SensorValuesData(self, data)
            if (sensor_values.serial_number - self.serial_number_prev) != 1:
                # データ欠損の場合
                print(
                    f"Data loss detected. {self.serial_number_prev} <-> {sensor_values.serial_number}")
            self.serial_number_prev = sensor_values.serial_number

    async def start_sensor_values_notification(self):
        await self.client.start_notify(CHARACTERISTIC_SENSOR_VALUES_UUID, self.sensor_values_notification_handler)

    async def start_step_analysis_notification(self):
        await self.client.start_notify(CHARACTERISTIC_STEP_ANALYSIS_UUID, self.step_analysis_notification_handler)

    async def stop_sensor_values_notification(self):
        await self.client.stop_notify(CHARACTERISTIC_SENSOR_VALUES_UUID)

    async def stop_step_analysis_notification(self):
        await self.client.stop_notify(CHARACTERISTIC_STEP_ANALYSIS_UUID)

    async def disconnect(self):
        await self.client.disconnect()
