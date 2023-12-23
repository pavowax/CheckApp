
NAME = 'DenyALL (Rohde & Schwarz CyberSecurity)'


def is_waf(self):
    if not self.matchStatus(200):
        return False

    if not self.matchReason('Condition Intercepted'):
        return False

    return True
