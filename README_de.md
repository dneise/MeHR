# Mews HoKo Reporter (MeHR)

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/uq2ZysrAoT4/0.jpg)](https://www.youtube.com/watch?v=uq2ZysrAoT4)

[English version](README.md)

Der Mews Hoko Reporter ist ein kleines Programm, welches automatisch
die Meldeschein-Reports für die
[Zürcher Hotel Kontrolle (HoKo)](https://www.hotelkontrolle.zh.ch)
aus [Mews](https://www.mewssystems.com/) zieht und der HoKo über die SiDAP Schnittstelle überträgt.
Es läuft lokal auf einem Ihrer Computer im Hintergrund, am Besten auf genau dem Computer,
auf welchem Sie im Augenblick bereits den [SiDAP client](https://www.hotelkontrolle.zh.ch/HoKoDMZ/pages/info.xhtml) installiert haben.


## Arbeitsweise

MeHR fragt einmal pro Tag die Kundenprofile (Anreisen vom Vortag) ab, die notwendig sind, um die Meldeschein-Reports zusammen zu stellen, die von der Kantons Polizei verlangt werden. Sobald die notwendigen Daten heruntergeladen wurden, erzeugt MeHR einen speziell formatierten Report (in form einer sog. CSV-Datei), der direkt vom SiDAP-Client in die Datenbanken der Hotelkontrolle hochgeladen wird.

Hierfür ist es notwendig, dass der SiDAP-Client auf Ihrem System installiert ist. MeHR ist kein Ersatz für den SiDAP-Client sondern eine Schnittstelle zwischen Mews und dem SiDAP-Client.


## Vorbereitungen

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/MXrxauWNL-k/0.jpg)](https://www.youtube.com/watch?v=MXrxauWNL-k)

### ClientToken

Damit ein Programm mit Mews in Kontakt treten darf, muss es mit einem sog. *ClientToken* beweisen, dass es sich um ein Programm handelt, welches von Mews zeritfiziert wurde. MeHR wurde von Mews zeritfiziert, enthält aber nicht den ClientToken, da es sich bei MeHR um freie und quelloffene Software handelt.

Daher müssen Sie sich, als zukünftiger Benutzer von MeHR, mit dem Integrations Team von Mews in Verbindung setzen und den ClientToken für MeHR erfragen. Dies ist vermutlich am einfachsten per Email.
Durch einen Klick auf [diesen Link](mailto:integrations@mewssystems.com?subject=ClientToken%20request%3A%20Connector%20Integration%20SiDAP&body=Dear%20Mews%20Integrations%20Team%2C%0A%0AWe%20would%20like%20to%20use%20the%20%22Connector%20Integration%20SiDAP%22%20for%20our%20Zurich%20based%20Hotel%20and%20therefore%20would%20like%20to%20request%20the%20ClientToken%20for%20this%20integration.%0AAdditionally%20we%20would%20like%20to%20ask%20for%20activation%20of%20this%20integration%2C%20so%20that%20we%20can%20find%20the%20access%20token%20there.%0A%0ABest%20regards%20and%20many%20thanks%20in%20advance%0A) sollte sich Ihr Email Programm öffnen und eine Email mit einem bereits vorformulierten Text erscheinen.

### AccessToken

Der ClientToken ermöglicht den Zugriff auf Mews, aber noch nicht auf die Daten Ihres Hotels. Die Daten Ihres Hotels sind mit einem zweiten Token, dem sog. *AccessToken*, geschützt. Sie können MeHR Zugriff auf Ihre Kundendaten ermöglichen, indem Sie für jedes Hotel, für das MeHR Reports erstellen soll, ein AccessToken bereithalten.

Sie finden den AccessToken für MeHR im Mews Commander unter Settings -> Integrations -> Connector Integration SiDAP. Oben rechts auf der Seite finden Sie dann ein Schlüssel Symbol. Wenn Sie dies anklicken, erscheint ein AccessToken, welchen Sie bitte für die folgenden Schritte bereithalten.

### HoKo Code

Jedem Hotel in Zürich wurde von der Kantonspolizei ein vierstelliger Code zugeteilt. Auch diesen benötigt MeHR, bitte halten sie also für jedes Ihrer Zürcher Hotels den HoKo Code bereit.

# Installation

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/zv3GeBg5esw/0.jpg)](https://www.youtube.com/watch?v=zv3GeBg5esw)


## Erste Schritte

Ich habe MeHR in meiner Freizeit entwickelt und stelle es Ihnen frei zur Verfügung. Näheres entnehmen sie bitte der [Lizenz](LICENSE). Falls MeHR auf Ihrem System nicht wie gewünscht funktionieren sollte, können Sie gerne über das [Ticketsystem](https://github.com/dneise/mehr/issues) Kontakt aufnehmen und Ihre Fragen stellen.

Um die Funktionalität von MeHR zu prüfen, gehen Sie bei der Installation bitte schrittweise vor.

Laden Sie bitte die aktuelle Version von MeHR hier herunter:
<https://github.com/dneise/MeHR/releases>

Die aktuelle Version ist [mehr_v0.4.4.exe](https://github.com/dneise/MeHR/releases/download/v0.4.4/mehr_v0.4.4.exe).

Sie sollten die Datei nun in Ihrem `Downloads` Ordner finden. Für den ersten Testbetrieb schlage ich vor, diese exe-Datei in einen leeren Ordner zu verschieben, z.B. auf Ihrem Desktop.

Führen Sie bitte die Datei einmal aus, z.B. mit einem Doppelklick links.
Es öffnet sich für sehr kurze Zeit ein Fenster und schliesst sich sofort wieder.
Dies ist normal: MeHR kann nicht ohne eine sog. Konfigurations Datei funktionieren. Fehlt diese Datei, reklamiert MeHR und erzeugt für Sie eine solche Konfigurations Datei, welche bereits mit einer Test-Konfiguration gefüllt ist. Der Name der Konfigurationsdatei lautet `config.json`.

Starten Sie die `mehr_v0.4.4.exe` nun noch einmal, wird ein Test-Meldeschein-Report erstellt.
Hierzu nimmt MeHR bereits Kontakt zu einem Mews Demo-Hotel auf und fragt ab, welche Gäste in diesem Demo-Hotel am 22.06.2018 eingecheckt haben. Dies diente als Test während der Entwicklung von MeHR und dient Ihnen nun als kurze Bestätigung, dass MeHR auf Ihrem Computer korrekt läuft und mit Mews Kontakt aufnehmen kann.

Im nächsten Schritt werden Sie MeHR für Ihr Hotel konfigurieren.

Sie können den Test-Meldeschein-Report nun löschen.
Falls sie an dieser Stelle keinen Test-Meldeschein-Report sehen, funktioniert MeHR auf Ihrem System nicht korrekt. Ich würde Sie in diesem Fall bitten, ein Ticket zu eröffnen und mir das Problem zu schildern.

## Konfiguration

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/kCho1oRCoy8/0.jpg)](https://www.youtube.com/watch?v=kCho1oRCoy8)

Die Konfigurationsdatei `config.json` ist im sog. [JSON Format](https://de.wikipedia.org/wiki/JavaScript_Object_Notation#Beispiel) geschrieben. Dies ist ein Dateiformat, welches
sowohl maschinen- als auch menschenlesbar ist, so dass Sie die Konfiguration bequem durchführen können
aber auch das MeHR Programm Ihre Einträge sicher und fehlerfrei versteht.

Falls sie einen Fehler in der Konfiguration machen und MeHR Ihre Eingaben nicht versteht, wird es schlicht abbrechen und nicht mit fehlerhaften Einstellungen zu arbeiten beginnen.

Zur Konfiguration öffnen Sie bitte die `config.json` mit einem Text-Editor Ihrer Wahl. Das Programm "Notepad" ist unter Windows vorinstalliert und völlig ausreichend.

Sie sollten in Ihrer `config.json` solche Einträge sehen. Die Reihenfolge der Einträge ist nicht von Belang.

```json
{
    "PlatformAddress": "https://demo.mews.li",
    "ClientToken": "E0D439EE522F44368DC78E1BFB03710C-D24FB11DBE31D4621C4817E028D9E1D",
    "HoursAfterMidnight": 3,
    "TestStartTime": "22.06.2018 03:00",
    "TestMode": true,
    "OutFolder": "C:\\Users\\Dominik\\Downloads\\MeHR-0.4.3\\dist",
    "Hotels": [
        {
            "AccessToken": "C66EF7B239D24632943D115EDE9CB810-EA00F8FD8294692C940F6B5A8F9453D",
            "HoKoCode": "1234"
        }
    ]
}
```

Im Folgenden werde ich Sie anleiten, die Konfiguration entsprechend Ihrer Wünsche anzupassen.

### `OutFolder`

Zu Beginn steht hier der Pfad auf den Ordner, in dem Sie MeHR zum erstem Mal gestartet haben. Tragen Sie hier bitte den Pfad ein, wo MeHR für Sie die Meldescheinreports künftig ablegen soll.

Final sollte dies der Ordner sein, in dem der SiDAP-Client die Reports erwartet. In der Standardinstallation des SiDAP-Clients ist das dieser Ordner:

```json
    "OutFolder": "C:\\SiDAP\\SiDAP-Client\\Upload\\Hoko"
```

Bevor die Meldescheinreports das erste Mal vom SiDAP-Client automatisch an die Hoko übermittelt werden, 
können Sie sich diese gerne einmal selbst ansehen. Tragen Sie hier einfach einen belieben Pfad ein oder lassen Sie den Pfad einfach zunächst so, wie er ist.

### `TestMode` und `TestStartTime`

Diese Einträge sind für den ersten Test notwendig. Wir werden noch einen
weiteren Test durchführen, für den diese Einträge notwendig sind. Danach können sie gelöscht werden.

### `HoursAfterMidnight`

Bitte tragen sie hier die Zeit ein, zu der der Bericht erstellt werden soll.
Voreingestellt ist `3` Uhr morgens.

### `ClientToken`

Bitte tragen sie hier, dass *ClientToken* ein, welches Ihnen von Mews (vermutlich per Email) auf Ihre Anfrage hin zugesandt wurde.

### `PlatformAddress`

Dieser Eintrag muss von Ihnen wie folgt eingestellt werden:

```json
    "PlatformAddress": "https://www.mews.li"
```

### `Hotels`

Dies ist eine Liste, zu erkennen an den beiden eckigen Klammern `[` und `]`.
In diese Liste können Sie für Ihr(e) Zürcher Hotel(s) den `HoKoCode` und den `AccessToken` eintragen.
Zur besseren Übersicht ist es erlaubt, weitere Felder wie z.B. `Name` hinzuzufügen.

### Beispiel für Ihren ersten Test:

Am Ende wird Ihre `config.json` so aussehen:
```json
{
    "PlatformAddress": "https://www.mews.li",
    "ClientToken": "<geheimes ClientToken via email>",
    "HoursAfterMidnight": 3,
    "OutFolder": "C:\\SiDAP\\SiDAP-Client\\Upload\\Hoko",
    "Hotels": [
        {
            "Name": "Super-Hotel",
            "HoKoCode": "1111",
            "AccessToken": "geheimes AccessToken vom Super-Hotel"
        },
        {
            "Name": "Wunderbares-Hotel",
            "HoKoCode": "2222",
            "AccessToken": "geheimes AccessToken vom wunderbaren Hotel"
        },
        {
            "Name": "Megafeines-Hotel",
            "HoKoCode": "3333",
            "AccessToken": "geheimes AccessToken vom Megafeinen Hotel"
        }
    ],
    "TestMode": true,
    "TestStartTime": "<heute> 03:00"
}
```

Bitte beachten sie die Kommasetzung. Alle Einträge sind durch Komma `,` zu trennen. Der letzte Eintrag einer Liste bekommt kein Komma am Ende.

Wenn Sie die `config.json` wie hier beschrieben angepasst haben, ist es Zeit für einen zweiten Testlauf. Speichern Sie die `config.json` und führen sie MeHR nocheinmal aus.
Sie werden jeweils eine Datei für jedes Ihrer Hotels am angegebenen Ort sehen.

Sie können sich nun anhand dieser Reports überzeugen, dass MeHR die Reports korrekt zusammenstellt.


## Dauerbetrieb

Nach erfolgreichem Test ist es an der Zeit MeHR dauerhaft laufen zu lassen.
Hierzu löschen Sie die beiden Einträge namens `TestMode` und `TestStartTime`.

Nun haben sie prinzipiell zwei Möglichkeiten.

Starten Sie MeHR einfach mit einem Doppelklick, wird sich ein Fenster öffnen, in welchem angezeigt wird, wann MeHR für Sie die nächsten Reports erstellen wird (z.B. am nächsten Morgen um 3 Uhr).

Um MeHR dauerhaft laufen zu lassen, können Sie dieses Fenster minimieren, an diesem PC dauerhaft eingeloggt bleiben und auf diese Weise MeHR im Hintergrund ausführen.

Angenehmer ist es aber, wenn kein Fenster dauerhaft geöffnet bleiben muss, man sich ausloggen kann und MeHR trotzdem weiterläuft. Hierzu muss MeHR als sog. Dienst (engl. Service) installiert werden.

Hierzu empfehle ich das Programm [NSSM](<http://nssm.cc/release/nssm-2.24.zip>).

Die Einrichtung von MeHR als Dienst mit Hilfe von NSSM ist viel leichter in einem kleinen Video zu erklären, als es hier im Text zu beschreiben. Daher verweise ich Sie an dieser Stelle auf das unten stehende Video:

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/_CcAJm1uYrc/0.jpg)](https://www.youtube.com/watch?v=_CcAJm1uYrc)

# [License](LICENSE)

Dieses Programm ist kostenfrei und quelloffen. 
Sie können es für Ihr Hotel kostenfrei benutzen, ändern und weitergeben.

