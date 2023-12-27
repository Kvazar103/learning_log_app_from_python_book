from django.contrib import admin
from .models import Topic,Entry
# Register your models here.

admin.site.register(Topic)
# Этот код импортирует регистрируемую модель Topic. Точка перед models сообщает Django, что файл models.py следует 
# искать в одном каталоге с admin .py. Вызов admin.site.register() сообщает Django, что управление моделью 
# должно осуществляться через административный сайт.
admin.site.register(Entry)
