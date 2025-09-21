from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.conf import settings


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print(f"Request headers: {request.headers}")
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        print(f"Access token from cookie: {access_token}")

        if access_token:
            try:
                validated_token = self.get_validated_token(access_token)
                user = self.get_user(validated_token)
                print(f"Valid token for user: {user.id}")
                return (user, validated_token)
            except (InvalidToken, AuthenticationFailed) as e:
                print(f"Token validation error: {str(e)}")
                return None

        print("No cookie found, trying Bearer token...")
        result = super().authenticate(request)
        print(f"Bearer token result: {result}")
        return result
