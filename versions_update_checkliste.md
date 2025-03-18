Checkliste: Manuelles Update von MeHR

Ensprechend diesem Video:
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/JqLEYAoF7ro/0.jpg)](https://www.youtube.com/watch?v=JqLEYAoF7ro)


- [ ] **Vorbereitung**
    - [ ] Falls nicht geschehen: NSSM Herunterladen von https://nssm.cc/release/nssm-2.24.zip und die ZIP Datei entpacken
    - [ ] Neueste MeHR version herunterladen von https://github.com/dneise/MeHR/releases
- [ ] MeHR Dienst stoppen
   - via Win-Taste und "Dienste" gelangt man zum Windows Dienste Manager.
   - Bitte notieren sie sich den Namen, den sie bei der Installation des Dienstes gewählt haben. In meinem Fall: `MeHR`
- [ ] Neueste Version der `mehr_v???.exe` Datei an die Stelle verschiebe, an der bereits die alte EXE Datei liegt
   - Das ist in meinem Fall unter `C:\SiDAP\SiDAP-Client\Upload\MeHR` 
- [ ] Alte MeHR Version in einen "Backup Ordner" verschieben
    - [ ] Neuen Ordner namens `backup` erzeugen
    - [ ] Alte `mehr_v???.exe` in den Ordner `backup` verschieben
    - [ ] `stderr.txt` und `stdout.txt` in den Ordner `backup` verschieben
- [ ] NSSM benutzen um den MeHR Dienst zu editieren
   - [ ] Eingabeaufforderung starten
   - [ ] `cd` benutzen um in den Ordner zu gelangen in dem die `nssm.exe` Datei liegt. In meinem Fall:
        `cd Downloads\nssm-2.24\nssm-2.24\win32`
   - [ ] `nssm.exe edit MeHR` ausführen
   - [ ] Eventuelle Sicherheitsabfrage bestätigen
   - [ ] Im "NSSN Service Editor" unter "Application" im "Path" den richtigen Dateinamen eingeben.
- [ ] MeHR Dienst starten
   - via Win-Taste und "Dienste" gelangt man zum Windows Dienste Manager.
   - [ ] Dienst starten
   - [ ] Es sollten die beiden Textdateien `stdout.txt` und `stderr.txt` erscheinen, und in einer davon sollte zu sehen sein, dass MeHR den nächsten Durchlauf am nächsten Morgen um 3 Uhr geplant hat.

😃 Geschafft!
