"""Signalling module"""
from scalesvc import logging

OPERATING = True

def stop(signal=None, frame=None):
    """Stop event loop"""
    if signal:
        logging.debug(f'signal: {signal}')
    if frame:
        logging.debug(frame)
    logging.info("Shutting down...")
    global OPERATING # pylint: disable=global-statement
    OPERATING = False

def operating():
    """Should the event loop shutdown"""
    return OPERATING
