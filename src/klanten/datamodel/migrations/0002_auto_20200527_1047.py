# Generated by Django 2.2.11 on 2020-05-27 10:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import vng_api_common.fields


class Migration(migrations.Migration):

    dependencies = [
        ("datamodel", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="Adres", new_name="KlantAdres"),
        migrations.CreateModel(
            name="VerblijfsAdres",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("woonplaats_naam", models.CharField(max_length=80)),
                (
                    "huisnummer",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(99999)]
                    ),
                ),
                ("huisletter", models.CharField(blank=True, max_length=1)),
                ("huisnummertoevoeging", models.CharField(blank=True, max_length=4)),
                ("postcode", models.CharField(blank=True, max_length=7)),
                (
                    "aoa_identificatie",
                    models.CharField(
                        help_text="De unieke identificatie van het OBJECT",
                        max_length=100,
                    ),
                ),
                (
                    "gor_openbare_ruimte_naam",
                    models.CharField(
                        help_text="Een door het bevoegde gemeentelijke orgaan aan een OPENBARE RUIMTE toegekende benaming",
                        max_length=80,
                    ),
                ),
                (
                    "inp_locatiebeschrijving",
                    models.CharField(blank=True, max_length=1000),
                ),
                (
                    "natuurlijkpersoon",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="verblijfsadres",
                        to="datamodel.NatuurlijkPersoon",
                    ),
                ),
                (
                    "vestiging",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="verblijfsadres",
                        to="datamodel.Vestiging",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.AddField(
            model_name="klant",
            name="bedrijfsnaam",
            field=models.CharField(
                blank=True, help_text="De bedrijfsnaam van de klant.", max_length=200
            ),
        ),
        migrations.AddField(
            model_name="klant",
            name="bronorganisatie",
            field=vng_api_common.fields.RSINField(
                default="",
                help_text="Het RSIN van de Niet-natuurlijk persoon zijnde de organisatie die de klant heeft gecreeerd. Dit moet een geldig RSIN zijn van 9 nummers en voldoen aan https://nl.wikipedia.org/wiki/Burgerservicenummer#11-proef",
                max_length=9,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="klant",
            name="klantnummer",
            field=models.CharField(
                default="",
                help_text="De unieke identificatie van de klant binnen de bronorganisatie.",
                max_length=8,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="klant",
            name="voorvoegsel_achternaam",
            field=models.CharField(
                blank=True,
                help_text="Het voorvoegsel van de achternaam van de klant.",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="klant",
            name="website_url",
            field=models.URLField(
                default="",
                help_text="Het label of etiket dat aan de specifieke informatiebron, zoals een webpagina, een bestand of een plaatje op internet is toegewezen waar de KLANT in de regel op het internet vindbaar is.",
                max_length=1000,
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="klant", unique_together={("bronorganisatie", "klantnummer")},
        ),
        migrations.AddField(
            model_name="klantadres",
            name="klant",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="datamodel.Klant"
            ),
        ),
    ]