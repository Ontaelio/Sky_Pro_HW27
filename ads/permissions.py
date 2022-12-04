from rest_framework import permissions


class SelectionEditPermission(permissions.BasePermission):
    message = "Deleting and editing a selection can be done only by it's author."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner

