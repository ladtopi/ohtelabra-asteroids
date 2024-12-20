# Testausdokumentti

Ohjelman automaattiset testit sisältävät sekä puhtaita yksikkötestejä että
erilaisia integraatiotestejä. Testit on kirjoitettu käyttäen Pythonin
`unittest`-kirjastoa. Lisäksi ohjelmaa on luonnollisesti testattu runsain
manuaalisin testein, sillä pelin toiminnallisuuden kehittäminen mielekkääksi
vaatii joka tapauksessa myös paljon sen pelaamista.

## Automaattitestit

### Sovelluslogiikka

Itse pelitilan tilalle ja sen hallinnalle on kohtalaisen kattavat testit, joilla
on pyritty varmistamaan että peli toimii kuten pitää. Osa testeistä on puhtaita
yksikkötestejä: esimerkiksi objektien perusluokan `SpaceObject` testit
tarkistavat että objektit voivat pelin avaruudessa vain sallitulla tavalla. Osa
testeistä vuorostaan on integraatiotestejä: esimerkiksi `Game`-luokan testit mm.
testaavat, että asteroidien loputtua tapahtumajonoon laitetaan ajastettu eventti
jonka pohjalta uusi asteroidiaalto lopulta generoidaan.

### Tukiluokat

Sovelluksessa on joitain tukimoduuleja, kuten `cartesian`, joka auttaa
generoimaan satunnaisia koordinaatteja kauas pelaajan aluksesta. moduuli
`leaderboard` puolestaan sisältää `Leaderboard`-luokan, joka vastaa nimensä
mukaisesti pelaajien pisteiden tallentamisesta ja hakemisesta. Näillekin on
kirjoitettu testit, ensimmäiselle nämä ovat perinteisiä puhtaita yksikkötestejä
ja jälkimmäiselle integraatiotestejä, jotka kirjoittavat testitietokantaan.

### Järjestelmätestaus

Järjestelmätestaus on käytännössä toteutettu manuaalisesti. Pelinäkymille ei
myöskään ole automaattisia testejä, vaan niiden testaus on tapahtunut osana
järjestelmätestausta, käytännössä pelaamalla peliä.

## Testikattavuus

Testikattavuuden mittaamiseen on käytetty Pythonin `coverage`-kirjastoa. HTML-muotoisen kattavuusraportin voi generoida komennolla `poetry run inv cov`, joka myös automaattisesti avaa luodun raportin selaimeen.

Kattavuusraportti on hyvä, mutta ei täydellinen. Alla raportti nykyisestä tilanteesta:

```
Name                       Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/cartesian.py              17      0      4      0   100%
src/collisions.py              4      1      0      0    75%   6
src/config.py                  9      0      0      0   100%
src/core/__init__.py           4      0      0      0   100%
src/core/asteroid.py          23      0      4      0   100%
src/core/bullet.py            18      1      4      1    91%   32
src/core/game.py             110      9     32      6    89%   86, 90, 100->104, 116, 122, 153, 170-171, 175-176
src/core/ship.py              44      0     10      0   100%
src/core/space_object.py      82      0     40      0   100%
src/db.py                     17      1      0      0    94%   31
src/events.py                 10      3      0      0    70%   10, 13, 16
src/graphics/__init__.py       2      0      0      0   100%
src/graphics/colors.py         4      0      0      0   100%
src/graphics/text.py          35     17      6      1    46%   22->exit, 30-36, 40-42, 46-48, 52-53, 57-58
src/keyboard.py                4      1      0      0    75%   6
src/leaderboard.py            13      0      2      0   100%
src/loop.py                   47      0     16      1    98%   14->exit
src/pysteroids.py             26     26      0      0     0%   1-41
src/view/__init__.py           6      0      0      0   100%
src/view/base.py              15      0      0      0   100%
src/view/game_over.py         24     14      8      0    31%   14-15, 18-23, 26-35
src/view/menu.py              24     13      8      0    34%   14-15, 18-21, 24, 27-34
src/view/playing.py           52     34     22      0    24%   15-16, 19, 22-33, 36-41, 44-46, 49-54, 57, 61, 66, 70
src/view/state.py              6      0      0      0   100%
src/view/submit_score.py      33     18      8      0    37%   17-20, 29-34, 37, 40-47, 50-53
----------------------------------------------------------------------
TOTAL                        629    138    164      9    75%
```

Kuten näkyy, pelin ytimestä suurin osa on testattu, mutta varsinkaan näkymätason
toiminnallisuutta ei automaattisissa testeissä juuri testata. Toisaalta, tämä ei
kai tällä kurssilla ollut tarpeenkaan, joten jos nämä tiputtaisi raportista
kokonaan pois niin kokonaiskattavuus olisi vielä parempi.
