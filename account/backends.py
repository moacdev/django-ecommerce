from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model,login
from django.db.models import Q

User = get_user_model()


class MultiAuthBackend(object):
    """It provides the functionality to slide down to email to login,
    instead of just username"""
    def authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(Q(email=username) | Q(username=username) | Q(phone=username))
            if user.check_password(password):   #you can also test user.is_active
                login(request=request, user=user)
                return user 
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None