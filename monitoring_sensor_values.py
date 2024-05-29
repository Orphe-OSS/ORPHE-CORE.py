import asyncio
from bleak import BleakClient, BleakScanner


# 加速度センサ値のキャラクタリスティックUUID
CHARACTERISTIC_UUID = "f3f9c7ce-46ee-4205-89ac-abe64e626c0f"
# デバイスのサービスUUID（例：OrpheのサービスUUID）
SERVICE_UUID = "01a9d6b5-ff6e-444a-b266-0be75e85c064"


class AccData:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class SensorValuesData:
    def __init__(self, data):
        self.data = data
        self.type = int.from_bytes(data[0:1], byteorder='big', signed=False)
        self.serial_number = int.from_bytes(
            data[1:3], byteorder='big', signed=False)
        self.acc = AccData()
        self.acc.x = int.from_bytes(data[22:24], byteorder='big', signed=True)
        self.acc.y = int.from_bytes(data[24:26], byteorder='big', signed=True)
        self.acc.z = int.from_bytes(data[26:28], byteorder='big', signed=True)


serial_number_prev = 0


async def notification_handler(sender, data):
    global serial_number_prev
    # データの長さを確認
    if len(data) == 92:
        sensor_values = SensorValuesData(data)
        if (sensor_values.type != 50):
            return
        print(f"Sending type: {sensor_values.type}")
        print(f"Serial number: {sensor_values.serial_number}")
        print(
            f"Accelerometer data - X: {sensor_values.acc.x}, Y: {sensor_values.acc.y}, Z: {sensor_values.acc.z}")

        if (sensor_values.serial_number - serial_number_prev) != 1:
            # データ欠損の場合
            print(
                f"Data loss detected. {serial_number_prev} <-> {sensor_values.serial_number}")
        serial_number_prev = sensor_values.serial_number


async def main():
    print("Scanning for ORPHE CORE BLE device...")
    devices = await BleakScanner.discover()

    # スキャン結果の詳細を表示
    # for device in devices:
    #     print(
    #         f"Device found: {device.name} ({device.address}), RSSI={device.rssi}")
    #     for uuid in device.metadata.get("uuids", []):
    #         print(f"  UUID: {uuid}")

    target_device = None
    for device in devices:
        if SERVICE_UUID.lower() in [uuid.lower() for uuid in device.metadata.get("uuids", [])]:
            target_device = device
            print(f"Found target device: {device.name}, {device.address}")
            break

    if target_device is None:
        print("Target device not found.")
        return

    async with BleakClient(target_device.address) as client:
        if await client.is_connected():
            print("Connected to the device")

            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
            # Ctrl+Cが押されるまで待機
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Stopping notification...")
                await client.stop_notify(CHARACTERISTIC_UUID)
                print("Notification stopped. Disconnecting from the device.")
            # await asyncio.sleep(10)  # 通知を受け取るために10秒間待機
            # await client.stop_notify(CHARACTERISTIC_UUID)
        else:
            print("Failed to connect to the device")


if __name__ == "__main__":
    asyncio.run(main())
