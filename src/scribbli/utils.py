import re
from functools import wraps

from django.middleware.csrf import get_token

from graphql_relay import to_global_id


EMAIL_REGEX = re.compile(r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{'
                         r'1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{'
                         r'2,}))$')


def is_email(email: str):
    """Test if given string is an email."""
    return EMAIL_REGEX.search(email) is not None


def get_app_context(request):
    """Get context for app."""
    from scribbli.universe.models import Universe
    from scribbli.universe.schema.universe import UniverseNode

    class AppContext:
        def __init__(self, csrftoken, universe_id, is_logged_in, userdata):
            self.csrftoken = csrftoken
            self.universe_id = universe_id
            self.is_logged_in = is_logged_in
            self.userdata = userdata

    token = get_token(request)

    universe = Universe.objects.filter(is_active=True).first()
    if universe:
        universe_id = to_global_id(UniverseNode._meta.name, universe.pk)
    else:
        universe_id = None

    is_logged_in = request.user.is_authenticated

    return AppContext(
        csrftoken=token,
        universe_id=universe_id,
        is_logged_in=is_logged_in,
        userdata=request.user if is_logged_in else None,
    )


class GrapheneDecorators:

    @staticmethod
    def ensure_auth(exception_class=Exception, message="Authentication required"):
        def actual_decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                for arg in args:
                    if hasattr(arg, 'context'):
                        user = arg.context.user
                        if not user.is_authenticated:
                            raise exception_class(message)
                        kwargs['author'] = user
                if 'author' not in kwargs:
                    raise Exception('No context could be found')
                return f(*args, **kwargs)
            return wrapper
        return actual_decorator
