
NAME = 'Varnish (OWASP)'


def is_waf(self):
    if self.matchContent(r'Request rejected by xVarnish\-WAF'):
        return True

    return False
