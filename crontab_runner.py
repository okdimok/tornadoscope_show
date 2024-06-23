import os, sys, time
sys.path.insert(0, ".")
from run_once import should_this_continue_running
import datetime
import logging
import asyncio
from gyverhub_device import GHDevice, GHDummyDevice
logger = logging.getLogger(__name__)

async def main():
    if not should_this_continue_running("/tmp/crontab_runner_pid"):
        logger.critical("Another instance is already running, exiting")
        sys.exit(1)
    logger.info(f"Running from crontab {os.getpid()} at {datetime.datetime.now()}")
    from main_runner import MainRunner
    runner = MainRunner()
    # await runner.set_device()
    await runner.set_device(GHDummyDevice())
    runner.run()
    logger.critical(f"Stopping from crontab {os.getpid()} at {datetime.datetime.now()}")

if __name__ == "__main__":
    asyncio.run(main())