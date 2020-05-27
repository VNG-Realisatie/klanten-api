import factory.fuzzy

from ..constants import KlantType, SoortRechtsvorm


class KlantFactory(factory.django.DjangoModelFactory):
    bronorganisatie = factory.Faker("ssn", locale="nl_NL")
    klantnummer = factory.Sequence(lambda n: f"{n}")
    website_url = factory.Faker("url")
    voornaam = factory.Faker("first_name")
    achternaam = factory.Faker("last_name")
    adres = factory.Faker("address")
    emailadres = factory.Faker("email")
    functie = factory.Faker("word")
    subject = factory.Faker("url")
    subject_type = factory.fuzzy.FuzzyChoice(KlantType.values)

    class Meta:
        model = "datamodel.Klant"


# klant factories
class NatuurlijkPersoonFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    anp_identificatie = factory.Sequence(lambda n: f"{n}")
    geslachtsnaam = factory.Faker("last_name")
    voornamen = factory.Faker("first_name")
    geboortedatum = factory.Faker("date")

    class Meta:
        model = "datamodel.NatuurlijkPersoon"


class NietNatuurlijkPersoonFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    inn_nnp_id = factory.Faker("ssn", locale="nl_NL")
    statutaire_naam = factory.Faker("word")
    inn_rechtsvorm = factory.fuzzy.FuzzyChoice(SoortRechtsvorm.values)
    bezoekadres = factory.Faker("address", locale="nl_NL")

    class Meta:
        model = "datamodel.NietNatuurlijkPersoon"


class VestigingFactory(factory.django.DjangoModelFactory):
    klant = factory.SubFactory(KlantFactory)
    vestigings_nummer = factory.Sequence(lambda n: f"{n}")
    handelsnaam = factory.List([factory.Faker("word")])

    class Meta:
        model = "datamodel.Vestiging"


# factories for nested objects
class SubVerblijfBuitenlandFactory(factory.django.DjangoModelFactory):
    natuurlijkpersoon = factory.SubFactory(NatuurlijkPersoonFactory)
    # nietnatuurlijkpersoon = factory.SubFactory(NietNatuurlijkPersoonFactory)
    # vestiging = factory.SubFactory(VestigingFactory)
    lnd_landcode = factory.fuzzy.FuzzyText(length=4)
    lnd_landnaam = factory.Faker("word")

    class Meta:
        model = "datamodel.SubVerblijfBuitenland"


class VerblijfsAdresFactory(factory.django.DjangoModelFactory):
    natuurlijkpersoon = factory.SubFactory(NatuurlijkPersoonFactory)
    # vestiging = factory.SubFactory(VestigingFactory)
    aoa_identificatie = factory.Sequence(lambda n: f"{n}")
    woonplaats_naam = factory.Faker("city")
    gor_openbare_ruimte_naam = factory.Faker("word")
    huisnummer = factory.fuzzy.FuzzyInteger(99999)

    class Meta:
        model = "datamodel.VerblijfsAdres"
