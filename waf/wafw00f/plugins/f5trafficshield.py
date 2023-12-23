
NAME = 'Trafficshield (F5 Networks)'


def is_waf(self):
    if self.matchCookie('^ASINFO='):
        return True

    if self.matchHeader(('Server', 'F5-TrafficShield')):
        return True

    return False
