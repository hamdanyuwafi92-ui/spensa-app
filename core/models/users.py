from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models, transaction

from core.utilities.constants import (
    GENDER_CHOICES,
    STUDENT_JOB_CHOICES,
    STUDENT_STATUS_CHOICES,
    TEACHER_JOB_CHOICES,
)
from core.utilities.managers import UserManager
from core.utilities.services import create_user_for_person
from core.utilities.validators import (
    validate_nip,
    validate_nis,
    validate_nisn,
    validate_nuptk,
    validate_phone,
)

from .base import BaseModel


class User(AbstractUser):
    objects = UserManager()


class Person(BaseModel):
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    tempat_lahir = models.CharField(max_length=100, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    nomor_hp = models.CharField(
        max_length=20,
        validators=[validate_phone],
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True


class Teacher(Person):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    nip = models.CharField(
        max_length=18,
        unique=True,
        validators=[validate_nip],
    )
    nuptk = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_nuptk],
    )
    gelar_depan = models.CharField(max_length=50, blank=True, null=True)
    gelar_belakang = models.CharField(max_length=50, blank=True, null=True)
    job = models.CharField(max_length=20, choices=TEACHER_JOB_CHOICES)
    photo = models.ImageField(upload_to="teachers/", blank=True, null=True)

    def fullname(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return ""

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if not self.user:
                user = create_user_for_person(self)
                if user:
                    self.user = user
                    super().save(update_fields=["user"])

    def __str__(self):
        return f"{self.fullname()} ({self.nip})"


class Student(Person):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    nisn = models.CharField(
        max_length=10,
        unique=True,
        validators=[validate_nisn],
    )
    job = models.CharField(
        max_length=20,
        choices=STUDENT_JOB_CHOICES,
        default="Siswa",
        editable=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STUDENT_STATUS_CHOICES,
        default="Aktif",
        blank=True,
        null=True,
    )
    nis = models.CharField(
        max_length=10,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_nis],
    )
    nama_ayah = models.CharField(max_length=255, blank=True, null=True)
    nama_ibu = models.CharField(max_length=255, blank=True, null=True)
    nomor_hp_ortu = models.CharField(
        max_length=20,
        validators=[validate_phone],
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to="students/", blank=True, null=True)

    def fullname(self):
        if self.user:
            return self.user.get_full_name() or self.user.username
        return ""

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)
            if not self.user:
                user = create_user_for_person(self)
                if user:
                    self.user = user
                    super().save(update_fields=["user"])

    def __str__(self):
        return f"{self.fullname()} ({self.nisn})"
