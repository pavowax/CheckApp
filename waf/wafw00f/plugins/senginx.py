
NAME = 'SEnginx (Neusoft)'


def is_waf(self):
    if self.matchContent(r'SENGINX\-ROBOT\-MITIGATION'):
        return True

    return False
