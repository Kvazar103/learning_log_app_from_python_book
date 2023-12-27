
#Определяет схемы URL для learning_logs.
from django.urls import path #импортируется функция path, она необходима для связывания URL с представлениями 

from . import views #точка приказывает Python импортировать представления из каталога, в котором находится текущий модуль urls .py

app_name = 'learning_logs'#Переменная app_name помогает Django отличить этот файл urls .py от одноименных файлов в других приложениях в проекте 
 
urlpatterns = [ #Переменная urlpatterns в этом модуле представляет собой список страниц, которые могут запрашиваться из приложения learning_logs
    # Домашняя страница
    path('', views.index, name='index'),
    # Страница со списком всех тем.
    path('topics/',views.topics,name='topics'),
    # Когда Django проверяет запрашиваемый URL-адрес, эта схема совпадет с любым URL-адресом, 
    # который состоит из базового URL-адреса и слова topics. Слеш в конце можно включить, а можно не включать, 
    # но после слова topics ничего быть не должно, иначе схема не совпадет. Любой запрос с URL-адресом, 
    # соответствующим этой схеме, будет передан функции topics() в views .py.
    
    # Страница с подробной информацией по отдельной теме
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Вторая часть строки, /<int:topic_id>/, описывает целое число, заключенное между двумя слешами; 
    # это целое число сохраняется в аргу- менте topic_id.
    #Когда Django находит URL-адрес, соответствующий этой схеме, вызывается функция представления topic(), 
    # в аргументе которой передается значение, хранящееся в topic_id.
    
    path('new_topic/',views.new_topic,name='new_topic'),
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry')
]