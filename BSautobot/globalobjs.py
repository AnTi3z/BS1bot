resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'Ратуша' : {'lvl' : 0}, 'Склад' : {'lvl' : 0, 'ppl' : 0}, 'Дома' : {'lvl' : 0, 'ppl' : 0},
	'Лесопилка' : {'lvl' : 0, 'ppl' : 0}, 'Шахта' : {'lvl' : 0, 'ppl' : 0}, 'Ферма' : {'lvl' : 0, 'ppl' : 0}}

war_bldngs = {'Казармы' : {'lvl' : 0, 'ppl' : 0}, 'Стена' : {'lvl' : 0, 'ppl' : 0}, 'Требушет'  : {'lvl' : 0, 'ppl' : 0}}

costCoef = {'Ратуша' : (500, 200, 200), 'Склад' : (200, 100, 100), 'Дома' : (200, 100, 100),
	'Лесопилка' : (100, 50, 50), 'Шахта' : (100, 50, 50), 'Ферма' : (100, 50, 50),
	'Казармы' : (200, 100, 100), 'Стена' : (5000, 500, 1500), 'Требушет'  : (8000, 1000, 300)}

SendMsg_cb = None
SendInfo_cb = None

AUTOBUILD = True
AUTOFEED = True
FOOD_RESERV_TIME = 4

debug_on = False
