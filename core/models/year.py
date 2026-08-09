from django.db import models, transaction

from .base import BaseModel


class Year(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Semester(BaseModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ActiveYear(BaseModel):
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            with transaction.atomic():
                ActiveYear.objects.select_for_update().filter(is_active=True).update(
                    is_active=False
                )
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    @classmethod
    def get_active(cls):
        try:
            return cls.objects.select_related("year", "semester").get(is_active=True)
        except cls.DoesNotExist:
            return None

    def __str__(self):
        status = " (Aktif)" if self.is_active else ""
        return f"{self.year} - {self.semester}{status}"
