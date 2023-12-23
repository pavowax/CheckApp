
NAME = 'SecuPress WP Security (SecuPress)'


def is_waf(self):
    if self.matchContent(r'<(title|h\d{1})>SecuPress'):
        return True

    return False
