# coding=utf-8

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from functools import wraps
from backs.models import Account
from backs.models import Menu


def authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(args) == 1:
            request = args[0]
        else:
            request = args[1]
        if request.session.get('user_id', None) == None:
            # 用户未登陆
            return HttpResponseRedirect('/admin/login')
        else:
            request.user = request.session.get('user', None)
        return func(*args, **kwargs)
    return wrapper


def backendmenu(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):

        return func(request, *args, **kwargs)
    return wrapper


class LoginBackend(object):

    # def authenticate(self, username=None, password=None):
    #     if username:
    #         # email
    #         if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", username) != None:
    #             try:
    #                 user = User.objects.get(email=username)
    #                 if user.check_password(password):
    #                     return user
    #             except User.DoesNotExist:
    #                 return None
    #         # mobile
    #         elif len(username) == 11 and re.match("^(1[3458]\d{9})$", username) != None:
    #             try:
    #                 user = User.objects.get(mobile=username)
    #                 if user.check_password(password):
    #                     return user
    #             except User.DoesNotExist:
    #                 return None
    #         # nick
    #         else:
    #             try:
    #                 user = User.objects.get(username=username)
    #                 if user.check_password(password):
    #                     return user
    #             except User.DoesNotExist:
    #                 return None
    #     else:
    #         return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def is_authenticated(self):
        return True

    # def authenticate(self, username=None, password=None, **kwargs):
    #     UserModel = get_user_model()
    #     if username is None:
    #         username = kwargs.get(UserModel.USERNAME_FIELD)
    #     try:
    #         user = UserModel._default_manager.get_by_natural_key(username)
    #         if user.check_password(password):
    #             return user
    #     except UserModel.DoesNotExist:
    #         # Run the default password hasher once to reduce the timing
    #         # difference between an existing and a non-existing user (#20760).
    #         UserModel().set_password(password)

    # def _get_user_permissions(self, user_obj):
    #     return user_obj.user_permissions.all()

    # def _get_group_permissions(self, user_obj):
    #     user_groups_field = get_user_model()._meta.get_field('groups')
    #     user_groups_query = 'group__%s' % user_groups_field.related_query_name()
    #     return Permission.objects.filter(**{user_groups_query: user_obj})

    # def _get_permissions(self, user_obj, obj, from_name):
    #     """
    #     Returns the permissions of `user_obj` from `from_name`. `from_name` can
    #     be either "group" or "user" to return permissions from
    #     `_get_group_permissions` or `_get_user_permissions` respectively.
    #     """
    #     if not user_obj.is_active or user_obj.is_anonymous() or obj is not None:
    #         return set()

    #     perm_cache_name = '_%s_perm_cache' % from_name
    #     if not hasattr(user_obj, perm_cache_name):
    #         if user_obj.is_superuser:
    #             perms = Permission.objects.all()
    #         else:
    #             perms = getattr(self, '_get_%s_permissions' %
    #                             from_name)(user_obj)
    #         perms = perms.values_list(
    #             'content_type__app_label', 'codename').order_by()
    #         setattr(user_obj, perm_cache_name, set("%s.%s" % (ct, name)
    #                                                for ct, name in perms))
    #     return getattr(user_obj, perm_cache_name)

    # def get_user_permissions(self, user_obj, obj=None):
    #     """
    #     Returns a set of permission strings the user `user_obj` has from their
    #     `user_permissions`.
    #     """
    #     return self._get_permissions(user_obj, obj, 'user')

    # def get_group_permissions(self, user_obj, obj=None):
    #     """
    #     Returns a set of permission strings the user `user_obj` has from the
    #     groups they belong.
    #     """
    #     return self._get_permissions(user_obj, obj, 'group')

    # def get_all_permissions(self, user_obj, obj=None):
    #     if not user_obj.is_active or user_obj.is_anonymous() or obj is not None:
    #         return set()
    #     if not hasattr(user_obj, '_perm_cache'):
    #         user_obj._perm_cache = self.get_user_permissions(user_obj)
    #         user_obj._perm_cache.update(self.get_group_permissions(user_obj))
    #     return user_obj._perm_cache

    # def has_perm(self, user_obj, perm, obj=None):
    #     if not user_obj.is_active:
    #         return False
    #     return perm in self.get_all_permissions(user_obj, obj)

    # def has_module_perms(self, user_obj, app_label):
    #     """
    #     Returns True if user_obj has any permissions in the given app_label.
    #     """
    #     if not user_obj.is_active:
    #         return False
    #     for perm in self.get_all_permissions(user_obj):
    #         if perm[:perm.index('.')] == app_label:
    #             return True
    #     return False

    # def get_user(self, user_id):
    #     UserModel = get_user_model()
    #     try:
    #         return UserModel._default_manager.get(pk=user_id)
    #     except UserModel.DoesNotExist:
    #         return None
