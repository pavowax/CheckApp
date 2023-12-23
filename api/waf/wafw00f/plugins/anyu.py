
NAME = 'AnYu (AnYu Technologies)'


def is_waf(self):
    if self.matchContent(r'anyu.{0,10}?the green channel'):
        return True

    if self.matchContent(r'your access has been intercepted by anyu'):
        return True

    return False
