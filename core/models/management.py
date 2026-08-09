from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from core.utilities.validators import validate_teacher_job

from .academic import Classroom, Club, Subject
from .base import BaseModel
from .users import Student, Teacher
from .year import ActiveYear


class ActiveClass(BaseModel):
    activeyear = models.ForeignKey(ActiveYear, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(
        default=25,
        validators=(MinValueValidator(0), MaxValueValidator(35)),
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_classes_wali",
    )
    students = models.ManyToManyField(Student, through="ActiveClassStudent", blank=True)

    class Meta:
        ordering = ("activeyear", "classroom__mainclassroom", "classroom__name")
        constraints = (
            models.UniqueConstraint(
                fields=["activeyear", "classroom"],
                name="unique_activeclass_year_classroom",
            ),
            models.UniqueConstraint(
                fields=["activeyear", "teacher"],
                condition=models.Q(teacher__isnull=False),
                name="unique_wali_per_year",
            ),
        )

    def clean(self):
        super().clean()
        validate_teacher_job(self.teacher)
        if self.pk and self.capacity < self.students.count():
            raise ValidationError(
                f"Kapasitas ({self.capacity}) lebih kecil dari jumlah siswa yang sudah terdaftar ({self.students.count()})."
            )

    def __str__(self):
        return f"{self.activeyear} - {self.classroom}"


class ActiveClassStudent(models.Model):
    activeclass = models.ForeignKey(ActiveClass, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("activeclass", "student")

    def save(self, *args, **kwargs):
        if self.pk is None:  # only on creation
            active_year = self.activeclass.activeyear
            other_classes = ActiveClass.objects.filter(
                activeyear=active_year, students=self.student
            ).exclude(pk=self.activeclass.pk)
            if other_classes.exists():
                raise ValidationError(
                    f"Siswa {self.student} sudah terdaftar di kelas {other_classes.first().classroom}"
                )

            current_count = self.activeclass.students.count()
            if current_count >= self.activeclass.capacity:
                raise ValidationError(
                    f"Kapasitas kelas {self.activeclass.classroom} sudah penuh ({self.activeclass.capacity})."
                )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} di {self.activeclass}"


class ActiveSubject(BaseModel):
    activeyear = models.ForeignKey(ActiveYear, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_subjects",
    )

    class Meta:
        unique_together = ("activeyear", "subject", "classroom")
        ordering = ("activeyear", "classroom__mainclassroom", "classroom__name")

    def clean(self):
        super().clean()
        validate_teacher_job(self.teacher)

    def __str__(self):
        return f"{self.activeyear} - {self.subject} - {self.classroom}"


class ActiveClub(BaseModel):
    activeyear = models.ForeignKey(ActiveYear, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="active_clubs",
    )
    students = models.ManyToManyField(Student, blank=True)

    class Meta:
        unique_together = ("activeyear", "club")
        ordering = ("activeyear", "club__name")

    def clean(self):
        super().clean()
        validate_teacher_job(self.teacher)

    def __str__(self):
        return f"{self.activeyear} - {self.club}"
