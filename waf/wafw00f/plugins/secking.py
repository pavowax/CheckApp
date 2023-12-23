
NAME = 'SecKing (SecKing)'


def is_waf(self):
    if self.matchHeader(('Server', r'secking(.?waf)?')):
        return True

    return False
