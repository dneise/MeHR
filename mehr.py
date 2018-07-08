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


def main():
    config = load_config()
    mews = MewsClient(
        platform_address=config.PlatformAddress,
        client_token=config.ClientToken,
        hours_after_midnight=config.HoursAfterMidnight
    )
    if config.HoKoTest:
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

            output_entries = []
            output_entries.append(SimpleNamespace(
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
            ))
            write_text_file(outpath, output_entries)
        return

    elif config.TestMode:
        for hotel in config.Hotels:
            mews_report = mews.reservations(
                hotel,
                start_utc=config.TestStartTime
            )
            outpath = make_outpath(config.outpath_template, mews_report)
            output_entries = make_output_entries(mews_report)

            write_text_file(outpath, output_entries)
        return

    else:  # Normal Mode
        while True:
            for hotel in config.Hotels:
                mews_report = mews.reservations(hotel)
                outpath = make_outpath(config.outpath_template, mews_report)
                output_entries = make_output_entries(mews_report)
                write_text_file(outpath, output_entries)
            mews.wait_for_next_execution()

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        sys.exit(0)
