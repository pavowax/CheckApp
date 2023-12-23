
NAME = 'GoDaddy Website Protection (GoDaddy)'


def is_waf(self):
    if self.matchContent(r'GoDaddy (security|website firewall)'):
        return True

    return False
