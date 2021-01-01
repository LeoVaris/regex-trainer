# regex-trainer

Harjoitustyön aihe oli toteuttaa web-sovellus, joka opettaa regexin syntaksia ja käytännön käyttötarkoituksia. 
Sovellus on toteutettu niin, että ohjeita ja tehtäviä on helppo lisätä hallintapaneelista. 
Sovellus tarkastaa palautukset automaattisesti, sekä antaa käyttäjälle palautetta vastauksesta. 
Ylläpitäjät näkevät kaikki palautukset ja voivat muokata tai poistaa tehtäviä/ohjeita. 

**Linkki sovellukseen:** [Regex-trainer](https://tsoha-regex-trainer.herokuapp.com).

Sovellus on toteutettu harjoitustyönä Helsingin yliopiston kurssille Tietokantasovellus.

## Käyttöohjeet

1. Luo käyttäjä 'rekisteröidy'-kohdasta. 
2. Siirry tehtäväsivulle
3. Ennen tehtävien tekoa, on hyvä lukea kaikki sitä ylempänä olevat ohjeet, niistä on hyötyä varsinkin alussa.
4. Tee tehtäviä ja katsoa tulokset, ne kertovat miten lausekkeesi toimi.

## Tekninen toteutus

Sovellus on toteutettu Pythonilla Flask-kirjastoa käyttäen. Viimeistellyssä versiossa ei ole tietääkseni bugeja. 
Opiskelija oikeuksilla käyttäjä pystyy katsomaan tilastoja, sekä palauttamaan tehtäviä ja katsomaan niiden tuloksia. 
Opiskelijalla ei ole mahdollisuutta saada haltuunsa hänelle kuulumatonta tietoa, eikä muokata muiden tietoja. 
Ylläpitäjillä ja opettajilla on mahdollisuus muokata tehtäviä ja lisätä uusia. Heillä on myös tietoisesti mahdollisuus moniin tietoturvaongelmiin, 
koska he voivat lähettää tietoa, jota ei tarkoituksella tarkisteta. Sovellus siis olettaa, että opettajat/ylläpitäjät eivät hyväksikäytä järjestelmää. 
Sovelluksen ulkoasua olisi hyvä parantaa, mutta kaikki tarvittava tieto on jo haettu palvelimelta. 
