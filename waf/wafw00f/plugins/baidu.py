
NAME = 'Yunjiasu (Baidu Cloud Computing)'


def is_waf(self):
    if self.matchHeader(('Server', r'Yunjiasu(.+)?')):
        return True

    return False
