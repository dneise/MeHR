import sys
from types import SimpleNamespace
from datetime import datetime
from mehr_config import load_config
from mehr_lib import (
    MewsClient,
    write_text_file,
    make_outpath,
    make_output_entries
)
import logging


def do_normal_mode(config):
    mews = MewsClient(
        platform_address=config.PlatformAddress,
        client_token=config.ClientToken,
        hours_after_midnight=config.HoursAfterMidnight
    )

    while True:
        mews.wait_for_next_execution()
        for hotel in config.Hotels:
            try:
                mews_report = mews.reservations(hotel)
                outpath = make_outpath(config.outpath_template, mews_report)
                output_entries = make_output_entries(mews_report)
                write_text_file(outpath, output_entries)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                logging.exception(e)


def do_fix_date_test_mode(config):
    mews = MewsClient(
        platform_address=config.PlatformAddress,
        client_token=config.ClientToken,
        hours_after_midnight=config.HoursAfterMidnight
    )

    for hotel in config.Hotels:
        mews_report = mews.reservations(
            hotel,
            start_utc=config.TestStartTime
        )
        outpath = make_outpath(config.outpath_template, mews_report)
        output_entries = make_output_entries(mews_report)

        write_text_file(outpath, output_entries)
    sys.exit(0)


def do_hoko_test(config):
    mews = MewsClient(
        platform_address=config.PlatformAddress,
        client_token=config.ClientToken,
        hours_after_midnight=config.HoursAfterMidnight
    )

    for hotel in config.Hotels:
        mews_report = mews.reservations(
            hotel,
            start_utc=config.TestStartTime
        )
        outpath = make_outpath(config.outpath_template, mews_report)

        all_chars = ''.join(
            b
            for b in bytes([i for i in range(256)]).decode('latin-1')
            if b.isalpha()
        )
        N = len(all_chars) // 2
        last_name, first_name = all_chars[:N], all_chars[N:]

        write_text_file(outpath, output_entries=[SimpleNamespace(
            creation_date=datetime.utcnow(),
            last_name=last_name,
            first_name=first_name,
            date_of_birth_str='01.01.1980',
            gender='w',
            nationality='CH',
            address1='Zwingly Weg 1',
            address2='',
            zip_code='8000',
            city='Zürich',
            doc_type='ID',
            doc_number_str='1234567890',
            room_number='101',
            number_of_children=0,
            number_of_adults=0,
            arrival_date='06.07.2018',
            departure_date='16.07.2018',
        )])
    sys.exit(0)


def main():
    config = load_config()
    logging.basicConfig(
        level=config.log_level,
        format='%(asctime)s %(levelname)-8s %(message)s',
    )
    if config.HoKoTest:
        do_hoko_test(config)
    elif config.TestMode:
        do_fix_date_test_mode(config)
    else:  # Normal Mode
        try:
            do_normal_mode(config)
        except Exception as e:
            logging.exception(e)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
