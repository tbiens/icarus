"""creates files that are stored entirely in memory"""

import app.cfg


def lastattacker(ipaddr):
    """keeps track of the last 5 unique attackers."""
    app.cfg.numattacks['num'] = app.cfg.numattacks['num'] + 1
    # Last 5 reports.
    if ipaddr in app.cfg.attackers:
        pass
    else:
        if len(app.cfg.attackers) > 4:
            del app.cfg.attackers[-1]
        app.cfg.attackers.insert(0, ipaddr)

