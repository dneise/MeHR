import os
import time
from datetime import datetime, timedelta
import iso8601
import requests
import unicodedata
from collections import defaultdict
from types import SimpleNamespace

mews_gender_to_hoko_gender = defaultdict(str, Male='m', Female='w')


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
        hours_after_midnight
    ):
        self.platform_address = platform_address
        self.client_token = client_token
        self.hours_after_midnight = hours_after_midnight
        self.last_execution = None

    def wait_for_next_execution(self):
        last_execution_date = self.last_execution.date()
        last_execution_midnight = datetime(
            *last_execution_date.timetuple()[:6]
        )
        next_execution = (
            last_execution_midnight +
            timedelta(hours=self.hours_after_midnight) +
            timedelta(days=1)
        )
        print(time.asctime(), 'next_execution:', next_execution, flush=True)

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


def make_latin1_compliant(string):
    result = ''
    for char in string:
        try:
            result += unicodedata.normalize(
                'NFKC', char
            ).encode(
                'latin-1'
            ).decode('latin-1')
        except UnicodeEncodeError:
            result += unicodedata.normalize(
                'NFKD', char
            ).encode(
                'latin-1', 'ignore'
            ).decode('latin-1')
    return result


def write_text_file(
    outpath,
    output_entries
):
    outfolder = os.path.dirname(outpath)
    if not os.path.isdir(outfolder):
        os.makedirs(outfolder)

    with open(outpath, 'w', encoding="latin-1") as outfile:
        outfile.write(';'.join([c[0] for c in csv_columns]) + '\n')
        for entry in output_entries:
            line = (
                ';'.join([c[1] for c in csv_columns]) + '\n'
            ).format(e=entry)
            line = make_latin1_compliant(line)
            outfile.write(line)


def doc_from_customer(customer):
    ''' customers can identify with different documents
    we have a certain order of how much we like different documents
    so when a customer identifies with multiple documents we only give the
    number of the document we like best.
    '''
    DOCU_TYPES = {
        'Passport': "PASS",
        'IdentityCard': "ID",
        'Visa': "AUSW",
        'DriversLicense': "AUTO"
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


def make_outpath(outpath_template, mews_report):
    return outpath_template.format(
        hoko=mews_report['HoKoCode'],
        timestamp=mews_report['ReportStartTimeUtc']
    )


def parse_date_to_ddmmyyyy(dt):
    try:
        return iso8601.parse_date(dt).strftime('%d.%m.%Y')
    except:
        return ''


def spaces_from_mews_report(mews_report):
    if mews_report['Spaces'] is not None:
        spaces = {
            space['Id']: space
            for space in mews_report['Spaces']
        }
    else:
        spaces = {}

    spaces = defaultdict(lambda x: {'Number': ''}, **spaces)
    return spaces


def customers_from_mews_report(mews_report):
    customers = {}
    for customer in mews_report['Customers']:
        foo = customer.get('Address', {})
        if foo is None:
            foo = {}
        customer['Address'] = defaultdict(str, foo)
        customers[customer['Id']] = customer
    return customers


def make_output_entries(mews_report):

    customers = customers_from_mews_report(mews_report)
    spaces = spaces_from_mews_report(mews_report)

    output_entries = []
    for reservation in mews_report['Reservations']:
        customer = customers[reservation['CustomerId']]
        output_entries.append(SimpleNamespace(
            creation_date=mews_report['ReportStartTimeUtc'],
            last_name=customer.get('LastName', '')[:100],
            first_name=customer.get('FirstName', '')[:100],
            date_of_birth_str=parse_date_to_ddmmyyyy(customer['BirthDateUtc']),
            gender=mews_gender_to_hoko_gender[customer['Gender']],
            nationality=customer.get('NationalityCode', ''),
            address1=customer['Address']['Line1'][:100],
            address2=customer['Address']['Line2'][:100],
            zip_code=customer['Address']['PostalCode'][:100],
            city=customer['Address']['City'][:100],
            doc_type=doc_from_customer(customer)[0],
            doc_number_str=doc_from_customer(customer)[1][:100],
            room_number=spaces[reservation['AssignedSpaceId']]['Number'][:10],
            number_of_children=reservation.get('ChildCount', 0),
            number_of_adults=int(reservation.get('AdultCount')) - 1,
            arrival_date=parse_date_to_ddmmyyyy(reservation['StartUtc']),
            departure_date=parse_date_to_ddmmyyyy(reservation['EndUtc']),
        ))



    return output_entries

csv_columns = [
    ('ERSTELLDATUM', '{e.creation_date:%d.%m.%Y}'),
    ('FAMILIENNAME', '"{e.last_name}"'),
    ('VORNAME', '"{e.first_name}"'),
    ('GEBURTSDATUM', '{e.date_of_birth_str}'),
    ('GESCHLECHT', '"{e.gender}"'),
    ('GEBURTSORT', '""'),
    ('HEIMATORT', '""'),
    ('NATIONALITAET', '"{e.nationality}"'),
    ('ADRESSE', '"{e.address1}"'),
    ('ADRESSE2', '"{e.address2}"'),
    ('PLZ', '"{e.zip_code}"'),
    ('ORT', '"{e.city}"'),
    ('LAND', '""'),
    ('LANDESKENNZEICHEN', '""'),
    ('BERUF', '""'),
    ('FZ_KENNZEICHEN', '""'),
    ('AUSWEISTYP', '"{e.doc_type}"'),
    ('AUSWEIS_NR', '"{e.doc_number_str}"'),
    ('ZIMMER_NR', '"{e.room_number}"'),
    ('ANZPERS_BIS16', '"{e.number_of_children}"'),
    ('ANZPERS_AB16', '"{e.number_of_adults}"'),
    ('ANKUNFTSDATUM', '{e.arrival_date}'),
    ('ABREISEDATUM', '{e.departure_date}'),
]
