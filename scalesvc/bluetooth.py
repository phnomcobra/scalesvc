"""Late model QN-Scale BLE Consumer"""
import asyncio
from enum import Enum, auto
from time import time
from typing import Any, Callable, Union

from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

from scalesvc import logging, pretty_hex
from scalesvc.signals import operating
from scalesvc.decoder import process

NOTIFICATION_CHARACTERISTIC = "0000fff1-0000-1000-8000-00805f9b34fb"
WRITE_CHARACTERISTIC = "0000fff2-0000-1000-8000-00805f9b34fb"
BATTERY_LEVEL_CHARACTERISTIC = "00002a19-0000-1000-8000-00805f9b34fb"
ADVERTISEMENT_LOCAL_NAME = "QN-Scale"

class Direction(Enum):
    """Message direction enum"""
    TX = auto()
    RX = auto()

async def handler(
    characteristic: Union[BleakGATTCharacteristic | str],
    data: bytearray,
    direction: Direction=Direction.RX
    ):
    """Handle and dispaly transmission activity.
    
    Args:
        characteristic:
            Any

        data:
            bytearray
    
        direction:
            Direction
    """
    if isinstance(characteristic, BleakGATTCharacteristic):
        logging.debug(f'{direction.name}:{characteristic.uuid}: {pretty_hex(data)}')
    else:
        logging.debug(f'{direction.name}:{characteristic}: {pretty_hex(data)}')
    await process(data)

def apply_checksum(message: bytearray) -> bytearray:
    """Compute order independent checksum of the leading n-1 bytes of the message.
    Write checksum byte as the message's last index.

    Args:
        message:
            bytearray
    
    Returns:
        bytearray
    """
    verify = 0x00
    for i in range(0, len(message)-1):
        verify = (verify + message[i]) & 0xff
    message[len(message)-1] = verify
    return message

async def retry(call: Callable, *args, **kwargs) -> Any:
    """Retry"""
    tries = 3
    backoff = 1
    exception = None
    while tries > 0 and operating():
        try:
            return await call(*args, **kwargs)
        except Exception as e: # pylint: disable=broad-exception-caught
            exception = e
            logging.warning(f'{str(call)}({args},{kwargs}): {str(e)}')
            await asyncio.sleep(backoff)
        finally:
            tries -= 1
    raise exception

async def loop():
    """Entry point for the scanner"""
    logging.info("Starting Bluetooth Scanner...")
    scanner = BleakScanner()

    while operating():
        await scanner.start()
        await asyncio.sleep(1.0)
        await scanner.stop()

        logging.debug(f"Detected {len(scanner.discovered_devices)} device(s)...")

        for device, advertisement in scanner.discovered_devices_and_advertisement_data.values():
            if advertisement.local_name == ADVERTISEMENT_LOCAL_NAME:
                client = BleakClient(device.address)

                try:
                    logging.info(f"Connecting to {device.address} ...")
                    await retry(client.connect)
                    logging.info("Connected")

                    await asyncio.sleep(1.0)

                    try:
                        logging.info(f"Pairing: {await client.pair()}")
                    except Exception as pair_error: # pylint: disable=broad-exception-caught
                        logging.warning(f"Pairing: {pair_error}")

                    for service in client.services:
                        for characteristic in service.characteristics:
                            reading = None
                            try:
                                reading = await client.read_gatt_char(characteristic)
                            except Exception as read_error: # pylint: disable=broad-exception-caught
                                reading = str(read_error)
                            logging.debug(f'{characteristic}: {reading}')

                    try:
                        logging.info(f"Enable notifications: {NOTIFICATION_CHARACTERISTIC}")
                        await retry(client.start_notify, NOTIFICATION_CHARACTERISTIC, handler)

                        await asyncio.sleep(1.0)

                        logging.info('Initializing parameters')
                        message = bytearray()
                        weight_byte = 0x01 # Set units to KG
                        message.extend(
                            (0x13, 0x09, 0x15, weight_byte, 0x10, 0x00, 0x00, 0x00, 0x00))
                        message = apply_checksum(message)
                        await handler(WRITE_CHARACTERISTIC, message, Direction.TX)
                        await retry(client.write_gatt_char, WRITE_CHARACTERISTIC, message)

                        await asyncio.sleep(1.0)

                        logging.info('Initializing time')
                        # seconds since 2000-01-01 00:00:00 (utc)
                        scale_time = int(time()) - 946702800
                        message = bytearray()
                        message.extend((0x02, *scale_time.to_bytes(4, 'little')))
                        await handler(WRITE_CHARACTERISTIC, message, Direction.TX)
                        await retry(client.write_gatt_char, WRITE_CHARACTERISTIC, message)

                        await asyncio.sleep(1.0)

                        # Poll the battery level until the scale shuts off
                        # pylint: disable=line-too-long
                        while battery_level := await client.read_gatt_char(BATTERY_LEVEL_CHARACTERISTIC):
                            logging.debug(f'Battery level: {battery_level}')
                            await asyncio.sleep(3)

                    except Exception as e: # pylint: disable=broad-exception-caught
                        logging.info(f"Disconnected: {e}")

                except Exception as e: # pylint: disable=broad-exception-caught
                    logging.error(f'Connection Failed: {e}')
