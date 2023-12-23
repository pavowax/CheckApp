
NAME = 'Puhui (Puhui)'


def is_waf(self):
    if self.matchHeader(('Server', r'Puhui[\-_]?WAF')):
        return True

    return False
