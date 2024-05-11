from rest_framework.authtoken.models import Token


class TokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'HTTP AUTHORIZATION' not in request.headers:
            # Assuming the token is stored in session after login
            token_key = request.session.get('auth_token', None)
            if token_key:
                token = Token.objects.get(key=token_key)
                request.headers['Authorization'] = f'Token {token.key}'
        response = self.get_response(request)
        return response
