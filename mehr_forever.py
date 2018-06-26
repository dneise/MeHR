import os.path
import time
from types import SimpleNamespace
from datetime import timedelta, datetime
from mehr import (
    load_config,
    get_started_reservations_yesterday,
    mews_report_to_report_rows,
    write_excel_output_file
)

here = os.path.dirname(os.path.realpath(__file__))


def repeat():
    configs = load_config(here)
    period = timedelta(hours=24).total_seconds()
    next_execution = 0
    while True:
        current_time = time.time()
        if current_time >= next_execution:
            for config in configs:
                config = SimpleNamespace(**config)
                mews_report = get_started_reservations_yesterday(config)
                rows = mews_report_to_report_rows(mews_report)
                now = datetime.now()
                outpath = os.path.join(
                    config.OutFolder,
                    now.strftime(config.FileName)
                )
                write_excel_output_file(
                    rows,
                    outpath=outpath
                )
            next_execution = current_time + period
        time.sleep(60)


if __name__ == '__main__':
    repeat()
