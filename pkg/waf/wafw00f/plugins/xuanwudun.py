
NAME = 'Xuanwudun (Xuanwudun)'


def is_waf(self):
    if self.matchContent(r"admin\.dbappwaf\.cn/(index\.php/Admin/ClientMisinform/)?"):
        return True

    if self.matchContent(r'class=.(db[\-_]?)?waf(.)?([\-_]?row)?>'):
        return True

    return False
