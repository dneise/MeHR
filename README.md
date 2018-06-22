# Mews HoKo Reporter (MeHR)

There is also a [german version of this document](README_de.md).

The Mews HoKo Reporter is a little tool to create dedicated reports for the
[Zurich Hotel Kontrolle (HoKo)](https://www.hotelkontrolle.zh.ch)
from [Mews](https://www.mewssystems.com/).
It is supposed to run on-premises on either a Windows or Linux machine of your choice.

## Purpose

MeHR will once per night (exact time can be configured by you)
request the necessary customer profiles needed to compile the report which is
mandatory in Zurich and requested by the cantonal police. Once the customer data is
downloaded this tool will create a report (usually in form of an excel file)
and upload this file for you to <https://www.hotelkontrolle.zh.ch/>.

In order to perform the upload, MeHR might or might not utilize
the [SiDAP client](https://www.hotelkontrolle.zh.ch/HoKoDMZ/pages/info.xhtml)
provided by the zurich police for this purpose

Optionally these excel files will not be deleted after uploading them, but will
remain on your disk for later reference.

## Configuration

In order to be able to download your customer profiles from Mews this tool
needs two cryptographic keys:
 * one key, you can generate yourself, which is called `AccessToken` and
 * one you'll need to request from Mews called `ClientToken`.

After installing MeHR please ask Mews to give you a `ClientToken` and find the
`AccessToken` in the Mews Commander (**TODO: write/find detailed description how to find the AccessToken**)

In order to upload the excel file to the HoKo, MeHR needs your HoKo username and
password. Please provide these 4 credentials in a [text-file](explain_windows_people_what_a_textfile_is)
looking like this:
**TBR:** If the SiDAP client is used, MeHR does not need the HoKo credentials, c.f. [issues/3](https://github.com/dneise/MeHR/issues/3)
```
ClientToken: E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D
AccessToken: C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D
HoKoUsername: my_secret_hoko_username
HoKoPassword: my_very_secret_hoko_password
```

You can use a single MeHR installation to create and upload HoKo reports
for multiple hotels of your chain, so in order to keep everything nice and tidy, please
specify the aforementioned credentials for each hotel, it should look like this:

```
MyAwesomeHotel:
  ClientToken: E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D
  AccessToken: C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D
  HoKoUsername: my_secret_hoko_username
  HoKoPassword: my_very_secret_hoko_password
MyVeryBestHotel:
  ClientToken: E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D
  AccessToken: same_client_token_but_different_access_token
  HoKoUsername: another_different_hoko_username
  HoKoPassword: another_very_secret_hoko_password
```

As you can see the `ClientToken` is always the same for each hotel, but the
`AccessToken` is different for the different hotels.



# Installation

[
TBR: deliver a windows installer for convenience, so people do not need to install
first Python3 and then MeHR
]

The software is written in Python 3, if you do not have Python 3 installed on
your machine (which is likely on both Windows and Linux) I recommend to install
the Python distribution called [Anaconda](https://www.anaconda.com/download).
It is free of charge and makes installation of additional libraries and packages
much easier than the vanilla Python you get on [python.org](https://www.python.org/downloads/).


Once Python 3 is installed you can install MeHR by typing:

    pip install git+https://github.com/dneise/mehr


# Usage

[work in progress]


# [License](LICENSE)

This tool is both free of charge and open source, i.e. you can use it for your
hotel without paying me a dime and you can modify it as you like and even
distribute modified versions to your friends.



