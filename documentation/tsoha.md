# Tsoha-arvostelun kannalta tärkeitä asioita

* Tauluja on yhteensä neljä, joista yksi on monesta moneen.
* Accounts ja Rooms-taulujen sisältöä voi muokata suoraan UI:sta, muttei poistaa. Accounts-tauluun on erillinen Hidden-attribuutti jonka avulla käyttäjä voidaan disabloida, "poistaa käytöstä".
* Events-tauluun tapahtumien poistaminen on kuitenkin kehitetty, ja se poistaa oikeat tietokantakohdat myös liitostaulusta. Täydellistä CRUDia ei yksittäisessä taulussa ole, mutta kaikki oppimisen kannalta tärkeät osat on toteutettu.
* Events-taulussa oli myös tapahtumien editointi, mutta siihen viittaava linkki otettiin pois esiltä. Syy löytyy koodista application/calendar/events/views.py. 
* Sovelluksessa "rekisteröityminen" tapahtuu Adminin toimesta, ideana että vain admin hallinnoi käyttäjiä, myös uusia. Kirjautuminen toimii kuten pitääkin. Autorisointi toimii kuten pitääkin.
* Heroku on kasassa.

Lisää tietoa löytyy dokumentaatiosta.
