import logging


logger = logging.getLogger('dev')


class LoggingGrapheneMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        import json
        logger.info('Request.body: %s', json.loads(info.context.body))
        logger.info('Request.META: %s', info.context.META)

        return next(root, info, **kwargs)
