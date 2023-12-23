
NAME = 'Secure Entry (United Security Providers)'


def is_waf(self):
    if self.matchHeader(('Server', 'Secure Entry Server')):
        return True

    return False
