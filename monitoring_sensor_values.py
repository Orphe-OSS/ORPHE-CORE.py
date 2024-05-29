import asyncio
from bleak import BleakClient, BleakScanner

# 加速度センサ値のキャラクタリスティックUUID
CHARACTERISTIC_UUID = "f3f9c7ce-46ee-4205-89ac-abe64e626c0f"
# デバイスのサービスUUID（例：OrpheのサービスUUID）
SERVICE_UUID = "01a9d6b5-ff6e-444a-b266-0be75e85c064"


async def notification_handler(sender, data):
    # データの長さを確認
    print(f"Data length: {len(data)}")

    # sending type
    type = int.from_bytes(data[0:1], byteorder='big', signed=False)
    print(f"Sending type: {type}")
    # 1: シリアルナンバー上位バイト, 2: シリアルナンバー下位バイト
    serial_number = int.from_bytes(data[1:3], byteorder='big', signed=False)
    print(f"Serial number: {serial_number}")

    # データが送信されるたびに呼び出されるハンドラ
    # print(f"Notification from {sender}: {data}")
    acc_x = int.from_bytes(data[0:2], byteorder='little', signed=True)
    acc_y = int.from_bytes(data[2:4], byteorder='little', signed=True)
    acc_z = int.from_bytes(data[4:6], byteorder='little', signed=True)
    # print(f"Accelerometer data - X: {acc_x}, Y: {acc_y}, Z: {acc_z}")


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
            await asyncio.sleep(10)  # 通知を受け取るために10秒間待機
            await client.stop_notify(CHARACTERISTIC_UUID)
        else:
            print("Failed to connect to the device")

if __name__ == "__main__":
    asyncio.run(main())
