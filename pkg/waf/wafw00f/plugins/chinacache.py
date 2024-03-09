
NAME = 'ChinaCache Load Balancer (ChinaCache)'


def is_waf(self):
    if self.matchHeader(('Powered-By-ChinaCache', '.+')):
        return True

    return False
