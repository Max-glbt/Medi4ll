from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication sans vérification CSRF
    """
    def enforce_csrf(self, request):
        return  # Ne pas vérifier le CSRF
