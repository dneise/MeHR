import os.path
import time
from datetime import timedelta, datetime
from mehr import (
    load_config,
    get_started_reservations_yesterday,
    mews_report_to_report_rows,
    write_excel_output_file
)


def repeat():
    configs = load_config()
    period = timedelta(hours=24).total_seconds()
    next_execution = 0
    while True:
        current_time = time.time()
        if current_time >= next_execution:
            for config in configs:
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


if __name__ == '__main__':
    repeat()
