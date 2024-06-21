from __future__ import print_function

import io
import logging
import os
import random
import re
import sys
import string
from optparse import OptionParser

from pkg.waf.wafw00f.lib.asciiarts import Color
from pkg.waf.wafw00f.lib.evillib import urlParser, waftoolsengine
from pkg.waf.wafw00f.manager import load_plugins
from pkg.waf.wafw00f.wafprio import wafdetectionsprio


class WAFW00F(waftoolsengine):

    xsstring = '<script>alert("XSS");</script>'
    sqlistring = "UNION SELECT ALL FROM information_schema AND ' or SLEEP(5) or '"
    lfistring = '../../../../etc/passwd'
    rcestring = '/bin/cat /etc/passwd; ping 127.0.0.1; curl google.com'
    xxestring = '<!ENTITY xxe SYSTEM "file:///etc/shadow">]><pwn>&hack;</pwn>'

    def __init__(self, target='www.example.com', debuglevel=0, path='/',
                 followredirect=True, extraheaders={}, proxies=None):

        self.log = logging.getLogger('wafw00f')
        self.attackres = None
        waftoolsengine.__init__(self, target, debuglevel, path, proxies, followredirect, extraheaders)
        self.knowledge = dict(generic=dict(found=False, reason=''), wafname=list())
        self.rq = self.normalRequest()

    def normalRequest(self):
        return self.Request()

    def customRequest(self, headers=None):
        return self.Request(
            headers=headers
        )

    def nonExistent(self):
        return self.Request(
            path=self.path + str(random.randrange(100, 999)) + '.html'
        )

    def xssAttack(self):
        return self.Request(
            path=self.path,
            params={
                create_random_param_name(): self.xsstring
            }
        )

    def xxeAttack(self):
        return self.Request(
            path=self.path,
            params={
                create_random_param_name(): self.xxestring
            }
        )

    def lfiAttack(self):
        return self.Request(
            path=self.path + self.lfistring
        )

    def centralAttack(self):
        return self.Request(
            path=self.path,
            params={
                create_random_param_name(): self.xsstring,
                create_random_param_name(): self.sqlistring,
                create_random_param_name(): self.lfistring
            }
        )

    def sqliAttack(self):
        return self.Request(
            path=self.path,
            params={
                create_random_param_name(): self.sqlistring
            }
        )

    def osciAttack(self):
        return self.Request(
            path=self.path,
            params= {
                create_random_param_name(): self.rcestring
            }
        )

    def performCheck(self, request_method):
        r = request_method()
        if r is None:
            raise RequestBlocked()
        return r, r.url

    # Most common attacks used to detect WAFs
    attcom = [xssAttack, sqliAttack, lfiAttack]
    attacks = [xssAttack, xxeAttack, lfiAttack, sqliAttack, osciAttack]

    def genericdetect(self):
        reason = ''
        reasons = ['Blocking is being done at connection/packet level.',
                   'The server header is different when an attack is detected.',
                   'The server returns a different response code when an attack string is used.',
                   'It closed the connection for a normal request.',
                   'The response was different when the request wasn\'t made from a browser.'
                ]
        try:
            # Testing for no user-agent response. Detects almost all WAFs out there.
            resp1, _ = self.performCheck(self.normalRequest)
            if 'User-Agent' in self.headers:
                self.headers.pop('User-Agent')  # Deleting the user-agent key from object not dict.
            resp3 = self.customRequest(headers=self.headers)
            if resp3 is not None and resp1 is not None:
                if resp1.status_code != resp3.status_code:
                    self.log.info('Server returned a different response when request didn\'t contain the User-Agent header.')
                    reason = reasons[4]
                    reason += '\r\n'
                    reason += 'Normal response code is "%s",' % resp1.status_code
                    reason += ' while the response code to a modified request is "%s"' % resp3.status_code
                    self.knowledge['generic']['reason'] = reason
                    self.knowledge['generic']['found'] = True
                    return True

            # Testing the status code upon sending a xss attack
            resp2, xss_url = self.performCheck(self.xssAttack)
            if resp1.status_code != resp2.status_code:
                self.log.info('Server returned a different response when a XSS attack vector was tried.')
                reason = reasons[2]
                reason += '\r\n'
                reason += 'Normal response code is "%s",' % resp1.status_code
                reason += ' while the response code to cross-site scripting attack is "%s"' % resp2.status_code
                self.knowledge['generic']['reason'] = reason
                self.knowledge['generic']['found'] = True
                return xss_url

            # Testing the status code upon sending a lfi attack
            resp2, lfi_url = self.performCheck(self.lfiAttack)
            if resp1.status_code != resp2.status_code:
                self.log.info('Server returned a different response when a directory traversal was attempted.')
                reason = reasons[2]
                reason += '\r\n'
                reason += 'Normal response code is "%s",' % resp1.status_code
                reason += ' while the response code to a file inclusion attack is "%s"' % resp2.status_code
                self.knowledge['generic']['reason'] = reason
                self.knowledge['generic']['found'] = True
                return lfi_url

            # Testing the status code upon sending a sqli attack
            resp2, sqli_url = self.performCheck(self.sqliAttack)
            if resp1.status_code != resp2.status_code:
                self.log.info('Server returned a different response when a SQLi was attempted.')
                reason = reasons[2]
                reason += '\r\n'
                reason += 'Normal response code is "%s",' % resp1.status_code
                reason += ' while the response code to a SQL injection attack is "%s"' % resp2.status_code
                self.knowledge['generic']['reason'] = reason
                self.knowledge['generic']['found'] = True
                return sqli_url

            # Checking for the Server header after sending malicious requests
            normalserver, attackresponse_server = '', ''
            response = self.attackres
            if 'server' in resp1.headers:
                normalserver = resp1.headers.get('Server')
            if response is not None and 'server' in response.headers:
                attackresponse_server = response.headers.get('Server')
            if attackresponse_server != normalserver:
                self.log.info('Server header changed, WAF possibly detected')
                self.log.debug('Attack response: %s' % attackresponse_server)
                self.log.debug('Normal response: %s' % normalserver)
                reason = reasons[1]
                reason += '\r\nThe server header for a normal response is "%s",' % normalserver
                reason += ' while the server header a response to an attack is "%s",' % attackresponse_server
                self.knowledge['generic']['reason'] = reason
                self.knowledge['generic']['found'] = True
                return True

        # If at all request doesn't go, press F
        except RequestBlocked:
            self.knowledge['generic']['reason'] = reasons[0]
            self.knowledge['generic']['found'] = True
            return True
        return False

    def matchHeader(self, headermatch, attack=False):
        if attack:
            r = self.attackres
        else:
            r = self.rq
        if r is None:
            return

        header, match = headermatch
        headerval = r.headers.get(header)
        if headerval:
            # set-cookie can have multiple headers, python gives it to us
            # concatinated with a comma
            if header == 'Set-Cookie':
                headervals = headerval.split(', ')
            else:
                headervals = [headerval]
            for headerval in headervals:
                if re.search(match, headerval, re.I):
                    return True
        return False

    def matchStatus(self, statuscode, attack=True):
        if attack:
            r = self.attackres
        else:
            r = self.rq
        if r is None:
            return
        if r.status_code == statuscode:
            return True
        return False

    def matchCookie(self, match, attack=False):
        return self.matchHeader(('Set-Cookie', match), attack=attack)

    def matchReason(self, reasoncode, attack=True):
        if attack:
            r = self.attackres
        else:
            r = self.rq
        if r is None:
            return
        # We may need to match multiline context in response body
        if str(r.reason) == reasoncode:
            return True
        return False

    def matchContent(self, regex, attack=True):
        if attack:
            r = self.attackres
        else:
            r = self.rq
        if r is None:
            return
        # We may need to match multiline context in response body
        if re.search(regex, r.text, re.I):
            return True
        return False

    wafdetections = dict()

    plugin_dict = load_plugins()
    result_dict = {}
    for plugin_module in plugin_dict.values():
        wafdetections[plugin_module.NAME] = plugin_module.is_waf
    # Check for prioritized ones first, then check those added externally
    checklist = wafdetectionsprio
    checklist += list(set(wafdetections.keys()) - set(checklist))

    def identwaf(self, findall=False):
        detected = list()
        try:
            self.attackres, xurl = self.performCheck(self.centralAttack)
        except RequestBlocked:
            return detected, None
        for wafvendor in self.checklist:
            self.log.info('Checking for %s' % wafvendor)
            if self.wafdetections[wafvendor](self):
                detected.append(wafvendor)
                if not findall:
                    break
        self.knowledge['wafname'] = detected
        return detected, xurl

