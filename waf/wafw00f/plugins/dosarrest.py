
NAME = 'DOSarrest (DOSarrest Internet Security)'


def is_waf(self):
    if self.matchHeader(('X-DIS-Request-ID', '.+')):
        return True

    # Found samples of DOSArrest returning 'Server: DoSArrest/3.5'
    if self.matchHeader(('Server', r'DOSarrest(.*)?')):
        return True

    return False
