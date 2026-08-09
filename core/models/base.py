from django.conf import settings
from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="+",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="+",
    )

    class Meta:
        abstract = True


class SlugMixin(models.Model):
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def get_slug_source(self):
        raise NotImplementedError("Subclasses must define get_slug_source()")

    def save(self, *args, **kwargs):
        if not self.slug:
            source = self.get_slug_source()
            self.slug = slugify(source)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while type(self).objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
