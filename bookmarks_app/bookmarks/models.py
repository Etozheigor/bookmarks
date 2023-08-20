from django.db import models
from users.models import User

WEBSITE = "website"
BOOK = "book"
ARTICLE = "article"
MUSIC = "music"
VIDEO = "video"

URL_TYPES = (
    (WEBSITE, "website"),
    (BOOK, "book"),
    (ARTICLE, "article"),
    (MUSIC, "music"),
    (VIDEO, "video"),
)


class Collection(models.Model):
    """Модель Коллекции."""

    name = models.CharField(verbose_name="Имя", max_length=50)
    description = models.CharField(verbose_name="Описание", max_length=100)
    date_of_creation = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    date_of_change = models.DateTimeField(
        verbose_name="Дата изменения", null=True)
    creator = models.ForeignKey(
        User,
        verbose_name="Создатель",
        on_delete=models.CASCADE,
        related_name="collections",
    )

    class Meta:
        verbose_name = "Коллекция"
        verbose_name_plural = "Коллекции"


class Bookmark(models.Model):
    """Модель закладки."""

    title = models.CharField(
        verbose_name="Заголовок страницы", null=True, max_length=100
    )
    description = models.CharField(
        verbose_name="Описание", null=True, max_length=100)
    url = models.URLField(verbose_name="Ссылка на страницу", max_length=500)
    url_type = models.CharField(
        verbose_name="Тип ссылки", null=True, choices=URL_TYPES, max_length=20
    )
    image = models.ImageField(
        "Картинка превью", blank=True, null=True, upload_to="bookmarks_images"
    )
    date_of_creation = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    date_of_change = models.DateTimeField(
        verbose_name="Дата изменения", null=True)
    collections = models.ManyToManyField(
        Collection,
        through="BookmarkCollection",
        verbose_name="Коллекции",
        related_name="bookmarks",
    )
    creator = models.ForeignKey(
        User,
        verbose_name="Создатель",
        on_delete=models.CASCADE,
        related_name="bookmarks",
    )

    class Meta:
        verbose_name = "Закладка"
        verbose_name_plural = "Закладки"


class BookmarkCollection(models.Model):
    """Промежуточная модель для связи закладка-коллекция."""

    bookmark = models.ForeignKey(Bookmark, on_delete=models.CASCADE)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    # class Meta:
    #     verbose_name = "Коллекция закладки"
    #     verbose_name_plural = "Коллекции закладок"
    #     constraints = (
    #         models.UniqueConstraint(
    #             fields=("bookmark", "collection"),
    #             name="unique_bookmark_collection"
    #         ),
    #     )
