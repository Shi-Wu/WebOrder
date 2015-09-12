from management.models import *


class UserView(object):
    @staticmethod
    def get_user(username):
        if username:
            try:
                user = MyUser.objects.get(user__username=username)
            except:
                user = ''
        else:
            user = ''
        return user
