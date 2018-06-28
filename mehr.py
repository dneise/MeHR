import os.path
import time
from datetime import timedelta

from mehr_config import load_config
from mehr_lib import reservations_getAll, write_text_file


here = os.path.dirname(os.path.realpath(__file__))

next_execution = 0


def wait_for_next_execution(period=timedelta(hours=24).total_seconds()):
    global next_execution
    current_time = time.time()
    if current_time >= next_execution:
        next_execution = current_time + period
        return
    else:
        seconds_to_wait = int(next_execution - current_time)
        for i in range(int(seconds_to_wait//10)+1):
            if current_time >= next_execution:
                next_execution = current_time + period
                return

            time.sleep(10)


def repeat():
    configs = load_config(here)

    while True:
        try:
            wait_for_next_execution()
            for config in configs:
                print('Working on Hotel: {}'.format(
                    config.Name))
                mews_report, start_time = reservations_getAll(config)
                outpath = os.path.join(
                    config.OutFolder,
                    start_time.strftime(config.FileName)
                )
                print('Writing File: {}'.format(
                    outpath))
                write_text_file(
                    mews_report,
                    outpath=outpath,
                    hoko_code=config.HoKoCode
                )
        except (KeyboardInterrupt, SystemExit):
            return


if __name__ == '__main__':
    repeat()
