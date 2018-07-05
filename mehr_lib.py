import os
import time
from datetime import datetime, timedelta
import iso8601
import requests
import unicodedata
from collections import OrderedDict, defaultdict

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

csv_columns = [
    'ERSTELLDATUM',
    'FAMILIENNAME',
    'VORNAME',
    'GEBURTSDATUM',
    'GESCHLECHT',
    'GEBURTSORT',
    'HEIMATORT',
    'NATIONALITAET',
    'ADRESSE',
    'ADRESSE2',
    'PLZ',
    'ORT',
    'LAND',
    'LANDESKENNZEICHEN',
    'BERUF',
    'FZ_KENNZEICHEN',
    'AUSWEISTYP',
    'AUSWEIS_NR',
    'ZIMMER_NR',
    'ANZPERS_BIS16',
    'ANZPERS_AB16',
    'ANKUNFTSDATUM',
    'ABREISEDATUM',
]


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

    print(time.asctime(), 'writing:', outpath, flush=True)
    with open(outpath, 'w', encoding="latin-1") as outfile:
        outfile.write(';'.join(csv_columns) + '\n')

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
                city = customer['Address']['City']
            else:
                address1 = ''
                address2 = ''
                zip_code = ''
                city = ''
            address1 = address1 if address1 is not None else ''
            address2 = address2 if address2 is not None else ''
            zip_code = zip_code if zip_code is not None else ''
            city = city if city is not None else ''

            doc_type, doc_number = doc_from_customer(customer)
            data = OrderedDict(
                ERSTELLDATUM=mews_report['ReportStartTimeUtc'],
                FAMILIENNAME=customer['LastName'][:100],
                VORNAME=customer['FirstName'][:100],
                GEBURTSDATUM=date_of_birth_str,
                GESCHLECHT=mews_gender_to_hoko_gender[customer['Gender']],
                GEBURTSORT='',
                HEIMATORT='',
                NATIONALITAET=customer['NationalityCode'],
                ADRESSE=address1,
                ADRESSE2=address2,
                PLZ=zip_code,
                ORT=city,
                LAND='',
                LANDESKENNZEICHEN='',
                BERUF='',
                FZ_KENNZEICHEN='',
                AUSWEISTYP=doc_type,
                AUSWEIS_NR=doc_number[:100],
                ZIMMER_NR=room_number[:10],
                ANZPERS_BIS16=reservation['ChildCount'],
                ANZPERS_AB16=str(int(reservation['AdultCount']) - 1),
                ANKUNFTSDATUM=iso8601.parse_date(reservation['StartUtc']),
                ABREISEDATUM=iso8601.parse_date(reservation['EndUtc']),
            )

            line = (
                '{ERSTELLDATUM:%d.%m.%Y};'
                '"{FAMILIENNAME}";'
                '"{VORNAME}";'
                '{GEBURTSDATUM};'
                '"{GESCHLECHT}";'
                '"{GEBURTSORT}";'
                '"{HEIMATORT}";'
                '"{NATIONALITAET}";'
                '"{ADRESSE}";'
                '"{ADRESSE2}";'
                '"{PLZ}";'
                '"{ORT}";'
                '"{LAND}";'
                '"{LANDESKENNZEICHEN}";'
                '"{BERUF}";'
                '"{FZ_KENNZEICHEN}";'
                '"{AUSWEISTYP}";'
                '"{AUSWEIS_NR}";'
                '{ZIMMER_NR};'
                '{ANZPERS_BIS16};'
                '{ANZPERS_AB16};'
                '{ANKUNFTSDATUM:%d.%m.%Y};'
                '{ABREISEDATUM:%d.%m.%Y}\n'
            ).format(**data)
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
