"""Post decoded values to API endpoint."""
from aiohttp import ClientSession
from pydantic import BaseModel, PositiveInt, PositiveFloat

from scalesvc.config import CONFIG
from scalesvc import logging

HEADERS = { 'Content-Type': 'Application/JSON' }

class WeightRequestObject(BaseModel): # pylint: disable=too-few-public-methods
    """The class encapsulates and validates API requests."""
    weight_lbs: PositiveFloat
    weight_kg: PositiveFloat
    resistance_one_kohms: PositiveInt
    resistance_two_kohms: PositiveInt

async def post(sample: WeightRequestObject):
    """Post sample data to API endpoint.
    
    Args:
        sample:
            WeightRequestObject
    """
    if CONFIG.url is None:
        logging.error("No URL set!")
        return

    logging.debug(f'Posting sample to {CONFIG.url}')
    async with ClientSession() as session:
        async with session.post(
            CONFIG.url, headers=HEADERS, json=sample.dict()) as response:
            if response.status != 200:
                logging.error(response)
                logging.error(await response.text())
            else:
                logging.info('Completed')
