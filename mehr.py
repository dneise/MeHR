import sys
import os.path
from dateutil.parser import parse as datetime_parse
from mehr_config import load_config
from mehr_lib import MewsClient, write_text_file

here = os.path.dirname(os.path.realpath(__file__))


def main():
    config = load_config(here)
    mews = MewsClient(
        platform_address=config.PlatformAddress,
        client_token=config.ClientToken,
        hours_after_midnight=config.HoursAfterMidnight
    )
    outpath_template = os.path.join(
        config.OutFolder,
        '{hoko}_{timestamp:%Y%m%d_%H%M}_mews.txt'
    )

    if not config.TestMode:
        while True:
            for hotel in config.Hotels:
                mews_report = mews.reservations(hotel)
                write_text_file(mews_report, outpath_template)
            mews.wait_for_next_execution()

    else:
        for hotel in config.Hotels:
            mews_report = mews.reservations(
                hotel,
                start_utc=datetime_parse(config.TestStartTime)
            )
            write_text_file(mews_report, outpath_template)
        return


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
