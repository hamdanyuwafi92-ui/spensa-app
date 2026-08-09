from django.db import models
from solo.models import SingletonModel

from core.utilities.validators import validate_logo

from .base import BaseModel


class Brand(BaseModel, SingletonModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=50, default="1.0.0")
    tahun = models.CharField(max_length=4, default="2026")
    logo = models.ImageField(
        upload_to="brand/",
        validators=[validate_logo],
    )
    instagram = models.URLField(default="https://www.instagram.com/hamdayuwafii/")
    youtube = models.URLField(default="https://www.youtube.com/@hamdayuwafii")
    tiktok = models.URLField(default="https://www.tiktok.com/@hamdayuwafii")
    facebook = models.URLField(default="https://web.facebook.com/hamdayuwafii/")
    developer = models.CharField(max_length=200, default="Hamdan Yuwafi")

    def __str__(self):
        return self.name
