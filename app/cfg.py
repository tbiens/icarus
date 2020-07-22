import multiprocessing

manager = multiprocessing.Manager()
attackers = manager.list()
attackdb = manager.dict()
