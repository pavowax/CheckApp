
NAME = 'Safeline (Chaitin Tech.)'


def is_waf(self):
    if self.matchContent(r'safeline|<!\-\-\sevent id:'):
        return True

    return False
