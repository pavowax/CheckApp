
NAME = 'Azure Front Door (Microsoft)'


def is_waf(self):
    if self.matchHeader(('X-Azure-Ref', '.+?')):
        return True

    return False
