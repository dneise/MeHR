from datetime import datetime
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
    for config in configs:
        mews_report = reservations_getAll(
            config,
            start_utc=None if when is None else parse(when).date()
        )
        rows = mews_report_to_report_rows(mews_report)

        now = datetime.now()
        outpath = os.path.join(config.OutFolder, now.strftime(config.FileName))
        write_excel_output_file(
            rows,
            outpath=outpath
        )

if __name__ == '__main__':
    date()
