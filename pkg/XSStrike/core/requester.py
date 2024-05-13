import random
import requests
import time
from urllib3.exceptions import ProtocolError
import warnings
import traceback

import pkg.XSStrike.core.config as config
from pkg.XSStrike.core.utils import converter, getVar
from pkg.XSStrike.core.log import setup_logger

logger = setup_logger(__name__)

warnings.filterwarnings('ignore')  # Disable SSL related warnings


def requester(url, data, headers, GET, delay, timeout):
    if getVar('jsonData'):
        data = converter(data)
    elif getVar('path'):
        url = converter(data, url)
        data = []
        GET, POST = True, False
    time.sleep(delay)
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']
    if 'User-Agent' not in headers:
        headers['User-Agent'] = random.choice(user_agents)
    elif headers['User-Agent'] == '$':
        headers['User-Agent'] = random.choice(user_agents)
    logger.info('Requester url: {}'.format(url))
    logger.debug('Requester GET: {}'.format(GET))
    logger.debug_json('Requester data:', data)
    logger.debug_json('Requester headers:', headers)
    try:
        if GET:
            response = requests.get(url, params=data, headers=headers,
                                    timeout=timeout, verify=False )
        elif getVar('jsonData'):
            response = requests.post(url, json=data, headers=headers,
                                    timeout=timeout, verify=False, proxies=config.proxies )
        else:
            response = requests.post(url, data=data, headers=headers,
                                     timeout=timeout, verify=False)
        return response
    except ProtocolError:
        logger.warning('WAF is dropping suspicious requests.')
        logger.warning('Scanning will continue after 10 minutes.')
        time.sleep(600)
    except Exception as e:
        logger.warning(f'Unable to connect to the target. {traceback.format_tb(e.__traceback__)}')
        return requests.Response()