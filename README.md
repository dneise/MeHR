# Mews HoKo Reporter (MeHR)


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

## Configuration and Usage

In order to be able to download your customer profiles from Mews this tool
needs two cryptographic keys:
 * the `AccessToken` (one per property) and
 * the `ClientToken`.

After installing MeHR please ask Mews to give you a `ClientToken` and one `AccessToken` per property you would like to creat ereports for.

In order to install MeHR you only need to download `mehr.exe` from here:

https://github.com/dneise/MeHR/releases

You can put the `mehr.exe` file in any location you like. In order to configure it, please double click on the file. When started for the first time, it will only create `config.json` file and end itself. You can now open that file and enter the secret `ClientToken` and `AccessToken`s as well as adjust the Name of the hotel and the location you would like the output to be stored as well as the file name.

Once you have configured mehr correctly, just save the `config.json` and start mehr.exe again. It will immediately start creating the excel files and put them into the requested location for every hotel you have configured. Then it will wiat 24 hours and repeat the same step again.

In order to keep it running you will have to keep the window open forever and never log out. If you do not want this, you can install Mehr as a service as outlined below.

# Installation as a service

In order to install `mehr.exe` on your Windows machine as a service, you will have to use a tool called `NSSM`, which can be [downloaded here](https://nssm.cc/download). I used the "nssm 2.24 (2014-08-31)" for testing.

This tool can be used to install any program as a service to run in the background of your computer, NSSM claims to even restart the program should it ever crash and restart it. 

Dedicated Help on how to install any program as a service can be found on the NSSM website.

I did not need administrator rights to do this on my machine, but I also did not restrict my user very much.


# [License](LICENSE)

This tool is both free of charge and open source, i.e. you can use it for your
hotel without paying me a dime and you can modify it as you like and even
distribute modified versions to your friends.



