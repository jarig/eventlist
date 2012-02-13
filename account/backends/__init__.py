from importlib import import_module
from django.contrib.auth.models import User
from account import settings
from django.core.exceptions import ImproperlyConfigured


class PublicAuth:
    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, provider=None, identity=None, request=None):
        for authProfile in settings.BACKENDS:
            try:
                classPath = settings.BACKENDS[authProfile]["CLASS"]
                if provider == settings.BACKENDS[authProfile]["NAME"]:
                    return get_instance_from_path(classPath).authenticate(identity, request)
            except KeyError:
                pass
            
        return None
        pass


#from openauth module
def get_instance_from_path(path, *args, **kwargs):
    """
    Return an instance of a class, given the dotted
    Python import path (as a string) to the backend class.

    If the backend cannot be located (e.g., because no such module
    exists, or because the module does not contain a class of the
    appropriate name), ``django.core.exceptions.ImproperlyConfigured``
    is raised.

    """
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading registration backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))

    return backend_class(*args, **kwargs)