from django.contrib.auth import get_user_model

User = get_user_model()

def set_user_logged(username):
    try:
        # user = User.objects.get(username=username)
        # if not user.is_authenticated:
        #     if user.online:
        #         user.online = False
        #         user.save()
        # else:
        #     if not user.online:
        #         user.online = True
        #         user.save()
        pass
    except Exception as e:
        print(str(e))

def get_user_by_id(username):
    try:
        user = User.objects.get(username=username)
        return user            
    except Exception as e:
        return None

def get_users_logged():
    try:
        # users = User.objects.filter(online=True)
        users = []
        return users            
    except:
        return []