# Imgur Foto Viewer

## Beschrijving
Dit project biedt een eenvoudige manier om foto's van Imgur op te halen en op te slaan in een lokale database. Gebruikers kunnen vervolgens deze foto's online bekijken. Het bestaat uit twee hoofdonderdelen: een Python-script dat foto's van Imgur haalt en ze in een database opslaat, en een webapplicatie waarmee gebruikers de opgeslagen foto's kunnen doorbladeren.

## Bestanden
- `script.py`: Haalt foto's van Imgur op en slaat deze op in de database.
- `website.py`: Webapplicatie waar gebruikers de foto's kunnen bekijken.

## Installatie
Om dit project te gebruiken, volg je de volgende stappen:

```bash
git clone https://github.com/jouwgebruikersnaam/imgur-foto-viewer.git
cd imgur-foto-viewer
pip install -r requirements.txt

```

## Gebruik
Na installatie kunt u het project als volgt gebruiken:
- Voer `script.py` uit om foto's van Imgur op te halen en op te slaan in de database.
- Start `website.py` om de webinterface te openen waar gebruikers de foto's kunnen bekijken.

## Bijdragen
Bijdragen aan dit project zijn welkom. Om bij te dragen, fork de repository, maak je wijzigingen, en stuur een pull request. Alle bijdragen moeten in overeenstemming zijn met de projectrichtlijnen.

## Licentie
Dit project is gelicenseerd onder de [MIT License](LICENSE).

## Contact
Voor vragen of ondersteuning, neem contact op via [jouwemail@example.com](mailto:jouwemail@example.com).



CREATE TABLE imgur_photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    date_added DATE NOT NULL
);