import copy
import re

import pkg.XSStrike.core.config as config
from pkg.XSStrike.core.colors import green, end
from pkg.XSStrike.core.config import xsschecker
from pkg.XSStrike.core.filterChecker import filterChecker
from pkg.XSStrike.core.generator import generator
from pkg.XSStrike.core.htmlParser import htmlParser
from pkg.XSStrike.core.requester import requester
from pkg.XSStrike.core.log import setup_logger

logger = setup_logger(__name__)


def crawl(scheme, host, main_url, form, blindXSS, blindPayload, headers, delay, timeout, encoding,data):
    cikti = []
    if form:
        for each in form.values():
            url = each['action']
            if url:
                if url.startswith(main_url):
                    pass
                elif url.startswith('//') and url[2:].startswith(host):
                    url = scheme + '://' + url[2:]
                elif url.startswith('/'):
                    url = scheme + '://' + host + url
                elif re.match(r'\w', url[0]):
                    url = scheme + '://' + host + '/' + url
                if url not in config.globalVariables['checkedForms']:
                    config.globalVariables['checkedForms'][url] = []
                method = each['method']
                GET = True if method == 'get' else False
                inputs = each['inputs']
                paramData = {}
                for one in inputs:
                    paramData[one['name']] = one['value']
                    for paramName in paramData.keys():
                        if paramName not in config.globalVariables['checkedForms'][url]:
                            config.globalVariables['checkedForms'][url].append(paramName)
                        paramsCopy = copy.deepcopy(paramData)
                        paramsCopy[paramName] = xsschecker
                        response = requester(
                            url, paramsCopy, headers, GET, delay, timeout)
                        occurences = htmlParser(response, encoding)
                        positions = occurences.keys()
                        occurences = filterChecker(
                            url, paramsCopy, headers, GET, delay, occurences, timeout, encoding)
                        vectors = generator(occurences, response.text)
                        if vectors:
                            for confidence, vects in vectors.items():
                                try:
                                    payload = list(vects)[0]
                                    logger.vuln('Vulnerable webpage : %s%s%s' %
                                                (green, url, end))
                                    cikti.append(f'Vulnerable webpage : {url}')
                                    logger.vuln('Vector for %s%s%s: %s' %
                                                (green, paramName, end, payload))   
                                    cikti.append(f'Vector for {paramName} : {payload} ')
                                    break
                                except IndexError:
                                    pass
                        if blindXSS and blindPayload:
                            paramsCopy[paramName] = blindPayload
                            requester(url, paramsCopy, headers,
                                        GET, delay, timeout)
                        #data = {}
                        i = 0
                        for ciktis in cikti:
                                data[f'[{i}]'] = f'{ciktis}'
                                i+=1
                        return data    

