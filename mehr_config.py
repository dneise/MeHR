import sys
from types import SimpleNamespace
import os
import os.path
import json
from dateutil.parser import parse as datetime_parse
import logging

config_template = {
    'PlatformAddress': "https://demo.mews.li",
    'ClientToken': "E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D",
    'OutFolder': None,
    'HoursAfterMidnight': 3,
    'TestMode': True,
    'TestStartTime': "22.06.2018 03:00",
    'Hotels': [
        {
            'AccessToken': "C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D",
            'HoKoCode': '1234',
        },
    ]
}

config_not_found_message = '''\
There is no "config.json" file in {here}
I am going to make one for you now.
Please, adjust the file to your personal needs.
'''


def load_config(path_to_config=None):
    if path_to_config is None:
        path_to_config = os.getcwd()
    config_path = os.path.join(path_to_config, 'config.json')
    if not os.path.isfile(config_path):
        logging.info(config_not_found_message.format(here=path_to_config))
        config_template['OutFolder'] = path_to_config
        json.dump(
            config_template,
            open(config_path, 'w'),
            indent=4,
        )
        sys.exit(0)
    config = json.load(
        open(config_path),
        object_hook=lambda x: SimpleNamespace(**x)
    )

    config.outpath_template = os.path.join(
        config.OutFolder,
        '{hoko}_{timestamp:%d%m%Y_%H%M}_GEN_MEW.csv'
    )

    if 'TestMode' not in config.__dict__:
        config.TestMode = False

    if 'HoKoTest' not in config.__dict__:
        config.HoKoTest = False

    if config.TestMode:
        config.TestStartTime = datetime_parse(config.TestStartTime)

    if 'log_level' in config.__dict__:
        try:
            config.log_level = getattr(logging, config.log_level)
        except AttributeError as e:
            logging.exception(e)
            logging.warning(
                '"log_level" in config.json is not a valid log_level: \n'
                'Has to be one of CRITICAL, ERROR, WARNING, INFO, DEBUG'
                'log_level is set to DEBUG now.'
            )
            config.log_level = logging.DEBUG
    else:
        config.log_level = logging.INFO

    return config
