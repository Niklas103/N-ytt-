# Models kuvastaa tietokannan rakennetta. Kun modelit on tehty annetaan migraatio komento, jolloin tietokanta tulee luoduksi.

# Django databasesta importataan modelit
from django.db import models

# Model on djangon database tyyppinen model luokka
class Toimittaja(models.Model):
    yritysnimi = models.CharField(max_length = 50, default="yritysnimi")
    yhteyshenkilö = models.CharField(max_length = 50, default="yhteyshenkilö")
    osoite = models.CharField(max_length = 100, default="osoite")
    puhelin = models.CharField(max_length = 20, default="puhelin")
    sähköposti = models.CharField(max_length = 50, default="sähköposti")
    maa = models.CharField(max_length = 50, default="maa")
    # ao:n voi tehdä jos haluaa että admin sivu toimii myöhemmässä vaiheessa paremmin,
    # mutta se ei ole välttämätöntä alussa
    def __str__(self):
        return f"{self.yritysnimi} from {self.maa}"


class Tuote(models.Model):
    tuotenimi = models.CharField(max_length = 20, default = "tuotenimi")
    painoperkappale = models.CharField(max_length = 20, default = 3)
    kappalehinta = models.DecimalField(max_digits=8, decimal_places=2, default=1.00)
    tuotteitavarastossa = models.IntegerField(default = 3)
    toimittaja = models.ForeignKey(Toimittaja, on_delete=models.CASCADE, default=1)  # Oletusarvo lisätty tähän
     # ao:n voi tehdä jos haluaa että admin sivu toimii myöhemmässä vaiheessa hienommin,
     # mutta se ei ole välttämätöntä alussa
    def __str__(self):
        return f"{self.tuotenimi} produced by {self.toimittaja.yritysnimi}"
    
class Varasto(models.Model):
    tuotenimi = models.CharField(max_length=20)
    painoperkappale = models.CharField(max_length=20)
    kappalehinta = models.DecimalField(max_digits=8, decimal_places=2)
    tuotteitavarastossa = models.IntegerField()
    toimittaja_nimi = models.CharField(max_length=50, null=True, blank=True)
    toimittaja_maa = models.CharField(max_length=50, null=True, blank=True)
    #Kun null=True (tietokanta) ja blank=True (lomake) ovat molemmat asetettuina:
    # Tietokantaan voi tallentaa NULL-arvon.
    # Lomakkeet eivät pakota käyttäjää täyttämään kenttää.
    # Lomakkeella kenttä voi jäädä tyhjäksi.
    # Tietokannassa kentän arvo tallennetaan NULL, jos käyttäjä ei anna mitään arvoa.

    def __str__(self):
        return f"{self.tuotenimi} in storage"