<div lang = "nb_no">

`# lesemarkør finn

* NVDA -kompatibilitet: 2024.4 og utover.
* Last ned: [stabil versjon](https://github.com/emil-18/reviewcursorfind/releases/download/v1.2.2/reviewcursorfind-1.2.2.nvda-addon).

Dette tillegget legger til finn-funksjonalitet for lesemarkøren, som finn (NVDA+Control+F) gjør i nett modus. Du kan finne hvilken som helst tekst tilgjengelig med lesemarkør navigasjonskommandoene (numerisk 6, numerisk 9, og så vidre), før du opnet dialogen, For eksempel hvis lesemarkøren er i et dokument og du åpner dialogen, vil teksten i det dokumentet bli søkt etter
Du kan valgfritt bruke regulære uttrykk. [En veiledning om hva de er og hvordan de kan brukes finner du her.](https://coderpad.io/blog/development/the-complete-guide-to-regular-expressions-regex/)
Dette tillegget er spesielt nyttig i:

* Terminalprogrammer
* les skjerm
* Situasjoner der du vil søke etter tekst, men ikke vil flytte innsettingspunktet
* Situasjoner der programmet du bruker ikke implementerer sin egen søkefunksjonalitet

## Noen få merknader om støtte for regulære uttrykk

* På NVDA 2026.2 eller nyere vil den bruke regex-modulen. Dette lar deg bruke lookbehinds med strenger som ikke har fast lengde.
	Dette lar deg også bruke uklar søking. På tidligere NVDA-versjoner vil den falle tilbake til re-modulen
* Lookaheads og lookbehinds vil alltid være basert på den vanlige retningen til teksten, uansett om du bruker neste eller forrige søk.
	For eksempel, hvis du har strengen "asdf", og ditt regulære uttrykk er mellom s og d, vil en lookahead alltid peke Mot d og f.

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
* Støtt alle regulære uttrykk. Skru av hvis du opplever problemer med å bruke tillegget, for eksempel  hakking eller at lesemarkøren flytter til feil tekst:
	Når denne er krysset av, kan du pålitelig bruke regulære uttrykk som bruker kriterier som ikke er basert på den faktiske teksten det søkes etter, som lookaheads/lookbehinds, ordgrenser osv.
	Når det ikke er merket av, vil tillegget gå tilbake til sin gamle oppførsel. Dette får den til å finne den Ønskede strengen ved å bruke regex, og mate resultatet inn i NVDAs vanlige finn algoritme. Denne algoritmen bruker ikke regulært uttrykk.
	Denne innstillingen bør alltid være på, men du har muligheten til å slå den av i tilfelle.
* Si den funnede teksten, i stedet for linjen der lesemarkøren havner:
	Når denne er merket av, vil bare teksten du søkte etter bli lest opp. Dette kan være nyttig hvis du vil hoppe over gjentatt tekst.
	For eksempel, hvis du har en liste som alltid starter med samme streng, kan du lage et regulært uttrykk som fanger opp alt mellom forekomsten av denne strengen og den neste
* Flytt innsettingspunktet avkryssingsboks: Hvis denne er krysset av, flyttes innsettingspunktet med lesemarkøren når du søker

## forandringslog

### v1.2.2

* Når "Støtt alle regulæruttrykk" innstillingen er på, vil tillegget fungere i flere situasjoner

### v1.2.1

* Tillegget vil altid raportere "ikke funnet" når det ikke kan finne tekst



### v1.2

* Det er nå mulig å bruke alle regulære uttrykk
* Når du bruker NVDA 2026.2 eller nyere, vil regex-modulen bli brukt, i stedet for re

### v1.1.1

* Lagt til kompatibilitet med NVDA 2026.1
* flyttet tilleggs gestene til tekst lesnings kategorien i indatagester dialogen

### v1.1

* Lagt til funksjonen til å bruke regulært uttrykk når du søker.
* Lagt til finn gestene fra nettmodus i redigerbare kontroller.
* fikset en feil som noen ganger fikk NVDA til å lese hele søketeksten når du bruker les gjeldende tegn gesten etter et søk

### v1.0

* første utgivelse
</div>