def calclogginglevel(verbosity):
    default = 40  # errors are printed out
    level = default - (verbosity * 10)
    if level < 0:
        level = 0
    return level

def buildResultRecord(url, waf, evil_url=None):
    result = {}
    result['url'] = url
    if waf:
        result['detected'] = True
        if waf == 'generic':
            result['trigger_url'] = evil_url
            result['firewall'] = 'Generic'
            result['manufacturer'] = 'Unknown'
        else:
            result['trigger_url'] = evil_url
            result['firewall'] = waf.split('(')[0].strip()
            result['manufacturer'] = waf.split('(')[1].replace(')', '').strip()
    else:
        result['trigger_url'] = evil_url
        result['detected'] = False
        result['firewall'] = 'None'
        result['manufacturer'] = 'None'
    return result

def getTextResults(res=None):
    # leaving out some space for future possibilities of newer columns
    # newer columns can be added to this tuple below
    keys = ('detected')
    res = [({key: ba[key] for key in ba if key not in keys}) for ba in res]
    rows = []
    for dk in res:
        p = [str(x) for _, x in dk.items()]
        rows.append(p)
    for m in rows:
        m[1] = '%s (%s)' % (m[1], m[2])
        m.pop()
    defgen = [
        (max([len(str(row[i])) for row in rows]) + 3)
        for i in range(len(rows[0]))
    ]
    rwfmt = "".join(["{:>"+str(dank)+"}" for dank in defgen])
    textresults = []
    for row in rows:
        textresults.append(rwfmt.format(*row))
    return textresults

