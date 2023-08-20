from rest_framework import permissions


class IsCreatorOrReadOnly(permissions.BasePermission):
    """Пермишен для доступа к редактированию и удалению объекта.

    Доступ только создателю объекта.
    """

    message = "Редактирование и удаление доступно только автору"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user


class IsCreator(permissions.BasePermission):
    """Пермишен для доступа к объектам.

    Доступ только создателю объекта.
    """

    message = "Любой доступ разрешен только автору"

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
