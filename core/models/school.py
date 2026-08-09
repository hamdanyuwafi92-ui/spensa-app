from django.db import models
from solo.models import SingletonModel

from core.utilities.validators import (
    validate_fax,
    validate_kode_pos,
    validate_logo,
    validate_nip,
    validate_npsn,
    validate_phone,
)

from .base import BaseModel, SlugMixin


class School(SlugMixin, BaseModel, SingletonModel):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(
        max_length=20, blank=True, null=True, validators=[validate_phone]
    )
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="school_logos/",
        blank=True,
        null=True,
        validators=[validate_logo],
    )
    npsn = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        validators=[validate_npsn],
    )
    status = models.CharField(
        max_length=20,
        choices=[("Negeri", "Negeri"), ("Swasta", "Swasta")],
        blank=True,
        null=True,
    )
    jenjang = models.CharField(
        max_length=10,
        choices=[
            ("SD", "SD"),
            ("SMP", "SMP"),
            ("SMA", "SMA"),
            ("SMK", "SMK"),
        ],
        blank=True,
        null=True,
    )
    akreditasi = models.CharField(
        max_length=20,
        choices=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("Unggul", "Unggul"),
            ("Baik Sekali", "Baik Sekali"),
            ("Baik", "Baik"),
            ("Tidak Terakreditasi", "Tidak Terakreditasi"),
        ],
        blank=True,
        null=True,
    )
    kepala_sekolah = models.CharField(max_length=255, blank=True, null=True)
    nip_kepsek = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        validators=[validate_nip],
    )
    fax = models.CharField(
        max_length=20, blank=True, null=True, validators=[validate_fax]
    )
    kode_pos = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        validators=[validate_kode_pos],
    )

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return self.name
