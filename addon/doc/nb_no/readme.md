<div lang = "nb_no">
# lesemarkør finn

* NVDA -kompatibilitet: 2024.4 og utover.
* Last ned: [stabil versjon](https://github.com/emil-18/reviewcursorfind/releases/download/v1.1/reviewcursorfind-1.1.nvda-addon).

Dette tillegget legger til finn-funksjonalitet for lesemarkøren, som finn (NVDA+Control+F) gjør i nett modus. Du kan finne hvilken som helst tekst tilgjengelig med lesemarkør navigasjonskommandoene (numerisk 6, numerisk 9, og så vidre), før du opnet dialogen, For eksempel hvis lesemarkøren er i et dokument og du åpner dialogen, vil teksten i det dokumentet bli søkt etter

Dette tillegget er spesielt nyttig i:

* Terminalprogrammer
* les skjerm
* Situasjoner der du vil søke etter tekst, men ikke vil flytte innsettingspunktet
* Situasjoner der programmet du bruker ikke implementerer sin egen søkefunksjonalitet

## gester

* NVDA+Kontroll+skift+G: Finner en tekststreng fra lesemarkørposisjonen
* NVDA+G: Flytter lesemarkøren til neste forekomst av tidligere skrevet inn søketekst
* NVDA+SHIFT+G: Flytter lesemarkøren til forrige forekomst av tidligere skrevet inn søketekst

Hvis du er i en redigerbar kontroll (en kontroll der du kan navigere i teksten med piltastene), kan du bruke de normale Find -kommandoene du er vant til fra nettmodus.
NVDA+Kontroll+F for finn, NVDA+F3 for å finne neste, og NVDA+Shift+F3 for å finne tidligere. Disse gestene oppfører seg på samme måte som de globale gestene, bortsett fra at de vil flytte navigasjonsobjektet til objektet med fokus før de søker. Dette gjøres fordi det antas at du vil søke i objektet med fokus.

## Innstillinger:

Alle innstillingene er i finn dialogboksen for lesemarkør

* Skild mellom små og store bokstaver avkryssingsboks: Selvforklarende.
* Bruk regulært  uttrykk når du søker avkryssingsboks: Hvis denne er krysset av, vil tillegget søke ved å bruke regulært uttrykk. [En guide til hva de er og hvordan de kan brukes kan bli funnet her.](Https://coderpad.io/blog/development/the-complete-guide-to-regular-adressions-egex/)
* Flytt innsettingspunktet avkryssingsboks: Hvis denne er krysset av, flyttes innsettingspunktet med lesemarkøren når du søker

## forandringslog

### v1.1

* Lagt til funksjonen til å bruke regulært uttrykk når du søker.
* Lagt til finn gestene fra nettmodus i redigerbare kontroller.
* fikset en feil som noen ganger fikk NVDA til å lese hele søketeksten når du bruker les gjeldende tegn gesten etter et søk

### v1.0

* første utgivelse
</div>