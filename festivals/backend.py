from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import django.contrib.auth.hashers as hasher


class AuthBackend(BaseBackend):
    class BadEmail(Exception):
        pass

    class BadPassword(Exception):
        pass

    def authenticate(self, request, username=None, password=None):
        # find user in database by email
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            # user not found
            raise self.BadEmail
            return None

        if(hasher.check_password(password, user.password)):
            # password match
            request.session['session_uid'] = user.id
            request.session.set_expiry(0)

            return user
        else:
            # password mismatchs
            raise self.BadPassword
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