def create_random_param_name(size=8, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def disableStdOut():
    sys.stdout = None

def enableStdOut():
    sys.stdout = sys.__stdout__

def getheaders(fn):
    headers = {}
    if not os.path.exists(fn):
        logging.getLogger('wafw00f').critical('Headers file "%s" does not exist!' % fn)
        return
    with io.open(fn, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            _t = line.split(':', 2)
            if len(_t) == 2:
                h, v = map(lambda x: x.strip(), _t)
                headers[h] = v
    return headers

class RequestBlocked(Exception):
    pass

def waf_ps(address):
    parser = OptionParser(usage='%prog url1 [url2 [url3 ... ]]\r\nexample: %prog http://www.victim.org/')
    parser.add_option('-v', '--verbose', action='count', dest='verbose', default=0,
                      help='Enable verbosity, multiple -v options increase verbosity')
    parser.add_option('-a', '--findall', action='store_true', dest='findall', default=False,
                      help='Find all WAFs which match the signatures, do not stop testing on the first one')
    parser.add_option('-r', '--noredirect', action='store_false', dest='followredirect',
                      default=True, help='Do not follow redirections given by 3xx responses')
    
    response_sentences=[]

    options, args = parser.parse_args()
    (W,Y,G,R,B,C,E) = Color.unpack()

    logging.basicConfig(level=calclogginglevel(options.verbose))
    log = logging.getLogger('wafw00f')
    
    extraheaders = {}
    #args boşa çıktı
    if len(address) == 0:
        parser.error('No test target specified.')

    targets = []
    targets.append(address)

    results = []
    for target in targets:
        if not target.startswith('http'):
            log.info('The url %s should start with http:// or https:// .. fixing (might make this unusable)' % target)
            target = 'https://' + target
        print('[*] Checking %s' % target) #checking in response
        response_sentences.append(f'Checking  {target}') #here
        pret = urlParser(target)

        if pret is None:
            log.critical('The url %s is not well formed' % target)
            sys.exit(1)
        (hostname, _, path, _, _) = pret
        log.info('starting wafw00f on %s' % target)

        proxies = dict()
        attacker = WAFW00F(target, debuglevel=options.verbose, path=path,
                    followredirect=options.followredirect, extraheaders=extraheaders,
                        proxies=proxies)
        if attacker.rq is None:
            log.error('Site %s appears to be down' % hostname) #can writable in response
            continue
        
        waf, xurl = attacker.identwaf(options.findall)
        log.info('Identified WAF: %s' % waf)
        if len(waf) > 0:
            response_sentences.append('Generic Detection results:') #here
            for i in waf:
                results.append(buildResultRecord(target, i, xurl))
            print('[+] The site %s%s%s is behind %s%s%s WAF.' % (B, target, E, C, (E+' and/or '+C).join(waf), E)) # in response 
            response_sentences.append(f'The site {target} is behind {" and/or ".join(waf)} WAF.') #here
        
        if (options.findall) or len(waf) == 0:
            print('[+] Generic Detection results:')# in response
            response_sentences.append('Generic Detection results:') #here

            generic_url = attacker.genericdetect()
            if generic_url:
                log.info('Generic Detection: %s' % attacker.knowledge['generic']['reason'])
                print('[*] The site %s seems to be behind a WAF or some sort of security solution' % target)#in response
                response_sentences.append(f'The site {target} seems to be behind a WAF or some sort of security solution')#here

                print('[~] Reason: %s' % attacker.knowledge['generic']['reason'])#in response
                response_sentences.append(f'Reason: {attacker.knowledge["generic"]["reason"]}')#here

                results.append(buildResultRecord(target, 'generic', generic_url))
            else:
                print('[-] No WAF detected by the generic detection')#in response
                response_sentences.append('No WAF detected by the generic detection')#here

                results.append(buildResultRecord(target, None, None))

        print('Number of requests: %s' % attacker.requestnumber)# in response
        response_sentences.append(f'Number of requests: {attacker.requestnumber}')#here
        # data = {}
        # i=0
        result=""
        for value in response_sentences:
            result += f'{value} '
            # i+=1
        # json_data = json.dumps(data)

        return result

    #print table of results
    if len(results) > 0:
        log.info("Found: %s matches." % (len(results))) #in response
        
# if __name__ == '__main__':
#     main()