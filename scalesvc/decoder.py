"""Message decoder"""
from scalesvc import logging
from scalesvc.api import post, WeightRequestObject

MESSAGE_TYPE_IDX = 0
PROTOCOL_TYPE_IDX = 2
SCALE_READY_IDX = 5
WEIGHT_HIGH_IDX = 3
WEIGHT_LOW_IDX = 4
WEIGHT_MESSAGE_TYPE_ID = 0x10
RESISTANCE_ONE_HIGH_IDX = 6
RESISTANCE_ONE_LOW_IDX = 7
RESISTANCE_TWO_HIGH_IDX = 8
RESISTANCE_TWO_LOW_IDX = 9

async def process(message: bytearray):
    """Process message data
    
    Args:
        data:
            bytearray
    """
    if len(message) == 0:
        return

    if message[MESSAGE_TYPE_IDX] == WEIGHT_MESSAGE_TYPE_ID:
        await weight(message)
        return

    logging.debug(f'Unrecognized message type: {message[MESSAGE_TYPE_IDX]}')

async def weight(message: bytearray):
    """Process Weight Reading Message (0x10)

    Args:
        message:
            bytearray

    Layout:
        offset:            0       1       2             3              4          
        description: |Message Type|?|Protocol Type|Weight Hi Byte|Weight Lo Byte|

        offset:         5       6          7          8          9      a
        description: |Ready|R1 Hi Byte|R1 Lo Byte|R2 Hi Byte|R2 Lo Byte|?|

    Example:
        10 0b ff 0b 2c 11 00 00 00 00 62  # 28.6 KG example
    """
    if len(message) != 11:
        logging.error('Invalid length')
        return

    if message[PROTOCOL_TYPE_IDX] != 0xff:
        logging.error('Invalid protocol type')
        return

    if message[SCALE_READY_IDX] != 0x01:
        logging.debug('Scale not ready')
        return

    # Weight reading is registered as a 16 bit unsigned integer registering centigrams
    weight_kg = float(message[WEIGHT_HIGH_IDX] * 256 + message[WEIGHT_LOW_IDX]) / 100.0
    weight_lbs = round(weight_kg * 2.20462, 1)
    logging.info(f'Weight: {weight_kg} KG, {weight_lbs} LBS')

    # Read resistance as a 16 bit unsigned integer registering KOhms?
    resistance_one = message[RESISTANCE_ONE_HIGH_IDX] * 256 + message[RESISTANCE_ONE_LOW_IDX]
    logging.info(f'Resistance One: {resistance_one} KOhms') # Educated guess for KOhms

    # Read resistance as a 16 bit unsigned integer registering KΩ?
    resistance_two = message[RESISTANCE_TWO_HIGH_IDX] * 256 + message[RESISTANCE_TWO_LOW_IDX]
    logging.info(f'Resistance Two: {resistance_two} KOhms') # Educated guess for KOhms

    await post(
        WeightRequestObject(
            weight_lbs=weight_lbs,
            weight_kg=weight_kg,
            resistance_one_kohms=resistance_one,
            resistance_two_kohms=resistance_two,
        )
    )
