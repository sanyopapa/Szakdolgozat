from django.contrib.auth.backends import ModelBackend
from .models import RendeloUser

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = RendeloUser.objects.get(email=username)
            if user.check_password(password):
                return user
        except RendeloUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return RendeloUser.objects.get(pk=user_id)
        except RendeloUser.DoesNotExist:
            return None