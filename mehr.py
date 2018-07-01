import sys
from mehr_config import load_config
from mehr_lib import MewsClient, write_text_file


def main():
    config = load_config()
    mews = MewsClient(
        platform_address=config.PlatformAddress,
        client_token=config.ClientToken,
        hours_after_midnight=config.HoursAfterMidnight
    )

    if not config.TestMode:
        while True:
            for hotel in config.Hotels:
                mews_report = mews.reservations(hotel)
                write_text_file(mews_report, config.outpath_template)
            mews.wait_for_next_execution()

    else:
        for hotel in config.Hotels:
            mews_report = mews.reservations(
                hotel,
                start_utc=config.TestStartTime
            )
            write_text_file(mews_report, config.outpath_template)
        return


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
