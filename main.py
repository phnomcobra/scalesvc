"""Late model QN-Scale message relay"""
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import signal
import sys

from scalesvc.bluetooth import loop
from scalesvc.config import CONFIG
from scalesvc.signals import stop, operating

def init_logging():
    """Initialize logging"""
    logger = logging.getLogger('app')

    if CONFIG.logging.path is not None:
        os.makedirs(CONFIG.logging.path, exist_ok=True)

        app_handler = TimedRotatingFileHandler(
            os.path.join(CONFIG.logging.path, 'application.log'),
            when="D",
            backupCount=CONFIG.logging.retention_days
        )

        logger.addHandler(app_handler)

    logger.setLevel(CONFIG.logging.level.value)

    logging.info(CONFIG)

def main():
    """Main entry point"""
    init_logging()
    asyncio.run(loop())

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)

    if sys.platform == 'win32':
        from PySimpleGUIQt import SystemTray
        from threading import Thread
        tray = SystemTray(menu=['Scale Service', ['Exit']])
        Thread(target=main).start()

        while operating():
            if tray.Read(timeout=1) == 'Exit':
                stop()
                sys.exit()
    else:
        main()
