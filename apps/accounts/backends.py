from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameBackend(ModelBackend):
    """Allow authentication with either username or email address."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            return None
        try:
            user = (
                UserModel.objects.get(email=username)
                if '@' in username
                else UserModel.objects.get(username=username)
            )
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
