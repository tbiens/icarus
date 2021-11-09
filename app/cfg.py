import multiprocessing

manager = multiprocessing.Manager()
attackers = manager.list()
attackdb = manager.dict()
numattacks = manager.dict()
numattacks['num'] = 0
largfeedqueue = manager.list()
whitelist = manager.list()



