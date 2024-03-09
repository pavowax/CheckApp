
NAME = 'NullDDoS Protection (NullDDoS)'


def is_waf(self):
    if self.matchHeader(('Server', r'NullDDoS(.System)?')):
        return True

    return False
