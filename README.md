# Pysteroids

Tämä projekti sisältää kloonin klassisesta Asteroids-pelistä, jonka toteutan
Helsingin yliopiston kurssille _Aineopintojen harjoitustyö:
Ohjelmistotekniikka_. Peli on toteutettu Pythonilla ja Pygame-kirjastolla.

Peli lienee jossain muodossa useimmille tuttu, mutta kerrataan kuitenkin
lyhyesti pelin kuva. Peli on reaaliaikainen arcade-peli, jossa pelaaja ohjaa
avaruusalusta ja pyrkii selviytymään avaruudessa mahdollisimman pitkään tuhoten
samalla mahdollisimman monta asteroidia.

## Dokumentaatio

- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)

## Asennus ja suorittaminen

> [!NOTE]
> Peli vaatii Pythonin version 3.8 tai uudemman.

Asenna riippuvuudet komennolla

```
poetry install
```

Käynnistä tämän jälkeen peli komennolla

```
poetry run invoke start
```

## Muut komentorivitoiminnot

- Yksikkötestien ajaminen: `poetry run invoke test`
- Pylint-tarkistukset: `poetry run invoke lint`
- HTML-muotoisen testikattavuusraportin generoiminen: `poetry run invoke coverage-report`

## Lyhyt käyttöohje

Avaruusalusta käännetään nuolinäppäimillä, ja kiihdyttää voi ylänuolella. Ampua voi välilyönnillä. Pelin tavoitteena on tuhota mahdollisimman monta asteroidia ja selviytyä mahdollisimman pitkään.
