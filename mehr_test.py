import os.path
from dateutil.parser import parse

from mehr_config import load_config
from mehr_lib import reservations_getAll, write_text_file

here = os.path.dirname(os.path.realpath(__file__))


def date(when='22.06.2018'):
    configs = load_config(here)
    when = parse(when)
    for config in configs:
        mews_report, start_time = reservations_getAll(
            config,
            start_utc=when
        )
        outpath = os.path.join(
            config.OutFolder,
            start_time.strftime(config.FileName)
        )
        write_text_file(
            mews_report,
            outpath=outpath,
            hoko_code=config.HoKoCode
        )
    return mews_report

if __name__ == '__main__':
    mews_report = date()
