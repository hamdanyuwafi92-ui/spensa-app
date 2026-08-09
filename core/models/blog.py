from django.db import models

from core.utilities.constants import TAG_CHOICES
from core.utilities.validators import validate_logo

from .base import BaseModel, SlugMixin


class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=50, choices=TAG_CHOICES, unique=True)

    def __str__(self):
        return self.name


class Article(SlugMixin, BaseModel):
    title = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to="articles/",
        validators=[validate_logo],
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)
    content = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[("publish", "Publish"), ("draft", "Draft")],
        default="draft",
    )

    def get_slug_source(self):
        return self.title

    def __str__(self):
        return self.title


class Album(SlugMixin, BaseModel):
    title = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to="albums/",
        validators=[validate_logo],
    )
    caption = models.CharField(max_length=500, blank=True)

    def get_slug_source(self):
        return self.title

    def __str__(self):
        return self.title


class Photo(SlugMixin, BaseModel):
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.URLField()
    caption = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def get_slug_source(self):
        return self.caption or "photo"

    def __str__(self):
        return f"Photo {self.id} - {self.album.title if self.album else ''}"


class Comment(BaseModel):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    body = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.article.title}"


class Page(SlugMixin, BaseModel):
    title = models.CharField(max_length=255, unique=True)
    thumbnail = models.ImageField(
        upload_to="pages/",
        validators=[validate_logo],
        blank=True,
        null=True,
    )
    content = models.TextField()

    def get_slug_source(self):
        return self.title

    def __str__(self):
        return self.title
