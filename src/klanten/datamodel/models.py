import uuid

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from vng_api_common.fields import BSNField, RSINField
from vng_api_common.models import APIMixin

from .constants import GeslachtsAanduiding, KlantType, SoortRechtsvorm


class Klant(APIMixin, models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, help_text="Unieke resource identifier (UUID4)"
    )
    voornaam = models.CharField(
        max_length=200,
        blank=True,
        help_text="De voornaam, voorletters of roepnaam van de klant.",
    )
    achternaam = models.CharField(
        max_length=200, blank=True, help_text="De achternaam van de klant."
    )
    adres = models.CharField(
        max_length=1000, blank=True, help_text="Het adres van de klant."
    )
    functie = models.CharField(
        max_length=200, blank=True, help_text="De functie van de klant."
    )
    telefoonnummer = models.CharField(
        max_length=20,
        blank=True,
        help_text="Het mobiele of vaste telefoonnummer van de klant.",
    )
    emailadres = models.EmailField(
        blank=True, help_text="Het e-mail adres van de klant."
    )
    subject = models.URLField(
        help_text="URL-referentie naar een subject", max_length=1000, blank=True
    )
    subject_type = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        choices=KlantType.choices,
        help_text="Type van de `subject`.",
    )

    class Meta:
        verbose_name = "klant"
        verbose_name_plural = "klanten"

    @property
    def subject_identificatie(self):
        if hasattr(self, self.subject_type):
            return getattr(self, self.subject_type)
        return None


class NatuurlijkPersoon(models.Model):
    klant = models.OneToOneField(
        "datamodel.Klant", on_delete=models.CASCADE, related_name="natuurlijk_persoon"
    )

    inp_bsn = BSNField(
        blank=True,
        help_text="Het burgerservicenummer, bedoeld in artikel 1.1 van de Wet algemene bepalingen burgerservicenummer.",
    )
    anp_identificatie = models.CharField(
        max_length=17,
        blank=True,
        help_text="Het door de gemeente uitgegeven unieke nummer voor een ANDER NATUURLIJK PERSOON",
    )
    inp_a_nummer = models.CharField(
        max_length=10,
        blank=True,
        help_text="Het administratienummer van de persoon, bedoeld in de Wet BRP",
        validators=[
            RegexValidator(
                regex=r"^[1-9][0-9]{9}$",
                message=_("inpA_nummer must consist of 10 digits"),
                code="a-nummer-incorrect-format",
            )
        ],
    )
    geslachtsnaam = models.CharField(
        max_length=200, blank=True, help_text="De stam van de geslachtsnaam."
    )
    voorvoegsel_geslachtsnaam = models.CharField(max_length=80, blank=True)
    voorletters = models.CharField(
        max_length=20,
        blank=True,
        help_text="De verzameling letters die gevormd wordt door de eerste letter van "
        "alle in volgorde voorkomende voornamen.",
    )
    voornamen = models.CharField(
        max_length=200,
        blank=True,
        help_text="Voornamen bij de naam die de persoon wenst te voeren.",
    )
    geslachtsaanduiding = models.CharField(
        max_length=1,
        blank=True,
        help_text="Een aanduiding die aangeeft of de persoon een man of een vrouw is, "
        "of dat het geslacht nog onbekend is.",
        choices=GeslachtsAanduiding.choices,
    )
    geboortedatum = models.CharField(max_length=18, blank=True)

    class Meta:
        verbose_name = "natuurlijk persoon"


class NietNatuurlijkPersoon(models.Model):
    klant = models.OneToOneField(
        "datamodel.Klant",
        on_delete=models.CASCADE,
        related_name="niet_natuurlijk_persoon",
    )

    inn_nnp_id = RSINField(
        blank=True,
        help_text="Het door een kamer toegekend uniek nummer voor de INGESCHREVEN NIET-NATUURLIJK PERSOON",
    )

    ann_identificatie = models.CharField(
        max_length=17,
        blank=True,
        help_text="Het door de gemeente uitgegeven unieke nummer voor een ANDER NIET-NATUURLIJK PERSOON",
    )

    statutaire_naam = models.TextField(
        max_length=500,
        blank=True,
        help_text="Naam van de niet-natuurlijke persoon zoals deze is vastgelegd in de statuten (rechtspersoon) of "
        "in de vennootschapsovereenkomst is overeengekomen (Vennootschap onder firma of Commanditaire "
        "vennootschap).",
    )

    inn_rechtsvorm = models.CharField(
        max_length=50,
        choices=SoortRechtsvorm.choices,
        blank=True,
        help_text="De juridische vorm van de NIET-NATUURLIJK PERSOON.",
    )
    bezoekadres = models.CharField(
        max_length=1000,
        blank=True,
        help_text="De gegevens over het adres van de NIET-NATUURLIJK PERSOON",
    )

    class Meta:
        verbose_name = "niet-natuurlijk persoon"


