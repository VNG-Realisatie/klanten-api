from django.test import TestCase

from ..constants import KlantType
from .factories import (
    KlantFactory,
    NatuurlijkPersoonFactory,
    NietNatuurlijkPersoonFactory,
    VestigingFactory,
)


class UniqueRepresentationTests(TestCase):
    def test_natuurlijk_persoon(self):
        klant = KlantFactory(subject_type=KlantType.natuurlijk_persoon, subject="")
        NatuurlijkPersoonFactory.create(klant=klant, inp_bsn="100000007")

        self.assertEqual(klant.unique_representation(), "natuurlijk_persoon: 100000007")

    def test_niet_natuurlijk_persoon(self):
        klant = KlantFactory(subject_type=KlantType.niet_natuurlijk_persoon, subject="")
        NietNatuurlijkPersoonFactory.create(klant=klant, inn_nnp_id="1234567")

        self.assertEqual(
            klant.unique_representation(), "niet_natuurlijk_persoon: 1234567"
        )

    def test_vestiging(self):
        klant = KlantFactory(subject_type=KlantType.vestiging, subject="")
        VestigingFactory.create(klant=klant, vestigings_nummer="1234")

        self.assertEqual(klant.unique_representation(), "vestiging: 1234")

    def test_subject_url(self):
        klant = KlantFactory(
            subject_type=KlantType.vestiging,
            subject="http://example.com/subjects/123456",
        )

        self.assertEqual(
            klant.unique_representation(),
            "vestiging: http://example.com/subjects/123456",
        )

    def test_no_subject(self):
        klant = KlantFactory(
            achternaam="Jackson",
            voornaam="Samuel",
            telefoonnummer="061234567",
            subject_type=KlantType.natuurlijk_persoon,
            subject="",
        )
        self.assertEqual(
            klant.unique_representation(),
            "natuurlijk_persoon: Jackson Samuel - 061234567",
        )
