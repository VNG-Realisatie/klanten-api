from rest_framework import status
from rest_framework.test import APITestCase
from vng_api_common.tests import JWTAuthMixin, get_validation_errors, reverse

from klanten.datamodel.constants import KlantType, SoortRechtsvorm
from klanten.datamodel.models import Klant
from klanten.datamodel.tests.factories import (
    KlantAdresFactory,
    KlantFactory,
    NatuurlijkPersoonFactory,
    NietNatuurlijkPersoonFactory,
    SubVerblijfBuitenlandFactory,
    VerblijfsAdresFactory,
    VestigingFactory,
)

SUBJECT = "http://example.com/subject/1"


class KlantTests(JWTAuthMixin, APITestCase):
    heeft_alle_autorisaties = True
    maxDiff = None

    def test_list_klanten(self):
        list_url = reverse(Klant)
        KlantFactory.create_batch(2)

        response = self.client.get(list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)

    def test_read_klant_url(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.natuurlijk_persoon
        )
        KlantAdresFactory.create(klant=klant)
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.natuurlijk_persoon,
                "subjectIdentificatie": None,
            },
        )

    def test_read_klant_natuurlijkpersoon(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.natuurlijk_persoon
        )
        KlantAdresFactory.create(klant=klant)
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.natuurlijk_persoon,
                "subjectIdentificatie": {
                    "inpBsn": natuurlijkpersoon.inp_bsn,
                    "anpIdentificatie": natuurlijkpersoon.anp_identificatie,
                    "inpANummer": natuurlijkpersoon.inp_a_nummer,
                    "geslachtsnaam": natuurlijkpersoon.geslachtsnaam,
                    "voorvoegselGeslachtsnaam": natuurlijkpersoon.voorvoegsel_geslachtsnaam,
                    "voorletters": natuurlijkpersoon.voorletters,
                    "voornamen": natuurlijkpersoon.voornamen,
                    "geslachtsaanduiding": natuurlijkpersoon.geslachtsaanduiding,
                    "geboortedatum": natuurlijkpersoon.geboortedatum,
                    "verblijfsadres": {
                        "aoaIdentificatie": adres.aoa_identificatie,
                        "wplWoonplaatsNaam": adres.woonplaats_naam,
                        "gorOpenbareRuimteNaam": adres.gor_openbare_ruimte_naam,
                        "aoaPostcode": adres.postcode,
                        "aoaHuisnummer": adres.huisnummer,
                        "aoaHuisletter": adres.huisletter,
                        "aoaHuisnummertoevoeging": adres.huisnummertoevoeging,
                        "inpLocatiebeschrijving": adres.inp_locatiebeschrijving,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_read_klant_nietnatuurlijkpersoon(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.niet_natuurlijk_persoon
        )
        KlantAdresFactory.create(klant=klant)
        nietnatuurlijkpersoon = NietNatuurlijkPersoonFactory.create(klant=klant)
        buitenland = SubVerblijfBuitenlandFactory.create(
            nietnatuurlijkpersoon=nietnatuurlijkpersoon
        )
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.niet_natuurlijk_persoon,
                "subjectIdentificatie": {
                    "innNnpId": nietnatuurlijkpersoon.inn_nnp_id,
                    "annIdentificatie": nietnatuurlijkpersoon.ann_identificatie,
                    "statutaireNaam": nietnatuurlijkpersoon.statutaire_naam,
                    "innRechtsvorm": nietnatuurlijkpersoon.inn_rechtsvorm,
                    "bezoekadres": nietnatuurlijkpersoon.bezoekadres,
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_read_klant_vestiging(self):
        klant = KlantFactory.create(subject=SUBJECT, subject_type=KlantType.vestiging)
        KlantAdresFactory.create(klant=klant)
        vestiging = VestigingFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(vestiging=vestiging)
        buitenland = SubVerblijfBuitenlandFactory.create(vestiging=vestiging)
        detail_url = reverse(klant)

        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(
            data,
            {
                "url": f"http://testserver{detail_url}",
                "bronorganisatie": klant.bronorganisatie,
                "klantnummer": klant.klantnummer,
                "bedrijfsnaam": klant.bedrijfsnaam,
                "functie": klant.functie,
                "websiteUrl": klant.website_url,
                "voornaam": klant.voornaam,
                "voorvoegselAchternaam": klant.voorvoegsel_achternaam,
                "achternaam": klant.achternaam,
                "telefoonnummer": klant.telefoonnummer,
                "emailadres": klant.emailadres,
                "adres": {
                    "straatnaam": klant.adres.straatnaam,
                    "huisnummer": klant.adres.huisnummer,
                    "huisletter": klant.adres.huisletter,
                    "huisnummertoevoeging": klant.adres.huisnummertoevoeging,
                    "postcode": klant.adres.postcode,
                    "woonplaatsnaam": klant.adres.woonplaats_naam,
                    "landcode": klant.adres.landcode,
                },
                "subject": SUBJECT,
                "subjectType": KlantType.vestiging,
                "subjectIdentificatie": {
                    "vestigingsNummer": vestiging.vestigings_nummer,
                    "handelsnaam": vestiging.handelsnaam,
                    "verblijfsadres": {
                        "aoaIdentificatie": adres.aoa_identificatie,
                        "wplWoonplaatsNaam": adres.woonplaats_naam,
                        "gorOpenbareRuimteNaam": adres.gor_openbare_ruimte_naam,
                        "aoaPostcode": adres.postcode,
                        "aoaHuisnummer": adres.huisnummer,
                        "aoaHuisletter": adres.huisletter,
                        "aoaHuisnummertoevoeging": adres.huisnummertoevoeging,
                        "inpLocatiebeschrijving": adres.inp_locatiebeschrijving,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": buitenland.lnd_landcode,
                        "lndLandnaam": buitenland.lnd_landnaam,
                        "subAdresBuitenland1": buitenland.sub_adres_buitenland_1,
                        "subAdresBuitenland2": buitenland.sub_adres_buitenland_2,
                        "subAdresBuitenland3": buitenland.sub_adres_buitenland_3,
                    },
                },
            },
        )

    def test_create_klant_url(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Xavier",
            "achternaam": "Jackson",
            "emailadres": "test@gmail.com",
            "adres": {
                "straatnaam": "Keizersgracht",
                "huisnummer": "117",
                "huisletter": "A",
                "postcode": "1015CJ",
                "woonplaatsnaam": "test",
                "landcode": "1234",
            },
            "subjectType": KlantType.natuurlijk_persoon,
            "subject": SUBJECT,
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Xavier")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "test@gmail.com")
        self.assertEqual(klant.subject, SUBJECT)
        self.assertEqual(klant.adres.straatnaam, "Keizersgracht")

    def test_create_klant_natuurlijkpersoon(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "adres": {
                "straatnaam": "Keizersgracht",
                "huisnummer": 117,
                "huisletter": "A",
                "postcode": "1015CJ",
                "woonplaatsnaam": "test",
                "landcode": "1234",
            },
            "subjectType": KlantType.natuurlijk_persoon,
            "subjectIdentificatie": {
                "anpIdentificatie": "123",
                "geslachtsnaam": "Jackson2",
                "voornamen": "Samuel2",
                "geboortedatum": "1962-06-28",
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "East Meaganchester",
                    "gorOpenbareRuimteNaam": "New Amsterdam",
                    "aoaHuisnummer": 21,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.subject, "")
        self.assertEqual(klant.subject_type, KlantType.natuurlijk_persoon)

        klantadres = klant.adres

        self.assertEqual(klantadres.straatnaam, "Keizersgracht")
        self.assertEqual(klantadres.huisnummer, 117)
        self.assertEqual(klantadres.huisletter, "A")
        self.assertEqual(klantadres.postcode, "1015CJ")
        self.assertEqual(klantadres.woonplaats_naam, "test")
        self.assertEqual(klantadres.landcode, "1234")

        natuurlijkpersoon = klant.natuurlijk_persoon

        self.assertEqual(natuurlijkpersoon.anp_identificatie, "123")
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "Jackson2")
        self.assertEqual(natuurlijkpersoon.voornamen, "Samuel2")
        self.assertEqual(natuurlijkpersoon.geboortedatum, "1962-06-28")

        verblijfsadres = natuurlijkpersoon.verblijfsadres

        self.assertEqual(verblijfsadres.aoa_identificatie, "1234")
        self.assertEqual(verblijfsadres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(verblijfsadres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(verblijfsadres.huisnummer, 21)

        buitenland = natuurlijkpersoon.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_create_klant_nietnatuurlijkpersoon(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "subjectType": KlantType.niet_natuurlijk_persoon,
            "subjectIdentificatie": {
                "innNnpId": "314273268",
                "annIdentificatie": "",
                "statutaireNaam": "ACME",
                "innRechtsvorm": SoortRechtsvorm.europese_naamloze_vennootschap,
                "bezoekadres": "Somewhere",
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.subject, "")
        self.assertEqual(klant.subject_type, KlantType.niet_natuurlijk_persoon)

        nietnatuurlijkpersoon = klant.niet_natuurlijk_persoon

        self.assertEqual(nietnatuurlijkpersoon.inn_nnp_id, "314273268")
        self.assertEqual(nietnatuurlijkpersoon.ann_identificatie, "")
        self.assertEqual(nietnatuurlijkpersoon.statutaire_naam, "ACME")
        self.assertEqual(
            nietnatuurlijkpersoon.inn_rechtsvorm,
            SoortRechtsvorm.europese_naamloze_vennootschap,
        )
        self.assertEqual(nietnatuurlijkpersoon.bezoekadres, "Somewhere")

        buitenland = nietnatuurlijkpersoon.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_create_klant_vestiging(self):
        list_url = reverse(Klant)
        data = {
            "bronorganisatie": "950428139",
            "klantnummer": "1111",
            "websiteUrl": "http://some.website.com",
            "voornaam": "Samuel",
            "achternaam": "Jackson",
            "emailadres": "samuel@jackson.com",
            "subjectType": KlantType.vestiging,
            "subjectIdentificatie": {
                "vestigingsNummer": "123",
                "handelsnaam": ["WB"],
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "East Meaganchester",
                    "gorOpenbareRuimteNaam": "New Amsterdam",
                    "aoaHuisnummer": 21,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "ABCD",
                    "lndLandnaam": "Hollywood",
                },
            },
        }

        response = self.client.post(list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        klant = Klant.objects.get()

        self.assertEqual(klant.bronorganisatie, "950428139")
        self.assertEqual(klant.klantnummer, "1111")
        self.assertEqual(klant.website_url, "http://some.website.com")
        self.assertEqual(klant.voornaam, "Samuel")
        self.assertEqual(klant.achternaam, "Jackson")
        self.assertEqual(klant.emailadres, "samuel@jackson.com")
        self.assertEqual(klant.subject, "")
        self.assertEqual(klant.subject_type, KlantType.vestiging)

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_partial_update_klant_url(self):
        klant = KlantFactory.create(subject=SUBJECT, voornaam="old name")
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {"voornaam": "new name"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_partial_update_klant_naturlijkpersoon(self):
        klant = KlantFactory.create(
            subject_type=KlantType.natuurlijk_persoon, subject=SUBJECT
        )
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)

        data = {
            "voornaam": "New name",
            "subject": "",
            "subjectIdentificatie": {
                "geslachtsnaam": "New name2",
                "verblijfsadres": {
                    "aoaIdentificatie": "1234",
                    "wplWoonplaatsNaam": "New place",
                    "gorOpenbareRuimteNaam": "New place2",
                    "aoaHuisnummer": 1,
                },
                "subVerblijfBuitenland": {
                    "lndLandcode": "XXXX",
                    "lndLandnaam": "New land",
                },
            },
        }

        response = self.client.patch(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.subject, "")

        natuurlijkpersoon.refresh_from_db()
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "New name2")

        adres.refresh_from_db()
        self.assertEqual(adres.woonplaats_naam, "New place")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_partial_update_klant_vestiging(self):
        klant = KlantFactory.create(subject_type=KlantType.vestiging)
        detail_url = reverse(klant)

        response = self.client.patch(
            detail_url,
            {
                "subject": "",
                "subjectIdentificatie": {
                    "vestigingsNummer": "123",
                    "handelsnaam": ["WB"],
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "East Meaganchester",
                        "gorOpenbareRuimteNaam": "New Amsterdam",
                        "aoaHuisnummer": 21,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "ABCD",
                        "lndLandnaam": "Hollywood",
                    },
                },
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.subject, "")

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_partial_update_klant_subject_type_fail(self):
        klant = KlantFactory.create(
            subject=SUBJECT, subject_type=KlantType.natuurlijk_persoon
        )
        detail_url = reverse(klant)

        response = self.client.patch(detail_url, {"subjectType": KlantType.vestiging})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        validation_error = get_validation_errors(response, "subjectType")
        self.assertEqual(validation_error["code"], "wijzigen-niet-toegelaten")

    def test_update_klant_url(self):
        klant = KlantFactory.create(subject=SUBJECT, voornaam="old name")
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        del data["subjectIdentificatie"]
        data["voornaam"] = "new name"

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.voornaam, "new name")

    def test_update_klant_naturlijkpersoon(self):
        klant = KlantFactory.create(
            subject_type=KlantType.natuurlijk_persoon, subject=SUBJECT
        )
        natuurlijkpersoon = NatuurlijkPersoonFactory.create(klant=klant)
        adres = VerblijfsAdresFactory.create(natuurlijkpersoon=natuurlijkpersoon)
        buitenland = SubVerblijfBuitenlandFactory.create(
            natuurlijkpersoon=natuurlijkpersoon
        )
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        data.update(
            {
                "voornaam": "New name",
                "subject": "",
                "subjectIdentificatie": {
                    "geslachtsnaam": "New name2",
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "New place",
                        "gorOpenbareRuimteNaam": "New place2",
                        "aoaHuisnummer": 1,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "XXXX",
                        "lndLandnaam": "New land",
                    },
                },
            }
        )

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.subject, "")

        natuurlijkpersoon.refresh_from_db()
        self.assertEqual(natuurlijkpersoon.geslachtsnaam, "New name2")

        adres.refresh_from_db()
        self.assertEqual(adres.woonplaats_naam, "New place")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_update_klant_nietnaturlijkpersoon(self):
        klant = KlantFactory.create(
            subject_type=KlantType.niet_natuurlijk_persoon, subject=SUBJECT
        )
        nietnatuurlijkpersoon = NietNatuurlijkPersoonFactory.create(klant=klant)
        buitenland = SubVerblijfBuitenlandFactory.create(
            nietnatuurlijkpersoon=nietnatuurlijkpersoon
        )
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        data.update(
            {
                "voornaam": "New name",
                "subject": "",
                "subjectIdentificatie": {
                    "statutaireNaam": "New name2",
                    "subVerblijfBuitenland": {
                        "lndLandcode": "XXXX",
                        "lndLandnaam": "New land",
                    },
                },
            }
        )

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()
        self.assertEqual(klant.voornaam, "New name")
        self.assertEqual(klant.subject, "")

        nietnatuurlijkpersoon.refresh_from_db()
        self.assertEqual(nietnatuurlijkpersoon.statutaire_naam, "New name2")

        buitenland.refresh_from_db()
        self.assertEqual(buitenland.lnd_landnaam, "New land")

    def test_update_klant_vestiging(self):
        klant = KlantFactory.create(subject_type=KlantType.vestiging)
        detail_url = reverse(klant)
        data = self.client.get(detail_url).json()
        del data["url"]
        data.update(
            {
                "subject": "",
                "subjectIdentificatie": {
                    "vestigingsNummer": "123",
                    "handelsnaam": ["WB"],
                    "verblijfsadres": {
                        "aoaIdentificatie": "1234",
                        "wplWoonplaatsNaam": "East Meaganchester",
                        "gorOpenbareRuimteNaam": "New Amsterdam",
                        "aoaHuisnummer": 21,
                    },
                    "subVerblijfBuitenland": {
                        "lndLandcode": "ABCD",
                        "lndLandnaam": "Hollywood",
                    },
                },
            }
        )

        response = self.client.put(detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        klant.refresh_from_db()

        self.assertEqual(klant.subject, "")

        vestiging = klant.vestiging

        self.assertEqual(vestiging.vestigings_nummer, "123")
        self.assertEqual(vestiging.handelsnaam, ["WB"])

        adres = vestiging.verblijfsadres

        self.assertEqual(adres.aoa_identificatie, "1234")
        self.assertEqual(adres.woonplaats_naam, "East Meaganchester")
        self.assertEqual(adres.gor_openbare_ruimte_naam, "New Amsterdam")
        self.assertEqual(adres.huisnummer, 21)

        buitenland = vestiging.sub_verblijf_buitenland

        self.assertEqual(buitenland.lnd_landcode, "ABCD")
        self.assertEqual(buitenland.lnd_landnaam, "Hollywood")

    def test_destroy_klant(self):
        klant = KlantFactory.create()
        detail_url = reverse(klant)

        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Klant.objects.count(), 0)
