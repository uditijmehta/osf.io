import urlparse

import requests
from celery.utils.log import get_task_logger

from api.base import settings

logger = get_task_logger(__name__)

def get_varnish_servers():
    #  TODO: this should get the varnish servers from HAProxy or a setting
    return settings.VARNISH_SERVERS

def ban_url(url):
    timeout = 0.5  # 500ms timeout for bans
    if settings.ENABLE_VARNISH:
        parsed_url = urlparse.urlparse(url)

        for host in get_varnish_servers():
            varnish_parsed_url = urlparse.urlparse(host)
            ban_url = '{scheme}://{netloc}{path}.*'.format(
                scheme=varnish_parsed_url.scheme,
                netloc=varnish_parsed_url.netloc,
                path=parsed_url.path
            )
            response = requests.request('BAN', ban_url, timeout=timeout, headers=dict(
                Host=parsed_url.hostname
            ))
            if not response.ok:
                logger.error('Banning {} failed: {}'.format(
                    url,
                    response.text
                ))
