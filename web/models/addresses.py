from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.core.validators import (
    MinLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)


User = get_user_model()

DISTANCE_MAX = 30


class UserAddress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        verbose_name="Użytkownik",
        on_delete=models.CASCADE,
    )
    street = models.CharField(verbose_name="Ulica", max_length=128)
    house = models.CharField(verbose_name="Nr domu", max_length=8)
    door = models.CharField(
        verbose_name="Nr lokalu", null=True, blank=True, max_length=16
    )
    city = models.CharField(verbose_name="Miasto", max_length=64)
    post_code = models.CharField(
        verbose_name="Kod pocztowy", max_length=6, null=True, blank=True
    )
    main = models.BooleanField(verbose_name="Główny adres?")
    location = models.PointField(null=True, blank=True)
    precision = models.CharField(
        verbose_name="Precyzja Geo",
        max_length=64,
        default="Brak danych",
        null=True,
        blank=True,
    )
    is_located = models.BooleanField(
        verbose_name="Lokalizacja Geo API", default=False
    )
    geo_data = models.JSONField(
        verbose_name="Dane z geolokalizacji", null=True, blank=True
    )
    info = models.TextField(verbose_name="Informacje", null=True, blank=True)
    nearest_point = models.ForeignKey(
        "PostCodeWarsaw",
        verbose_name="Najbliższy punkt odległości",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    distance_to_center = models.IntegerField(
        verbose_name="Odległość do Centrum w kilometrach",
        default=999,
        validators=[MaxValueValidator(1000), MinValueValidator(0)],
    )
    distance_allowed = models.BooleanField(
        verbose_name="Czy adres jest w strefie?", default=False
    )
    distance_to_point = models.IntegerField(
        verbose_name="Odległość do punktu w metrach",
        default=999,
        validators=[MinValueValidator(0)],
    )

    def save(self, *args, **kwargs):
        if self.main:
            disable_main = UserAddress.objects.exclude(id=self.id).filter(
                user=self.user, main=True
            )
            for el in disable_main:
                el.main = False
                el.save()
        if self.is_located and self.distance_to_center < DISTANCE_MAX:
            self.distance_allowed = True
        else:
            self.distance_allowed = False
        super(UserAddress, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.main:
            default_main = (
                UserAddress.objects.filter(user=self.user)
                .exclude(id=self.id)
                .first()
            )
            if default_main:
                default_main.main = True
                default_main.save()
        super(UserAddress, self).delete(*args, **kwargs)

    class Meta:
        ordering = (
            "user",
            "-main",
            "street",
            "-id",
        )
        verbose_name_plural = "Adresy"

    def __str__(self):
        return "{} {}, {}, {}".format(
            self.street, self.house, self.post_code, self.city
        )


class CompanyData(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        db_index=True,
        verbose_name="Użytkownik",
        on_delete=models.CASCADE,
    )
    company_name = models.CharField(
        verbose_name="Płatnik",
        max_length=128,
    )
    company_name_l = models.CharField(
        verbose_name="Odbiorca",
        max_length=128,
        null=True,
        blank=True,
    )
    street = models.CharField(verbose_name="Ulica", max_length=128)
    house = models.CharField(verbose_name="Nr domu", max_length=8)
    door = models.CharField(verbose_name="Nr lokalu", default="", max_length=8)
    city = models.CharField(verbose_name="Miasto", max_length=64)
    post_code = models.CharField(
        verbose_name="Kod pocztowy", max_length=6, null=True, blank=True
    )
    nip = models.CharField(
        verbose_name="Numer nip",
        validators=[MinLengthValidator(10)],
        max_length=13,
    )
    main = models.BooleanField(verbose_name="Firma domyślna ?", default=False)

    def save(self, *args, **kwargs):
        if self.main:
            disable_main = CompanyData.objects.exclude(id=self.id).filter(
                user=self.user, main=True
            )
            for el in disable_main:
                el.main = False
                el.save()
        super(CompanyData, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.main:
            default_main = (
                CompanyData.objects.filter(user=self.user)
                .exclude(id=self.id)
                .first()
            )
            if default_main:
                default_main.main = True
                default_main.save()
        super(CompanyData, self).delete(*args, **kwargs)

    class Meta:
        ordering = (
            "user",
            "-main",
            "company_name",
            "-id",
        )
        verbose_name_plural = "Firmy użytkowników"

    def __str__(self):
        return "{} {}, {}, {}".format(
            self.company_name,
            self.street,
            self.house,
            self.post_code,
            self.city,
        )


class DistrictWarsaw(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa", max_length=128)
    city = models.ForeignKey(
        "City", verbose_name="Miato", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Dzielnice"

    def __str__(self):
        return "{}".format(self.name)


class SubDistrictWarsaw(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa", max_length=128)
    district = models.ForeignKey(
        "DistrictWarsaw",
        db_index=True,
        verbose_name="Dzielnica",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Małe Dzielnice"

    def __str__(self):
        return "{}, {}".format(self.name, self.district)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nazwa", max_length=128)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Miasto"

    def __str__(self):
        return self.name


class StreetWarsaw(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Ulica", max_length=128, db_index=True
    )

    district = models.ForeignKey(
        "DistrictWarsaw",
        db_index=True,
        verbose_name="Dzielnica",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Spis ulic"

    def __str__(self):
        if self.district:
            return self.name, +self.district
        return self.name


class PostCodeWarsaw(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Kod pocztowy", max_length=6, db_index=True
    )
    sub_district = models.ForeignKey(
        "SubDistrictWarsaw",
        db_index=True,
        verbose_name="Mała dzielnica",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    location = models.PointField()
    precision = models.CharField(
        verbose_name="Precyzja Geo", max_length=64, default="Błędne dane"
    )
    is_located = models.BooleanField(
        verbose_name="GeoLokalizacja", default=False
    )
    geo_data = models.JSONField(
        verbose_name="Dane z geolokalizacji", default=dict
    )

    class Meta:
        verbose_name_plural = "Kody pocztowe"

    def __str__(self):
        return self.name
