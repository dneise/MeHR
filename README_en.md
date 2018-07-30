# Mews HoKo Reporter (MeHR)

[Deutsche Version](README.md)

The Mews HoKo Reporter is a little tool to create dedicated reports for the
[Zurich Hotel Kontrolle (HoKo)](https://www.hotelkontrolle.zh.ch)
from [Mews](https://www.mewssystems.com/).
It is supposed to run on-premises on either a Windows or Linux machine of your choice.

## Purpose

MeHR will once per days
request the necessary customer profiles needed to compile the report which is
mandatory in Zurich and requested by the cantonal police. Once the customer data is
downloaded this tool will create a report (excel file) and place the file in a locations (specified by the user)
so the SiDAP Client (c.f. below) can find it and upload it.

In order to perform the upload uses the
the [SiDAP client](https://www.hotelkontrolle.zh.ch/HoKoDMZ/pages/info.xhtml)
provided by the zurich police for this purpose.

## Preparation

In order to use MeHR you need to request the "Connector Integration SiDAP" [via email](mailto:integrations@mewssystems.com) from Mews, Mews will then provide you with the `ClientToken` and you can find the `AccessToken`s in the Mews Commander under: Settings -> Integrations.

In order to install MeHR you only need to download `mehr.exe` from here:

https://github.com/dneise/MeHR/releases

You can put the `mehr.exe` file in any location you like. In order to configure it, please double click on the file. When started for the first time, it will only create `config.json` file and end itself. You can now open that file and enter the secret `ClientToken` and `AccessToken`s as well as adjust the Name of the hotel and the location you would like the output to be stored as well as the file name.

Once you have configured mehr correctly, just save the `config.json` and start mehr.exe again. It will immediately start creating the text files and put them into the requested location for every hotel you have configured. Then it will wait 24 hours and repeat the same step again.

In order to keep it running you will have to keep the window open forever and never log out. If you do not want this, you can install Mehr as a service as outlined below.


# Setup

 * find a place to put MeHR, e.g. close to the SiDAP client:
    - if your SiDAP Client is installed in `C:\SiDAP\SiDAP-Client`
    - then there is an upload folder here: `C:\SiDAP\SiDAP-Client\Upload`
    - I propose you make a folder called `MeHR` in the Upload folder.
    - --> `C:\SiDAP\SiDAP-Client\Upload\MeHR`
 * download and copy `mehr.exe` to that place
 * create a `config.json` file and enter the required Mews and HoKo credentials
   For your convenience, `mehr.exe` creates this config file for you, so you
   only need to fill in the information.
    - in `OutFolder` finally you want to put this: `C:\SiDAP\SiDAP-Client\Upload\HoKo`
    - any file in that folder are automatically uploaded to the Zurich Hotel Kontrolle
    - so for testing, when you do not yet trust MeHR to do the job correctly, it is best to
      invent a different place, e.g. `C:\SiDAP\SiDAP-Client\Upload\MeHR-test` or so.
    - Also you'll have to replace every backslash `\` in the path with a double backslash `\\`
  *


# Install MeHR as windows service

 * Get NSSM V2.24 from <http://nssm.cc/release/nssm-2.24.zip>
 * unpack it
 * use nssm to install `MeHR.exe` as a service using the nssm GUI.
 * don't forget to setup stdout and stderr as logfiles.
 * go to the windows "services" app and start the MeHR service
 * observe how one textfile per hotel is created immediately in the destination specified in the config file.


# Build executables on Windows

 * Install Miniconda (or Anaconda).
 * Download mehr sources zip-folder from github; unzip it.
 * start Anaconda Prompt and go to mehr folder.
 * install dependencies `conda env create -f environment.yml`
 * activate environment `conda activate mehr_build`
 * build the executables `pyinstaller -F -w mehr.py`
 * find the executables in the `dist` folder



# [License](LICENSE)

This tool is both free of charge and open source, i.e. you can use it for your
hotel without paying me a dime and you can modify it as you like and even
distribute modified versions to your friends.
