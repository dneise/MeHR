from setuptools import setup

setup(
    name='MeHR',
    version='0.0.1',
    description="Mews HoKo Reporter",
    author="Dominik Neise",
    author_email='neised@phys.ethz.ch',
    url='https://github.com/dneise/MeHR',
    py_modules=['mehr', ],
    install_requires=[],
    license="MIT license",

    entry_points={
        'console_scripts': [
            'MeHR=mehr:entry',
        ],
    }
)
