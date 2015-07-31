import logging

from pyramid.view import view_config
from pyramid.response import Response


log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='templates/index.jinja2')
def main_view(request):
    return {
    }


@view_config(context=Exception)
def system_error_view(context, request):
    """Example catch all exception handler."""

    # Notify sentry.
    request.raven.captureException()

    # XXX E.g.: render error page.
    # ...

    log.error("Traceback: %s", context, exc_info=(context))
    response =  Response('%s' % context)
    response.status_int = 500

    return response