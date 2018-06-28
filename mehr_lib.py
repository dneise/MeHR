from datetime import datetime, timedelta
from datetime import time as dt_time
import requests
import os
import os.path
import iso8601


def last_midnight():
    return datetime.combine(datetime.utcnow().date(), dt_time())


def reservations_getAll(
    config,
    time_filter='Start',
    start_utc=None,
    end_utc=None,
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
    if start_utc is None:
        start_utc = last_midnight() - timedelta(days=1)
    if end_utc is None:
        end_utc = start_utc + timedelta(days=1)

    response = requests.post(
        '{PlatformAddress}/api/connector/v1/{Resource}/{Operation}'.format(
            PlatformAddress=config.PlatformAddress,
            Resource='reservations',
            Operation='getAll',
        ),
        json={
            "ClientToken": config.ClientToken,
            "AccessToken": config.AccessToken,
            "LanguageCode": None,
            "CultureCode": None,
            "TimeFilter": time_filter,
            "StartUtc": start_utc.isoformat(),
            "EndUtc": end_utc.isoformat(),
            "Extent": extent,
        }
    )
    return response.json(), start_utc


def write_text_file(mews_report, outpath, hoko_code):
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
                hoko_code=hoko_code,
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
            outfile.write(line)


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
