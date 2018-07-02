import os
import time
from datetime import datetime, timedelta
import iso8601
import requests


def hours_after_last_midnight(hours=0):
    right_now = datetime.now()
    today_date = right_now.date()
    todays_midnight = datetime(*today_date.timetuple()[:6])
    hours_after_midnight = todays_midnight + timedelta(hours=hours)
    return hours_after_midnight


class MewsClient:
    def __init__(
        self,
        platform_address,
        client_token,
        hours_after_midnight,
        period
    ):
        self.platform_address = platform_address
        self.client_token = client_token
        self.hours_after_midnight = hours_after_midnight
        self.period = period
        self.last_execution = None

    def wait_for_next_execution(self):
        last_execution_date = self.last_execution.date()
        last_execution_midnight = datetime(
            *last_execution_date.timetuple()[:6]
        )
        next_execution = (
            last_execution_midnight +
            timedelta(hours=self.hours_after_midnight) +
            self.period
        )
        print('next_execution:', next_execution)

        while True:
            if not datetime.utcnow() >= next_execution:
                time.sleep(10)
        return

    def reservations(
        self,
        hotel_config,
        start_utc=None,
        end_utc=None,
        time_filter='Start',
        states=['Started', ],
        extent={
            "Customers": True,
            "Reservations": True,
            "Spaces": True,
        },
    ):
        '''
        time_filter - string, default Colliding
        start_utc - string, default: Now
        end_utc - string, default: Now + 1 day
        states - array of string, default ['Confirmed', 'Started', 'Processed']
        extent - string, default Reservations, Groups and Customers
        currency - string
        '''
        access_token = hotel_config.AccessToken

        if start_utc is None and end_utc is None:
            end_utc = hours_after_last_midnight(self.hours_after_midnight)
        if start_utc is None and end_utc is not None:
            start_utc = end_utc - timedelta(days=1)
        if end_utc is None and start_utc is not None:
            end_utc = start_utc + timedelta(days=1)

        response = requests.post(
            '{PlatformAddress}/api/connector/v1/{Resource}/{Operation}'.format(
                PlatformAddress=self.platform_address,
                Resource='reservations',
                Operation='getAll',
            ),
            json={
                "ClientToken": self.client_token,
                "AccessToken": access_token,
                "LanguageCode": None,
                "CultureCode": None,
                "TimeFilter": time_filter,
                "StartUtc": start_utc.isoformat(),
                "EndUtc": end_utc.isoformat(),
                "Extent": extent,
            }
        )
        self.last_execution = datetime.utcnow()

        mews_report = response.json()
        mews_report['ReportStartTimeUtc'] = start_utc
        mews_report['ReportEndTimeUtc'] = end_utc
        mews_report['HoKoCode'] = hotel_config.HoKoCode
        return mews_report


def write_text_file(
    mews_report,
    outpath_template
):
    outpath = outpath_template.format(
        hoko=mews_report['HoKoCode'],
        timestamp=mews_report['ReportStartTimeUtc']
    )
    outfolder = os.path.dirname(outpath)
    if not os.path.isdir(outfolder):
        os.makedirs(outfolder)

    customers = {
        customer['Id']: customer
        for customer in mews_report['Customers']
    }

    if mews_report['Spaces'] is not None:
        spaces = {
            space['Id']: space
            for space in mews_report['Spaces']
        }
    else:
        spaces = {}

    with open(outpath, 'w', encoding="latin-1") as outfile:
        for reservation in mews_report['Reservations']:
            customer = customers[reservation['CustomerId']]
            try:
                room_number = spaces[reservation['AssignedSpaceId']]['Number']
            except:
                room_number = ''

            if customer['BirthDateUtc'] is not None:
                date_of_birth_str = iso8601.parse_date(
                    customer['BirthDateUtc']
                ).strftime('%d.%m.%Y')
            else:
                date_of_birth_str = ''

            if customer['Address'] is not None:
                address1 = customer['Address']['Line1']
                address2 = customer['Address']['Line2']
                zip_code = customer['Address']['PostalCode']
                city_iso = customer['Address']['CountryCode']
                city = customer['Address']['City']
            else:
                address1 = ''
                address2 = ''
                zip_code = ''
                city_iso = ''
                city = ''

            doc_type, doc_number = doc_from_customer(customer)
            line = (
                '{hoko_code}|'
                '{arrival_date:%Y%m%d}|'
                '{last_name}|'
                '{first_name}|'
                '{date_of_birth_str}|'
                '{nationality_iso}|'
                '{address1}|'
                '{address2}|'
                '{zip_code}|'
                '{city}|'
                '{city_iso}|'
                '{city_iso}|'
                '{doc_number}|'
                '{doc_type}|'
                '{room_number}|'
                '{number_adults}|'
                '{number_children}|'
                '{arrival_date:%d.%m.%Y}|'
                '{departure_date:%d.%m.%Y}|'
                '{departure_date:%d.%m.%Y}\r\n'
            ).format(
                hoko_code=mews_report['HoKoCode'],
                arrival_date=iso8601.parse_date(reservation['StartUtc']),
                departure_date=iso8601.parse_date(reservation['EndUtc']),
                last_name=customer['LastName'],
                first_name=customer['FirstName'],
                date_of_birth_str=date_of_birth_str,
                room_number=room_number,
                nationality_iso=customer['NationalityCode'],
                address1=address1,
                address2=address2,
                zip_code=zip_code,
                city=city,
                city_iso=city_iso,
                number_adults=reservation['AdultCount'],
                number_children=reservation['ChildCount'],
                doc_type=doc_type,
                doc_number=doc_number,
            )
            outfile.write(line.encode('latin-1', 'replace'))


def doc_from_customer(customer):
    ''' customers can identify with different documents
    we have a certain order of how much we like different documents
    so when a customer identifies with multiple documents we only give the
    number of the document we like best.
    '''
    DOCU_TYPES = {
        'Passport': "Reisepass",
        'IdentityCard': "Personalausweis / ID",
        'Visa': "Reisepass",
        'DriversLicense': "Führerschein"
    }

    for doc_type in DOCU_TYPES:
        if customer[doc_type] is not None:
            number = customer[doc_type]['Number'].strip()
            # with the if below we just make sure that customers having
            # by accident or human error multiple documents, but some
            # without a number, are not identified with a passport with an
            # empty number as long as they have a drivers license with a valid
            # number.
            # Not sure if this is needed, depends on business logic on the
            # mews side, which I do not know.
            if number:
                return DOCU_TYPES[doc_type], number
    return '', ''
