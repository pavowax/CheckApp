
NAME = 'Janusec Application Gateway (Janusec)'


def is_waf(self):
    if self.matchContent(r'janusec application gateway'):
        return True

    return False
