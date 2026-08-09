from typing import ClassVar

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from solo.admin import SingletonModelAdmin

from core.models import (
    ActiveClass,
    ActiveClassStudent,
    ActiveClub,
    ActiveSubject,
    ActiveYear,
    Album,
    Article,
    Brand,
    Category,
    Classroom,
    Club,
    Comment,
    Formative,
    Page,
    Performance,
    Photo,
    School,
    Semester,
    Student,
    Subject,
    Summary,
    Summative,
    Tag,
    Teacher,
    User,
    Year,
)


class ReadOnlyCreatedByMixin:
    extra_readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")

    def get_readonly_fields(self, request, obj=None):
        return (
            super().get_readonly_fields(request, obj=obj) + self.extra_readonly_fields
        )


class CreatedBySaveMixin:
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class TeacherJobFilterMixin:
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "teacher":
            kwargs["queryset"] = Teacher.objects.filter(
                job__in=["Guru", "Developer", "Administrator", "Agent"]
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ActiveClassStudentInline(admin.TabularInline):
    model = ActiveClassStudent
    extra = 1
    autocomplete_fields: ClassVar[tuple] = ("student",)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(ReadOnlyCreatedByMixin, SingletonModelAdmin):
    pass


@admin.register(School)
class SchoolAdmin(ReadOnlyCreatedByMixin, SingletonModelAdmin):
    prepopulated_fields: ClassVar[dict] = {"slug": ("name",)}


@admin.register(Year)
class YearAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Semester)
class SemesterAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(ActiveYear)
class ActiveYearAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("year", "semester", "is_active", "created_at")
    list_filter = ("is_active",)


@admin.register(Classroom)
class ClassroomAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("mainclassroom", "name", "slug", "created_at")


@admin.register(Subject)
class SubjectAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("code", "name", "slug", "created_at")


@admin.register(Club)
class ClubAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("code", "name", "slug", "created_at")


@admin.register(Teacher)
class TeacherAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("fullname", "nip", "job", "gender", "created_at")
    list_filter = ("job", "gender")
    search_fields = ("nip", "nuptk")


@admin.register(Student)
class StudentAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("fullname", "nisn", "nis", "status", "gender", "created_at")
    list_filter = ("status", "gender")
    search_fields = ("nisn", "nis")


@admin.register(Category)
class CategoryAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Tag)
class TagAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("name", "created_at")


@admin.register(Article)
class ArticleAdmin(ReadOnlyCreatedByMixin, CreatedBySaveMixin, admin.ModelAdmin):
    list_display = ("title", "category", "status", "created_at")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "content")
    readonly_fields = ("slug",)
    filter_horizontal: ClassVar[tuple] = ("tags",)


@admin.register(Album)
class AlbumAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("title", "created_at")
    readonly_fields = ("slug",)


@admin.register(Photo)
class PhotoAdmin(ReadOnlyCreatedByMixin, CreatedBySaveMixin, admin.ModelAdmin):
    list_display = ("id", "album", "category", "created_at")
    list_filter = ("category",)
    readonly_fields = ("slug",)
    filter_horizontal: ClassVar[tuple] = ("tags",)


@admin.register(Comment)
class CommentAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("name", "article", "active", "created_at")
    list_filter = ("active",)
    search_fields = ("name", "body")


@admin.register(Page)
class PageAdmin(ReadOnlyCreatedByMixin, CreatedBySaveMixin, admin.ModelAdmin):
    list_display = ("title", "created_at")
    readonly_fields = ("slug",)


@admin.register(ActiveClass)
class ActiveClassAdmin(ReadOnlyCreatedByMixin, TeacherJobFilterMixin, admin.ModelAdmin):
    list_display = ("activeyear", "classroom", "capacity", "teacher", "created_at")
    list_filter = ("activeyear",)
    inlines: ClassVar[tuple] = (ActiveClassStudentInline,)
    search_fields = ("classroom__name", "teacher__fullname")


@admin.register(ActiveClassStudent)
class ActiveClassStudentAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("activeclass", "student", "created_at")
    search_fields = (
        "student__fullname",
        "student__nisn",
        "activeclass__classroom__name",
    )
    autocomplete_fields: ClassVar[tuple] = ("student", "activeclass")


@admin.register(ActiveSubject)
class ActiveSubjectAdmin(
    ReadOnlyCreatedByMixin, TeacherJobFilterMixin, admin.ModelAdmin
):
    list_display = ("activeyear", "subject", "classroom", "teacher", "created_at")
    list_filter = ("activeyear", "classroom")
    search_fields = ("subject__name", "classroom__name", "teacher__fullname")


@admin.register(ActiveClub)
class ActiveClubAdmin(ReadOnlyCreatedByMixin, TeacherJobFilterMixin, admin.ModelAdmin):
    list_display = ("activeyear", "club", "teacher", "created_at")
    list_filter = ("activeyear",)
    filter_horizontal: ClassVar[tuple] = ("students",)
    search_fields = ("club__name", "teacher__fullname")


@admin.register(Formative)
class FormativeAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("teacher", "student", "type", "score", "created_at")
    list_filter = ("type",)
    autocomplete_fields: ClassVar[tuple] = ("teacher", "student")


@admin.register(Summative)
class SummativeAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("teacher", "student", "score", "created_at")
    autocomplete_fields: ClassVar[tuple] = ("teacher", "student")


@admin.register(Summary)
class SummaryAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "formatif_score",
        "summatif_score",
        "final_score",
        "created_at",
    )
    readonly_fields = ("formatif_score", "summatif_score", "final_score")
    autocomplete_fields: ClassVar[tuple] = ("student", "subject")


@admin.register(Performance)
class PerformanceAdmin(ReadOnlyCreatedByMixin, admin.ModelAdmin):
    list_display = ("active_club", "student", "score", "created_at")
    autocomplete_fields: ClassVar[tuple] = ("active_club", "student")
