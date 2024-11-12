import unittest
from maksukortti import Maksukortti


class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_luodulla_kortilla_pyydetty_saldo(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)

    def test_luodun_kortin_merkkijonoesitys_on_oikea(self):
        self.assertEqual(str(self.maksukortti),
                         "Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataaminen_lisaa_saldoa_pyydetyn_maaran(self):
        self.maksukortti.lataa_rahaa(350)
        self.assertEqual(self.maksukortti.saldo_euroina(), 13.5)

    def test_rahan_ottaminen_vahentaa_saldoa_pyydetyn_maaran(self):
        self.assertEqual(self.maksukortti.ota_rahaa(450), True)
        self.assertEqual(self.maksukortti.saldo_euroina(), 5.5)

    def test_rahan_ottaminen_ei_onnistu_jos_saldo_ei_riita(self):
        self.assertEqual(self.maksukortti.ota_rahaa(15000), False)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10)
