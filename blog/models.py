from django.core.validators import URLValidator
from django.db import models


class Ads(models.Model):
    TYPE_CHOICES = [
        ("leaderboard", "Leaderboard (728x90)"),
        ("skyscraper", "Skyscraper (300x250)"),
        ("banner", "Banner (468x60)"),
        ("square", "Square (250x250)"),
    ]

    name = models.CharField(max_length=255)
    link = models.URLField(validators=[URLValidator()])
    image = models.URLField(validators=[URLValidator()])
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="leaderboard")

    @property
    def size_info(self):
        size_map = {
            "leaderboard": "728x90",
            "skyscraper": "300x250",
            "banner": "468x60",
            "square": "250x250",
        }
        return size_map.get(self.type, "Ukuran tidak diketahui")

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Message(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    content = models.TextField()

    def __str__(self):
        return f"Pesan dari {self.name}"


class Feature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(
        max_length=100,
        help_text="Nama class FontAwesome, contoh: fa-solid fa-book-open-reader",
    )

    def __str__(self):
        return self.title


class HeroSlide(models.Model):
    image = models.URLField(help_text="URL gambar untuk background hero")
    title = models.CharField(max_length=255, blank=True)
    subtitle = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Slide {self.order}: {self.title or 'Tanpa Judul'}"
