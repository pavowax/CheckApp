
NAME = 'Variti (Variti)'

def is_waf(self):
    if self.matchHeader(('Server', r'Variti(?:\/[a-z0-9\.\-]+)?')):
        return True

    return False
