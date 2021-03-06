resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'Ратуша' : {'lvl' : 0}, 'Склад' : {'lvl' : 0, 'ppl' : 0}, 'Дома' : {'lvl' : 0, 'ppl' : 0},
	'Лесопилка' : {'lvl' : 0, 'ppl' : 0}, 'Шахта' : {'lvl' : 0, 'ppl' : 0}, 'Ферма' : {'lvl' : 0, 'ppl' : 0},
	'Казармы' : {'lvl' : 0, 'ppl' : 0}, 'Стена' : {'lvl' : 0, 'ppl' : 0, 'str' : 0}, 'Требушет'  : {'lvl' : 0, 'ppl' : 0}, 'time' : None}

COST_COEF = {'Ратуша' : (500, 200, 200), 'Склад' : (200, 100, 100), 'Дома' : (200, 100, 100),
	'Лесопилка' : (100, 50, 50), 'Шахта' : (100, 50, 50), 'Ферма' : (100, 50, 50),
	'Казармы' : (200, 100, 100), 'Стена' : (5000, 500, 1500), 'Требушет'  : (8000, 1000, 300)}

SendMsg_cb = None
SendInfo_cb = None

AUTOBUILD = True
AUTOFEED = True
AUTOMONEY = True
AUTOPPL = True

FOOD_RESERV_TIME = 7 #в часах
SAVE_MONEY_TIME = 40 #в минутах
MAX_GOLD = 2630000
MIN_GOLD = 171000

ICON_PPL = ''
ICON_CLOCK = ''
ICON_INFO = ''
ICON_SWORDS = ''
ICON_ATTEN = ''
