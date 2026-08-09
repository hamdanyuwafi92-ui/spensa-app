from django.contrib import admin

from .models import Ads, Feature, HeroSlide, Message


@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "size_info", "link")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email")


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon")


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("order", "title", "image")
