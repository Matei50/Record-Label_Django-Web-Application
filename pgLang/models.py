from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class CustomUser(AbstractUser):    
    data_nasterii = models.DateField(null=True, blank=True)
    telefon = models.CharField(max_length=15, blank=True)
    adresa = models.CharField(max_length=255, blank=True)
    oras = models.CharField(max_length=100, blank=True)
    judet = models.CharField(max_length=100, blank=True)
    cod_postal = models.CharField(max_length=10, blank=True)
    cod = models.CharField(max_length=100, null=True, blank=True) 
    email_confirmat = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class GenMuzical(models.Model):
    nume = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    descriere = models.TextField(blank=True, null=True)
    culoare = models.CharField(max_length=7, default="#FFFFFF", help_text="Codul Hex al culorii, ex: #FF5733")

    imagine = models.ImageField(upload_to='genuri/', null=True, blank=True, help_text="O imagine reprezentativa pentru gen")
    
    class Meta:
        verbose_name = "Gen Muzical"
        verbose_name_plural = "Genuri Muzicale"

    def __str__(self):
        return self.nume
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nume)
        super().save(*args, **kwargs)

class Artist(models.Model):
    nume = models.CharField(max_length=100, unique=True)  
    bio = models.TextField(null=True, blank=True)
    imagine = models.ImageField(upload_to='artisti/', null=True, blank=True)
    an_formare = models.IntegerField(null=True, blank=True, help_text="Anul in care s-a format trupa/artistul")
    gen_muzical = models.ForeignKey(GenMuzical, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name = "Artist"
        verbose_name_plural = "Artisti"

    def __str__(self):
        return self.nume

class Producator(models.Model):
    nume = models.CharField(max_length=100, unique=True)
    telefon = models.CharField(max_length=15, blank=True)
    adresa = models.CharField(max_length=255, blank=True)
    oras = models.CharField(max_length=100, blank=True)
    judet = models.CharField(max_length=100, blank=True)
    cod_postal = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = "Producator"
        verbose_name_plural = "Producatori"

    def __str__(self):
        return self.nume

class Album(models.Model):
    titlu = models.CharField(max_length=200)
    data_lansarii = models.DateField()
    coperta = models.ImageField(upload_to='coperte/', null=True, blank=True)

    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="albume")

    producator = models.ForeignKey(
        Producator,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="albume"
    )

    pret = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True,
                               help_text="Pretul final de vanzare (calculat automat)")
    gen = models.CharField()

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albume"

    def __str__(self):
        return f"{self.titlu} ({self.artist.nume})"
    
class Piesa(models.Model):
    titlu = models.CharField(max_length=200)
    
    
    numar_piesa = models.PositiveIntegerField()
    
    
    durata = models.DurationField() 
    
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="piese")

    class Meta:
        ordering = ['numar_piesa']
        verbose_name = "Piesa"
        verbose_name_plural = "Piese"

    def __str__(self):
        return f"{self.numar_piesa}. {self.titlu}"
    
    @property
    def durata_formatata(self):     
        total_secunde = int(self.durata.total_seconds())
        
        minute = total_secunde // 60 
        secunde = total_secunde % 60
        
        return f"{minute:02}:{secunde:02}"
    from django.conf import settings
from django.utils import timezone

class Comanda(models.Model):
    utilizator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comenzi'
    )

    albume = models.ManyToManyField(
        Album,
        related_name='comenzi'
    )

    nume_destinatar = models.CharField(max_length=100)
    telefon_destinatar = models.CharField(max_length=15)
    adresa_destinatar = models.CharField(max_length=255)

    data_plasare = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Comandă"
        verbose_name_plural = "Comenzi"

    def __str__(self):
        return f"Comanda #{self.id} - {self.utilizator.username}"


class LinieComanda(models.Model):
    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE,
        related_name='linii'
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.PROTECT,
        related_name='linii_comanda'
    )

    # cele 2 campuri extra
    cantitate = models.PositiveIntegerField(default=1)
    pret_unitar = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Linie comandă"
        verbose_name_plural = "Linii comandă"

    def __str__(self):
        return f"{self.album.titlu} x {self.cantitate} (Comanda #{self.comanda.id})"
    
class Voucher(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='vouchere'
    )

    procentaj = models.PositiveSmallIntegerField()
    perioada = models.PositiveIntegerField()
    transmisibilitate = models.BooleanField(default=False)

    def __str__(self):
        return f"Voucher {self.procentaj}% - {self.album.titlu}"
    
class Rating(models.Model):
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        related_name='ratinguri'
    )

    popularitate = models.PositiveSmallIntegerField()
    credibilitate = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Rating - {self.album.titlu}"