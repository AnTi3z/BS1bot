import networkx as nx
import matplotlib.pyplot as plt

menu=nx.DiGraph()
menu.add_node('ROOT')

#Корень->
lst = ('Постройки','Мастерская','Война','Торговля')
menu.add_nodes_from(lst)
for nd in lst:
    menu.add_edge('ROOT',nd, cmd=nd)
    menu.add_edge(nd,'ROOT', cmd='Наверх')

#Корень->Постройки->
lst = ('Ратуша','Дома','Склад','Казармы','Стена','Лесопилка','Шахта','Ферма')
menu.add_nodes_from(lst)
for nd in lst:
    menu.add_edge('Постройки',nd, cmd=nd)
    menu.add_edge(nd,'Постройки', cmd='Назад')
    menu.add_edge(nd,'ROOT', cmd='Наверх')

#Мастерская->
menu.add_node('Требушет')
menu.add_edge('Постройки','Требушет', cmd='Требушет')
menu.add_edge('Требушет','Постройки', cmd='Назад')
menu.add_edge('Требушет','ROOT', cmd='Наверх')

#Война

#Корень->Торговля->
menu.add_node('РесурсКупить')
menu.add_node('РесурсПродать')
menu.add_edge('Торговля','РесурсКупить', cmd='Купить')
menu.add_edge('Торговля','РесурсПродать', cmd='Продать')
for u in ('РесурсКупить','РесурсПродать'):
    menu.add_edge(u,'ROOT', cmd='Наверх')
    menu.add_edge(u,'Торговля', cmd='Назад')

#Корень->Торговля->Купить->
menu.add_node('КупитьДерево')
menu.add_node('КупитьКамень')
menu.add_node('КупитьЕда')
menu.add_edge('РесурсКупить','КупитьДерево', cmd='Дерево')
menu.add_edge('РесурсКупить','КупитьКамень', cmd='Камень')
menu.add_edge('РесурсКупить','КупитьЕда', cmd='Еда')
for u in ('КупитьДерево','КупитьКамень','КупитьЕда'):
    menu.add_edge(u,'ROOT', cmd='Наверх')
    menu.add_edge(u,'РесурсКупить', cmd='Назад')

#Корень->Торговля->Продать->
menu.add_node('ПродатьДерево')
menu.add_node('ПродатьКамень')
menu.add_node('ПродатьЕда')
menu.add_edge('РесурсПродать','ПродатьДерево', cmd='Дерево')
menu.add_edge('РесурсПродать','ПродатьКамень', cmd='Камень')
menu.add_edge('РесурсПродать','ПродатьЕда', cmd='Еда')
for u in ('ПродатьДерево','ПродатьКамень','ПродатьЕда'):
    menu.add_edge(u,'ROOT', cmd='Наверх')
    menu.add_edge(u,'РесурсПродать', cmd='Назад')

#nx.draw(menu)
#plt.show()

