import logging

from django.contrib.auth import get_user_model

devlog = logging.getLogger("dev")


# Maybe do this in the future? For now realize JWT not needed
#class JwtAuthGrapheneMiddleware(object):
#    """Authentication via JWT in GraphQL requests."""
#
#    def __init__(self):
#        self.noop_paths = set()
#
#    @staticmethod
#    def get_jwt(info, **kwargs):
#        return None
#
#    def resolve(self, next, root, info, **kwargs):
#
#        devlog.info('request headers: %s', info.context.headers)
#
#        # Continue to the next middleware in the graphene chain
#        return next(root, info, **kwargs)

