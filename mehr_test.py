import os.path
from dateutil.parser import parse

from mehr_config import load_config
from mehr_lib import (
    reservations_getAll,
    mews_report_to_report_rows,
    write_excel_output_file
)

here = os.path.dirname(os.path.realpath(__file__))


def date(when='22.06.2018'):
    configs = load_config(here)
    when = parse(when)
    for config in configs:
        mews_report, start_time = reservations_getAll(
            config,
            start_utc=when
        )
        rows = mews_report_to_report_rows(mews_report)
        outpath = os.path.join(
            config.OutFolder,
            start_time.strftime(config.FileName)
        )
        write_excel_output_file(
            rows,
            outpath=outpath
        )
    return mews_report

if __name__ == '__main__':
    mews_report = date()
