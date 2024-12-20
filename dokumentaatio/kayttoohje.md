# Käyttöohje

Avaruusalusta käännetään nuolinäppäimillä, ja kiihdyttää voi ylänuolella. Ampua voi välilyönnillä. Pelin tavoitteena on tuhota mahdollisimman monta asteroidia ja selviytyä mahdollisimman pitkään.

## Asennus ja suorittaminen

> [!NOTE]
> Peli vaatii Pythonin version 3.8 tai uudemman.

Voit kloonata joko kloonata tämän repositorion tai ladata pelin lähdekoodin zip-tiedostona viimeisimmän [releasen](https://github.com/ladtopi/ohtelabra-asteroids/releases) kautta.

Asenna riippuvuudet komennolla

```
poetry install
```

Käynnistä tämän jälkeen peli komennolla

```
poetry run invoke start
```

## Pelin lyhyt käyttöohje

Avaruusalusta käännetään nuolinäppäimillä, ja kiihdyttää voi ylänuolella. Ampua
voi välilyönnillä. Kun olet tuhonnut asteroidiaallon, peli generoi
automaattisesti uuden. Pelin tavoitteena on tuhota mahdollisimman monta
asteroidia ja selviytyä mahdollisimman pitkään. Onnea ja menestystä!

> [!TIP]
> Pelistä voi poistua joko sulkemalla ikkunan, tai painamalla `ESC`-näppäintä.

## Konfigurointi

Peli tukee joitain konfiguraatioasetuksia. Näitä voi muuttaa ympäristömuuttujilla.

Esimerkiksi käynnistämällä pelin seuraavasti saat leveämmän ikkunan.

```
WINDOW_WIDTH=1024 poetry run invoke start
```

Kaikki optiot ovat seuraavat:

- `WINDOW_WIDTH` - ikkunan leveys pikseleinä
- `WINDOW_HEIGHT` - ikkunan korkeus pikseleinä
- `INITIAL_WAVE_SIZE` - ensimmäisen asteroidiaallon koko
- `SHIP_MAX_SPEEd` - pelaajan aluksen maksiminopeus
- `SHIP_BULLETS` - yksittäisen aluksen ammusten määrä
