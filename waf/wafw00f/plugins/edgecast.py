
NAME = 'Edgecast (Verizon Digital Media)'


def is_waf(self):
    if self.matchHeader(('Server', r'^ECD(.+)?')):
        return True

    if self.matchHeader(('Server', r'^ECS(.*)?')):
        return True

    return False
