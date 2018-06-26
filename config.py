'''
'''
import os.path
import yaml
from types import SimpleNamespace

here = os.path.dirname(os.path.realpath(__file__))

config_template = '''
{
    PlatformAddress: "https://demo.mews.li",
    ClientToken: "E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D",
    Hotels: [
        {
            Name: "Test Hotel",
            AccessToken: "C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D",
            OutFolder: {here},
        },
    ]
}
'''

config_not_found_message = '''\
There is no "config.json" file in {here}
I am going to make one for you now.
Please, adjust the file to your personal needs and start me again.
'''


def load_config():
    config_path = os.path.join(here, 'config.json')
    if not os.path.isfile(config_path):
        print(config_not_found_message.format(here=here))
        open(config_path, 'w').write(config_template.format(here=here))
    config = SimpleNamespace(**yaml.load(open(config_path)))
    return config


