import queue

AllBldngsNames = ('hall', 'storage', 'houses', 'sawmill', 'mine',
'farm', 'barracks', 'wall', 'trebuchet')

resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'hall' : {'lvl' : 0}, 'storage' : {'lvl' : 0, 'ppl' : 0}, 'houses' : {'lvl' : 0, 'ppl' : 0},
	'sawmill' : {'lvl' : 0, 'ppl' : 0}, 'mine' : {'lvl' : 0, 'ppl' : 0}, 'farm' : {'lvl' : 0, 'ppl' : 0}}

war_bldngs = {'barracks' : {'lvl' : 0, 'ppl' : 0}, 'wall' : {'lvl' : 0, 'ppl' : 0}, 'trebuchet'  : {'lvl' : 0, 'ppl' : 0}}

costCoef = {'hall' : (500, 200, 200), 'storage' : (200, 100, 100), 'houses' : (200, 100, 100),
	'sawmill' : (100, 50, 50), 'mine' : (100, 50, 50), 'farm' : (100, 50, 50),
	'barracks' : (200, 100, 100), 'wall' : (5000, 500, 1500), 'trebuchet'  : (8000, 1000, 300)}

que = queue.Queue()
SendMsg_cb = None
SendInfo_cb = None

debug_on = True
