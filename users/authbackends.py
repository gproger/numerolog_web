from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import UserInfo

UserModel = get_user_model()


class NumerologBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        use_phone = False

        if kwargs.get('email'):
            username = kwargs['email']  # Bias to email if it was passed explictly

        if kwargs.get('phone'):
            use_phone = True
            phone = kwargs['phone']
            username = kwargs['phone']

        if not username or not password:
            # If no username or password was given, skip rest of this auth
            # This may happen if we are during different auth flow (eg. OAuth/JWT)
            return None


        if not use_phone:
            try:
                user = UserModel.objects.get_by_username_or_email(username)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user (#20760).
                UserModel().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
        else:
            userInfo = UserInfo.objects.filter(phone=phone)
            if userInfo.count() > 0:
                user = userInfo[0].user
                if user is None:
                    UserModel().set_password(password)
                    return None
                elif self.user_can_authenticate(user):
                    return user
            else:
                UserModel().set_password(password)
                return None


    def get_user(self, pk):
        try:
            manager = UserModel._default_manager
            relations = ('rank', 'online_tracker', 'ban_cache')
            user = manager.select_related(*relations).get(pk=pk)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
