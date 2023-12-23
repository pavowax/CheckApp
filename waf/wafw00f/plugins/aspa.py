
NAME = 'ASPA Firewall (ASPA Engineering Co.)'


def is_waf(self):
    if self.matchHeader(('Server', r'ASPA[\-_]?WAF')):
        return True

    if self.matchHeader(('ASPA-Cache-Status', r'.+?')):
        return True

    return False
