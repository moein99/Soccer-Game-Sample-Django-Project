import rest_framework.views
from django.http import JsonResponse
from rest_framework import status, exceptions

from game.api.helpers import get_redis_connection


class SessionRequiredMixin(rest_framework.views.APIView):
    """ A Quick Session Required Mixin For Soccer Game """

    def dispatch(self, request, *args, **kwargs):
        connection = get_redis_connection()
        session_id = request.headers.get("session")
        is_session_valid = session_id is not None and connection.get(session_id) is not None
        if not is_session_valid:
            return JsonResponse(
                {'error': 'Session not found. Please try to login.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super(SessionRequiredMixin, self).dispatch(request, *args, **kwargs)

    def permission_denied(self, request, message=None, code=None):
        """
        If request is not permitted, determine what kind of exception to raise.
        """
        if request.authenticators and not request.successful_authenticator:
            raise exceptions.NotAuthenticated(detail="You do not have the permission to access this resource.")
        raise exceptions.PermissionDenied(detail=message, code=code)

