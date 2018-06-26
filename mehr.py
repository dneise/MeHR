import os.path
import time
from datetime import timedelta, datetime
from tqdm import trange

from mehr_config import load_config
from mehr_lib import (
    reservations_getAll,
    mews_report_to_report_rows,
    write_excel_output_file
)


here = os.path.dirname(os.path.realpath(__file__))

next_execution = 0


def wait_for_next_execution(period=timedelta(hours=24).total_seconds()):
    global next_execution
    current_time = time.time()
    if current_time >= next_execution:
        next_execution = current_time + period
        return
    else:
        minutes_until = int((next_execution - current_time) / 60)
        print(
            '{} minutes until next report to be made... waiting'.format(
                minutes_until
            )
        )
        for i in trange(minutes_until * 6):
            if current_time >= next_execution:
                next_execution = current_time + period
                return
            time.sleep(10)


def repeat():
    configs = load_config(here)

    while True:
        wait_for_next_execution()
        for config in configs:
            print('Working on Hotel: {}'.format(
                config.Name))
            mews_report = reservations_getAll(config)
            rows = mews_report_to_report_rows(mews_report)
            now = datetime.now()
            outpath = os.path.join(
                config.OutFolder,
                now.strftime(config.FileName)
            )
            print('Writing Excel File: {}'.format(
                outpath))
            write_excel_output_file(
                rows,
                outpath=outpath
            )


if __name__ == '__main__':
    repeat()
