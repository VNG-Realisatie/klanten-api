# Resources

Dit document beschrijft de (RGBZ-)objecttypen die als resources ontsloten
worden met de beschikbare attributen.


## Klant

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/klant)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| url | URL-referentie naar dit object. Dit is de unieke identificatie en locatie van dit object. | string | nee | ~~C~~​R​~~U~~​~~D~~ |
| voornaam | De voornaam, voorletters of roepnaam van de klant. | string | nee | C​R​U​D |
| achternaam | De achternaam van de klant. | string | nee | C​R​U​D |
| adres | Het adres van de klant. | string | nee | C​R​U​D |
| telefoonnummer | Het mobiele of vaste telefoonnummer van de klant. | string | nee | C​R​U​D |
| emailadres | Het e-mail adres van de klant. | string | nee | C​R​U​D |
| functie | De functie van de klant. | string | nee | C​R​U​D |
| subject | URL-referentie naar een subject | string | nee | C​R​U​D |
| subjectType | Type van de `subject`.

Uitleg bij mogelijke waarden:

* `natuurlijk_persoon` - Natuurlijk persoon
* `niet_natuurlijk_persoon` - Niet-natuurlijk persoon
* `vestiging` - Vestiging | string | nee | C​R​U​D |

## SubVerblijfBuitenland

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/subverblijfbuitenland)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| lndLandcode | De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | ja | C​R​U​D |
| lndLandnaam | De naam van het land, zoals opgenomen in de Land/Gebied-tabel van de BRP. | string | ja | C​R​U​D |
| subAdresBuitenland1 |  | string | nee | C​R​U​D |
| subAdresBuitenland2 |  | string | nee | C​R​U​D |
| subAdresBuitenland3 |  | string | nee | C​R​U​D |

## NatuurlijkPersoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/natuurlijkpersoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| inpBsn | Het burgerservicenummer, bedoeld in artikel 1.1 van de Wet algemene bepalingen burgerservicenummer. | string | nee | C​R​U​D |
| anpIdentificatie | Het door de gemeente uitgegeven unieke nummer voor een ANDER NATUURLIJK PERSOON | string | nee | C​R​U​D |
| inpANummer | Het administratienummer van de persoon, bedoeld in de Wet BRP | string | nee | C​R​U​D |
| geslachtsnaam | De stam van de geslachtsnaam. | string | nee | C​R​U​D |
| voorvoegselGeslachtsnaam |  | string | nee | C​R​U​D |
| voorletters | De verzameling letters die gevormd wordt door de eerste letter van alle in volgorde voorkomende voornamen. | string | nee | C​R​U​D |
| voornamen | Voornamen bij de naam die de persoon wenst te voeren. | string | nee | C​R​U​D |
| geslachtsaanduiding | Een aanduiding die aangeeft of de persoon een man of een vrouw is, of dat het geslacht nog onbekend is.

Uitleg bij mogelijke waarden:

* `m` - Man
* `v` - Vrouw
* `o` - Onbekend | string | nee | C​R​U​D |
| geboortedatum |  | string | nee | C​R​U​D |

## NietNatuurlijkPersoon

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/nietnatuurlijkpersoon)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| innNnpId | Het door een kamer toegekend uniek nummer voor de INGESCHREVEN NIET-NATUURLIJK PERSOON | string | nee | C​R​U​D |
| annIdentificatie | Het door de gemeente uitgegeven unieke nummer voor een ANDER NIET-NATUURLIJK PERSOON | string | nee | C​R​U​D |
| statutaireNaam | Naam van de niet-natuurlijke persoon zoals deze is vastgelegd in de statuten (rechtspersoon) of in de vennootschapsovereenkomst is overeengekomen (Vennootschap onder firma of Commanditaire vennootschap). | string | nee | C​R​U​D |
| innRechtsvorm | De juridische vorm van de NIET-NATUURLIJK PERSOON. | string | nee | C​R​U​D |
| bezoekadres | De gegevens over het adres van de NIET-NATUURLIJK PERSOON | string | nee | C​R​U​D |

## Vestiging

Objecttype op [GEMMA Online](https://www.gemmaonline.nl/index.php/Rgbz_1.0/doc/objecttype/vestiging)

| Attribuut | Omschrijving | Type | Verplicht | CRUD* |
| --- | --- | --- | --- | --- |
| vestigingsNummer | Een korte unieke aanduiding van de Vestiging. | string | nee | C​R​U​D |
| handelsnaam | De naam van de vestiging waaronder gehandeld wordt. | array | nee | C​R​U​D |


* Create, Read, Update, Delete
