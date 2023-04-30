
'''
Solar data logger.

This system reads from my local Enphase envoy and writes to a database.

The two steps are handled in separate threads so that delays while writing to the database don't
delay collection of data points.  

If the database is unavailable, data points are stored in a local CSV file and transmitted
next time the database is available.
'''
import argparse
import logging
import logging.config
import pathlib
import time
import threading
import sys
import datetime
import queue
import os
import json

import dotenv
import yaml

import sdlogger
import sditem
import envoy

logger = logging.getLogger(pathlib.Path(sys.argv[0]).stem)


ENV_LOGGING_CONFIG = "LOGGING_CONFIG"


class SDLoggerThread(object):
    '''
    Read log items from a queue and log them
    '''
    def __init__(self, q: queue.Queue, solarloger: sdlogger.SDLogger):
        self.queue = q
        self.solarlogger = solarloger

    def run(self):
        while True:
            # Get the next work item
            item: sditem.SDItem = self.queue.get()

            # Termination Signal?
            if item is None:
                self.queue.task_done()
                logger.warning("LoggerThread exiting")
                return

            # Process the work item
            try:
                self.solarlogger.log_item(item)
            except Exception as e:
                logger.error("Unexpected exception from solar logger: %s", str(e), exc_info=True)

            # Signal completion
            self.queue.task_done()





def run_loger(interval: int = 60) -> None:

    logger.info("----- STARTING -----")


    #
    # Create the solar logger
    #
    data_logger = sdlogger.SDLogger("local_cache.csv", 
                    os.getenv('SOLARDB_NAME', ""),
                    os.getenv('SOLARDB_TABLE', ""),
                    os.getenv('SOLARDB_USER', ""),
                    os.getenv('SOLARDB_PASS', ""), 
                    os.getenv('SOLARDB_HOST', ""),
                    int(os.getenv('SOLARDB_PORT', "")))

    envoy_system = envoy.EnvoySystem(
                    host = os.getenv('ENPHASE_HOST', 'envoy.local'), 
                    port = int(os.getenv('ENPHASE_PORT', 80)),
                    api_key = os.getenv('ENPHASE_API_KEY')
                )


    #
    # Create a thread to do the logging
    #
    data_queue: queue.Queue = queue.Queue()
    c = SDLoggerThread(data_queue, data_logger)
    data_thread = threading.Thread(target=c.run)
    data_thread.start()


    #
    # Main thread then loops forever
    #
    try:
        while True:
            try:
                item = envoy_system.get_power()
                if item is not None:
                    data_queue.put_nowait(item)
                    print (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {item.production:.1f} - {item.consumption:.1f} -> {item.production - item.consumption:.1f}")
                else:
                    print (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: no data captured")
                # TODO:  more precise sleep time so we are closer to every even 10 seconds.
            except KeyboardInterrupt:
                raise
            except Exception as e:
                logger.error("Unexpected exception: %s", str(e), exc_info=True)
                # TODO:  Notify

            time.sleep(interval)
    except KeyboardInterrupt:
        logger.warning ("Keyboard interrupt")



    #
    # clean up
    #
    logger.warning ("Sending termination signal")
    data_queue.put_nowait(None)

    logger.warning ("Waiting for logger thread")
    data_thread.join()

    logger.warning("----- ENDING -----")
    logging.shutdown()




def main():
    #
    # Set up argument parsing
    #
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
        description=''''

''')

    parser.add_argument('-L', help='Logging configuration file')
    parser.add_argument('-E', help='dotenv configuration file.')
    parser.add_argument('-d', help='Debug level logging', action='store_true')
    parser.add_argument('-i', help='Collection interval in seconds', type=int, default=60)

    args = parser.parse_args()

    if args.E:
        dotenv.load_dotenv(args.E)

 
    # 
    # Configure logging.
    #
    if args.L:
        log_config_path = pathlib.Path(args.L)
        if not log_config_path.exists():
            print(f'Could not find log configuration file {log_config_path}')
            sys.exit(1)
        with open(log_config_path, 'r') as f:
            log_config = yaml.safe_load(f)
        logging.config.dictConfig(log_config)
    else:
        env_config = os.getenv(ENV_LOGGING_CONFIG)
        if env_config is not None:
            logging.config.dictConfig(json.loads(env_config))
        else:
            logging.basicConfig(level=logging.DEBUG if args.d else logging.INFO)

    run_loger(interval = args.i)
    



if __name__ == "__main__":
    #
    # Set up argument parsing
    #
    main()