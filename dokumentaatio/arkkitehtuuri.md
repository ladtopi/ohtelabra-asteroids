# Arkkitehtuurikuvaus

Pelin korkean tason arkkitehtuurikaavio on jotakuinkin seuraava. Pelin pääluokka
`Game` (jota tosin toistaiseksi sijaistaa pääohjelman koodi) hallinnoi pelin
tilaa `GameState` ja pelin näkymää `GameView`, joista ensimmäinen ylläpitää
pelin logiikkaa (yhdessä pelissä olevien objektien kanssa) ja jälkimmäinen
hoitaa pelin piirtämisen näytölle. Esimerkiksi pakkausjako muotoutuu projektin
edetessä, ja peliin saattaa tulla myös lisää objekteja. Korkean tason idea
kuitenkin on tämä.

```mermaid
---
  config:
    class:
      hideEmptyMembersBox: true
---

classDiagram
    class Game
    class GameState
    class GameView
    class GameObject
    class Ship
    class Asteroid
    class Bullet

    Game ..> GameState
    Game ..> GameView
    GameView ..> GameState
    GameState --> "*" GameObject: manages

    GameObject <|-- Ship: inherits
    GameObject <|-- Asteroid: inherits
    GameObject <|-- Bullet: inherits
```

## Päätoiminnallisuus

Pelin päätoiminnallisuus on käytännössä pelilogiikan hallinta, ja siitä
seuraavan tilan piirtäminen kääyttäjälle. Jälkimmäisessä raskaan työn tekee `pygame`.

Pelin suoritus etenee niin, että pääohjelma alustaa `pygame`-instanssin, ja luo
sen jälkeen joukon olioita (GameState, GameRenderer, GameLoop), jotka
hallinnoivat pelin suoritusta, eli pelin tilan hallintaa ja ruudunpäivitystä.

Alla kuvattuna pääpiirteittäin sekvenssi siitä, miten käyttäjän antama
komento kääntää laivaa myötäpäivään käytännössä toteutuu.

```mermaid
sequenceDiagram
    actor User
    participant game program
    participant GameLoop
    participant Keyboard
    participant GameState
    participant GameRenderer
    participant pygame

    User ->> game program: press right key
    game program ->> pygame: register key press
    GameLoop ->> Keyboard: is_pressed(RIGHT_KEY)
    activate GameLoop
    activate Keyboard

    Keyboard ->> pygame: key.get_pressed()
    pygame ->> Keyboard: "{K_RIGHT: ...}
    Keyboard ->> GameLoop: True
    deactivate Keyboard
    GameLoop ->> GameState: ship_rotate_right()
    activate GameState
    GameState ->> Ship: rotate_right()
    deactivate GameState
    GameLoop ->> GameRenderer: render(state)
    activate GameRenderer
    GameRenderer ->> pygame: display.flip()
    deactivate GameRenderer
    pygame ->> game program: render new frame
    deactivate GameLoop
    game program ->> User: new frame
```
