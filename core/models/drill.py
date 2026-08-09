from django.core.exceptions import ValidationError
from django.db import models

from .base import BaseModel
from .management import ActiveClassStudent, ActiveClub, ActiveSubject
from .users import Student, Teacher


class BaseScore(BaseModel):
    teacher = models.ForeignKey(
        ActiveSubject,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )
    student = models.ForeignKey(
        ActiveClassStudent,
        on_delete=models.CASCADE,
        related_name="%(class)ss",
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if self.teacher.classroom != self.student.activeclass.classroom:
            raise ValidationError(
                "Siswa harus berada di kelas yang sama dengan mata pelajaran yang diajar."
            )


class Formative(BaseScore):
    type = models.CharField(
        max_length=2,
        choices=[(f"F{i}", f"F{i}") for i in range(1, 6)],
    )

    class Meta:
        ordering = ("teacher", "student", "type")

    def __str__(self):
        return f"{self.student.student} - {self.type} ({self.score})"


class Summative(BaseScore):
    class Meta:
        ordering = ("teacher", "student")

    def __str__(self):
        return f"{self.student.student} - Summative ({self.score})"


class Summary(BaseModel):
    student = models.ForeignKey(
        ActiveClassStudent,
        on_delete=models.CASCADE,
        related_name="summaries",
    )
    subject = models.ForeignKey(
        ActiveSubject,
        on_delete=models.CASCADE,
        related_name="summaries",
    )
    formatif_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        default=0,
    )
    summatif_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        default=0,
    )
    final_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        editable=False,
        default=0,
    )

    class Meta:
        unique_together = ("student", "subject")
        verbose_name_plural = "Summaries"

    def save(self, *args, **kwargs):
        self.final_score = (self.formatif_score + self.summatif_score) / 2
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Summary: {self.student.student} - {self.subject.subject}"


class Performance(BaseModel):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    active_club = models.ForeignKey(
        ActiveClub,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="performances",
    )
    score = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("active_club", "student")

    def clean(self):
        super().clean()
        if self.active_club.teacher != self.teacher:
            raise ValidationError(
                "Hanya guru pembina yang dapat memberikan nilai performance."
            )
        if not self.active_club.students.filter(pk=self.student.pk).exists():
            raise ValidationError("Siswa bukan anggota dari ekstrakurikuler ini.")

    def __str__(self):
        return f"Performance: {self.student} in {self.active_club.club}"
