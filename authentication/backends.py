from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailPhoneNumberBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)

            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None
