from rest_framework import viewsets

from bookmarks.models import Collection

from .permissions import IsCreator, IsCreatorOrReadOnly
from .serializers import (BookmarkAddToCollectionSerializer,
                          BookmarkCreateDeleteSerializer,
                          BookmarkGetSerializer, CollectionSerializer)


class CollectionViewSet(viewsets.ModelViewSet):
    """Вьюсет для коллекций."""

    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    permission_classes = (IsCreatorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class BookmarkViewSet(viewsets.ModelViewSet):
    """Вьюсет для закладок."""

    permission_classes = (IsCreator,)

    def get_queryset(self):
        return self.request.user.bookmarks.all()

    def get_serializer_class(self):
        if self.action == "update":
            return BookmarkAddToCollectionSerializer
        if self.action in ("list", "retrieve"):
            return BookmarkGetSerializer
        return BookmarkCreateDeleteSerializer
