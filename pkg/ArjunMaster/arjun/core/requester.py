import json
import time
import random
import requests
import warnings

from pkg.ArjunMaster.arjun.core import config as mem

from ratelimit import limits, sleep_and_retry
from pkg.ArjunMaster.arjun.core.utils import dict_to_xml



warnings.filterwarnings('ignore') # Disable SSL related warnings

@sleep_and_retry
@limits(calls=50, period=1)
def requester(request, payload={}):
    """
    central function for making http requests
    returns str on error otherwise response object of requests library
    """
    if request.get('include') and len(request.get('include', '')) != 0:
        payload.update(request['include'])
    # if mem.var['stable']:
    #     mem.var['delay'] = random.choice(range(3, 10))
    # time.sleep(mem.var['delay'])
    url = request['url']
    # if mem.var['kill']:
    #     return 'killed'
    if request['method'] == 'GET':
        response = requests.get(url,
            params=payload,
            headers=request['headers'],
            verify=False,
            allow_redirects=False,
            timeout=10,
        )
    elif request['method'] == 'JSON':
        request['headers']['Content-Type'] = 'application/json'
        # if mem.var['include'] and '$arjun$' in mem.var['include']:
        #     payload = mem.var['include'].replace('$arjun$',
        #         json.dumps(payload).rstrip('}').lstrip('{'))
        #     response = requests.post(url,
        #         data=payload,
        #         headers=request['headers'],
        #         verify=False,
        #         allow_redirects=False,
        #         timeout=mem.var['timeout'],
        #     )
        # else:
        response = requests.post(url,
            json=payload,
            headers=request['headers'],
            verify=False,
            allow_redirects=False,
            timeout=10,
        )
    elif request['method'] == 'XML':
        request['headers']['Content-Type'] = 'application/xml'
        # payload = mem.var['include'].replace('$arjun$',
        #     dict_to_xml(payload))
        response = requests.post(url,
            # data=payload,
            headers=request['headers'],
            verify=False,
            allow_redirects=False,
            timeout=10,
        )
    else:
        response = requests.post(url,
            data=payload,
            headers=request['headers'],
            verify=False,
            allow_redirects=False,
            timeout=10,
        )
    return response

