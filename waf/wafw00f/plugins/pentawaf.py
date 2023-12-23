
NAME = 'PentaWAF (Global Network Services)'


def is_waf(self):
    if self.matchHeader(('Server', r'PentaWaf(/[0-9\.]+)?')):
        return True

    if self.matchContent(r'Penta.?Waf/[0-9\.]+?.server'):
        return True

    return False
