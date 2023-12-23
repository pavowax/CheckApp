
NAME = 'VirusDie (VirusDie LLC)'


def is_waf(self):
    if self.matchContent(r"cdn\.virusdie\.ru/splash/firewallstop\.png"):
        return True

    if self.matchContent(r'copy.{0,10}?Virusdie\.ru'):
        return True

    return False
