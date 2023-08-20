from django.contrib import admin

from .models import Bookmark, BookmarkCollection, Collection


class BookmarkCollectionInLine(admin.TabularInline):
    """Кастомный класс для отображения в админке поля коллекций закладок."""

    model = BookmarkCollection


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Кастомный класс для администрирования модели закладок."""

    inlines = (BookmarkCollectionInLine,)


admin.site.register(Collection)
admin.site.register(BookmarkCollection)
