
NAME = 'Comodo cWatch (Comodo CyberSecurity)'


def is_waf(self):
    if self.matchHeader(('Server', r'Protected by COMODO WAF(.+)?')):
        return True

    return False
