
NAME = 'KS-WAF (KnownSec)'


def is_waf(self):
    if self.matchContent(r'/ks[-_]waf[-_]error\.png'):
        return True

    return False