class Vestiging(models.Model):
    """
    Een gebouw of complex van gebouwen waar duurzame uitoefening van de activiteiten
    van een onderneming of rechtspersoon plaatsvindt.
    """

    klant = models.OneToOneField("datamodel.Klant", on_delete=models.CASCADE)

    vestigings_nummer = models.CharField(
        max_length=24,
        blank=True,
        help_text="Een korte unieke aanduiding van de Vestiging.",
    )
    handelsnaam = ArrayField(
        models.TextField(max_length=625, blank=True),
        default=list,
        help_text="De naam van de vestiging waaronder gehandeld wordt.",
    )

    class Meta:
        verbose_name = "vestiging"


# models for nested objects
class SubVerblijfBuitenland(models.Model):
    """
    Datamodel afwijking, model representatie van de Groepattribuutsoort 'Verblijf buitenland'
    """

    natuurlijkpersoon = models.OneToOneField(
        NatuurlijkPersoon,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_verblijf_buitenland",
    )
    nietnatuurlijkpersoon = models.OneToOneField(
        NietNatuurlijkPersoon,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_verblijf_buitenland",
    )
    vestiging = models.OneToOneField(
        Vestiging,
        on_delete=models.CASCADE,
        null=True,
        related_name="sub_verblijf_buitenland",
    )
    lnd_landcode = models.CharField(
        max_length=4,
        help_text="De code, behorende bij de landnaam, zoals opgenomen in de Land/Gebied-tabel van de BRP.",
    )
    lnd_landnaam = models.CharField(
        max_length=40,
        help_text="De naam van het land, zoals opgenomen in de Land/Gebied-tabel van de BRP.",
    )
    sub_adres_buitenland_1 = models.CharField(max_length=35, blank=True)
    sub_adres_buitenland_2 = models.CharField(max_length=35, blank=True)
    sub_adres_buitenland_3 = models.CharField(max_length=35, blank=True)

    def clean(self):
        super().clean()
        if (
            self.natuurlijkpersoon is None
            and self.nietnatuurlijkpersoon is None
            and self.vestiging is None
        ):
            raise ValidationError(
                "Relations to NatuurlijkPersoon, NietNatuurlijkPersoon or Vestiging "
                "models should be set"
            )


class Adres(models.Model):
    natuurlijkpersoon = models.OneToOneField(
        "datamodel.NatuurlijkPersoon",
        on_delete=models.CASCADE,
        null=True,
        related_name="verblijfsadres",
    )
    vestiging = models.OneToOneField(
        "datamodel.Vestiging",
        on_delete=models.CASCADE,
        null=True,
        related_name="verblijfsadres",
    )
    aoa_identificatie = models.CharField(
        max_length=100, help_text="De unieke identificatie van het OBJECT"
    )
    wpl_woonplaats_naam = models.CharField(max_length=80)
    gor_openbare_ruimte_naam = models.CharField(
        max_length=80,
        help_text="Een door het bevoegde gemeentelijke orgaan aan een "
        "OPENBARE RUIMTE toegekende benaming",
    )
    aoa_huisnummer = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    aoa_huisletter = models.CharField(max_length=1, blank=True)
    aoa_huisnummertoevoeging = models.CharField(max_length=4, blank=True)
    aoa_postcode = models.CharField(max_length=7, blank=True)
    inp_locatiebeschrijving = models.CharField(max_length=1000, blank=True)

    def clean(self):
        super().clean()
        if self.natuurlijkpersoon is None and self.vestiging is None:
            raise ValidationError(
                "Relations to NatuurlijkPersoon or Vestiging models should be set"
            )
