import logging

from pyramid.view import view_config


log = logging.getLogger(__name__)


@view_config(route_name='home', renderer='templates/index.jinja2')
def main_view(request):
    return {
    }
