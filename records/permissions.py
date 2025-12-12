# records/permissions.py
from rest_framework import permissions

class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the creator of a record (Patient/Doctor)
    to perform update (PUT, PATCH) or delete (DELETE) operations.
    Read operations (GET, HEAD, OPTIONS) are allowed for any authenticated user.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated request.
        # SAFE_METHODS include GET, HEAD, and OPTIONS.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the creator of the record.
        # The 'obj.created_by' field is the ForeignKey to the User model.
        # The 'request.user' is the authenticated user attached by the JWT.
        return obj.created_by == request.user