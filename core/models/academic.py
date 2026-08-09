from typing import ClassVar

from django.db import models

from core.utilities.constants import LEVEL_CHOICES, SUBJECT_CHOICES

from .base import BaseModel, SlugMixin


class Classroom(SlugMixin, BaseModel):
    mainclassroom = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    name = models.CharField(max_length=10)

    class Meta:
        constraints: ClassVar[list] = [
            models.UniqueConstraint(
                fields=["mainclassroom", "name"], name="unique_classroom"
            )
        ]

    def get_slug_source(self):
        return f"kelas-{self.mainclassroom}-{self.name}"

    def __str__(self):
        return f"Kelas {self.mainclassroom} {self.name}"


class Subject(SlugMixin, BaseModel):
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=100, choices=SUBJECT_CHOICES, unique=True)

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return f"{self.code} - {self.name}"


class Club(SlugMixin, BaseModel):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def get_slug_source(self):
        return self.name

    def __str__(self):
        return f"{self.code} - {self.name}"
