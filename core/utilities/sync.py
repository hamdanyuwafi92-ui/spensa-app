from core.models import (
    Formative,
    Summative,
    Performance,
    Summary,
    ActiveSubject,
    ActiveClub,
    ActiveClassStudent,
)


def sync_all():
    existing_formatives = set(
        Formative.objects.values_list("teacher_id", "student_id", "type")
    )
    existing_summatives = set(Summative.objects.values_list("teacher_id", "student_id"))
    existing_performances = set(
        Performance.objects.values_list("teacher_id", "active_club_id", "student_id")
    )

    new_formatives = []
    new_summatives = []
    new_performances = []
    new_formative_pairs = set()
    new_summative_pairs = set()

    subjects = ActiveSubject.objects.select_related("classroom", "activeyear")
    for subject in subjects:
        students = ActiveClassStudent.objects.filter(
            activeclass__classroom=subject.classroom,
            activeclass__activeyear=subject.activeyear,
        )
        for student in students:
            for i in range(1, 6):
                key = (subject.pk, student.pk, f"F{i}")
                if key not in existing_formatives:
                    new_formatives.append(
                        Formative(
                            teacher=subject,
                            student=student,
                            type=f"F{i}",
                            score=0,
                        )
                    )
                    new_formative_pairs.add((subject.pk, student.pk))
            sum_key = (subject.pk, student.pk)
            if sum_key not in existing_summatives:
                new_summatives.append(
                    Summative(teacher=subject, student=student, score=0)
                )
                new_summative_pairs.add(sum_key)

    if new_formatives:
        Formative.objects.bulk_create(new_formatives)
    if new_summatives:
        Summative.objects.bulk_create(new_summatives)

    all_new_pairs = new_formative_pairs | new_summative_pairs
    for teacher_id, student_id in all_new_pairs:
        Summary.objects.get_or_create(
            student_id=student_id,
            subject_id=teacher_id,
            defaults={
                "formatif_score": 0,
                "summatif_score": 0,
                "final_score": 0,
            },
        )

    clubs_processed = 0
    students_total = 0
    clubs = ActiveClub.objects.filter(teacher__isnull=False).prefetch_related(
        "students"
    )
    for club in clubs:
        club_students = club.students.all()
        if not club_students:
            continue
        clubs_processed += 1
        for student in club_students:
            students_total += 1
            perf_key = (club.teacher_id, club.pk, student.pk)
            if perf_key not in existing_performances:
                new_performances.append(
                    Performance(
                        teacher=club.teacher,
                        active_club=club,
                        student=student,
                        score=0,
                        description="Silahkan Isi Deskripsi",
                    )
                )

    if new_performances:
        Performance.objects.bulk_create(new_performances)

    return {
        "formatif": len(new_formatives),
        "summatif": len(new_summatives),
        "performance": len(new_performances),
        "clubs_processed": clubs_processed,
        "students_total": students_total,
    }
