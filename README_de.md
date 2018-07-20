# Mews HoKo Reporter (MeHR)

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/uq2ZysrAoT4/0.jpg)](https://www.youtube.com/watch?v=uq2ZysrAoT4)

[English version](README.md)

Der Mews Hoko Reporter ist ein kleines Programm, welches automatisch
die Meldeschein-Reports für die
[Zürcher Hotel Kontrolle (HoKo)](https://www.hotelkontrolle.zh.ch)
aus [Mews](https://www.mewssystems.com/) zieht und der HoKo über die SiDAP Schnittstelle überträgt.
Es läuft lokal auf einem Ihrer Computer im Hintergrund, am besten auf genau dem Computer
auf welchem Sie im Augenblick bereits den [SiDAP client](https://www.hotelkontrolle.zh.ch/HoKoDMZ/pages/info.xhtml) installiert haben.


## Arbeitsweise

MeHR fragt einmal pro Tag die Kundenprofile ab, die notwendig sind um die Meldeschein-Reports zusammen zu stellen, die von der Kantons Polizei verlangt werden. Sobald die notwendigen Daten heruntergeladen wurden, erzeugt MeHR einen speziell formatierten Report (in form einer sog. CSV-Datei), der direkt vom SiDAP-Client in die Datenbanken der Hotelkontrolle hochgeladen werden kann.

Hierfür ist es notwendig, dass der SiDAP-Client auf Ihrem System installiert ist. MeHR ist kein Ersatz für den SiDAP-Client sondern eine Schnittstelle zwischen Mews und dem SiDAP-Client.


## Vorbereitungen

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/MXrxauWNL-k/0.jpg)](https://www.youtube.com/watch?v=MXrxauWNL-k)

### ClientToken

Damit ein Programm mit Mews in Kontakt treten darf, muss es mit einem sog. *ClientToken* beweisen, dass es sich um ein Programm handelt, welches von Mews zeritfiziert wurde. MeHR wurde von Mews zeritfiziert, enthält aber nicht den ClientToken, da es sich bei MeHR um freie und quelloffene Software handelt.

Daher müssen sie als zukünftiger Benutzer von MeHR sich mit dem integrations team von Mews in Verbindung setzen und den ClientToken für MeHR erfragen. Dies ist vermutlich am einfachsten per email.
Durch einen click auf [diesen Link](mailto:integrations@mewssystems.com?subject=ClientToken%20request%3A%20Connector%20Integration%20SiDAP&body=Dear%20Mews%20Integrations%20Team%2C%0A%0AWe%20would%20like%20to%20use%20the%20%22Connector%20Integration%20SiDAP%22%20for%20our%20Zurich%20based%20Hotels%20and%20therefore%20would%20like%20to%20request%20the%20ClientToken%20for%20this%20integration.%0A%0ABest%20regards%20and%20many%20thanks%20in%20advance%0A) sollte sich ihr email Programm öffnen und eine email mit einem bereits vorformulierten Text erscheinen.

### AccessToken

Das ClientToken ermöglicht den Zugriff auf Mews, aber noch nicht auf die Daten Ihres Hotels. Die Daten Ihres Hotels sind jeweils mit einem AccessToken geschützt. Sie können MeHR Zugriff auf Ihre Kundendaten ermöglichen, indem Sie für jedes Hotel, für das MeHR reports erstellen soll, ein AccessToken bereithalten.

Sie finden das AccessToken für MeHR im Mews Commander under Settings -> Integrations -> Connector Integration SiDAP. Oben rechts auf der Seite finden Sie dann ein Schlüssel Symbol. Wenn sie dies anklicken, erscheint ein AccessToken, welches sie bitte für die folgenden Schritte bereithalten.

### HoKo Code

Jedem Hotel in Zürich wurden von der Kantonspolizei ein vierstelliger Code zugeteilt. Auch diesen benötigt MeHR, bitte halten sie also für jedes Ihrer Zürcher Hotels den HoKo Code bereit.

# Installation

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/zv3GeBg5esw/0.jpg)](https://www.youtube.com/watch?v=zv3GeBg5esw)


## Erste Schritte

Ich habe MeHR in meiner Freizeit entwickelt und stelle es Ihnen frei zur Verfügung. Näheres entnehmen sie bitte der [Lizenz](LICENSE). Falls MeHR auf ihrem System nicht wie gewünscht funktionieren sollte können sie gerne über das [Ticketsystem](https://github.com/dneise/mehr/issues) Kontakt aufnehmen und fragen stellen.

Die Funktionalität von MeHR zu prüfen gehen wir bei der Installation Schrittweise vor.

Laden Sie nun bitte die aktuelle Version von MeHR hier herunter:
<https://github.com/dneise/MeHR/releases>

Die aktuelle Version ist [mehr_v0.4.3.exe](https://github.com/dneise/MeHR/releases/download/v0.4.3/mehr_v0.4.3.exe).

Sie finden die Datei nun vermutlich in Ihrem `Downloads` Ordner. Für den ersten Testbetrieb schlage ich vor diese exe-Datei in einen leeren Ordner zu verschieben, z.B. auf Ihrem Desktop.

Führen Sie nun bitte die Datei einmal aus, z.B. mit einem Doppelklick.
Es öffnet sich für sehr kurze Zeit ein Fenster und schliesst sich sofort wieder.
Dies ist normal, MeHR kann nicht ohne eine sog. Konfigurations Datei funktionieren. Fehlt diese Datei, reklamiert MeHR und erzeugt für Sie eine solche Konfigurations Datei, welche bereits mit einer Test-Konfiguration gefüllt ist. Der Name der Konfigurationsdatei lautet `config.json`.

Sie können die `config.json` Datei nun ansehen wenn sie möchten, aber wir kommen im nächsten Schritt noch darauf zu sprechen.

Starten Sie die die `mehr_v0.4.3.exe` nun noch einmal, wird ein Test-Meldeschein-Report erstellt.
Hierzu nimmt MeHR bereits Kontakt zu einem Mews Demo-Hotel auf und fragt ab, welche Gäste in diesem Demo-Hotel am 22.06.2018 eingecheckt haben. Dies diente als Test während der Entwicklung von MeHR und
dient Ihnen nun als kurze Bestätigung, dass MeHR auf ihrem System korrekt läuft und von Ihrem System aus mit Mews Kontakt aufnehmen kann.

Im nächsten Schritt werden wir MeHR nun für Ihr Hotel Konfigurieren.

Sie können den Test-Meldeschein-Report nun löschen.

Falls sie an dieser Stelle keinen Test-Meldeschein-Report sehen, funktioniert MeHR auf Ihrem System vermutlich nicht korrekt. Ich würde Sie an dieser Stelle bitten ein Ticket zu eröffnen und mir das Problem zu schildern.

## Konfiguration

Die Konfigurationsdatei `config.json` ist im sog. [JSON Format](https://de.wikipedia.org/wiki/JavaScript_Object_Notation#Beispiel) geschrieben. Dies ist ein Dateiformat, welches
sowohl maschinen- als auch menschenlesbar ist, so dass Sie die Konfiguration bequem durchführen,
aber auch das MeHR Programm ihre Einträge sicher und fehlerfrei versteht.

Falls sie einen Fehler in der Konfiguration machen und MeHR ihre Eingaben nicht versteht, wird es schlicht abbrechen und nicht mit fehlerhaften Einstellungen zu arbeiten beginnen.

Zur Konfiguration öffnen Sie bitte die `config.json` mit einem Text-Editor Ihrer Wahl. Das Programm "Notepad" ist unter Windows vorinstalliert und völlig ausreichend.

Sie sollten in Ihrer `config.json` in etwa diese Einträge sehen. Die Reihenfolge der Einträge ist nicht von belang.

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

Im Folgenden werde ich sie Anleiten, die Konfiguration entsprechend Ihrer Wünsche anzupassen.

### `OutFolder`

Zu Beginn steht hier der Pfad auf den Ordner in dem Sie MeHR zum erstem Mal gestartet haben. Tragen Sie hier bitte den Pfad ein, wo MeHR für Sie die Meldeschein-reports künftig ablegen soll.

Final sollte dies der Ordner sein, in dem der SiDAP-Client die reports erwaret. In einer Standardinstallation ist dies dieser Ordner:

```json
    "OutFolder": "C:\\SiDAP\\SiDAP-Client\\Upload\\Hoko"
```

Falls Sie allerdings zunächst Ihre MeHR reports ansehen wollen, bevor sie vom SiDAP-Client automatisch an die Hoko übermittelt werden, können Sie hier einen belieben Pfad eintragen, oder den Pfad einfach zunächst so lassen wie er ist.

### `TestMode` und `TestStartTime`

Diese Einträge sind für den ersten Tests notwendig. Wir werden noch einen
weiteren Test durchführen, für den diese Einträge notwendig sind. Danach können sie gelöscht werden.

### `HoursAfterMidnight`

Bitte tragen sie hier die Zeit ein, zu der der Bericht erstellt werden soll.
Voreingestellt ist `3` Uhr morgens.

### `ClientToken`

Bitte tragen sie hier, dass *ClientToken* ein, welches Ihnen von Mews (vermutlich per email) auf Ihre Anfrage hin zugesand wurde.

### `PlatformAddress`

Dieser Eintrag muss von Ihnen wie folgt eingestellt werden:

```json
    "PlatformAddress": "https://www.mews.li"
```

### `Hotels`

Dies ist eine Liste, zu erkennen an den beiden eckigen Klammern `[` und `]`.
In diese Liste können sie für alle Ihre Zürcher Hotels den `HoKoCode` und das `AccessToken` eintragen.
Zur besseren Übersicht ist es erlaubt weitere Felder wie z.B. `Name` hinzu zu fügen.

### Beispiel für Ihren ersten Test:

Am Ende könnte Ihre `config.json` so aussehen:
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

Bitte beachten sie die Kommasetzung. Alle Einträge sind durch Komma `,` zu trennen. Der letzte Eintrag einer Liste bekommt jedoch kein Komma am Ende.

Wenn Sie die `config.json` in etwa so wie hier beschrieben angepasst haben, ist
es Zeit für einen zweiten Testlauf. Speichern Sie die `config.json` und führen sie MeHR nocheinmal aus.
Wie werden nun jeweils eine Datei für jedes Ihrer Hotels am angegebenen Ort sehen.

Sie können sich nun anhand dieser Reports überzeugen, ob MeHR die Reports korreckt zusammenstellt.


## Dauerbetrieb

Nach dem obigen Test ist es an der Zeit MeHR dauerhaft laufen zu lassen.
Hierzu müssen sie lediglich die beiden Einträge namens `TestMode` und `TestStartTime` löschen, bzw. `TestMode`auf `false` sezen.

Nun haben sie prinzipiell zwei Möglichkeiten.

Starten Sie MeHR nun einfach mit einem Doppelklick, wird sich ein Fenster öffnen in welchem lediglich angezeigt wird, wann MeHR für Sie die nächsten Reports erstellen wird (z.B. am nächsten morgen um 3 Uhr).

Um MeHR nun für immer laufen zu lassen könnten sie dieses Fenster minimieren und an diesem PC dauerhaft eingeloggt bleiben und auf diese Weise MeHR im Hintergrund ausführen.

Angenehmer ist es aber, wenn kein Fenster dauerhaft geöffnet bleiben muss man sich ausloggen kann und MeHR trotzdem weiterläuft. Hierzu muss MeHR als sog. Dienst (engl. Service) installiert werden.

Hierzu empfehle ich das Programm [NSSM](<http://nssm.cc/release/nssm-2.24.zip>).

Die Einrichtung von MeHR als Dienst mit Hilfe von NSSM ist viel leichter in einem kleinen Video zu erklären als es hier im Text zu beschreiben. Daher würde ich Sie an dieser Stelle auf das unten stehende Video verweisen.


# [License](LICENSE)

This tool is both free of charge and open source, i.e. you can use it for your
hotel without paying me a dime and you can modify it as you like and even
distribute modified versions to your friends.
