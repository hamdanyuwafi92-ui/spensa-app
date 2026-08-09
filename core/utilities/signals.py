from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from core.models.drill import Formative, Summative, Summary
from core.models.users import Teacher, Student


def update_summary(instance):
    student = instance.student
    teacher = instance.teacher
    formatif_avg = (
        Formative.objects.filter(student=student, teacher=teacher).aggregate(
            avg=Avg("score")
        )["avg"]
        or 0
    )
    summatif_obj = Summative.objects.filter(student=student, teacher=teacher).first()
    summatif_val = summatif_obj.score if summatif_obj else 0

    summary, _ = Summary.objects.get_or_create(
        student=student,
        subject=teacher,
    )
    summary.formatif_score = formatif_avg
    summary.summatif_score = summatif_val
    summary.save()


@receiver(post_save, sender=Formative)
def handle_formative_save(sender, instance, **kwargs):
    update_summary(instance)


@receiver(post_delete, sender=Formative)
def handle_formative_delete(sender, instance, **kwargs):
    update_summary(instance)


@receiver(post_save, sender=Summative)
def handle_summative_save(sender, instance, **kwargs):
    update_summary(instance)


@receiver(post_delete, sender=Summative)
def handle_summative_delete(sender, instance, **kwargs):
    update_summary(instance)


@receiver(post_delete, sender=Teacher)
def handle_teacher_delete(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()


@receiver(post_delete, sender=Student)
def handle_student_delete(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
