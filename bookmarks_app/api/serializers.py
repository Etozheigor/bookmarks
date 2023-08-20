from datetime import datetime

from rest_framework import serializers

from bookmarks.models import Bookmark, Collection
from bookmarks.services.bookmarks import BookmarkService


class CollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для коллекций."""

    class Meta:
        model = Collection
        fields = ("name", "description")

    def validate_name(self, value):
        if Collection.objects.filter(
            creator=self.context["request"].user, name=value
        ).exists():
            raise serializers.ValidationError("Такая коллекция уже существует")
        return value

    def update(self, instance, validated_data):
        validated_data["date_of_change"] = datetime.now()
        return super().update(instance, validated_data)


class BookmarkGetSerializer(serializers.ModelSerializer):
    """Сериализатор для Get-запросов к модели коллекций."""
    class Meta:
        model = Bookmark
        fields = (
            "title",
            "description",
            "url",
            "url_type",
            "image",
            "date_of_creation",
            "date_of_change",
        )


class BookmarkCreateDeleteSerializer(serializers.ModelSerializer):
    """Сериализатор для получения, создания и удаления закладок."""

    bookmark_service = BookmarkService()

    class Meta:
        model = Bookmark
        fields = ("url",)

    def validate_url(self, value):
        if Bookmark.objects.filter(
            creator=self.context["request"].user, url=value
        ).exists():
            raise serializers.ValidationError("Такая закладка уже существует")
        return value

    def create(self, validated_data):
        bookmark = self.bookmark_service.create(
            validated_data["url"], self.context["request"].user
        )
        return bookmark


class BookmarkAddToCollectionSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления закладок в коллекции."""

    collections = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Collection.objects.all()
    )

    class Meta:
        model = Bookmark
        fields = ("collections",)

    def validate_collections(self, value):
        for collection in value:
            if collection.creator != self.context["request"].user:
                raise serializers.ValidationError(
                    f"Коллекции {collection.name}"
                    "не существует у данного пользователя."
                )
        return value

    def update(self, instance, validated_data):
        for collection in validated_data["collections"]:
            if collection not in instance.collections.all():
                instance.collections.add(collection)
        instance.date_of_change = datetime.now()
        instance.save()
        return instance
