import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti


class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luodulla_kassapaatteella_oikea_saldo(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_luodulla_kassapaatteella_ei_myytyja_lounaita(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisella_myyty_edullinen_kasvattaa_saldoa_hinnan_verran(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.4)

    def test_kateisella_myyty_edullinen_palauttaa_vaihtorahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_kateisella_myyty_maukas_kasvattaa_saldoa_hinnan_verran(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004)

    def test_kateisella_myyty_maukas_palautee_vaihtorahan_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_myyty_lounas_rekisteroityy(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateisella_maksu_ei_onnistu_jos_ei_tarpeeksi_rahaa(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(100), 100)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_edullisen_lounaan_korttimaksu_onnistuu_jos_saldoa_tarpeeksi(self):
        kortti = Maksukortti(1000)
        self.assertEqual(
            self.kassapaate.syo_edullisesti_kortilla(kortti), True)
        self.assertEqual(kortti.saldo_euroina(), 7.6)

    def test_maukkaan_lounaan_korttimaksu_onnistuu_jos_saldoa_tarpeeksi(self):
        kortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(kortti), True)
        self.assertEqual(kortti.saldo_euroina(), 6)

    def test_kortilla_ei_voi_maksaa_jos_saldo_ei_riita(self):
        kortti = Maksukortti(100)
        self.assertEqual(
            self.kassapaate.syo_edullisesti_kortilla(kortti), False)
        self.assertEqual(kortti.saldo_euroina(), 1)
        self.assertEqual(
            self.kassapaate.syo_maukkaasti_kortilla(kortti), False)
        self.assertEqual(kortti.saldo_euroina(), 1)

    def test_kortilla_maksu_ei_muuta_kassan_rahamaaraa(self):
        kortti = Maksukortti(1000)
        self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_korttia_ladattaessa_kassan_rahamaara_kasvaa(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti, 500)
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1005)

    def test_korttia_ladattaessa_kortin_saldo_kasvaa(self):
        kortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(kortti, 500)
        self.assertEqual(kortti.saldo_euroina(), 15)
