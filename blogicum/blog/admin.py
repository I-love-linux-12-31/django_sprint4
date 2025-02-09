from django.contrib import admin
from . models import Post, Category, Location


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    ...


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    ...
