
NAME = 'Kona SiteDefender (Akamai)'


def is_waf(self):
    if self.matchHeader(('Server', 'AkamaiGHost')):
        return True

    if self.matchHeader(('Server', 'AkamaiGHost'), attack=True)        :
        return True

    return False
