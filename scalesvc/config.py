"""This module implements the argument parser and validation classes."""
import argparse
from pathlib import Path
from typing import Union

from pydantic import BaseModel, PositiveInt, HttpUrl
import toml

from scalesvc.logging import LogLevel

class Logging(BaseModel): #  pylint: disable=too-few-public-methods
    """The class encapsulates and validates the logging settings."""
    retention_days: PositiveInt = 30
    level: LogLevel = LogLevel.INFO
    path: Union[Path, None] = None

class Configuration(BaseModel): # pylint: disable=too-few-public-methods
    """This class is the root level of encapsulation for the configuration settings."""    
    url: Union[HttpUrl, None] = None
    logging: Logging

parser = argparse.ArgumentParser(description = 'QN-Scale Message Relay')
parser.add_argument('-f', dest='config_file', action='store', default='config.toml')
kwargs = vars(parser.parse_args())
CONFIG = Configuration(**toml.load(kwargs['config_file']))
