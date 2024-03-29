import os
import time
from copy import deepcopy
from datetime import datetime, timedelta
import iso8601
import requests
import unicodedata
from collections import defaultdict
from types import SimpleNamespace
import logging

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
        self.last_execution = datetime.now()


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
        logging.info('next_execution: {}'.format(next_execution))

        while datetime.now() < next_execution:
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
            "Resources": True,
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
        response = requests.post(
            f'{self.platform_address}/api/connector/v1/services/getAll',
            json={
                "ClientToken": self.client_token,
                "AccessToken": access_token,
            }
        )
        if not response.ok:
            logging.warning(
                'unable to getall services: %r\nHeaders:\n%r\nText:\n%r\n',
                response,
                response.headers,
                response.text
            )

        services = response.json()["Services"]
        def is_reservable_and_active(service):
            return service["Type"] == "Reservable" and service["IsActive"]

        services = [s for s in services if is_reservable_and_active(s)]
        service_ids = [s["Id"] for s in services]

        if start_utc is None and end_utc is None:
            end_utc = hours_after_last_midnight(self.hours_after_midnight)
        if start_utc is None and end_utc is not None:
            start_utc = end_utc - timedelta(days=1)
        if end_utc is None and start_utc is not None:
            end_utc = start_utc + timedelta(days=1)

        copied_hotel_config = deepcopy(hotel_config)
        copied_hotel_config.AccessToken = (
            copied_hotel_config.AccessToken[:3] +
            '...' +
            copied_hotel_config.AccessToken[-3:]
        )
        logging.info(
            "Working on hotel %r timerange:%s - %s",
            copied_hotel_config,
            start_utc,
            end_utc
        )

        json={
            "ClientToken": self.client_token,
            "AccessToken": access_token,
            "LanguageCode": None,
            "CultureCode": None,
            "TimeFilter": time_filter,
            "StartUtc": start_utc.isoformat(),
            "EndUtc": end_utc.isoformat(),
            "Extent": extent,
            "ServiceIds": service_ids,
        }
        response = requests.post(
            f'{self.platform_address}/api/connector/v1/reservations/getAll',
            json=json
        )
        if not response.ok:
            logging.debug(
                'response not ok: %r\nHeaders:\n%r\nText:\n%r\n',
                response,
                response.headers,
                response.text
            )
        self.last_execution = datetime.now()

        mews_report = response.json()
        mews_report['ReportStartTimeUtc'] = start_utc
        mews_report['ReportEndTimeUtc'] = end_utc
        mews_report['HoKoCode'] = hotel_config.HoKoCode
        logging.debug('got mews_report: %r', mews_report)
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
    logging.info(
        'Writing %d output_entries to: %s',
        len(output_entries),
        outpath
    )

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
    spaces = mews_report.get('Resources', None)
    if spaces is None:
        spaces_by_id = {}
    else:
        spaces_by_id = {
            space['Id']: space
            for space in spaces
        }

    spaces_by_id = defaultdict(lambda: {'Name': ''}, **spaces_by_id)
    logging.debug('%d Spaces found in mews_report', len(spaces_by_id))
    return spaces_by_id


def get_no_None(dict_, key_, default=''):
    value = dict_.get(key_, default)
    if value is None:
        value = default
    return value


def customers_from_mews_report(mews_report):
    customers = {}
    if 'Customers' not in mews_report:
        return customers
    for customer in mews_report['Customers']:
        foo = customer.get('Address', {})
        if foo is None:
            foo = {}
        customer['Address'] = defaultdict(str, foo)
        for k in customer['Address']:
            if customer['Address'][k] is None:
                customer['Address'][k] = ''
        customers[customer['Id']] = customer
    logging.debug('%d Customers found in mews_report', len(customers))
    return customers


def make_output_entries(mews_report):

    customers = customers_from_mews_report(mews_report)
    spaces = spaces_from_mews_report(mews_report)

    output_entries = []
    if 'Reservations' not in mews_report:
        logging.warning(
            'no  Reservations found in mews_report'
        )
        return output_entries
    else:
        logging.debug(
            '%d Reservations found in mews_report',
            len(mews_report['Reservations'])
        )
    for reservation in mews_report['Reservations']:
        customer = customers[reservation['CustomerId']]
        entry = SimpleNamespace(
            creation_date=mews_report['ReportStartTimeUtc'],
            last_name=get_no_None(customer, 'LastName', '')[:100],
            first_name=get_no_None(customer, 'FirstName', '')[:100],
            date_of_birth_str=parse_date_to_ddmmyyyy(customer['BirthDateUtc']),
            gender=mews_gender_to_hoko_gender[customer['Gender']],
            nationality=get_no_None(customer, 'NationalityCode', ''),
            address1=customer['Address']['Line1'][:100],
            address2=customer['Address']['Line2'][:100],
            zip_code=customer['Address']['PostalCode'][:100],
            city=customer['Address']['City'][:100],
            doc_type=doc_from_customer(customer)[0],
            doc_number_str=doc_from_customer(customer)[1][:100],
            room_number=spaces[reservation['AssignedResourceId']]['Name'][:10],
            number_of_children=get_no_None(reservation, 'ChildCount', 0),
            number_of_adults=int(get_no_None(reservation, 'AdultCount')) - 1,
            arrival_date=parse_date_to_ddmmyyyy(reservation['StartUtc']),
            departure_date=parse_date_to_ddmmyyyy(reservation['EndUtc']),
        )
        # They to not like empty strings. They want a dot in some field
        # Go figure.
        if entry.nationality == '':
            entry.nationality = '.'
        if entry.date_of_birth_str == '':
            entry.date_of_birth_str = '.'
        if entry.doc_number_str == '':
            entry.doc_number_str = '.'
        output_entries.append(entry)

    logging.debug('%d output_entries generated', len(output_entries))
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
