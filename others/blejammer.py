import asyncio
from bleak import BleakAdvertiser

fake_devices = [f"FakeBLE_{i:03d}" for i in range(100)]

async def rotate_ads():
    advertiser = BleakAdvertiser()
    for device in fake_devices:
        print(f"Advertising as {device}")
        await advertiser.start(name=device)
        await asyncio.sleep(0.2)
        await advertiser.stop()

asyncio.run(rotate_ads())
