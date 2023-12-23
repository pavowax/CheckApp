
NAME = 'WebLand (WebLand)'


def is_waf(self):
    if self.matchHeader(('Server', r'protected by webland')):
        return True

    return False
