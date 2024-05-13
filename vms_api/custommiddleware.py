from rest_framework.authtoken.models import Token
from django.utils.deprecation import MiddlewareMixin


class TokenMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        super().__init__(get_response)

    def __call__(self, request):
        print(request.META)
        if 'HTTP AUTHORIZATION' not in request.META:
            # Assuming the token is stored in session after login
            token_key = request.session.get('auth_token', None)
            print(token_key)
            if token_key:
                token = Token.objects.get(key=token_key)
                request.META['Authorization'] = f'Token {token.key}'
        response = self.get_response(request)
        return response
